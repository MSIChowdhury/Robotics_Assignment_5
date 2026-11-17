# CS7389K Advanced Robotics and Autonomous Systems

## Assignment 5: Talking to Your Robot with Voice and Language Models

**Author:** MD Sameer Iqbal Chowdhury

## Introduction

This assignment shows how a robot could understand spoken instructions. You will build a system that listens to your voice and turns it into text, uses a large language model to write an answer, and then speaks the answer out loud. Three programs work together to do this.

| Tool | What it does |
| --- | --- |
| **Whisper** | It listens to your voice and turns it into written text (speech-to-text). |
| **LLaMa** | It is a large language model. It reads the text and writes an answer. |
| **eSpeak** | It reads the answer out loud (text-to-speech). |

You are not required to write any code. You will run the provided programs, change a small number of settings and prompts, and observe how the results change.

**How to use this guide.** Please complete the steps in the order given. Each step begins with what you will learn. After each command, we show an example of the output that you should see, so that you can check your own results. Small differences, such as numbers, timestamps, and the exact words of the language model's answers, are normal.

**Reading the code.** You are encouraged to read the code of each program to understand how it works. You are not required to change any code, except for the changes that this guide asks you to make.

**Getting help.** The Doctoral Instructor Assistant can be contacted only by email at vsj23@txstate.edu. Please do not contact the instructor with questions about the assignments.

---

## Submission Requirements (Please Read Before You Begin)

You will submit **three video clips**. Every step that requires a recording is marked with "Recording required" at the very beginning of the step, so you will always know when to record.

**Rules for all clips**

1. Each clip must be **one continuous recording with no editing**. Please do not cut, trim, speed up, or join any parts. If something goes wrong during a clip, please record the whole clip again from the beginning.
2. Please film the clips with a phone or a camera. The film must show the computer screen, and the narrator's voice must be clear, while one team member narrates what is happening.
3. At the beginning of Clip 1, please show the face of every team member and say each member's name.
4. Please name every clip with the convention `Assignment5_Group<number>_Clip<number>`. For example, the second clip of Group 2 is named `Assignment5_Group2_Clip2`.
5. Please upload each clip to YouTube and set its visibility to **Unlisted**. Please use the clip name as the video title. Please do not upload the raw video files to Canvas.
6. **Every team member** must paste all three links into Canvas under **Assignment 5**, even if the team recorded the clips together.
7. Source code is **not** required for this assignment.

**The three clips**

| Clip | File name (Group 2 as an example) | What the clip must show |
| --- | --- | --- |
| 1 | `Assignment5_Group2_Clip1` | The faces and names of all team members, your tests of the chat and instruct models, the system prompt, and the zero-shot, few-shot, and chain-of-thought prompts, together with spoken answers to four questions. |
| 2 | `Assignment5_Group2_Clip2` | A walkthrough of the server code and the client code, in which the narrator explains the chosen models, the settings, and how the three tools are joined. |
| 3 | `Assignment5_Group2_Clip3` | A live demonstration of menu options 1, 2, 3, and 4, ending with a full voice conversation without any use of the keyboard. |

---

## Step 1: Watch a Video About Docker

**What you will learn:** This step is a short reminder of what a Docker container is, which you studied in Assignment 1. The step is optional, and you may skip it if you already understand Docker.

Please watch the following video if you would like a short reminder: <https://www.youtube.com/watch?v=Gjnup-PuquQ>

A Docker container is a self-contained environment that holds a program together with all of the software that it depends on. Because everything is packaged together, the program runs in the same way on every computer. All of the software for this assignment is already installed inside such a container, so most commands are entered inside it.

---

## Step 2: Open the Docker Container

**What you will learn:** You will learn how to start the Docker container that holds all of the software for this assignment. This is the same container that you built in Assignment 1. It already contains Whisper, LLaMa, and eSpeak, so you do not need to install anything.

Please perform this step on the **Remote PC**, which is your laptop. Please open an ordinary terminal (not one inside Docker) and run the three commands below, one after the other.

The first command allows the container to open windows on your laptop's screen. Please copy and paste the following command and run it:

```bash
xhost +local:root
```

The second command starts the container in the background. It gives Docker your user ID and your home folder, which the container needs in order to use your microphone and speakers. If the container is already running, running this command again does no harm. Please copy and paste the following command and run it:

