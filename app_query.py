import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

from rag_system.retriever import query_chroma_db

load_dotenv()

def run_query_flow(query_string):
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set it with: export GOOGLE_API_KEY='YOUR_API_KEY_GOOGLE'", file=sys.stderr)
        sys.exit(1)

    model_type = os.getenv("LLM_TYPE", "gemini")
    if model_type == "gemini":
        print("Sono dentro gemini")

        if not os.getenv("GOOGLE_API_KEY"):
            print("Error: GOOGLE_API_KEY environment variable is not set.", file=sys.stderr)
            print("Please set it with: export GOOGLE_API_KEY='YOUR_API_KEY_GOOGLE'", file=sys.stderr)
            sys.exit(1)
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))
    elif model_type == "ollama":
        print("Sono dentro ollama")
        try:
            from langchain_community.llms import Ollama
            model = Ollama(model=os.getenv("OLLAMA_MODEL", "llama2"))
        except ImportError:
            print("Error: langchain_community is not installed. Please install it with 'pip install langchain-community'", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: Unknown LLM_TYPE: {model_type}. Please set LLM_TYPE to 'gemini' or 'ollama'.", file=sys.stderr)
        sys.exit(1)

    print(f"Querying knowledge base for: \"{query_string}\"")
    relevant_docs = query_chroma_db(query_string)

    if relevant_docs:
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        prompt = f"""Based on the following context, answer the question. If the answer is not in the context, say "Non ho informazioni sufficienti per rispondere a questa domanda basandomi sul contesto fornito.".\n\n        Context:\n        {context}\n\n        Question: {query_string}\n\n        Answer:"""
        print("\nGenerating AI response...")
        try:
            if model_type == "gemini":
                response = model.generate_content(prompt)
            elif model_type == "ollama":
                response = model.invoke(prompt)
            print("\nAI Response:")
            if model_type == "gemini":
                print(response.text.strip())
            elif model_type == "ollama":
                print(response.strip())
        except Exception as e:
            print(f"Error generating AI response: {e}", file=sys.stderr)
    else:
        print("No relevant documents found for your query. Cannot generate an AI response.")

def main():
    if len(sys.argv) > 1:
        query_string = " ".join(sys.argv[1:])
        run_query_flow(query_string)
    else:
        print("Usage: python app_query.py <your_query_string>")
        sys.exit(1)

if __name__ == "__main__":
    main()