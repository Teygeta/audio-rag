import sys
import os
import subprocess
import importlib.util

def check_python_version():
    print("Checking Python version...")
    if sys.version_info.major == 3 and sys.version_info.minor >= 10: # Assuming Python 3.10+ is required
        print(f"Python version {sys.version.split()[0]} is compatible. [OK]")
        return True
    else:
        print(f"Python version {sys.version.split()[0]} is not compatible. Please use Python 3.10 or higher. [FAIL]")
        return False

def check_dependencies():
    print("Checking Python dependencies...")
    required_modules = [
        "pydub", "openai", "google.generativeai", "chromadb", "dotenv",
        "langchain_openai", "langchain_chroma", "langchain_text_splitters"
    ]
    all_ok = True
    for module in required_modules:
        if importlib.util.find_spec(module):
            print(f"  - {module}: Installed. [OK]")
        else:
            print(f"  - {module}: Not installed. Please run 'pip install -r requirements.txt'. [FAIL]")
            all_ok = False
    return all_ok

def check_ffmpeg():
    print("Checking FFmpeg installation...")
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("FFmpeg is installed and accessible. [OK]")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg is not installed or not in PATH. Please install FFmpeg. [FAIL]")
        return False

def check_api_keys():
    print("Checking API keys...")
    from dotenv import load_dotenv
    load_dotenv() # Load .env file

    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")

    all_ok = True
    if openai_key:
        print("  - OPENAI_API_KEY: Set. [OK]")
    else:
        print("  - OPENAI_API_KEY: Not set. Please add it to your .env file. [FAIL]")
        all_ok = False
    
    if google_key:
        print("  - GOOGLE_API_KEY: Set. [OK]")
    else:
        print("  - GOOGLE_API_KEY: Not set. Please add it to your .env file. [FAIL]")
        all_ok = False
    return all_ok

def check_chroma_db_directory():
    print("Checking ChromaDB directory...")
    db_path = "chroma_db"
    if os.path.exists(db_path) and os.path.isdir(db_path):
        print(f"Directory '{db_path}' exists. [OK]")
        return True
    else:
        print(f"Directory '{db_path}' does not exist. It will be created when you index data. [WARNING]")
        return True # It's a warning, not a critical failure for setup

def main():
    print("\n--- Running Project Setup Verification ---")

    results = {
        "python_version": check_python_version(),
        "dependencies": check_dependencies(),
        "ffmpeg": check_ffmpeg(),
        "api_keys": check_api_keys(),
        "chroma_db_dir": check_chroma_db_directory()
    }

    print("\n--- Verification Summary ---")
    all_passed = True
    for check, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{check.replace('_', ' ').title()}: {status}")
        if not passed and check != "chroma_db_dir": # chroma_db_dir is a warning, not a hard fail
            all_passed = False

    if all_passed:
        print("\nAll critical checks passed! Your environment should be ready.")
        sys.exit(0)
    else:
        print("\nSome critical checks failed. Please address the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