```bash
cd ~/turtlebot_docker && HOST_UID=$(id -u) USER_HOME=$HOME docker compose up -d
```

The third command opens a terminal inside the container. You will type most of the remaining commands in this guide there. Please copy and paste the following command and run it:

```bash
docker exec -it remote_pc_humble bash
```

Then you will see something like this. The `root@` at the beginning of the line shows that you are now inside the container:

```text
root@your-laptop-name:~#
```

If you ever see your normal username at the beginning of the line instead, you are outside the container, and you should run the third command again.

---

## Step 3: Download the Assignment Files and the Language Models

**What you will learn:** You will learn that a trained AI model is stored as a large file. The two LLaMa models used in this assignment are about 4 GB each. Whisper does not need to be downloaded now, because it downloads its own model automatically the first time that you use it in Step 6.

Please perform this step on the **Remote PC**. Please open a **new ordinary terminal** (not inside Docker). The software is already installed in your container, but the two LLaMa model files are not part of any earlier assignment, so you must download them. This takes several minutes.

The following two lines go to the folder that your laptop shares with the Docker container and download the assignment repository from GitHub. Please copy and paste them and run them:

```bash
cd ~/turtlebot_docker/my_code
git clone https://github.com/MSIChowdhury/Robotics_Assignment_5.git
```

Then you will see something like this:

```text
Cloning into 'Robotics_Assignment_5'...
remote: Enumerating objects: 30, done.
Receiving objects: 100% (30/30), done.
```

The following command goes to the folder where the models must be stored. Please copy and paste it and run it:

```bash
cd Robotics_Assignment_5/Assignment_5_demo
```

The following two commands download the two LLaMa models, which are stored in a file format called GGUF, from the Hugging Face website. The option `-c` lets an interrupted download continue where it stopped. No account or access token is needed. Please copy and paste each command and run it:

```bash
wget -c https://huggingface.co/TheBloke/Llama-2-7B-32K-Instruct-GGUF/resolve/main/llama-2-7b-32k-instruct.Q4_K_M.gguf
```

```bash
wget -c https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
```

Then you will see a progress bar for each download, something like this:

```text
llama-2-7b-32k-instruct.Q4_K_M.gguf   100%[===================>]   3.8G  25.1MB/s    in 2m 30s
llama-2-7b-chat.Q4_K_M.gguf           100%[===================>]   3.8G  24.8MB/s    in 2m 32s
```

Finally, the following command lists the files in the folder so that you can check that both models are present. Please copy and paste it and run it:

```bash
ls
```

Then you will see something like this:

```text
llama-2-7b-32k-instruct.Q4_K_M.gguf   test_llama_text.py          test_llama_whisper_and_speach.py
llama-2-7b-chat.Q4_K_M.gguf           test_llama_text_system.py   test_whisper.py
```

---

## Step 4: Open Two Monitoring Windows

**What you will learn:** You will learn how to see how much memory a model is using. The graphics chip (GPU) of your laptop has only 8 GB of its own memory (called VRAM). A program that needs more than that will crash, so you should watch these windows whenever a model is loading.

Please perform this step on the **Remote PC**. Please open two new terminals. In each one, please enter the container by copying and pasting the following command and running it. This is the same command as in Step 2:

```bash
docker exec -it remote_pc_humble bash
```

In the first container terminal, please run the following command. It shows how busy the processor is and how much of the computer's main memory (RAM) is in use. Please leave it running:

```bash
top
```

In the second container terminal, please run the following command. It shows how busy the GPU is and how much of its memory is in use. Please leave it running:

```bash
nvidia-smi
```

Then you will see something like this from `nvidia-smi`. The number before `/` in the `Memory-Usage` column is the GPU memory that is in use, and the number after it is the total:

```text
| NVIDIA-SMI 580.126.09     Driver Version: 580.126.09     CUDA Version: 13.0 |
| GPU  Name                 ...                  Memory-Usage | GPU-Util |
| N/A   42C    P8              3W /   60W |    4893MiB /   8151MiB |      0%  |
```

If the first number gets close to the total, the program may crash. Please keep both windows open for the rest of the assignment.

---

## Step 5: Read About Whisper

**What you will learn:** You will learn what Whisper is. Whisper is a speech recognition program that was trained on a very large collection of recorded speech, so it can listen to audio and write down the words that were spoken.

Please read the following page: <https://openai.com/index/whisper/>

---

## Step 6: Try Whisper and eSpeak Together

