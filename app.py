from flask import Flask, render_template, request, jsonify
from tasks import add_task, list_tasks, complete_tasks, list_pending_tasks, list_completed_tasks

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]
    
    massage = message.strip()

    if message.lower().startswith("add task:"):
        task = massage[9:].strip()
        if task:
            add_task(task)
            reply = f"Task added: {task}"
        else:
            reply = "please provide a task."

    elif message.lower() == "show tasks":
        reply = list_tasks()

    elif message.lower() == "show pending":
        reply = list_pending_tasks()

    elif message.lower() == "show completed":
        reply = list_completed_tasks()

    elif message.lower().startswith("done task:"):
        try:
            index = int(message.split(":")[1].strip())
            reply = complete_tasks(index)
        except:
            reply = "Use: done task: number"

    else:
        reply = "hello! I'm Luna web. You can manage tasks or chat."

    return jsonify({"reply": reply})

if __name__ == "__main__":

    app.run(host="0.0.0", port=10000)


