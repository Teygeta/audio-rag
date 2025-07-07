from setuptools import setup, find_packages

setup(
    name='audio-rag', 
    version='0.1.0', 
    packages=find_packages(),
    
    
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