import pyaudio
import wave
from faster_whisper import WhisperModel
import os
import time

NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

def transcribe_chunk(model, file_path):
    segments, info = model.transcribe(file_path, beam_size=5)
    transcription = ' '.join(segment.text for segment in segments)
    return transcription

def record_chunk(p, stream, file_path, chunk_length=1):
    frames = []
    for _ in range(0, int(16000 / 1024 * chunk_length)):
        #data = stream.read(256, exception_on_overflow=True)
        try:
            data = stream.read(256, exception_on_overflow=False)  # Ignore overflow errors
        except OSError as e:
            print(f"Warning: Audio buffer overflowed - {e}")
            return  # Skip processing this chunk

        frames.append(data)

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

def main2():
    # Choose your model settings
    model_size = "medium.en"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=512,
                    stream_callback=None)

    accumulated_transcription = ""  # Initialize an empty string to accumulate transcriptions

    try:
        while True:
            chunk_file = "temp_chunk.wav"
            record_chunk(p, stream, chunk_file)
            transcription = transcribe_chunk(model, chunk_file)
            print(NEON_GREEN + transcription + RESET_COLOR)
            os.remove(chunk_file)

            # Append the new transcription to the accumulated transcription
            accumulated_transcription += transcription + " "

    except KeyboardInterrupt:
        print("Stopping...")
        # Write the accumulated transcription to the log file
        with open("log.txt", "w") as log_file:
            log_file.write(accumulated_transcription)
    finally:
        print("LOG:" + accumulated_transcription)
        if stream.is_active():  # Only stop if stream is open
            stream.stop_stream()
            stream.close()
        p.terminate()


if __name__ == "__main__":
    main2()