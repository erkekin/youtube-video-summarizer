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
Include a title at the top. 
Video source: {source}

{transcript_text}"""