**What you will learn:** You will see the listening part and the speaking part of the system working together. Whisper turns your voice into text, and eSpeak reads the text back to you.

Please perform this step inside the **Docker container on the Remote PC**. The following two lines go to the demonstration folder and start the test program. The program records 5 seconds of audio from your microphone, so please say one short sentence as soon as it says "Speak now". The first run is slow, because Whisper downloads its model. Please copy and paste them and run them:

```bash
cd ~/my_code/Robotics_Assignment_5/Assignment_5_demo
python3 test_whisper.py
```

Then you will see something like this:

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

You should also hear the computer repeat your sentence in a robot voice. You are encouraged to open `test_whisper.py` and read it to see how it works. You are not required to change it in this step.

---

## Step 7: Try a Different Whisper Size

**What you will learn:** You will learn that bigger models are usually more accurate but slower and use more memory, so choosing a model is always a trade-off. This step is optional, and you may skip it if you are short on time.

Please perform this step inside the **Docker container on the Remote PC**. Whisper comes in several sizes. The following table shows the approximate GPU memory that each size needs. Your laptop has 8 GB, so all of these sizes fit, but you should still watch `nvidia-smi`.

| Model | Approximate GPU memory | Description |
| --- | --- | --- |
| `tiny` | 0.15 GB | This is the fastest model, but it makes more mistakes. |
| `base` | 0.2 GB | This is the default size in the test program. |
| `small` | 0.6 GB | This model is a good balance between speed and accuracy. |
| `medium` | 1.5 GB | This model is slower, but it is usually more accurate. |

The following command opens the test program in `nano`, a text editor that works inside the terminal. After you make your change, please press `Ctrl+O` and then `Enter` to save, and then `Ctrl+X` to leave the editor. Please copy and paste it and run it:

```bash
nano test_whisper.py
```

Please find the following line, change `"base"` to `"tiny"`, and save the file:

```python
whisper_model = WhisperModel("base", device="cuda", compute_type="float16")
```

Please run the program again with the following command and say the same sentence as before. Then please repeat the process with `"small"` and `"medium"`, and please watch the `nvidia-smi` window each time:

```bash
python3 test_whisper.py
```

Then you will see the same kind of output as in Step 6. The bigger the model is, the longer it takes to load and the more GPU memory it uses.

---

## Step 8: Read About Large Language Models

**What you will learn:** You will learn the basic idea of a large language model (LLM). An LLM is a program that has learned to predict the next word in a text, again and again. This one skill allows it to answer questions and follow instructions.

Please read the following article: <https://mark-riedl.medium.com/a-very-gentle-introduction-to-large-language-models-without-the-hype-5f67941fa59e>

---

## Step 9: Chat with the Instruct Model

**What you will learn:** You will learn that the "instruct" model is trained to follow instructions: you give it a task, and it tries to carry out the task.

Please perform this step inside the **Docker container on the Remote PC**. The following command starts a text conversation with the instruct model. The model takes about a minute to load the first time. Please copy and paste the command and run it:

```bash
python3 test_llama_text.py
```

When the program asks for your input with `You:`, please copy and paste the following question and press `Enter`. You can type `exit` to quit the program when you are finished.

```text
Can you explain the difference between forward and inverse kinematics for a robotic arm?
```

Then you will see something like this. The program prints many loading messages first, and then your question, and then the answer appearing one word at a time. Your answer will be different from this one.

```text
Model loaded. Type 'exit' to quit.

You: Can you explain the difference between forward and inverse kinematics for a robotic arm?
Large Language Model: Forward kinematics finds the position of the robot's hand when you know
the angle of every joint. Inverse kinematics does the opposite: ...
```

Please also look at the `nvidia-smi` window. The GPU memory in use should have increased by about 4 GB, because the model is now loaded into GPU memory.

---

## Step 10: Chat with the Chat Model

**What you will learn:** You will learn that the "chat" model is trained for friendly, back-and-forth conversation. Please compare its answer with the answer of the instruct model. Which one is longer, friendlier, or more to the point?

Please perform this step inside the **Docker container on the Remote PC**. Please open `test_llama_text.py` in the `nano` editor, using the same saving method as in Step 7. Please copy and paste the following command and run it:

```bash
nano test_llama_text.py
```

Near the top of the file, there are two `MODEL_PATH` lines. Please put a `#` at the beginning of the first line and remove the `#` from the beginning of the second line, so that the chat model is used. The result should look like this:

