# CS7389K Advanced Robotics and Autonomous Systems

## Milestone 5: Talking to Your Robot (Voice and Language Models)

**Author:** MD Sameer Iqbal Chowdhury

## What is this assignment?

You will make a computer **listen** to your voice, **think** about what you said, and **talk** back. You do not need to write any code. You will run programs, change a few settings, and watch what happens.

| Tool | What it does |
| --- | --- |
| **Whisper** | Turns your voice into text |
| **LLaMa** | A language model. It reads text and writes an answer |
| **eSpeak** | Reads text out loud |

**How to use this page:** do the steps in order, one at a time. Each step tells you what to do, what you should see, and what you learn. Compare your screen with the "You should see" box. Small differences (numbers, timestamps, the exact words from the AI) are normal.

**What you hand in:** 3 short video clips, uploaded to YouTube (Unlisted), with the 3 links pasted into Canvas. The full checklist is in the last step.

Questions? Send a direct message to the Doctoral Instructor Assistant on Slack. Please do not email the instructor about the milestones.

---

## Step 1 (Optional): Watch a video about Docker

**Watch (optional):** <https://www.youtube.com/watch?v=Gjnup-PuquQ>

You already did this in Assignment 1, so skip it if you remember what Docker is.

**What you learn:** A Docker container is like a small, separate computer running inside your laptop. All the robot software lives inside it, so you will type most commands *inside* the container.

---

## Step 2: Start the container

**Do:** Open a normal terminal on the laptop and run these commands. (You did this in Assignment 1. If the container is already running, skip to the last command.)

```bash
xhost +local:root
cd ~/turtlebot_docker
HOST_UID=$(id -u) USER_HOME=$HOME docker compose up -d
docker exec -it remote_pc_humble bash
```

**You should see:** the last line changes your prompt to start with `root@`.

```text
root@your-laptop-name:~#
```

**What you learn:** The `root@` prompt means you are now *inside* the container. If you ever see your normal username instead, you are outside. Run the last command again. This is the same container you built in Assignment 1. It already has Whisper, LLaMa (`llama-cpp-python`) and eSpeak installed, so there is nothing to install for this assignment.

---

## Step 3: Download the assignment files

**Do:** Open a **new normal terminal** (not inside the container). Download the code and the two LLaMa model files. The programs are already in your container, but the model files are not in any of the earlier repos (they are about 4 GB each), so you must download them. Whisper needs no download now: it fetches its own model the first time you use it (Step 6).

```bash
cd ~/turtlebot_docker/my_code
git clone https://github.com/MSIChowdhury/Robotics_Assignment_5.git
cd Robotics_Assignment_5/Assignment_5_demo
wget -c https://huggingface.co/TheBloke/Llama-2-7B-32K-Instruct-GGUF/resolve/main/llama-2-7b-32k-instruct.Q4_K_M.gguf
wget -c https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
```

**You should see:** a progress bar for each download.

```text
Cloning into 'Robotics_Assignment_5'...
...
llama-2-7b-32k-instruct.Q4_K_M.gguf   100%[===================>]   3.8G  25.1MB/s    in 2m 30s
llama-2-7b-chat.Q4_K_M.gguf           100%[===================>]   3.8G  24.8MB/s    in 2m 32s
```

Check that both files are there:

```bash
ls
```

```text
llama-2-7b-32k-instruct.Q4_K_M.gguf   test_llama_text.py          test_llama_whisper_and_speach.py
llama-2-7b-chat.Q4_K_M.gguf           test_llama_text_system.py   test_whisper.py
```

**What you learn:** AI models are just big files. These two are about 4 GB each.

---

## Step 4: Open two monitor windows

**Do:** Open two new terminals, enter the container in each (`docker exec -it remote_pc_humble bash`), and run one command in each. Leave them open for the rest of the assignment.

```bash
top
```

```bash
nvidia-smi
```

**You should see:** `top` shows how busy the CPU and memory are. `nvidia-smi` shows the graphics card (GPU) memory.

```text
| NVIDIA-SMI 580.126.09     Driver Version: 580.126.09     CUDA Version: 13.0 |
| GPU  Name                 ...                  Memory-Usage | GPU-Util |
| N/A   42C    P8              3W /   60W |    4893MiB /   8151MiB |      0%  |
```

