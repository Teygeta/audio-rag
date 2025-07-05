import json
import os
from datetime import datetime

LOG_FILE = os.path.join(os.getcwd(), "logs", "api_usage.jsonl")

def log_api_usage(file_name: str, api_provider: str, operation: str, input_tokens: int = 0, output_tokens: int = 0, total_tokens: int = 0, estimated_cost: float = 0.0):
    """
    Logs API usage data to a JSONL file.
    Each log entry is a JSON object on a new line.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "file_name": file_name,
        "api_provider": api_provider,
        "operation": operation,
    }
    if api_provider == "OpenAI":
        log_entry["estimated_cost"] = estimated_cost
    else: # Gemini
        log_entry["input_tokens"] = input_tokens
        log_entry["output_tokens"] = output_tokens
        log_entry["total_tokens"] = total_tokens

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')

    if api_provider == "OpenAI":
        print(f"[LOG] API usage logged for {api_provider} - {operation} on {file_name}. Estimated Cost: ${estimated_cost:.4f}")
    else:
        print(f"[LOG] API usage logged for {api_provider} - {operation} on {file_name}. Tokens: Input={input_tokens}, Output={output_tokens}, Total={total_tokens}")

