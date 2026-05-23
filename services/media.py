import os
import subprocess
import tempfile

import yt_dlp


def download_video(url):
    """Download a video URL to a temporary file and return its path."""
    tmp_dir = tempfile.mkdtemp()
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": os.path.join(tmp_dir, "video.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = info.get("ext", "mp4")
    return os.path.join(tmp_dir, f"video.{ext}")


def burn_subtitles(video_path, srt_path):
    out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    out.close()
    srt_escaped = srt_path.replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles='{srt_escaped}'",
        "-c:a", "copy",
        out.name,
    ]
    subprocess.run(cmd, capture_output=True)
    return out.name


def extract_audio_for_api(media_path):
    out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    out.close()
    cmd = [
        "ffmpeg", "-y",
        "-i", media_path,
        "-vn",
        "-acodec", "libmp3lame",
        "-ar", "16000",
        "-ac", "1",
        out.name,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out.name
