"""
This module contains the prompt templates used for generating AI responses.
"""

def get_html_prompt(source, transcript_text, timestamp_map=None):
    """
    Returns a prompt template for generating HTML-formatted responses with timestamps.
    
    Args:
        source: The source URL or video ID
        transcript_text: The transcript text to analyze with timestamps
        timestamp_map: A dictionary mapping timestamp strings to seconds
    
    Returns:
        A formatted prompt string for HTML output
    """
    timestamp_instruction = """
When you mention specific points in the video, please reference them using timestamp links.
The transcript contains timestamps in [MM:SS] format at the beginning of segments.
Create timestamp links in this format: <a href="#t=MM:SS" class="timestamp">MM:SS</a>
Do NOT wrap timestamp links in parentheses.

For example, if you want to reference something at 2 minutes and 30 seconds, use:
<a href="#t=2:30" class="timestamp">2:30</a>
"""

    return f"""Explain the key points in the below video transcription. 
Format your response as HTML with proper headings, paragraphs, and lists.
Include a title at the top.

IMPORTANT FORMATTING REQUIREMENTS:
1. {timestamp_instruction}
2. Return only raw HTML without any code block markers or backticks.
3. These timestamp links will be used to control the embedded video player.

Video source: {source}

Transcript (with timestamps):
{transcript_text}"""


def get_markdown_prompt(source, transcript_text, timestamp_map=None):
    """
    Returns a prompt template for generating Markdown-formatted responses with timestamps.
    
    Args:
        source: The source URL or video ID
        transcript_text: The transcript text to analyze with timestamps
        timestamp_map: A dictionary mapping timestamp strings to seconds
    
    Returns:
        A formatted prompt string for Markdown output
    """
    timestamp_instruction = """
When you mention specific points in the video, please reference them using timestamps.
The transcript contains timestamps in [MM:SS] format at the beginning of segments.
When referencing timestamps in your response, use the format MM:SS without brackets.
"""

    return f"""Explain the key points in the below video transcription. 
Format your response in Markdown with proper headings, lists, and emphasis.
Include a title at the top.

IMPORTANT:
{timestamp_instruction}

Video source: {source}

Transcript (with timestamps):
{transcript_text}"""