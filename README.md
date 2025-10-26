# Dictify (AI Dictation) — (Ongoing/WIP) 🚧

Dictify is a privacy-focused **local speech-to-text assistant** that runs **Whisper** and **Ollama** models entirely offline.  
It aims to provide accurate transcription and intelligent text refinement **without sending user data to cloud APIs**.  

---

## Overview

Dictify enables users to **record speech**, **transcribe it locally** using Whisper, and **refine or summarize** it using Ollama. Live Editing.  
The system demonstrates a modular orchestration layer that ties together these AI components efficiently and transparently.

## Pipeline overview:

Audio Input → Whisper Transcription → Ollama Text Processing → Output Transcript


*(All steps are local; no external API calls.)*

---

## Design Philosophy
  
Modern speech-to-text tools often rely on remote servers, sacrificing privacy for convenience. Idea is to have a mvp of local transcription with live editing feature

You should be able to dictate the AI and it will edit the text that it has already transcribed even

- Running **AI inference locally** for security and latency benefits  
- Using **modular orchestration** rather than monolithic pipelines  
- Combining **open models** (Whisper + Ollama) to perform high-quality transcription and contextual rewriting
- Basic idea is to break transcribed texts or audios into chunks and NLP will understand if its text input or an instruction.   
- Maintaining extensibility for downstream NLP tasks (summarization, tagging, command generation)

---

## Screenshot (transcription collab notebook)

<img width="600" height="500" alt="Image" src="https://github.com/user-attachments/assets/f47e52d8-1c4a-49b0-9c2e-ad0cff1b86b0" />

---

## Progress

- Whisper transcription working (GPU / Colab / Real-time CPU)  
-  Ollama integration for text post-processing  (experimental - in progress)
-  Conceptual orchestration pipeline (`run_pipeline.py`) added  
- UI and full modular orchestration planned  

---

## Notes
This is a project in progress, its a conceptual project I started after having a look at aquavoice. Currently learning more of GenAI and how this project can come to life. 
