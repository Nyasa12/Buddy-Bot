"""
BuddyBot - A Beginner-Friendly AI Chatbot using NLTK
=====================================================
This chatbot uses pattern matching (regex) and NLTK's chat module
to respond to user inputs. Great for BTech students learning NLP basics!

Requirements:
    pip install nltk

How to run:
    python chatbot.py
"""

# ============================================================
# Step 1: Import required libraries
# ============================================================
import re       # Regular expressions for pattern matching
import random   # To pick random responses for variety
import nltk     # Natural Language Toolkit

# Download required NLTK data (only needed once)
#nltk.download('punkt', quiet=True)
try:
    nltk.download('punkt', quiet=True)
except Exception:
    pass  # Skip if already downloaded or no internet


# ============================================================
# Step 2: Define the Knowledge Base (Question-Answer Pairs)
# ============================================================
# Each entry is a tuple: (list_of_patterns, list_of_responses)
# Patterns use regex — if user input matches, a random response is picked.

knowledge_base = [
    # --- Greetings ---
    (
        [r'\b(hi|hello|hey|greetings|howdy)\b'],
        [
            "Hello! 👋 How can I help you today?",
            "Hey there! What's on your mind?",
            "Hi! Nice to chat with you. What would you like to know?",
        ]
    ),

    # --- How are you ---
    (
        [r'\bhow are you\b', r"\bhow('s| is) it going\b"],
        [
            "I'm just a bot, but I'm running great! How about you?",
            "Doing well, thanks for asking! What can I help you with?",
        ]
    ),

    # --- Bot identity ---
    (
        [r"\bwhat('s| is) your name\b", r'\bwho are you\b'],
        [
            "I'm BuddyBot 🤖 — a simple rule-based chatbot built to demonstrate NLP concepts!",
            "Call me BuddyBot! I'm a pattern-matching chatbot, similar to NLTK's chat module.",
        ]
    ),

    # --- NLP ---
    (
        [r'\b(what is|explain|tell me about) (nlp|natural language processing)\b'],
        [
            "NLP (Natural Language Processing) is a field of AI that helps computers understand, "
            "interpret, and generate human language. It powers things like chatbots, translation, "
            "and voice assistants!",
        ]
    ),

    # --- Python ---
    (
        [r'\b(what is|explain|tell me about) python\b'],
        [
            "Python is a beginner-friendly programming language widely used in AI, web development, "
            "data science, and more. It's perfect for building chatbots with libraries like NLTK "
            "and Transformers!",
        ]
    ),

    # --- NLTK ---
    (
        [r'\b(what is|explain|tell me about) nltk\b'],
        [
            "NLTK (Natural Language Toolkit) is a Python library for working with human language data. "
            "It provides tools for tokenization, stemming, tagging, parsing, and more. "
            "Great for beginners learning NLP!",
        ]
    ),

    # --- Machine Learning ---
    (
        [r'\b(what is|explain|tell me about) (machine learning|ml)\b'],
        [
            "Machine Learning is a subset of AI where systems learn from data to make predictions "
            "or decisions. In NLP, ML models can classify text, generate responses, and understand sentiment.",
        ]
    ),

    # --- Transformers ---
    (
        [r'\b(what is|explain|tell me about) (transformer|transformers|gpt|bert)\b'],
        [
            "Transformers are a neural network architecture that revolutionized NLP. "
            "Models like GPT and BERT use transformers to understand and generate text. "
            "The Hugging Face 'transformers' library makes them accessible in Python!",
        ]
    ),

    # --- How to build a chatbot ---
    (
        [r'\bhow (do|can) (i|you) (build|make|create) a chatbot\b'],
        [
            "Great question! Start simple:\n"
            "  1) Define patterns & responses (like this bot)\n"
            "  2) Use regex or keyword matching\n"
            "  3) Add NLP with NLTK for tokenization & stemming\n"
            "  4) Eventually try transformer models for smarter responses!",
        ]
    ),

    # --- Tokenization ---
    (
        [r'\b(what is|explain) (tokenization|tokenize)\b'],
        [
            "Tokenization is breaking text into smaller pieces called tokens — usually words or subwords. "
            "For example, 'Hello world' becomes ['Hello', 'world']. "
            "It's the first step in most NLP pipelines!",
        ]
    ),

    # --- Stemming ---
    (
        [r'\b(what is|explain) (stemming|lemmatization)\b'],
        [
            "Stemming reduces words to their root form (e.g., 'running' → 'run'). "
            "Lemmatization is similar but more accurate — it considers context. NLTK has both!",
        ]
    ),

    # --- Sentiment Analysis ---
    (
        [r'\b(what is|explain) sentiment analysis\b'],
        [
            "Sentiment analysis determines whether text is positive, negative, or neutral. "
            "It's used in product reviews, social media monitoring, and customer feedback. "
            "You can build one with NLTK's VADER or train your own ML model!",
        ]
    ),

# Add this inside the knowledge_base list
(
    [r'\b(what is|explain|tell me about) (deep learning|dl)\b'],
    [
        "Deep Learning is a subset of Machine Learning that uses neural networks with many layers. "
        "It powers image recognition, speech-to-text, and language models like GPT!",
        "Deep Learning uses multi-layered neural networks to learn complex patterns from data. "
        "Frameworks like TensorFlow and PyTorch make it accessible in Python.",
    ]
),


    # --- Help ---
    (
        [r'\bhelp\b', r'\bwhat can you do\b'],
        [
            "I can chat about NLP concepts! Try asking:\n"
            "  • What is NLP?\n"
            "  • Explain tokenization\n"
            "  • How do I build a chatbot?\n"
            "  • What is machine learning?\n"
            "  • Tell me a joke!",
        ]
    ),

    # --- Jokes ---
    (
        [r'\b(joke|funny|laugh)\b'],
        [
            "Why did the NLP model break up with the regex? Because it wanted a deeper relationship! 😄",
            "Why do Python programmers prefer dark mode? Because light attracts bugs! 🐛",
            "What's a chatbot's favorite music? Al-gorithm and blues! 🎵",
        ]
    ),

    # --- Goodbye ---
    (
        [r'\b(bye|goodbye|see you|quit|exit)\b'],
        [
            "Goodbye! Happy coding! 👋🚀",
            "See you later! Keep learning NLP — you're doing great! ✨",
            "Bye! Remember: every expert was once a beginner. Keep going! 💪",
        ]
    ),

    # --- Thanks ---
    (
        [r'\bthank(s| you)\b'],
        [
            "You're welcome! Happy to help! 😊",
            "Anytime! Feel free to ask more questions.",
        ]
    ),
]

