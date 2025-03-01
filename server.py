from flask import Flask, request, Response, render_template_string
import requests
import re
import gemini
from youtube_transcript_api import YouTubeTranscriptApi
import datetime
import os

app = Flask(__name__)

# Create storage directory if it doesn't exist
STORAGE_DIR = 'transcription_history'
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    """Serve a simple form for entering YouTube URLs"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Transcription Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #c00;
        }
        input[type="text"] {
            width: 70%;
            padding: 8px;
        }
        button {
            padding: 8px 15px;
            background: #c00;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background: #a00;
        }
    </style>
</head>
<body>
    <h1>YouTube Transcription Tool</h1>
    <p>Enter a YouTube URL or video ID below:</p>
    
    <form id="transcribe-form" action="/transcribe" method="get">
        <input type="text" id="source" name="source" placeholder="YouTube URL or ID" required>
        <button type="submit">Get Summary</button>
    </form>
</body>
</html>"""
    return html

@app.route('/transcribe', methods=['GET'])
def transcribe():
    """Serve a page with a loader that will fetch the transcription"""
    source = request.args.get('source')
    if not source:
        return "Error: 'source' parameter is required", 400
    
    # Basic validation
    video_id = extract_video_id(source)
    if not video_id:
        return "Error: Invalid YouTube URL or video ID", 400
    
    # Create loader page with JavaScript to fetch the actual content
    loader_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loading Transcription...</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }}
        .loader {{
            border: 16px solid #f3f3f3;
            border-top: 16px solid #c00;
            border-radius: 50%;
            width: 120px;
            height: 120px;
            animation: spin 2s linear infinite;
            margin: 40px auto;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .error {{
            color: red;
            padding: 20px;
            border: 1px solid red;
            display: none;
        }}
        .back-link {{
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>Processing YouTube Video</h1>
    <p id="status-message">Fetching and analyzing the transcript. This may take a minute...</p>
    <div class="loader" id="loader"></div>
    <div class="error" id="error-message">An error occurred while processing your request.</div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // Fetch the transcription results
            fetch('/api/transcribe?source={source}')
                .then(response => {{
                    if (!response.ok) {{
                        throw new Error('Network response was not ok');
                    }}
                    return response.text();
                }})
                .then(data => {{
                    // Replace the entire page content with the response
                    document.open();
                    document.write(data);
                    document.close();
                }})
                .catch(error => {{
                    // Show error message
                    document.getElementById('loader').style.display = 'none';
                    document.getElementById('error-message').style.display = 'block';
                    document.getElementById('error-message').textContent = 
                        'Error: ' + error.message + '. Please try again later.';
                    document.getElementById('status-message').textContent = 'Failed to process video';
                    
                    // Add a back link
                    const backLink = document.createElement('p');
                    backLink.className = 'back-link';
                    backLink.innerHTML = '<a href="/">Try another video</a>';
                    document.body.appendChild(backLink);
                }});
        }});
    </script>
</body>
</html>"""
    
    return loader_html

def save_transcription(source, response):
    """Save transcription request and response to a text file with timestamp."""
    # Create timestamp for filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a clean filename (remove URL characters)
    video_id = extract_video_id(source)
    filename = f"{timestamp}_{video_id}.txt"
    filepath = os.path.join(STORAGE_DIR, filename)
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"SOURCE: {source}\n\n")
        f.write(f"TIMESTAMP: {datetime.datetime.now().isoformat()}\n\n")
        f.write("RESPONSE:\n\n")
        f.write(response)
    
    return filepath

@app.route('/api/transcribe', methods=['GET'])
def process_transcribe():
    source = request.args.get('source')
    if not source:
        return "Error: 'source' parameter is required", 400
    
    # Extract video ID for validation purposes only
    video_id = extract_video_id(source)
    if not video_id:
        return "Error: Invalid YouTube URL or video ID", 400
    
    # If source is just a video ID, convert it to a full YouTube URL
    if re.match(r'^[a-zA-Z0-9_-]{11}$', source):
        source = f"https://www.youtube.com/watch?v={source}"
    
    try:
        # Get transcript using YouTubeTranscriptApi
        transcript_text = ""
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format transcript into a single string
        for entry in transcript:
            transcript_text += f"{entry['text']} "
        
        # Check if request is from a browser
        user_agent = request.headers.get('User-Agent', '').lower()
        is_browser = any(browser in user_agent for browser in ['mozilla', 'chrome', 'safari', 'edge', 'firefox', 'webkit'])
        
        # Create appropriate prompt based on client type
        if is_browser:
            prompt = f"Explain the key points in the below video transcription. Format your response as HTML with proper headings, paragraphs, and lists. Include a title at the top. IMPORTANT: Return only raw HTML without any code block markers or backticks. Video source: {source}\n\n{transcript_text}"
            response_type = 'text/html'
        else:
            prompt = f"Explain the key points in the below video transcription. Format your response in Markdown with proper headings, lists, and emphasis. Include a title at the top. Video source: {source}\n\n{transcript_text}"
            response_type = 'text/markdown'
        
        # Process with Gemini
        gemini_response = gemini.generate(prompt)
        
        # Clean up response if it's HTML (remove code block markers)
        if is_browser:
            # Remove ```html and ``` markers if present
            gemini_response = gemini_response.replace('```html', '').replace('```', '')
            # Ensure HTML has proper doctype if it's a full page
            if '<html' not in gemini_response.lower():
                gemini_response = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Transcription Summary</title>
</head>
<body>
{gemini_response}
</body>
</html>"""
        
        # Save the request and response to a file
        save_transcription(source, gemini_response)
        
        # Return Gemini's response with appropriate MIME type
        return Response(gemini_response, mimetype=response_type)
    except Exception as e:
        return f"Error processing request: {str(e)}", 500

def extract_video_id(source):
    """Extract YouTube video ID from various URL formats including YouTube Shorts."""
    # Check if source is already a video ID (simple format validation)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', source):
        return source
    
    # Try to extract from YouTube Shorts URL first
    shorts_regex = r'youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})'
    match = re.search(shorts_regex, source)
    if match:
        return match.group(1)
    
    # Extract from standard YouTube URL
    youtube_regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\s*[^\/\n\s]+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(youtube_regex, source)
    if match:
        return match.group(1)

    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666)