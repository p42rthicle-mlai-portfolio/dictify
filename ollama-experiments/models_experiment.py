import requests
import json
import time

ollama_url = "http://localhost:11434/api/generate"
models = ["phi4-mini", "mistral", "llama3.2"] # Add models you have downloaded
prompt = "Explain the difference between AI, Machine Learning, and Deep Learning in simple terms."

for model in models:
    print(f"\n--- Testing Model: {model} ---")
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False # Keep stream false for simple timing first
    }
    try:
        start_time = time.time()
        res = requests.post(ollama_url, json=payload)
        res.raise_for_status() # Raise an exception for bad status codes
        end_time = time.time()

        res_data = res.json()
        print(f"Response Received (in {end_time - start_time:.2f} seconds):")
        print(res_data.get("response", "No response field found")) # Extract the main text

    except requests.exceptions.RequestException as e:
        print(f"Error querying {model}: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from {model}")
        print("Raw response:", res.text)