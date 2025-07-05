from transcription_pipeline.transcriber import select_file, convert_to_audio, transcribe_audio_api, generate_title_with_gemini

import os
from datetime import datetime

import argparse
import sys

from app_upload import run_upload_flow
from app_query import run_query_flow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MP4-RAG: Transcribe audio, index, and query the knowledge base.")
    parser.add_argument("--upload", action="store_true", help="Run the file upload and transcription flow.")
    parser.add_argument("--query", type=str, help="Query the knowledge base with a given string.")
    
    args = parser.parse_args()

    if args.upload:
        run_upload_flow()
    elif args.query:
        run_query_flow(args.query)
    else:
        print("Please specify an action: --upload to process a file, or --query \"your question\" to query the knowledge base.")
        sys.exit(1)