**What you learn:** The GPU has only 8 GB of memory. If the number next to `MiB /` gets close to 8151, the program may crash. Watch these windows whenever you load a model.

---

## Step 5: Read about Whisper

**Read:** <https://openai.com/index/whisper/>

**What you learn:** Whisper is a program trained on lots of recorded speech. It listens to audio and writes down the words.

---

## Step 6: Try Whisper and eSpeak together

**Do:** In the container, go to the demo folder and run the test. When it says "Speak now", say a short sentence for 5 seconds. The first run is slow because it downloads the Whisper model.

```bash
cd ~/my_code/Robotics_Assignment_5/Assignment_5_demo
python3 test_whisper.py
```

**You should see:**

```text
Initializing Whisper
Whisper Ready.

Recording for 5 seconds using arecord. Speak now!
Recording WAVE 'echo_audio.wav' : Signed 16 bit Little Endian, Rate 44100 Hz, Stereo
Recording finished.

Transcribing.

You said: Hello, this is a test.

Speaking: 'Hello, this is a test.'
```

You should also **hear** the computer repeat your sentence in a robot voice.

**What you learn:** Your voice was turned into text by Whisper, then read back by eSpeak. This is the "ears" and "mouth" of your robot.

---

## Step 7: Try a different Whisper size

**Do:** Open `test_whisper.py` and find this line:

```python
whisper_model = WhisperModel("base", device="cuda", compute_type="float16")
```

Change `"base"` to `"tiny"`, run it again and say the same sentence. Then try `"small"` and `"medium"`. Watch the `nvidia-smi` window each time.

**You should see:** the same kind of output as Step 6. The bigger the model, the longer it takes to load and the more GPU memory it uses.

| Model | Memory (about) | What to notice |
| --- | --- | --- |
| tiny | 0.15 GB | Fast, but may mishear words |
| base | 0.2 GB | |
| small | 0.6 GB | |
| medium | 1.5 GB | Slower, usually more accurate |

**What you learn:** Bigger AI models are usually better but slower and hungrier for memory. Picking a model is always a trade-off.

---

## Step 8: Read about language models

**Read:** <https://mark-riedl.medium.com/a-very-gentle-introduction-to-large-language-models-without-the-hype-5f67941fa59e>

**What you learn:** A Large Language Model (LLM) is a program that is very good at guessing the next word. That one skill lets it answer questions and follow instructions.

---

## Step 9: Chat with the "instruct" model

**Do:** Run the text chat demo. When it asks `You:`, type the question below and press Enter. The model takes a minute to load the first time. Type `exit` to quit.

```bash
python3 test_llama_text.py
```

Type this question:

```text
Can you explain the difference between forward and inverse kinematics for a robotic arm?
```

**You should see:** a lot of loading messages first, then your prompt, then the answer appearing word by word. Your answer will be different.

```text
Model loaded. Type 'exit' to quit.

You: Can you explain the difference between forward and inverse kinematics for a robotic arm?
Large Language Model: Forward kinematics finds the position of the robot's hand when you know
the angle of every joint. Inverse kinematics does the opposite: ...
```

Also look at `nvidia-smi`: the memory number jumped up by about 4 GB.

**What you learn:** The "instruct" model is trained to follow instructions: you give it a task and it does it.

---

## Step 10: Chat with the "chat" model

**Do:** Open `test_llama_text.py`. Near the top, there are two `MODEL_PATH` lines. Put a `#` in front of the first one and remove the `#` from the second one, so the chat model is used.

```python
#MODEL_PATH = os.path.expanduser("~/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-32k-instruct.Q4_K_M.gguf")
MODEL_PATH = os.path.expanduser("~/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-chat.Q4_K_M.gguf")
```

Run it again and ask the **same question** as Step 9.

```bash
python3 test_llama_text.py
```

**You should see:** the same kind of output as Step 9, but the wording and style of the answer are different.

**What you learn:** The "chat" model is trained for friendly back-and-forth conversation. Compare the two answers: which is longer, friendlier, or more to the point?

---

## Step 11: Give the model a "system prompt"

