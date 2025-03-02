from flask import Flask, request, Response, render_template
import requests
import re
import gemini
from youtube_transcript_api import YouTubeTranscriptApi
import datetime
import os

# This is the default configuration, so you likely don't need to add anything
app = Flask(__name__, static_folder='static')

# Create storage directory if it doesn't exist
STORAGE_DIR = 'transcription_history'
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    """Serve a simple form for entering YouTube URLs"""
    return render_template('index.html')

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
    
    # Render the loader template with the source parameter
    return render_template('loader.html', source=source)

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
            
            # Use the result template and pass the video_id for embedding
            return render_template('result.html', 
                                  content=gemini_response,
                                  video_id=video_id)
        else:
            # For non-browser clients, just return the markdown
            return Response(gemini_response, mimetype=response_type)
        
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