# Default responses when no pattern matches
fallback_responses = [
    "Hmm, I'm not sure about that. Try asking about NLP topics like tokenization or transformers!",
    "I don't have an answer for that yet. Type 'help' to see what I can talk about!",
    "Interesting question! I'm a simple pattern-matching bot — try asking about Python or NLP!",
]


# ============================================================
# Step 3: Define the Response Function
# ============================================================
def get_response(user_input: str) -> str:
    """
    Match user input against patterns in the knowledge base.
    Returns a matching response, or a fallback if nothing matches.
    """
    user_input = user_input.strip()
    if not user_input:
        return "Please type something! 😊"

    # Check each pattern group
    for patterns, responses in knowledge_base:
        for pattern in patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return random.choice(responses)

    # No pattern matched — return fallback
    return random.choice(fallback_responses)


# ============================================================
# Step 4: Command-Line Interface (CLI)
# ============================================================
'''def main():
    """Main function — runs the chatbot in the terminal."""
    print("=" * 55)
    print("  🤖 BuddyBot — Beginner NLP Chatbot")
    print("  Type 'help' for suggestions, 'quit' to exit")
    print("=" * 55)
    print()

    # Print welcome message
    print(f"BuddyBot: Hi! I'm BuddyBot 🤖 Ask me about NLP, Python, or chatbot building!\n")

    while True:
        # Get user input
        user_input = input("You: ").strip()

        # Check for exit commands
        if user_input.lower() in ('quit', 'exit', 'bye', 'goodbye'):
            print(f"\nBuddyBot: {get_response(user_input)}")
            break

        # Get and display response
        response = get_response(user_input)
        print(f"\nBuddyBot: {response}\n")


# ============================================================
# Step 5: Run the chatbot
# ============================================================
if __name__ == "__main__":
    main()'''


