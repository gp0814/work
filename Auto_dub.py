import os
from moviepy.editor import VideoFileClip, AudioFileClip
from googletrans import Translator
from gtts import gTTS

try:
    import yt_dlp as youtube_dl  # Replacing outdated `youtube_dl` with `yt_dlp`
except ImportError:
    raise ImportError(
        "yt_dlp is not installed. Install it using `pip install yt_dlp`."
    )

def download_video(video_url, output_path="video.mp4"):
    """
    Downloads a YouTube video using yt_dlp.
    """
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Video downloaded: {output_path}")
    except Exception as e:
        print(f"Error downloading video: {e}")

def extract_audio(video_path, output_audio_path="audio.mp3"):
    """
    Extracts audio from the given video file.
    """
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_audio_path)
        print(f"Audio extracted: {output_audio_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")

def generate_translated_audio(input_text, target_language, output_audio_path="translated_audio.mp3"):
    """
    Translates the given text to the target language and generates audio using gTTS.
    """
    try:
        translator = Translator()
        translated_text = translator.translate(input_text, dest=target_language).text
        tts = gTTS(translated_text, lang=target_language)
        tts.save(output_audio_path)
        print(f"Translated audio saved: {output_audio_path}")
    except Exception as e:
        print(f"Error generating translated audio: {e}")

def merge_audio_video(video_path, audio_path, output_path="dubbed_video.mp4"):
    """
    Merges a new audio file with the original video.
    """
    try:
        video = VideoFileClip(video_path)
        new_audio = AudioFileClip(audio_path)
        video = video.set_audio(new_audio)
        video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print(f"Dubbed video saved: {output_path}")
    except Exception as e:
        print(f"Error merging audio and video: {e}")

def main():
    # User inputs
    video_url = input("Enter YouTube video URL: ").strip()
    target_language = input("Enter target language (e.g., 'es' for Spanish, 'fr' for French): ").strip()
    
    # File paths
    video_path = "video.mp4"
    audio_path = "audio.mp3"
    translated_audio_path = "translated_audio.mp3"
    dubbed_video_path = "dubbed_video.mp4"
    
    # Workflow
    try:
        download_video(video_url, video_path)
        extract_audio(video_path, audio_path)
        
        # Add subtitles manually or use a separate subtitle extractor
        input_text = input("Enter text to translate (e.g., subtitle text): ").strip()
        generate_translated_audio(input_text, target_language, translated_audio_path)
        
        merge_audio_video(video_path, translated_audio_path, dubbed_video_path)
        print("Auto-dubbing process completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
