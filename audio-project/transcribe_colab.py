# 1. Install necessary packages in Colab
# Using -q for quieter installation
# !pip install -q gradio faster-whisper torch torchaudio soundfile ctranslate2

import gradio as gr
import numpy as np
from faster_whisper import WhisperModel
import time
import os
import soundfile as sf # Better for saving numpy arrays to WAV

# 2. Load the faster-whisper model (do this once)
# Choose a model size suitable for GPU, medium.en or large-v3 are good choices
model_size = "large-v3"
device_type = "cuda" # Use "cuda" for Nvidia GPU in Colab
compute_type = "float16" # Use "float16" for faster GPU inference

print(f"Loading model: {model_size} on {device_type} with {compute_type}...")
try:
    # Try loading on GPU first
    model = WhisperModel(model_size, device=device_type, compute_type=compute_type)
    print("Model loaded successfully on GPU.")
except Exception as e:
    print(f"ERROR: Failed to load model on GPU: {e}")
    print("Attempting to load on CPU...")
    try:
        # Fallback to CPU if GPU fails
        device_type = "cpu"
        compute_type = "int8" # Quantized for CPU
        model = WhisperModel(model_size, device=device_type, compute_type=compute_type)
        print("Model loaded successfully on CPU (int8).")
    except Exception as e_cpu:
        print(f"ERROR: Failed to load model on CPU as well: {e_cpu}")
        # If model loading fails completely, we can't proceed
        model = None # Indicate model loading failed

# 3. Define the function that Gradio will call
def transcribe_microphone_input(audio_input):
    """
    Receives audio data from Gradio microphone, transcribes it using faster-whisper.
    """
    if model is None:
        return "ERROR: Whisper model failed to load. Cannot transcribe."

    if audio_input is None:
        return "No audio recorded. Click the microphone, record, and click stop."

    # Gradio microphone input provides a tuple: (sample_rate, numpy_data)
    sample_rate, audio_data = audio_input

    print(f"Received audio: Sample Rate={sample_rate}, Duration={len(audio_data)/sample_rate:.2f}s")

    # Ensure audio data is float32, as expected by many audio processing libs/models
    audio_data = audio_data.astype(np.float32)

    # Optional: Normalize audio (can sometimes improve transcription)
    audio_data = audio_data / np.max(np.abs(audio_data))

    # Save the numpy array to a temporary WAV file that faster-whisper can read
    temp_filename = f"temp_audio_{time.time_ns()}.wav"
    try:
        print(f"Saving temporary audio to {temp_filename}...")
        sf.write(temp_filename, audio_data, sample_rate)
        print("Temporary file saved.")
    except Exception as e:
        print(f"Error saving temporary audio file: {e}")
        return f"ERROR: Could not save temporary audio file: {e}"

    # Perform transcription
    transcription_text = "Transcription failed." # Default message
    try:
        print(f"Starting transcription using {model_size} ({device_type}, {compute_type})...")
        start_time = time.time()
        # You can add vad_filter=True here for Voice Activity Detection if desired
        segments, info = model.transcribe(temp_filename, beam_size=5) #, vad_filter=True)

        # Combine segments into a single string
        transcription_text = " ".join(segment.text for segment in segments).strip()

        end_time = time.time()
        duration = end_time - start_time
        print(f"Transcription complete in {duration:.2f} seconds.")
        print(f"Detected language: {info.language} (Prob: {info.language_probability:.2f})")
        print(f"Transcription Result: '{transcription_text}'")

        if not transcription_text:
             transcription_text = "(No speech detected or empty transcription)"

    except Exception as e:
        print(f"Error during transcription: {e}")
        transcription_text = f"ERROR: Transcription failed: {e}"
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
                print(f"Removed temporary file: {temp_filename}")
            except Exception as e_del:
                print(f"Warning: Could not remove temporary file {temp_filename}: {e_del}")

    return transcription_text

# 4. Create and launch the Gradio Interface
print("Setting up Gradio interface...")
iface = gr.Interface(
    fn=transcribe_microphone_input,
    # Input: Use gr.Audio with source "microphone" and type "numpy"
    inputs=gr.Audio(sources=["microphone"], type="numpy", label="Record Audio Here"),
    # Output: A simple text box
    outputs=gr.Textbox(label="Transcription"),
    title="Faster-Whisper Transcription (via Microphone)",
    description="Click the microphone icon below, record your speech, press stop, and the transcription will appear.",
    # live=False means processing happens *after* user clicks stop.
    # live=True tries to process in near real-time chunks (more complex setup often needed)
    live=False,
)

print("Launching Gradio interface...")
# debug=True provides more logs, share=True gives a public link (useful for Colab)
iface.launch(debug=True, share=True)