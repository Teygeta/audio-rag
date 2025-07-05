import os
import subprocess
import json



def get_audio_duration(audio_path):
    """
    Gets the duration of an audio file in seconds using ffprobe.
    """
    try:
        command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return duration
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error getting audio duration with ffprobe: {e}", file=sys.stderr)
        return None
