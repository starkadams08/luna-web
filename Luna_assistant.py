import tkinter as tk
from tkinter import scrolledtext
import json
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Create main window
root = tk.Tk()
root.title(" LUNA - Royal AI assistant")
root.geometry("500x600")
root.resizable(False, False)

# Chat display
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 11))
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_display.config(state=tk.DISABLED)

# Input field
user_input = tk.Entry(root, font=("Arial", 12))
user_input.pack(padx=10, pady=5, fill=tk.X)

def send_message():
    message = user_input.get().strip()
    if not message:
        return
    
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {message}\n")
    chat_display.config(state=tk.DISABLED)

    reply = get_reply(message)

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"LUNA: {reply}\n\n")
    chat_display.config(state=tk.DISABLED)

    user_input.delete(0, tk.END)

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

MEMORY_FILE = "memory.json"

def load_memory():
    with open(MEMORY_FILE, "r") as file:
        return json.load(file)
    
def save_memory(data):
    with open(MEMORY_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_task(task_text):
    data = load_memory()
    data["tasks"].append({
        "task": task_text,
        "done": False
    })
    save_memory(data)

def list_tasks():
    data = load_memory()
    tasks = data["tasks"]

    if not tasks:
        return "You have no tasks right now"
    
    response = "Here are your tasks:\n"
    for idx, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else "✗"
        response += f"{idx}. [{status}] {task['task']}\n"

    return response.strip()

def complete_task(index):
    data = load_memory()
    tasks = data["tasks"]

    if index < 1 or index > len(tasks):
        return "That task number doesn't exist in your list."
    
    tasks[index - 1]["done"] = True
    save_memory(data)
    return f"Task {index} marked as done."

def list_pending_tasks():
    data = load_memory()
    tasks = data["tasks"]
    pending = [task for task in tasks if not task["done"]]

    if not pending:
        return "You have no pending tasks"
    
    response = "Here are your pending tasks:\n"
    for idx, task in enumerate(pending, start=1):
        response += f"{idx}. {task['task']}\n"

    return response.strip()

def list_completed_tasks():
    data = load_memory()
    tasks = data["tasks"]
    completed = [task for task in tasks if task["done"]]

    if not completed:
        return "You have no completed tasks"
    
    response = "Here are your completed tasks:\n"
    for idx, task in enumerate(completed, start=1):
        response += f"{idx}. {task['task']}\n"

    return response.strip()

def get_reply(message):
    message = message.strip()

    # Add task
    if message.lower().startswith("add task:"):
        task = message[9:].strip()
        if task:
            add_task(task)
            reply = f"Task added successfully: {task}"
        else:
            reply = "Please tell me what task to add."
    
    # Show tasks 
    elif message.lower() == "show tasks":
        reply = list_tasks()

    elif message.lower() == "show pending":
        reply = list_pending_tasks()

    elif message.lower() == "show completed":
        reply = list_completed_tasks()

    # Complete task
    elif message.lower().startswith("done task:"):
        try:
            index = int(message.split(":")[1].strip())
            reply = complete_task(index)
        except:
            reply = "Please use: done task: number"

    # Friendly chat
    else:
        msg = message.lower()

        if "hello" in msg or "hi" in msg:
            reply = "I'm listening. You can chat with me or manage your tasks."
        elif "how are you" in msg:
            reply = "I'm feeling calm and ready to help you"
        elif "thank" in msg:
            reply = "you're always welcome"
        elif "bye" in msg:
            reply = "Goodbye, I'll be right here when you reply."
        else:
            reply = "I'm listening. You can chat with me or manage your tasks."

    return reply

# Start message
chat_display.config(state=tk.NORMAL)
chat_display.insert(tk.END, "LUNA: Hello! I'm LUNA, your Royal AI Assistant. How can I assist you today?\n\n")
chat_display.config(state=tk.DISABLED)

root.mainloop()

 