# ============================================================
# 🚀 SUGGESTIONS FOR IMPROVEMENTS (for advanced students):
# ============================================================
#
# 1. ADD NLTK TOKENIZATION & STEMMING:
#    from nltk.stem import PorterStemmer
#    stemmer = PorterStemmer()
#    # Stem user input before matching for better accuracy
#
# 2. USE TF-IDF FOR SMARTER MATCHING:
#    from sklearn.feature_extraction.text import TfidfVectorizer
#    from sklearn.metrics.pairwise import cosine_similarity
#    # Instead of regex, compare user input similarity to stored questions
#
# 3. ADD SENTIMENT ANALYSIS:
#    from nltk.sentiment import SentimentIntensityAnalyzer
#    sia = SentimentIntensityAnalyzer()
#    # Detect user mood and adjust responses accordingly
#
# 4. USE TRANSFORMERS FOR AI-POWERED RESPONSES:
#    from transformers import pipeline
#    chatbot = pipeline("text-generation", model="gpt2")
#    # Generate dynamic responses instead of picking from a fixed list
#
# 5. ADD CONVERSATION MEMORY:
#    # Store chat history in a list and pass context to the model
#    # This helps the bot remember what was discussed earlier
#
# 6. BUILD A WEB INTERFACE:
#    # Use Flask or Streamlit to create a web-based chat UI
#    # Example: streamlit run chatbot_web.py
#
# 7. LOAD Q&A FROM A JSON FILE:
#    # Store knowledge_base in a JSON file for easy editing
#    # import json; data = json.load(open('knowledge.json'))
#
# 8. ADD SPELL CHECKING:
#    # pip install pyspellchecker
#    # Correct typos before pattern matching


# ================= GUI PART =================
import tkinter as tk
from tkinter import scrolledtext

def send_message(event=None):
    user_input = entry.get().strip()
    
    if user_input == "":
        return
    
    chat_area.insert(tk.END, "You: " + user_input + "\n", "user")
    
    response = get_response(user_input)  # tera same function use hoga
    
    chat_area.insert(tk.END, "BuddyBot: " + response + "\n\n", "bot")
    
    entry.delete(0, tk.END)
    chat_area.yview(tk.END)

# Window
root = tk.Tk()
root.title("BuddyBot 🤖")
root.geometry("520x620")
root.configure(bg="#f5f5f5")

# Header
header = tk.Frame(root, bg="#d32f2f", height=60)
header.pack(fill=tk.X)

title = tk.Label(header, text="BuddyBot 🤖",
                 font=("Segoe UI", 16, "bold"),
                 bg="#d32f2f", fg="white")
title.pack(pady=15)

# Chat area
chat_area = scrolledtext.ScrolledText(root,
                                      wrap=tk.WORD,
                                      font=("Segoe UI", 11),
                                      bg="white",
                                      bd=0,
                                      padx=10,
                                      pady=10)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_area.tag_config("user", foreground="blue", font=("Arial", 11, "bold"))
chat_area.tag_config("bot", foreground="black")

# Input
frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(frame, font=("Segoe UI", 12), bd=2)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10), ipady=6)

btn = tk.Button(frame, text="Send", command=send_message,
                bg="#d32f2f", fg="white",
                font=("Segoe UI", 11, "bold"))
btn.pack(side=tk.RIGHT)

# Enter key
entry.bind("<Return>", send_message)

# Run
root.mainloop()