```python
#MODEL_PATH = os.path.expanduser("~/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-32k-instruct.Q4_K_M.gguf")
MODEL_PATH = os.path.expanduser("~/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-chat.Q4_K_M.gguf")
```

Please run the program again with the following command and ask the same question as in Step 9:

```bash
python3 test_llama_text.py
```

Then you will see the same kind of output as in Step 9, but the wording and the style of the answer will be different.

---

## Step 11: Give the Model a System Prompt

**What you will learn:** You will learn what a system prompt is. A system prompt is an instruction that you give to the model before your question, for example "You are a robotics teacher". It changes how the model answers without changing your question. Later, you will use this idea to make the model act as the brain of a robot.

Please perform this step inside the **Docker container on the Remote PC**. The following command starts a conversation in which a system prompt is used. Please copy and paste it and run it, and then ask the same question as in Step 9:

```bash
python3 test_llama_text_system.py
```

Then you will see something like this. The system prompt in the file asks the model to remind you to change the system prompt, so the answer ends with a reminder:

```text
Large Language Model: Forward kinematics ... Inverse kinematics ...
Please remember to change the system prompt after every prompt.
```

Next, please open the file in the `nano` editor with the following command:

```bash
nano test_llama_text_system.py
```

Please find the line that contains `"content": "You are Large Language Model of a Robot...` and replace the text inside the quotation marks with the following text. Then please save the file, run the program again, and ask the same question:

```text
You are a robotics teacher. Your goal is to teach students about robotics concepts. Do not output any conversational text or greetings.
```

You will notice that the style of the answer changes.

---

## Step 12: Compare Three Ways of Asking

**What you will learn:** You will learn that the way you word a question matters as much as the question itself. You will compare three ways of asking: zero-shot (no examples), few-shot (a few examples), and chain-of-thought (asking the model to reason step by step). Few-shot prompts usually give neater and more consistent answers.

Please perform this step inside the **Docker container on the Remote PC**. Please open `test_llama_text_system.py` with the same `nano` command as in Step 11, and replace the system prompt text (as in Step 11) with the following robot prompt. This prompt tells the model to behave as the reasoning engine of a robot and to answer only with a list of allowed actions:

```text
You are the reasoning engine for a mobile manipulator robot. Your goal is to break down user commands into a strict JSON array of physical actions. The only available actions you can choose from are: ["move_to_left", "move_to_right", "move_to_front", "move_to_back", "grab_object", "scan_environment", "release_object"]. Do not output any conversational text, greetings, or explanations. Only output the JSON array.
```

Please start the program with the following command:

```bash
python3 test_llama_text_system.py
```

The program remembers the entire conversation, so please type `exit` and start the program again between the three prompts below. Please copy and paste each prompt, one at a time.

**(a) Zero-shot prompt.** This prompt gives the model no examples:

```text
Please grab the bottle on the right and drop it in front of me, who is behind you at the start.
```

**(b) Few-shot prompt.** This prompt shows the model two examples before it asks the real question:

```text
Command: 'Find the teddy bear on the left.'
Output: [{"action": "scan_environment", "target": "teddy bear"}, {"action": "move_to_left", "target": "teddy bear"}, {"action": "grab_object", "target": "teddy bear"}]

Command: 'Move the bottle from the front to the back.'
Output: [{"action": "move_to_front", "target": "bottle"}, {"action": "grab_object", "target": "bottle"}, {"action": "move_to_back", "target": "bottle"}, {"action": "release_object", "target": "bottle"}]

Command: 'Please grab the bottle on the right and drop it in front of me, who is behind you at the start.'
```

**(c) Chain-of-thought prompt.** This prompt is the zero-shot prompt followed by an extra sentence that asks the model to reason step by step:

```text
Please grab the bottle on the right and drop it in front of me, who is behind you at the start. Think step by step, then output the final JSON array.
```

Then you will see something like this. The zero-shot answer may be chatty or wrong, while the few-shot answer should be a neat list like this one:

```text
[{"action": "move_to_right", "target": "bottle"}, {"action": "grab_object", "target": "bottle"}, {"action": "move_to_back", "target": "bottle"}, {"action": "release_object", "target": "bottle"}]
```

If you see an error that says that the prompt is too long, please complete Step 13 first and then return to this step.

---

## Step 13: See How Much the Model Can Remember

