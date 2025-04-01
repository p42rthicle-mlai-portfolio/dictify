**1. Files:**
1. `transcribe_gpu.py` for GPU offline
2. `transcribe_colab.py` for [Google colab](https://colab.research.google.com/drive/1YDx0bYgQ2V2Dd3E5BPIpi5q_T9wPhZUy?usp=sharing)
3. `real_time_transcriber.py` for CPU machine (Running very slow).  

**1. Setup Venv:**

```bash
# In project dir
python3 -m venv venv  
source venv/bin/activate
```

**2. Install Deps:**

```bash
pip install pyaudio wave
# macOS: brew install portaudio (Might be needed too before)
pip install faster-whisper
# macOS: brew install ffmpeg ((Might be needed if errors)
```

**3. Run:**

```bash
python transcriber_gpu.py
```

**4. Quick Fixes / Troubleshooting:**

*   **NumPy >= 2.0 Crash?:** `pip install "numpy<2" --force-reinstall`
*   **OMP: Error #15 (OpenMP Conflict)?** 
    -  Option A: Environment Variable (Workaround) - `export KMP_DUPLICATE_LIB_OK=TRUE` (before running script)
    -  Option B: Check & Reinstall Packages
       ```bash
        # Delete conflicting ones (these are the ones I encountered)
        pip uninstall torch ctranslate2 onnxruntime faster-whisper
        # Reinstall the ones that you need (These two steps in same virtual environment fixed it)
        # --no-cache-dir: pip wont use cached version that might be problematic
        pip install --no-cache-dir faster-whisper pyaudio
       ```
*   **Check GPU:** `python -c "import torch; print(torch.cuda.is_available())"`
*   Crucial for GPU: Install PyTorch *first*, making sure it supports your CUDA version. Go to [pytorch.org](https://pytorch.org/get-started/locally/), find the command for your setup (OS/CUDA), and run it. Example ( **Check the website for *your* command!** ):
        ```bash
        # Example for CUDA 11.8 - DON'T COPY PASTE, GET YOURS!
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        ```