**Do:** A system prompt is a rule you give the AI before the question, like "you are a robotics teacher". Run this demo and ask the same question again.

```bash
python3 test_llama_text_system.py
```

**You should see:** an answer that follows the rule in the file. The default rule asks the model to remind you to change the system prompt, so it will say so at the end.

```text
Large Language Model: Forward kinematics ... Inverse kinematics ...
Please remember to change the system prompt after every prompt.
```

Now open the file, find `"content": "You are Large Language Model of a Robot...` and change the text to:

```text
You are a robotics teacher. Your goal is to teach students about robotics concepts. Do not output any conversational text or greetings.
```

Run it again and ask the same question.

**What you learn:** A system prompt changes how the AI behaves without changing the question. This is how we will make the AI act like a robot's brain.

---

## Step 12: Try three ways of asking

**Do:** Open `test_llama_text_system.py` and replace the system prompt text (as in Step 11) with the robot prompt below. Then run it and type each of the prompts (a), (b), (c) after it, one at a time. The robot system prompt:

```text
You are the reasoning engine for a mobile manipulator robot. Your goal is to break down user commands into a strict JSON array of physical actions. The only available actions you can choose from are: ["move_to_left", "move_to_right", "move_to_front", "move_to_back", "grab_object", "scan_environment", "release_object"]. Do not output any conversational text, greetings, or explanations. Only output the JSON array.
```

**(a) Zero-shot** means asking with no examples:

```text
Please grab the bottle on the right and drop it in front of me, who is behind you at the start.
```

**(b) Few-shot** means giving examples first:

```text
Command: 'Find the teddy bear on the left.'
Output: [{"action": "scan_environment", "target": "teddy bear"}, {"action": "move_to_left", "target": "teddy bear"}, {"action": "grab_object", "target": "teddy bear"}]

Command: 'Move the bottle from the front to the back.'
Output: [{"action": "move_to_front", "target": "bottle"}, {"action": "grab_object", "target": "bottle"}, {"action": "move_to_back", "target": "bottle"}, {"action": "release_object", "target": "bottle"}]

Command: 'Please grab the bottle on the right and drop it in front of me, who is behind you at the start.'
```

**(c) Chain-of-thought** means asking it to think step by step. Add this sentence to the end of (a):

```text
Think step by step, then output the final JSON array.
```

**You should see:** (a) may give a chatty or wrong answer. (b) should give a neat list like this:

```text
[{"action": "move_to_right", "target": "bottle"}, {"action": "grab_object", "target": "bottle"}, {"action": "move_to_back", "target": "bottle"}, {"action": "release_object", "target": "bottle"}]
```

**What you learn:** How you ask matters as much as what you ask. Examples (few-shot) usually make the answer neater. The demo remembers the whole conversation, so quit (`exit`) and restart it between prompts. If you see an error about the prompt being too long, do Step 13 first, then come back.

---

## Step 13: See how much the model can remember

**Do:** The model can only read a limited number of words at once. This limit is called the **context window**. Open `test_llama_text_system.py` and find:

```python
n_ctx=512,
```

The value `512` is a tested, safe setting. Raise it one step at a time (`1024`, then `1536`, then `2048`), run the few-shot prompt from Step 12 each time, and watch `nvidia-smi`.

**You should see:** the memory number in `nvidia-smi` goes up a little each time. If the program crashes or says "out of memory", the number is too big. Go back to the last value that worked and write it down.

```text
ValueError: Requested tokens (631) exceed context window of 512
```

**What you learn:** A bigger memory lets the AI read longer prompts, but it costs GPU memory. Too big, and it crashes.

---

## Step 14: 🎥 Record Clip 1: testing the language models

**Do:** Film this with a phone or camera aimed at the computer screen, while one team member narrates. **At the very start, show the face of every team member and say everyone's name.** Then repeat your favourite test from Steps 9 to 12 on screen, and **say out loud** the answers to these four questions:

1. What is the difference between the "chat" and "instruct" models?
2. What changed when you used a system prompt and when you didn't?
3. Which way of asking (zero-shot, few-shot, chain-of-thought) worked best for you? Give one example.
4. Which model followed strict rules better (for example, "only output a JSON list")? Give one example.

