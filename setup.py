from setuptools import setup, find_packages

setup(
    name='audio-rag', 
    version='0.1.0', 
    packages=find_packages(),
    py_modules=['verify_setup'],
    entry_points={
        'console_scripts': [
            'run-app-query = app_query:main', 
            'run-app-upload = app_upload:main', 
            'verify-setup = verify_setup:main', 
            'setup-project = setup_project:main', # Cross-platform setup script
            'show-db = rag_system.verifier:main', # Show ChromaDB contents
            'manage-db = rag_system.cleaner:main', # Manage ChromaDB (list, delete, delete-all)
        ],
    },
    install_requires=[
        'pydub',
        'google-generativeai',
        'chromadb',
        'python-dotenv',
        'openai',
        'langchain_openai',
        'langchain_chroma',
        'langchain_text_splitters',
    ],
)