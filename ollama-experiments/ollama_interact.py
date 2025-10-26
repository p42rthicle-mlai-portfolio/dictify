import requests
import json

# The default URL where Ollama's API listens
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def generate_text(model_name, prompt_text):
    """
    Sends a prompt to the Ollama API and returns the generated response.

    Args:
        model_name (str): The name of the Ollama model to use (e.g., 'llama3').
                          Make sure this model is downloaded via 'ollama pull <model_name>'.
        prompt_text (str): The text prompt to send to the model.

    Returns:
        str: The generated text response from the model, or None if an error occurs.
    """
    try:
        # Data payload to send to the API according to Ollama's documentation
        payload = {
            "model": model_name,
            "prompt": prompt_text,
            "stream": False  # Set stream to False for a single blocking response
            # 'context' parameter could be added here later for conversational history
        }

        print(f"--- Sending Prompt to {model_name} ---")
        print(f"Prompt: {prompt_text}")

        # Send the POST request to the Ollama API endpoint
        # 'json=payload' automatically converts the dict to JSON and sets headers
        response = requests.post(OLLAMA_API_URL, json=payload)

        # Raise an exception if the request returned an error status code (like 404 or 500)
        response.raise_for_status()

        print("--- Received Response ---")

        # Parse the JSON response from the API
        response_data = response.json()

        # Extract the actual generated text (the 'response' key in the JSON)
        generated_response = response_data.get('response') # Use .get for safety

        if generated_response:
             # Optional: Print other details from the response for learning
            # print("\nFull Response JSON:")
            # print(json.dumps(response_data, indent=2))
            return generated_response.strip() # Remove leading/trailing whitespace
        else:
            print("Error: 'response' key not found in JSON data.")
            print(json.dumps(response_data, indent=2))
            return None


    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama API at {OLLAMA_API_URL}: {e}")
        print("Is the Ollama service running?")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    # --- Experimentation ---
    # 1. Choose the model you have downloaded (check with 'ollama list')
    model_to_use = "mistral" # <--- CHANGE THIS to a model you have (e.g., "llama3.1", "phi-4mini")

    # 2. Define your prompt
    # prompt = "Explain the concept of a REST API in simple terms."
    prompt = "Write a short poem about a robot learning python in less than 100 words"
    # prompt = "What is the capital of France?"

    # 3. Call the function and print the result
    llm_response = generate_text(model_to_use, prompt)

    if llm_response:
        print(f"\nOllama ({model_to_use}) Response:")
        print(llm_response)
    else:
        print("\nFailed to get response from Ollama.")

    # --- Try another model or prompt ---
    # model_to_use_2 = "phi" # If you have 'phi' downloaded
    # prompt_2 = "Tell me a joke."
    # llm_response_2 = generate_text(model_to_use_2, prompt_2)
    # if llm_response_2:
    #     print(f"\nOllama ({model_to_use_2}) Response:")
    #     print(llm_response_2)