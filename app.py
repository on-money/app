from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Setup yt-dlp options
    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }

    os.makedirs("downloads", exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)  # don’t download, just get info
            return jsonify({
                "title": info.get("title"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "direct_url": info.get("url")  # direct stream link
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "yt-dlp API is running!"
