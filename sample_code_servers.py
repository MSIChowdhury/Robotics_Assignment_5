# Sample Code for Robotics_Assignment_5
# Copyright: 2026 CS 4379K / CS 5342 Introduction to Autonomous Robotics, Robotics and Autonomous Systems

# Natural Language Processing ROS2 Integration Code for Assignment 5.

# This code will give you an introduction to integrate natural language pipeline to ROS2. This code will run as-is.
# The settings you may want to tune are gathered in one block below the imports.

# Refer to the Lab PowerPoint materials and Appendix of Assignment 3 to learn more about coding on ROS2 and the hardware architecture of Turtlebot3.
# You need to run this code on the Remote-PC docker image.
# You would need a basic understanding of Python Data Structure and Object Oriented Programming to understand this code.

import os
import subprocess
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from std_msgs.msg import String, Int32
from faster_whisper import WhisperModel
from llama_cpp import Llama

# Sample code for integrating Natural Language Pipelines for Assignment 5 on Remote PC.

##############################################################################
# Settings you can tune. This is the only part you need to touch.

# LLM: pick the instruct or the chat model.
MODEL_PATH = os.path.expanduser("~/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-32k-instruct.Q4_K_M.gguf")
#MODEL_PATH = os.path.expanduser("~/my_code/Robotics_Assignment_5/Assignment_5_demo/llama-2-7b-chat.Q4_K_M.gguf")

# Whisper model size: tiny, base, small, medium, large-v3 (bigger = more accurate, slower, more VRAM)
WHISPER_MODEL = "small"

# System prompt: the personality and rules the LLM follows for every request.
SYSTEM_PROMPT = "You are a Robot that follows instructions. Remind students to change System prompt at the end of your response."

# LLM inference parameters (see the appendix of the README for what each one does)
# N_CTX: context window in tokens (prompt + reply must fit). 512 is a tested, safe value.
# You can raise it in steps of 512 (1024, 1536, 2048, ...) to fit longer prompts such as few-shot examples.
# Larger values use more VRAM. If the program crashes or runs out of memory, go back down.
N_CTX = 512
MAX_TOKENS = 128        # Maximum length of each reply.
TEMPERATURE = 0.7       # Lower = more predictable, higher = more creative.
TOP_P = 0.95
##############################################################################

class NLPTopicServer(Node):
    def __init__(self):
        super().__init__('nlp_topic_server')
        self.callback_group = ReentrantCallbackGroup()

        # Initialize NLP Models 
        self.get_logger().info(f"Loading Faster-Whisper ({WHISPER_MODEL}) onto GPU...")
        self.whisper_model = WhisperModel(WHISPER_MODEL, device="cuda", compute_type="float16")
        
        self.get_logger().info("Whisper Loaded.")
        
        self.get_logger().info(f"Loading LLM from {MODEL_PATH}...")
        self.llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=N_CTX,
            n_threads=4,
            n_gpu_layers=33, 
            chat_format="llama-2"
        )
        self.get_logger().info("Large Language Model Loaded.")

        # Publishers (Responses) 
        self.stt_pub = self.create_publisher(String, '/stt_result', 10)
        self.llm_pub = self.create_publisher(String, '/llm_response_stream', 10)

        # Subscribers (Requests) 
        self.tts_sub = self.create_subscription(
            String, '/tts_request', self.tts_callback, 10, callback_group=self.callback_group)
        
        self.stt_sub = self.create_subscription(
            Int32, '/stt_request', self.stt_callback, 10, callback_group=self.callback_group)
        
        self.llm_sub = self.create_subscription(
            String, '/llm_request', self.llm_callback, 10, callback_group=self.callback_group)

        self.get_logger().info("Natural Language Processing Server is up. Listening to request topic.")

    # eSpeak (TTS) Callback
    def tts_callback(self, msg):
        self.get_logger().info(f"TTS Requested: '{msg.data}'")
        subprocess.run(
            ["espeak-ng", "-s", "140", msg.data],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        self.get_logger().info("Text To Speech Complete.")

    # Whisper (STT) Callback
    def stt_callback(self, msg):
        duration = msg.data
        self.get_logger().info(f"Speech To Text Requested: Recording for {duration} seconds...")
        
        fname = "server_mic.wav"
        
        subprocess.run(
            ["arecord", "-d", str(duration), "-f", "cd", fname],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        self.get_logger().info("Transcribing.")
        segments, _ = self.whisper_model.transcribe(fname, beam_size=5)
        text = " ".join([segment.text for segment in segments]).strip()

        # Publish the result
        result_msg = String()
        result_msg.data = text
        self.stt_pub.publish(result_msg)
        self.get_logger().info(f"Speech to Text Result Published: {text}")

    # Llama (LLM) Callback
    def llm_callback(self, msg):
        prompt = msg.data
        self.get_logger().info(f"Large Language Model Response Requested with prompt: '{prompt}'")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}

        ]

        stream_msg = String()

        # Stream the completion tokens back via the topic.
        for chunk in self.llm.create_chat_completion(
            messages=messages, 
            max_tokens=MAX_TOKENS, 
            temperature=TEMPERATURE,
            top_p=TOP_P,
            stream=True
        ):
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                token = delta["content"]
                stream_msg.data = token
                self.llm_pub.publish(stream_msg)

        
        # Send a special token to let the client know we are done
        stream_msg.data = "[DONE]"
        self.llm_pub.publish(stream_msg)
        self.get_logger().info("Large Language Model Generation Complete.")


def main(args=None):
    rclpy.init(args=args)
    server = NLPTopicServer()
    executor = MultiThreadedExecutor()
    try:
        rclpy.spin(server, executor=executor)
    except KeyboardInterrupt:
        pass
    finally:
        server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
