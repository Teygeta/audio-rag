from transcription_pipeline.transcriber import select_file, convert_to_audio, transcribe_audio_api, generate_title_with_gemini

import os
from datetime import datetime
import sys

def run_upload_flow():
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
            
            transcribed_data = transcribe_audio_api(audio_file_path, transcriptions_directory, os.path.basename(selected_file))
            
            if transcribed_data:
                transcribed_text, temp_text_path = transcribed_data

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
                        # Index the transcription in the vector database
                        from rag_system.indexer import index_transcription
                        index_transcription(final_text_path)
                    except OSError as e:
                        print(f"Error renaming file {temp_text_path} to {final_text_path}: {e}", file=sys.stderr)
                else:
                    # If title generation fails, keep the original name
                    final_text_path = os.path.join(transcriptions_directory, os.path.basename(temp_text_path).replace("temp_", ""))
                    os.rename(temp_text_path, final_text_path)
                    print(f"Title generation failed. Transcription file saved as: {final_text_path}")
                    # Index the transcription in the vector database (even if the title is generic)
                    from rag_system.indexer import index_transcription
                    index_transcription(final_text_path)

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

if __name__ == "__main__":
    run_upload_flow()
