import os
import subprocess
import sys

def create_venv():
    """Creates a virtual environment if it doesn't exist."""
    venv_dir = os.path.join(os.path.dirname(__file__), '.venv')
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
            print("Virtual environment created.")
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to create virtual environment: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Virtual environment already exists. Skipping creation.")

def activate_venv_and_run(command):
    """Activates the virtual environment and runs a command."""
    venv_dir = os.path.join(os.path.dirname(__file__), '.venv')
    if sys.platform == 'win32':
        activate_script = os.path.join(venv_dir, 'Scripts', 'activate')
        # On Windows, activating in a script is tricky. We'll just use the python/pip from venv directly.
        python_executable = os.path.join(venv_dir, 'Scripts', 'python')
    else:
        activate_script = os.path.join(venv_dir, 'bin', 'activate')
        python_executable = os.path.join(venv_dir, 'bin', 'python')

    # Ensure the venv python is used
    if isinstance(command, list):
        if command[0] == 'pip':
             command[0] = os.path.join(os.path.dirname(python_executable), 'pip')
        elif command[0] == 'python':
             command[0] = python_executable

    try:
        print(f"Running command: {' '.join(command)}")
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e}", file=sys.stderr)
        sys.exit(1)

def install_dependencies():
    """Installs dependencies from requirements.txt."""
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_file):
        print("Installing Python dependencies from requirements.txt...")
        activate_venv_and_run(['pip', 'install', '-r', req_file])
        print("Dependencies installed.")
    else:
        print("Warning: requirements.txt not found. Skipping dependency installation.", file=sys.stderr)

def setup_env_file():
    """Prompts for API keys and saves to .env."""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            pass # Create empty .env file
        print(".env file created.")

    print("Checking for API keys in .env...")
    env_content = ""
    with open(env_file, 'r') as f:
        env_content = f.read()

    if 'OPENAI_API_KEY' not in env_content:
        openai_key = input("Enter your OpenAI API Key: ")
        with open(env_file, 'a') as f:
            f.write(f"OPENAI_API_KEY='{openai_key}'\n")
        print("OPENAI_API_KEY added to .env")
    else:
        print("OPENAI_API_KEY already exists in .env. Skipping.")

    if 'GOOGLE_API_KEY' not in env_content:
        google_key = input("Enter your Google API Key (for Gemini): ")
        with open(env_file, 'a') as f:
            f.write(f"GOOGLE_API_KEY='{google_key}'\n")
        print("GOOGLE_API_KEY added to .env")
    else:
        print("GOOGLE_API_KEY already exists in .env. Skipping.")

def main():
    print("--- Setting up MP4-RAG Project ---")
    create_venv()
    # Activate venv and upgrade pip
    activate_venv_and_run(['pip', 'install', '--upgrade', 'pip'])
    install_dependencies()
    # Install the project in editable mode to register entry points
    activate_venv_and_run(['pip', 'install', '-e', '.'])
    setup_env_file()
    print("--- Setup Complete! ---")
    print("To activate the virtual environment, run:")
    if sys.platform == 'win32':
        print("  .venv\\Scripts\\activate")
    else:
        print("  source .venv/bin/activate")

if __name__ == "__main__":
    main()
