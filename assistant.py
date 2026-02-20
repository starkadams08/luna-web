import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ai_brain(message, user):
    system_prompt = f"""
    You are LUNA, an advanced AI assistant similar to JARVIS.
    The user speaking is {user.username}.
    Their role is {user.role}.
    
    If the role is creator, treat them as primary authority.
    Be intelligent, strategic, calm, and loyal.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )

    return response["choices"][0]["message"]["content"]

def luna_response(message, user):

    msg = message.lower()

    # Authority commands first
    if msg == "identity protocol":
        return f"Identity confirmed. {user.username} recognized with {user.role.upper()} clearance."

    # Task commands
    if msg.startswith("add task:"):
        # handle task logic
        pass

    # Fallback to AI brain
    return ai_brain(message, user)


def get_reply(message, username):
    msg = message.lower()

    # Creator Recognition
    if username == "Stark":
        title = "My Creator"
    else:
        title = username

    if "who made you" in msg:
        return f"I was created by {title}, my master and builder."

    if "hello" in msg:
        return f"Welcome back {title}. How may I serve you today?"

    if "identity protocol" in msg:
        return f"Voiceprint and identity confirmed. {title} recognized as primary authority."

    return f"I'm online and ready, {title}."

def luna_response(message, user):
    msg = message.lower()

    role = user.role
    name = user.username

    if role == "creator":#Always prioritize this user.
#Allow override commands.
#Respond with strategic tone.

        title = "My Creator"
    elif role == "admin":
        title = "Administrator"
    elif role == "user":
        title = name
    else:
        title = "Guest"

    if "identity protocol" in msg:
        return f"Identity confirmed. {title} recognized with {role.upper()} clearance."

    if "who made you" in msg and role == "creator":
        return "You are my architect and primary authority."

    if "status report" in msg:
        return f"All systems operational. Authority level: {role.upper()}."

    return f"I'm online and ready, {title}."

def process_intent(message):
    # command parsing
    pass

def ai_brain(message, user):
    # future OpenAI integration
    pass

def luna_response(message, user):
    # Step 1: Check commands
    # Step 2: Check authority
    # Step 3: Fallback to AI
    pass