**What you will learn:** You will learn that a model can only read a limited amount of text at one time. This limit is called the **context window**, and it is measured in tokens, which are small pieces of words. A larger context window lets the model read longer prompts, but it uses more GPU memory, and if it is too large the program crashes.

Please perform this step inside the **Docker container on the Remote PC**. Please open `test_llama_text_system.py` with the following command:

```bash
nano test_llama_text_system.py
```

Please find the following line:

```python
n_ctx=512,
```

The value 512 is a tested and safe setting. Please raise it one step at a time to 1024, then 1536, then 2048. After each change, please save the file, run the program again, paste the few-shot prompt from Step 12, and watch the `nvidia-smi` window. The following command starts the program each time:

```bash
python3 test_llama_text_system.py
```

Then you will see that the GPU memory in use in `nvidia-smi` increases a little each time. If the program crashes or reports that memory has run out, the value is too large. In that case, please go back to the last value that worked and write it down. With the original value of 512, a prompt that is too long produces an error like this:

```text
ValueError: Requested tokens (631) exceed context window of 512
```

---

## Step 14: Record Clip 1 (Testing the Language Models)

**Recording required:** Please record this step as one continuous video without editing. Please name the clip `Assignment5_Group<number>_Clip1`, for example `Assignment5_Group2_Clip1`.

**What you will learn:** You will practice explaining your results aloud, which shows that you understood them. Short answers are fine.

Please film the computer screen with a phone or a camera, while one team member narrates. **At the very beginning of the clip, please show the face of every team member and say each member's name.** Then please repeat your favorite tests from Steps 9 to 12 on the screen. You may start the programs again with the following commands, as needed:

```bash
cd ~/my_code/Robotics_Assignment_5/Assignment_5_demo
python3 test_llama_text.py
```

```bash
python3 test_llama_text_system.py
```

While you demonstrate the tests, please answer the following four questions aloud:

1. What is the difference between the chat model and the instruct model?
2. What changed when you used a system prompt compared with when you did not?
3. Which way of asking (zero-shot, few-shot, or chain-of-thought) worked best for you? Please give one example.
4. Which model followed strict rules better, for example "only output a JSON list"? Please give one example.

---

## Step 15: Have a Voice Conversation Without ROS

**What you will learn:** You will learn how the three tools are joined into one talking assistant in a single program. In the next steps, you will build the same assistant in the way that a real robot works, with separate programs that send messages to each other.

Please perform this step inside the **Docker container on the Remote PC**. The following two lines go to the demonstration folder and start a voice conversation with the model. Please copy and paste them and run them. When the program shows its prompt, please either type a question or wait 5 seconds, after which it records your voice for 5 seconds:

```bash
cd ~/my_code/Robotics_Assignment_5/Assignment_5_demo
python3 test_llama_whisper_and_speach.py
```

Then you will see something like this, and you will also hear the answer spoken aloud:

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

---

## Step 16: Start the Server

**What you will learn:** You will learn what a server is. A server is a program that waits for requests and does the heavy work whenever another program asks it to. This server loads Whisper and LLaMa into GPU memory, prepares eSpeak, and then waits for requests.

Please perform this step inside the **Docker container on the Remote PC**. Please close all other programs first by typing `exit` or pressing `Ctrl+C` in their windows, so that there is enough memory. The following two lines go to the assignment folder and start the server. Please copy and paste them and run them:

```bash
cd ~/my_code/Robotics_Assignment_5/
python3 sample_code_servers.py
```

Then you will see something like this after a minute or two. The last line shows that the server is ready:

```text
[INFO] [1780000000.123456789] [nlp_topic_server]: Loading Faster-Whisper (small) onto GPU...
[INFO] [1780000004.223456789] [nlp_topic_server]: Whisper Loaded.
[INFO] [1780000004.323456789] [nlp_topic_server]: Loading LLM from /root/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-32k-instruct.Q4_K_M.gguf...
[INFO] [1780000012.423456789] [nlp_topic_server]: Large Language Model Loaded.
[INFO] [1780000012.523456789] [nlp_topic_server]: Natural Language Processing Server is up. Listening to request topic.
```

You are encouraged to open `sample_code_servers.py` and read it. You are not required to change it yet.

---

## Step 17: Start the Client

**What you will learn:** You will learn that the client and the server are two separate programs that talk to each other using ROS 2 messages, in the same way as the parts of a real robot. The client works like a remote control for the server.