**What you learn:** Explaining your results out loud shows you understood them. Short answers are fine.

---

## Step 15: Have a voice chat, no ROS yet

**Do:** Run the voice chat demo. Wait for the text prompt, then either type or just wait 5 seconds and speak.

```bash
python3 test_llama_whisper_and_speach.py
```

**You should see:**

```text
Systems Ready — type 'exit' to quit.

Type now if you want to override voice input.

You (type or 's'/wait→voice):
 Recording for 5 seconds...
Recording finished.
Transcribing...
You (voice): Hello, what can you tell me about robotics?
Large Language Model: Robotics is the study of machines that ...
```

You will also **hear** the answer spoken aloud.

**What you learn:** You just built a talking assistant by joining the three tools. The next steps do the same thing the way a real robot does it, with separate programs talking to each other.

---

## Step 16: Start the server

**Do:** Close everything else (type `exit` or press `Ctrl+C` in the demo windows) so there is enough memory. Then, in the container, start the **server**. It loads all three tools and waits for requests.

```bash
cd ~/my_code/Robotics_Assignment_5/
python3 sample_code_servers.py
```

**You should see:** after a minute or two, the last line says the server is ready.

```text
[INFO] [1780000000.123456789] [nlp_topic_server]: Loading Faster-Whisper (small) onto GPU...
[INFO] [1780000004.223456789] [nlp_topic_server]: Whisper Loaded.
[INFO] [1780000004.323456789] [nlp_topic_server]: Loading LLM from /root/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-32k-instruct.Q4_K_M.gguf...
[INFO] [1780000012.423456789] [nlp_topic_server]: Large Language Model Loaded.
[INFO] [1780000012.523456789] [nlp_topic_server]: Natural Language Processing Server is up. Listening to request topic.
```

**What you learn:** The server is a program that sits and waits. It does the heavy AI work whenever another program asks.

---

## Step 17: Start the client

**Do:** Open a **new terminal**, enter the container, and start the **client**. The client is the remote control for the server.

```bash
docker exec -it remote_pc_humble bash
cd ~/my_code/Robotics_Assignment_5/
python3 sample_code_clients.py
```

**You should see:**

```text
========================================
Natural Language Processing Client Test Menu
1. Test Text-to-Speech (eSpeak)
2. Test Speech-to-Text (Whisper)
3. Test LLM Generation (Llama-2)
4. Test Full Integration Pipeline for 1. to 3.
5. Exit
========================================
Select an option (1-5):
```

**What you learn:** The client and the server are two separate programs. They talk to each other using ROS 2 messages, the same way parts of a real robot do.

---

## Step 18: Try menu options 1, 2 and 3

**Do:** Type each number, one at a time.

**Option 1:** type `1`, then a sentence.

```text
Select an option (1-5): 1
Enter text to speak: Hello, I am your robot.
Text to Speech request sent to Remote-PC. Listen for the audio.
```

**Option 2:** type `2`, then `5`, then speak.

```text
Select an option (1-5): 2
Enter recording duration (seconds): 5
Server on Remote-PC is recording for 5 seconds. Speak now.

Speech To Text Result : Hello, what can you tell me about robotics?
```

**Option 3:** type `3`, then a question.

```text
Select an option (1-5): 3
Enter your prompt for the Large Language Model: What is a robot?
Large Language Model: A robot is a machine that can ...
```

**You should see:** the matching lines in the server window.

```text
[INFO] [nlp_topic_server]: TTS Requested: 'Hello, I am your robot.'
[INFO] [nlp_topic_server]: Text To Speech Complete.
[INFO] [nlp_topic_server]: Speech To Text Requested: Recording for 5 seconds...
[INFO] [nlp_topic_server]: Speech to Text Result Published: Hello, what can you tell me about robotics?
[INFO] [nlp_topic_server]: Large Language Model Response Requested with prompt: 'What is a robot?'
[INFO] [nlp_topic_server]: Large Language Model Generation Complete.
```

**What you learn:** Each option asks the server to do one job: speak, listen, or think.

---

## Step 19: Try option 4, the full conversation

**Do:** Type `4`, then `5`, then say a sentence. Do not touch the keyboard after that.

