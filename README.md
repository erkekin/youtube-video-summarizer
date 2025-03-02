YouTube Transcription Summarizer
A web service that generates AI-powered summaries of YouTube videos based on their transcriptions.

Features
Extract transcriptions from any YouTube video (including YouTube Shorts)
Generate concise AI summaries using Google's Gemini model
View embedded video alongside the summary
Supports dark mode (follows system preferences)
API access for programmatic use
Persistent storage of transcription history
Installation
Prerequisites
Python 3.7+
pip
Setup
Clone the repository:
Install the required packages:
Create a .env file in the project root with your Gemini API key:
You can obtain a Gemini API key from Google AI Studio.

Usage
Running the Server
For development:

For production:

The server will be accessible at http://localhost:6666.

Using the Web Interface
Navigate to http://localhost:6666 in your web browser
Enter a YouTube URL or video ID in the input field
Click "Get Summary"
Wait for the processing to complete
View the embedded video and AI-generated summary
Using the API
You can access the transcription service programmatically:

Example:

API responses are returned in Markdown format.

File Structure
Deployment
Running as a Systemd Service
Create a systemd service file:
Add the following content:
Enable and start the service:
Troubleshooting
If you encounter "Address already in use" errors:

Or restart the service:

License
MIT License