Please perform this step on the **Remote PC**. Please open a **new ordinary terminal** and keep the server running. The first command opens a terminal inside the container. Please copy and paste it and run it:

```bash
docker exec -it remote_pc_humble bash
```

The following two lines then go to the assignment folder and start the client. Please copy and paste them and run them:

```bash
cd ~/my_code/Robotics_Assignment_5/
python3 sample_code_clients.py
```

Then you will see a menu like this:

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

You are encouraged to open `sample_code_clients.py` and read it. You are not required to change it.

---

## Step 18: Try Menu Options 1, 2, and 3

**What you will learn:** You will learn that each menu option asks the server to do one job: to speak, to listen, or to write an answer.

Please perform this step in the client terminal. Please try the three options one at a time.

For **option 1**, please type `1` and press `Enter`. Then please copy and paste the following sentence when the program asks for text:

```text
Hello, I am your robot.
```

Then you will see something like this, and you will hear the sentence spoken:

```text
Select an option (1-5): 1
Enter text to speak: Hello, I am your robot.
Text to Speech request sent to Remote-PC. Listen for the audio.
```

For **option 2**, please type `2` and press `Enter`, then type `5` for the recording duration, and then please speak a sentence. Then you will see something like this:

```text
Select an option (1-5): 2
Enter recording duration (seconds): 5
Server on Remote-PC is recording for 5 seconds. Speak now.

Speech To Text Result : Hello, what can you tell me about robotics?
```

For **option 3**, please type `3` and press `Enter`. Then please copy and paste the following question when the program asks for a prompt:

```text
What is a robot?
```

Then you will see something like this:

```text
Select an option (1-5): 3
Enter your prompt for the Large Language Model: What is a robot?
Large Language Model: A robot is a machine that can ...
```

At the same time, you will see the matching lines in the server window, something like this:

```text
[INFO] [nlp_topic_server]: TTS Requested: 'Hello, I am your robot.'
[INFO] [nlp_topic_server]: Text To Speech Complete.
[INFO] [nlp_topic_server]: Speech To Text Requested: Recording for 5 seconds...
[INFO] [nlp_topic_server]: Speech to Text Result Published: Hello, what can you tell me about robotics?
[INFO] [nlp_topic_server]: Large Language Model Response Requested with prompt: 'What is a robot?'
[INFO] [nlp_topic_server]: Large Language Model Generation Complete.
```

---

## Step 19: Try Option 4, the Full Conversation

**What you will learn:** You will see the whole pipeline working together: your voice is transcribed by Whisper, understood and answered by LLaMa, and spoken by eSpeak. At this point, you have a working system that you can talk to.

Please perform this step in the client terminal. Please type `4` and press `Enter`, then type `5` for the recording duration, and then please say one sentence. Please do not touch the keyboard after that.

Then you will see something like this. Your voice becomes text, the answer of the language model appears on the screen, and the answer is read to you out loud:

```text
Select an option (1-5): 4
Enter recording duration (seconds) [e.g. 5]: 5
Server on Remote-PC is recording for 5 seconds. Speak now.

Speech To Text Result : Hello, what can you tell me about robotics?
Large Language Model: Robotics is the study of machines that can sense, think, and act ...

Reply sent to eSpeak. Listen for the audio.
```

---

## Step 20: Change the Server's Settings

**What you will learn:** You will learn that you can change how an AI system behaves just by changing a few numbers and sentences.

Please perform this step inside the **Docker container on the Remote PC**. First, please stop the server by pressing `Ctrl+C` in its terminal. Then please open the server file in the `nano` editor, using the same saving method as in Step 7. Please copy and paste the following command and run it:

```bash
nano ~/my_code/Robotics_Assignment_5/sample_code_servers.py
```

Near the top of the file, there is a block that starts with `# Settings you can tune`. Please change **one** value, save the file, start the server again with the command from Step 16, and try option 4 again in the client. The following table explains each setting and what you should try.

| Setting | What to try | What you should notice |
| --- | --- | --- |
| `MODEL_PATH` | Please switch between the instruct model and the chat model. | The style of the answer changes. |
| `WHISPER_MODEL` | Please try `"tiny"` or `"medium"`. | The speed and the accuracy of the listening change. |
| `SYSTEM_PROMPT` | Please use the robot teacher prompt from Step 11. | The tone of the answer changes. |
| `TEMPERATURE` | Please try `0.1` and then `1.0`. | A low value gives steady and repeatable answers, and a high value gives more varied answers. |
| `MAX_TOKENS` | Please try `32` and then `256`. | The length of the answer changes, and short values may cut the answer off. |
| `N_CTX` | Please raise it in steps of 512. | Longer prompts fit, but the memory use rises. |