```text
Select an option (1-5): 4
Enter recording duration (seconds) [e.g. 5]: 5
Server on Remote-PC is recording for 5 seconds. Speak now.

Speech To Text Result : Hello, what can you tell me about robotics?
Large Language Model: Robotics is the study of machines that can sense, think, and act ...

Reply sent to eSpeak. Listen for the audio.
```

**You should see:** your voice turned into text, the AI's answer appearing on the screen, and the answer being read to you.

**What you learn:** This is the whole pipeline: **ears (Whisper) → brain (LLaMa) → mouth (eSpeak)**. You can now talk to a computer.

---

## Step 20: Change the server's settings

**Do:** Stop the server (`Ctrl+C` in its window). Open `sample_code_servers.py` and look at the block at the top that starts with `# Settings you can tune`. Change **one** value, start the server again, and try option 4 again.

| Setting | Try this | What to notice |
| --- | --- | --- |
| `MODEL_PATH` | Switch between instruct and chat | The style of the answer |
| `WHISPER_MODEL` | `"tiny"` or `"medium"` | Speed and accuracy of listening |
| `SYSTEM_PROMPT` | The robot teacher rule from Step 11 | The tone of the answer |
| `TEMPERATURE` | `0.1`, then `1.0` | Low is steady and repeatable. High is more random |
| `MAX_TOKENS` | `32`, then `256` | How long (or cut off) the answer is |
| `N_CTX` | Raise in steps of 512 | Longer prompts fit, but memory use goes up |

**You should see:** the same menu and output as Step 19, with small differences caused by your change.

**What you learn:** You can change how an AI behaves just by changing a few numbers and sentences.

---

## Step 21: 🎥 Record Clip 2: show us the code

**Do:** Start filming (phone or camera aimed at the screen). Open `sample_code_servers.py` and `sample_code_clients.py` on screen. Point at the code and say, in your own words, in about one minute:

1. **Server:** Which Whisper model and which LLaMa model did you choose, and why? Which settings did you change?
2. **Client:** How does the client ask the server to speak, listen and think?
3. **Option 4:** How does it join the three steps in order?

**What you learn:** You do not need to understand every line. The goal is to see the big picture: *request in, work done, answer out*.

---

## Step 22: 🎥 Record Clip 3: live demo

**Do:** Start filming (phone or camera aimed at the screen and the speaker, so the sound is clear). Start the server and the client. With the screen showing both windows, run:

1. Option 1: it speaks a sentence you type.
2. Option 2: say a clear sentence, for example "Hello, what can you tell me about robotics?", and show the text.
3. Option 3: type a question and show the LLM's reply.
4. Option 4: do the full voice conversation, with **no keyboard use** after choosing the option. Show that your voice became text, the LLM answered, and the answer was spoken.

**What you learn:** You can now show a working natural-language pipeline end to end.

---

## Step 23: Submit

You must submit **3 video clips**. Tick every box before you submit.

- [ ] **Clip 1: Testing the language models.** Shows every team member's face and name at the start. Shows your tests with the chat and instruct models, the system prompt, and zero-shot, few-shot and chain-of-thought prompts. The narrator answers the four questions from Step 14.
- [ ] **Clip 2: Code walkthrough.** Shows `sample_code_servers.py` and `sample_code_clients.py`. The narrator explains the models and settings chosen, how the client talks to the server, and how option 4 joins the three steps.
- [ ] **Clip 3: Live demo.** Shows the server and client running. Options 1, 2 and 3 each work once, then option 4 runs the full voice conversation with no keyboard use after choosing it.

For every clip: film the screen with a phone or camera while one team member narrates. You do not need to edit, and a few minutes in total is enough.

**How to hand in**

1. Upload each clip to YouTube and set it to **Unlisted**. Do not upload the raw video files to Canvas.
2. **Every team member** pastes all 3 links into Canvas under **Assignment 5**, even if the team recorded the clips together.

Source code is **not** required for this assignment.

---

## Optional: want to learn more?

- How LLMs can plan robot actions (ReAct): <https://www.promptingguide.ai/techniques/react>
- Prompting techniques guide: <https://www.promptingguide.ai/techniques>
