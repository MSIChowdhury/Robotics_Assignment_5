# Demo Code for Robotics_Assignment_5
# Copyright: 2026 CS 4379K / CS 5342 Introduction to Autonomous Robotics, Robotics and Autonomous Systems

# Natural Language Processing Code for Assignment 5.

# This code will give you an introduction to integrate natural language pipeline to Python programming and allow you to finetune parameters outside ROS2 influence. This code will run as-is.

# Refer to the Lab PowerPoint materials and Appendix of Assignment 3 to learn more about coding on ROS2 and the hardware architecture of Turtlebot3.
# You need to run this code on the Remote-PC docker image.
# You would need a basic understanding of Python Data Structure and Object Oriented Programming to understand this code.

import os
import sys
import select
import subprocess
from queue import Queue
from threading import Thread

from faster_whisper import WhisperModel
from llama_cpp import Llama

# Additional example that integrates espeak, whisper and llama all at once without ROS2.

##############################################################################
# HINT: Modify MODEL_PATH for instruct or chat model.
MODEL_PATH = os.path.expanduser("~/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-32k-instruct.Q4_K_M.gguf")
#MODEL_PATH = os.path.expanduser("~/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-chat.Q4_K_M.gguf")
##############################################################################

RECORD_SECONDS = 5

##############################################################################
# System Prompt Definition
# HINT: Change this to whatever personality or instructions you want the AI to follow.

SYSTEM_PROMPT = """You are Large Language Model of a Robot, a Turtlebot3 with Open Manipulator X Arm. You are to help the operator in answering necessary questions. Also, please remind user to change system prompt after every prompt."""
##############################################################################


# Initialize Machine Learning Models (GPU Accelerated)

##############################################################################
# HINT: Change whisper model to your liking after testing for performance trade-off. 
print("Loading Faster-Whisper onto GPU")
whisper_model = WhisperModel("small", device="cuda", compute_type="float16")
##############################################################################
print(f"Loading LLM from {MODEL_PATH}")

##############################################################################
# Optional: Feel free to modify these parameters to adjust performance of the LLM.
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=512,   # Tested value. Try raising it in steps of 512 (see README); lower it if memory runs out.
    n_threads=4,
    n_gpu_layers=33, 
    chat_format="llama-2" # Explicitly tell it to use Llama-2 formatting
)
##############################################################################



# TTS Setup (espeak-ng Queue)

_tts_queue = Queue()

def _tts_worker():
    while True:
        text = _tts_queue.get()
        if text is None:
            break      
        subprocess.run(
            ["espeak-ng", "-s", "140", text],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        _tts_queue.task_done()

_tts_thread = Thread(target=_tts_worker, daemon=True)
_tts_thread.start()

def speak(text: str):
    _tts_queue.put(text)


# Audio Recording & Transcription

def record_and_save(duration=RECORD_SECONDS, fname="mic.wav"):
    print(f"\n Recording for {duration} seconds...")
    subprocess.run(
        ["arecord", "-d", str(duration), "-f", "cd", fname],
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    print("Recording finished.")
    return fname

def transcribe_whisper(fname):
    print("Transcribing...")
    segments, _ = whisper_model.transcribe(fname, beam_size=5)
    text = " ".join([segment.text for segment in segments])
    return text.strip()


# User Interaction

def get_user_input():
    _tts_queue.join()
    sys.stdout.write("\nYou (type or 's'/wait→voice): ")   
    sys.stdout.flush()
    
    ready, _, _ = select.select([sys.stdin], [], [], 5)
    
    if ready:
        line = sys.stdin.readline().strip()
        if line.lower() in ("exit", "quit"):
            return None
        elif line.lower() == "s":
            speak("speak in voice now")
        else:
            return line
            
    speak("Voice Input:")
    wav = record_and_save()
    speak("Processing:")
    txt = transcribe_whisper(wav)
    print(f"You (voice): {txt}")
    speak("Robot speaking.")
    return txt

def main():
    if not os.path.isfile(MODEL_PATH):
        print(f"\nERROR: LLM model not found at {MODEL_PATH}")
        return

    print("\nSystems Ready — type 'exit' to quit.")
    speak("Systems Ready")
    print("\nType now if you want to override voice input.\n")
    
    while True:
        user_text = get_user_input()
        if user_text is None:
            break

        print("Large Language Model: ", end="", flush=True)
        buf = ""
        
        # Build the message array with the system prompt and the new user input
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
        
        ##############################################################################
        # Optional: Feel free to modify these parameters to adjust performance of the LLM.
        for chunk in llm.create_chat_completion(
            messages=messages, 
            max_tokens=128,
            temperature=0.7,
            top_p=0.95,
            stream=True,
        ):
        ##############################################################################
        
            # The chat API nests the text inside the 'delta' dictionary under 'content'
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                token = delta["content"]
                buf += token
                print(token, end="", flush=True)
                
                if token.endswith((" ", ".", "?", "!")):
                    if buf.strip():
                        speak(buf.strip())
                    buf = ""
                
        if buf.strip():
            speak(buf.strip())
        print()

    print("\nEnd of Demo")

if __name__ == "__main__":
    main()
