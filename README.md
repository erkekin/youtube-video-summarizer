# YouTube Transcription Summarizer

A web service that generates AI-powered summaries of YouTube videos based on their transcriptions. Easily extract, summarize, and review video content—perfect for researchers, students, and content creators!

---

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 Features
- 🎥 **Extract transcriptions** from any YouTube video (including Shorts)
- 🤖 **Generate concise AI summaries** using Google's Gemini model
- 🖼️ **View embedded video** alongside the summary
- 🌙 **Dark mode** (follows system preferences)
- 🔗 **API access** for programmatic use
- 💾 **Persistent storage** of transcription history

---

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- pip

### Setup
```bash
# Clone the repository
$ git clone https://github.com/yourusername/youtube-video-summarizer.git
$ cd youtube-video-summarizer

# Install dependencies
$ pip install -r requirements.txt

# Create a .env file in the project root with your Gemini API key:
GEMINI_API_KEY=your_gemini_api_key_here
```
You can obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🚦 Usage

### Running the Server
For development:
```bash
python main.py
```
For production (example using Gunicorn):
```bash
gunicorn -w 4 -b 0.0.0.0:6666 main:app
```
The server will be accessible at [http://localhost:6666](http://localhost:6666).

### Using the Web Interface
1. Open your browser and go to [http://localhost:6666](http://localhost:6666)
2. Enter a YouTube URL or video ID
3. Click **Get Summary**
4. Wait for processing to complete
5. View the embedded video and AI-generated summary

### Using the API
You can access the transcription service programmatically:

#### Example Request
```bash
curl -X POST http://localhost:6666/api/summarize \
     -H 'Content-Type: application/json' \
     -d '{"youtube_url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"}'
```
#### Example Response
```json
{
  "summary": "This video discusses ...",
  "transcription": "Welcome to ..."
}
```
API responses are returned in Markdown format.

---

## ⚙️ Configuration
- **GEMINI_API_KEY**: Required. Add to your `.env` file in the project root.
- **PORT**: (Optional) Set the port with `PORT=xxxx` in `.env` (default: 6666).

---

## 📁 File Structure
```
/ (project root)
├── main.py
├── requirements.txt
├── .env
├── static/
├── templates/
└── ...
```

---

## 🚀 Deployment

### Running as a Systemd Service
1. Create a systemd service file (e.g., `/etc/systemd/system/youtube-summarizer.service`):
2. Add the following content:
   ```ini
   [Unit]
   Description=YouTube Transcription Summarizer
   After=network.target

   [Service]
   User=YOUR_USER
   WorkingDirectory=/path/to/youtube-video-summarizer
   ExecStart=/usr/bin/python3 main.py
   Restart=always
   EnvironmentFile=/path/to/youtube-video-summarizer/.env

   [Install]
   WantedBy=multi-user.target
   ```
3. Enable and start the service:
   ```bash
   sudo systemctl enable youtube-summarizer
   sudo systemctl start youtube-summarizer
   ```

---

## 🐞 Troubleshooting
- If you encounter "Address already in use" errors:
  ```bash
  sudo fuser -k 6666/tcp
  ```
- Or restart the service:
  ```bash
  sudo systemctl restart youtube-summarizer
  ```

---

## 🤝 Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements and bug fixes.

---

## 📬 Contact
For questions, suggestions, or support, please open an issue.

---

## 📝 License
MIT License