Then you will see the same menu and the same kind of output as in Step 19, with small differences that are caused by your change.

---

## Step 21: Record Clip 2 (Code Walkthrough)

**Recording required:** Please record this step as one continuous video without editing. Please name the clip `Assignment5_Group<number>_Clip2`, for example `Assignment5_Group2_Clip2`.

**What you will learn:** You are not required to understand every line of the code. The goal is to understand the big picture: a request comes in, the work is done, and an answer is sent back.

Please film the computer screen with a phone or a camera, while one team member narrates. Please open the two code files on the screen with the following command, which opens the server file. You can open the client file in the same way by replacing `servers` with `clients`:

```bash
nano ~/my_code/Robotics_Assignment_5/sample_code_servers.py
```

Please point at the code and explain the following three topics in your own words, in about one minute:

1. **The server:** Which Whisper model and which LLaMa model did you choose, and why? Which settings did you change?
2. **The client:** How does the client ask the server to speak, to listen, and to think?
3. **Option 4:** How does option 4 join the three steps in the correct order?

---

## Step 22: Record Clip 3 (Live Demonstration)

**Recording required:** Please record this step as one continuous video without editing. Please name the clip `Assignment5_Group<number>_Clip3`, for example `Assignment5_Group2_Clip3`.

**What you will learn:** You will show a working system from beginning to end.

Please film the computer screen and the speaker with a phone or a camera, so that the sound is clear, while one team member narrates. Please start the server and the client with the commands from Step 16 and Step 17, and show both windows on the screen. For convenience, the commands are repeated here. Please run the first block in the server terminal, and the second block in the client terminal:

```bash
cd ~/my_code/Robotics_Assignment_5/
python3 sample_code_servers.py
```

```bash
cd ~/my_code/Robotics_Assignment_5/
python3 sample_code_clients.py
```

Then please demonstrate the following four items in order:

1. Option 1: Please type a sentence and show that the computer speaks it.
2. Option 2: Please say a clear sentence, for example "Hello, what can you tell me about robotics?", and show the text that appears.
3. Option 3: Please type a question and show the language model's reply.
4. Option 4: Please carry out the full voice conversation, without using the keyboard after you choose the option. Please show that your voice became text, that the language model answered, and that the answer was spoken.

---

## Step 23: Final Check and Submission

**What you will learn:** You will confirm that you have everything that the assignment requires before you submit.

Please check that each of the following three clips exists, and please tick every box before you submit.

- [ ] **Clip 1** (`Assignment5_Group<number>_Clip1`) shows the faces and names of all team members, your tests of the chat and instruct models, the system prompt, and the zero-shot, few-shot, and chain-of-thought prompts, together with spoken answers to the four questions from Step 14.
- [ ] **Clip 2** (`Assignment5_Group<number>_Clip2`) shows a walkthrough of `sample_code_servers.py` and `sample_code_clients.py`, in which the narrator explains the chosen models, the settings, how the client talks to the server, and how option 4 joins the three tools.
- [ ] **Clip 3** (`Assignment5_Group<number>_Clip3`) shows the server and the client running, options 1, 2, and 3 each working once, and option 4 running the full voice conversation without any use of the keyboard after choosing it.

Please also confirm the following rules before you upload:

- [ ] Every clip is one continuous recording with no editing.
- [ ] Every clip shows the computer screen, with a team member narrating.
- [ ] Every clip is named with the convention `Assignment5_Group<number>_Clip<number>`.

To submit, please upload each clip to YouTube and set its visibility to **Unlisted**, using the clip name as the title. Then every team member must paste all three links into Canvas under **Assignment 5**, even if the team recorded the clips together. Please do not upload the raw video files to Canvas. Source code is **not** required for this assignment.

---

## Additional Reading

The following two links are optional. They explain how language models can plan robot actions and describe more prompting techniques.

- How language models can plan robot actions (ReAct): <https://www.promptingguide.ai/techniques/react>
- A guide to prompting techniques: <https://www.promptingguide.ai/techniques>
