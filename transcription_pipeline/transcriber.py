import subprocess
import sys
import os
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

import google.generativeai as genai
from .logger import log_api_usage
from .utils import get_audio_duration

def select_file_applescript():
    """
    Uses an AppleScript command to open a native macOS file selection dialog.
    This is a workaround for environments where tkinter is not available.
    """
    applescript = """
    tell application "System Events"
        activate
        try
            set the_file to choose file with prompt "Select a video or audio file:" of type {"public.movie", "public.audio", "public.mpeg", "public.mp3", "com.apple.quicktime-movie", "public.avi", "public.mpeg-4", "public.aiff-audio", "public.wav", "com.microsoft.waveform-audio"}
            return POSIX path of the_file
        on error number -128 -- User cancelled
            return ""
        end try
    end tell
    """
    try:
        proc = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            check=True
        )
        file_path = proc.stdout.strip()
        if file_path:
            return file_path
        else:
            return None
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing AppleScript: {e}", file=sys.stderr)
        return None

def select_file():
    if sys.platform != "darwin":
        print("This file selection method is currently only implemented for macOS.")
        return None
    return select_file_applescript()



def convert_to_audio(video_path, temp_dir):
    """
    Converts the video file to an MP3 audio file using FFmpeg.
    """
    if not video_path:
        print("No video file provided for conversion.")
        return None
    try:
        base_name = os.path.basename(video_path)
        file_name_without_ext = os.path.splitext(base_name)[0]
        unique_id = uuid.uuid4().hex[:8]
        output_audio_path = os.path.join(temp_dir, f"{file_name_without_ext}_{unique_id}.mp3")
        print(f"\nStarting conversion of '{base_name}' to audio...")
        # Base FFmpeg command
        command = [
            'ffmpeg',
            '-i', video_path,
        ]

        # If DEV_MODE is active, process only the first 30 seconds
        if os.getenv('DEV_MODE') == 'true':
            print("\nDEV mode active: audio file will be limited to the first 30 seconds of the video.")
            command.extend(['-t', '30'])

        # Add remaining parameters for audio conversion
        command.extend([
            '-vn',
            '-filter:a', 'atempo=2.0',
            '-ar', '44100',
            '-ac', '2',
            '-b:a', '192k',
            '-y',
            output_audio_path
        ])
        proc = subprocess.run(command, capture_output=True, text=True)
        if proc.returncode == 0:
            print(f"Conversion completed successfully!")
            print(f"Audio file saved to: {output_audio_path}")
            return output_audio_path
        else:
            print("Error during FFmpeg conversion.", file=sys.stderr)
            print(f"Stderr: {proc.stderr}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"An unexpected error occurred during conversion: {e}", file=sys.stderr)
        return None

def generate_title_with_gemini(transcription_text, original_file_name):
    """Generates a title for the transcription using the Gemini API."""
    if not transcription_text:
        print("No transcription text provided for title generation.")
        return None

    try:
        if not os.getenv("GOOGLE_API_KEY"):
            print("Error: GOOGLE_API_KEY environment variable is not set.", file=sys.stderr)
            print("Please set it with: export GOOGLE_API_KEY='YOUR_API_KEY_GOOGLE'", file=sys.stderr)
            return None

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

        prompt = f"""Generate a concise and descriptive title (maximum 10 words) for the following audio transcription. The title should be suitable as a filename, in lowercase snake_case (e.g., 'my_new_title'). Return ONLY the title, without any introduction, explanation or additional text. Do not include quotes or special characters in the title, only the snakecase character "_". The title must be ready for use as a filename.

Transcription:
{transcription_text}"""

        print("\nRequesting title generation from Gemini...")
        response = model.generate_content(prompt)
        title = response.text.strip()

        # Log Gemini API usage
        input_tokens_gemini = 0
        output_tokens_gemini = 0
        total_tokens_gemini = 0

        if hasattr(response, 'usage_metadata'):
            usage = response.usage_metadata
            input_tokens_gemini = usage.prompt_token_count
            output_tokens_gemini = usage.candidates_token_count
            total_tokens_gemini = usage.total_token_count
        log_api_usage(original_file_name, "Gemini", "title_generation", input_tokens_gemini, output_tokens_gemini, total_tokens_gemini)

        # Post-process the title to ensure snake_case
        title = title.lower() # Convert to lowercase
        title = title.replace(" ", "_") # Replace spaces with underscores
        title = "".join(c for c in title if c.isalnum() or c == '_') # Keep only alphanumeric and underscores
        title = title[:50] # Limit title length for safety

        print(f"Title generated by Gemini: {title}")
        return title

    except Exception as e:
        print(f"An error occurred during title generation with Gemini: {e}", file=sys.stderr)
        return None


# Modify the transcribe_audio_api function to return the transcribed text
def transcribe_audio_api(audio_path, transcriptions_dir, original_file_name):
    """Transcribes the audio file using the OpenAI API and saves the text."""
    if not audio_path:
        print("No audio file provided for transcription.")
        return None
    try:
        if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
            print("Please set it with: export OPENAI_API_KEY='YOUR_API_KEY'", file=sys.stderr)
            return None
        client = OpenAI()
        print(f"\nSending '{os.path.basename(audio_path)}' to OpenAI API for transcription...")
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=os.getenv("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-transcribe"),
                file=audio_file
            )
        transcribed_text = transcription.text

        # Calculate estimated cost based on audio duration
        audio_duration = get_audio_duration(audio_path)
        estimated_cost = 0.0
        if audio_duration is not None:
            # OpenAI Whisper API cost: $0.006 / minute
            estimated_cost = (audio_duration / 60) * 0.006

        log_api_usage(original_file_name, "OpenAI", "transcription", estimated_cost=estimated_cost)
        
        # Save the transcribed text to a temporary file for title generation
        # The final filename will be decided after title generation
        temp_text_path = os.path.join(transcriptions_dir, "temp_transcription.txt")
        with open(temp_text_path, 'w', encoding='utf-8') as f:
            f.write(transcribed_text)

        print(f"API transcription completed successfully! Text saved temporarily.")
        return transcribed_text, temp_text_path # Returns the text and temporary path

    except Exception as e:
        print(f"An unexpected error occurred during API transcription: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    print("Opening native macOS file selection dialog...")
    selected_file = select_file()
    if selected_file:
        print(f"File selected successfully!")
        print(f"Path: {selected_file}")
        temp_directory = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_directory, exist_ok=True)
        audio_file_path = convert_to_audio(selected_file, temp_directory)
        if audio_file_path:
            transcriptions_directory = os.path.join(os.getcwd(), "transcriptions")
            os.makedirs(transcriptions_directory, exist_ok=True)
            
            # Call the API transcription which now returns the text and temporary path
            transcribed_data = transcribe_audio_api(audio_file_path, transcriptions_directory, os.path.basename(selected_file))
            
            if transcribed_data:
                transcribed_text, temp_text_path = transcribed_data

                # Generate title with Gemini
                generated_title = generate_title_with_gemini(transcribed_text, os.path.basename(selected_file))

                if generated_title:
                    # Get the creation date of the original file
                    creation_timestamp = os.path.getctime(selected_file)
                    creation_date = datetime.fromtimestamp(creation_timestamp).strftime('%Y-%m-%d')
                    
                    # Add the date as a prefix to the title
                    final_title = f"{creation_date}_{generated_title}"

                    # Rename the transcription file with the generated title and date
                    final_text_path = os.path.join(transcriptions_directory, f"{final_title}.txt")
                    try:
                        os.rename(temp_text_path, final_text_path)
                        print(f"Transcription file renamed to: {final_text_path}")
                    except OSError as e:
                        print(f"Error renaming file {temp_text_path} to {final_text_path}: {e}", file=sys.stderr)
                else:
                    # If title generation fails, keep the original name
                    final_text_path = os.path.join(transcriptions_directory, os.path.basename(temp_text_path).replace("temp_", ""))
                    os.rename(temp_text_path, final_text_path)
                    print(f"Title generation failed. Transcription file saved as: {final_text_path}")

                # Cleanup: delete temporary audio file
                print(f"\nCleanup: deleting temporary audio file: {audio_file_path}")
                try:
                    os.remove(audio_file_path)
                    print("Temporary file deleted successfully.")
                except OSError as e:
                    print(f"Error deleting file {audio_file_path}: {e}", file=sys.stderr)
            else:
                print("API transcription failed, cannot proceed with title generation.")
    else:
        print("\nNo file selected or operation cancelled.")