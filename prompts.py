"""
This module contains the prompt templates used for generating AI responses.
"""

def get_html_prompt(source, transcript_text):
    """
    Returns a prompt template for generating HTML-formatted responses.
    
    Args:
        source: The source URL or video ID
        transcript_text: The transcript text to analyze
    
    Returns:
        A formatted prompt string for HTML output
    """
    return f"""Explain the key points in the below video transcription. 
Format your response as HTML with proper headings, paragraphs, and lists. 
Include a title at the top. 
Provide timestamps for key points if possible. They should be a href links to correct timestamp of the original video like below.
<a href="https://youtu.be/eazqDdpsK8s?t=121">[2:01]</a>
if you can't provide timestamps, you can skip it.
Remove all ads and irrelevant information, sponsorships, etc.
IMPORTANT: Return only raw HTML without any code block markers or backticks. 
Video source: {source}

{transcript_text}"""


def get_markdown_prompt(source, transcript_text):
    """
    Returns a prompt template for generating Markdown-formatted responses.
    
    Args:
        source: The source URL or video ID
        transcript_text: The transcript text to analyze
    
    Returns:
        A formatted prompt string for Markdown output
    """
    return f"""Explain the key points in the below video transcription. 
Format your response in Markdown with proper headings, lists, and emphasis.
Remove all ads and irrelevant information, sponsorships, etc.
Include a title at the top. 
Video source: {source}

{transcript_text}"""