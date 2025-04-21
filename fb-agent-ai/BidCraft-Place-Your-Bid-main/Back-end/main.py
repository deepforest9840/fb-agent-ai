from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import requests
from fuzzywuzzy import fuzz
import google.generativeai as genai
from datetime import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
MYDATA_FILE = "mydata.txt"
LOG_FILE = "log.txt"
USER_ANSWERS_FILE = "user_comment_answer.txt"
GRAPH_API_URL = "https://graph.facebook.com/v18.0"

# Read credentials from file
def read_mydata():
    data = {"access_token": "", "post_id": ""}
    if os.path.exists(MYDATA_FILE):
        with open(MYDATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    data[key.strip()] = value.strip()
    return data

# Fetch credentials
credentials = read_mydata()
ACCESS_TOKEN = credentials.get("access_token", "").strip()
POST_ID = credentials.get("post_id", "").strip()
PAGE_ID = POST_ID.split("_")[0] if "_" in POST_ID else ""

# Debugging: Print loaded credentials
print(f"🔹 Loaded Credentials:\n  - Access Token: {'✅' if ACCESS_TOKEN else '❌ MISSING'}\n  - Post ID: {POST_ID or '❌ MISSING'}\n  - Page ID: {PAGE_ID or '❌ MISSING'}")

# Validate credentials
if not ACCESS_TOKEN or not POST_ID:
    raise ValueError("⚠️ Missing access token or post ID. Please update mydata.txt and restart.")

# Initialize Gemini AI
genai.configure(api_key="AIzaSyBdJEa_Z8S5T8lmc8o-qBRKRP4XGz2Q29o")


async def log_reply(comment_id, commenter_name, comment_text, reply_message, source):
    """Logs the comment ID, commenter's name, comment, and reply message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | Comment ID: {comment_id} | Name: {commenter_name} | Comment: {comment_text} | Replied: {reply_message} | Source: {source}\n"
    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)
    print(f"📝 Logged reply: {log_entry.strip()}")

async def get_comments():
    """Fetch comments from the Facebook Graph API."""
    url = f"{GRAPH_API_URL}/{POST_ID}/comments"
    params = {"access_token": ACCESS_TOKEN, "fields": "id,from{name},message"}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"⚠️ Error fetching comments: {response.json()}")
        return []
    
    return response.json().get("data", [])

async def has_replies(comment_id):
    """Check if a comment has replies."""
    url = f"{GRAPH_API_URL}/{comment_id}/comments"
    params = {"access_token": ACCESS_TOKEN}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"⚠️ Error checking replies: {response.json()}")
        return False
    
    return len(response.json().get("data", [])) > 0

def load_user_answers():
    """Load predefined user answers from a file."""
    answers = {}
    if not os.path.exists(USER_ANSWERS_FILE):
        return answers  # Return empty if file doesn't exist

    with open(USER_ANSWERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "---" in line:
                comment, answer = line.strip().split("---", 1)
                answers[comment.strip().lower()] = answer.strip()
    
    return answers

async def query_llm(prompt):
    """Query the Gemini AI model."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini API Error: {e}")
        return "Sorry, I couldn't process your request."

async def generate_reply(comment_text):
    """Generate a reply to a comment."""
    user_answers = load_user_answers()
    comment_text_lower = comment_text.strip().lower()

    # Check for an exact match in user answers
    if comment_text_lower in user_answers:
        return user_answers[comment_text_lower], "txt file"

    # Check for a fuzzy match
    best_match, best_score = None, 0
    for saved_comment, saved_answer in user_answers.items():
        score = fuzz.ratio(comment_text_lower, saved_comment)
        if score > best_score:
            best_score = score
            best_match = saved_answer
    
    # Prepare prompt
    prompt = (
        f"Comment: {comment_text}\nSimilar Answer: {best_match}\nProvide a direct response."
        if best_match else f"Comment: {comment_text}\nProvide a direct response."
    )

    # Query LLM
    llm_reply = await query_llm(prompt)

    # Save new answer to file
    with open(USER_ANSWERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{comment_text}---{llm_reply}\n")
    
    return llm_reply, "llm"

async def reply_to_comment(comment_id, commenter_name, comment_text):
    """Reply to a Facebook comment."""
    reply_message, source = await generate_reply(comment_text)
    url = f"{GRAPH_API_URL}/{comment_id}/comments"
    params = {"message": reply_message, "access_token": ACCESS_TOKEN}

    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        print(f"✅ Replied to {commenter_name} ({comment_id})")
        await log_reply(comment_id, commenter_name, comment_text, reply_message, source)
    else:
        print(f"❌ Error replying to {comment_id}: {response.json()}")

async def main():
    """Main function to fetch and reply to comments."""
    comments = await get_comments()
    
    if not comments:
        print("No comments found.")
        return

    tasks = []
    for comment in comments:
        comment_id = comment["id"]
        commenter_name = comment.get("from", {}).get("name", "Unknown")
        comment_text = comment.get("message", "")

        if not await has_replies(comment_id):
            tasks.append(reply_to_comment(comment_id, commenter_name, comment_text))
            await asyncio.sleep(2)  # Prevent rate limit
        else:
            print(f"⏭️ Skipping comment {comment_id} (already replied)")
    
    await asyncio.gather(*tasks)

@app.get("/process-comments")
async def process_comments():
    """Trigger comment processing."""
    asyncio.create_task(main())  # Run in background
    return {"status": "Processing comments", "message": "Check logs for details."}

@app.post("/update-credentials")
async def update_credentials(access_token: str, post_id: str):
    """Update access token and post ID."""
    if not access_token or not post_id:
        raise HTTPException(status_code=400, detail="Access token and post ID are required")
    
    with open(MYDATA_FILE, "w", encoding="utf-8") as file:
        file.write(f"access_token={access_token}\n")
        file.write(f"post_id={post_id}\n")
    
    global ACCESS_TOKEN, POST_ID, PAGE_ID
    ACCESS_TOKEN = access_token.strip()
    POST_ID = post_id.strip()
    PAGE_ID = POST_ID.split("_")[0] if "_" in POST_ID else ""

    return {"status": "success", "message": "Credentials updated successfully"}

@app.get("/get-credentials")
async def get_credentials():
    """Retrieve stored credentials."""
    return read_mydata()


@app.post("/update-user-answer")
async def update_user_answer(comment: str, answer: str):
    """Update or add a user-defined answer in user_comment_answer.txt."""
    if not comment or not answer:
        raise HTTPException(status_code=400, detail="Both comment and answer are required")
    
    comment = comment.strip().lower()
    answer = answer.strip()
    
    # Load existing answers
    user_answers = load_user_answers()
    
    # Update or add new entry
    user_answers[comment] = answer
    
    # Write updated answers back to the file
    with open(USER_ANSWERS_FILE, "w", encoding="utf-8") as f:
        for q, a in user_answers.items():
            f.write(f"{q}---{a}\n")
    
    return {"status": "success", "message": "User answer updated successfully"}


@app.get("/get-logs")
async def get_logs():
    """Retrieve log file contents."""
    if not os.path.exists(LOG_FILE):
        return {"status": "error", "message": "Log file not found."}
    
    with open(LOG_FILE, "r", encoding="utf-8") as log_file:
        logs = log_file.read()
    
    return {"status": "success", "logs": logs}
