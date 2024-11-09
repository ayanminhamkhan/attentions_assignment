from fastapi import FastAPI, Request
from transformers import AutoModelForCausalLM, AutoTokenizer
import sqlite3
import ollama
# import torch

app = FastAPI()

# Load a general-purpose LLM model from Hugging Face
# model_name = "openai-community/gpt2"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# Connect to SQLite database for chat history
conn = sqlite3.connect("chat_history2.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS chat")
cursor.execute("CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY, role TEXT, content TEXT)")
prompt_history=[]
prompt_history_1 = []
rules_1 = '''Follow these rules for all the following prompts:
1. Give answer only as an integer
2. Given the chat try to generate itinerary for a single day
3. if you have all of the following return '1' only: location, day of travelling, and interests, budget, place of stay
4. if there is a question asked just now you want any clarification return '2'
5. if you dont have any of these  or want more information return '2' only
'''
prompt_history_2=[]
rules_2='''Follow these rules for all the following prompts:
1. Given the chat for trying to generate a single day itinerary ask questions
2. if you dont have any of the following then ask me with a question : location, day of travelling, and interests, budget, place of stay
3. preferance of asking questions is time of travel, interest, budget 
3. if there is a question asked just now you want any clarification then give them some options like for interests or places and ask again
4. dont ask too many questions
'''
prompt_history_3=[]
rules_3='''Follow these rules for all the following prompts:
1.Based on given chat generate itinerary for a single day
'''



# Function to store chat messages
def store_message(role: str, content: str):
    cursor.execute("INSERT INTO chat (role, content) VALUES (?, ?)", (role, content))
    conn.commit()


def generate_itinerary(history):
    formatted_history = [{'role':'user','content' : rules_3}] +  history
    chat = generate_chat(formatted_history)
    return chat

def generate_question(history):
    formatted_history = [{'role':'user','content' : rules_2}] +  history
    chat = generate_chat(formatted_history)
    return chat

# Function to retrieve chat history
def get_chat_history():
    cursor.execute("SELECT role, content FROM chat")
    return cursor.fetchall()




def generate_chat(history):
    chat = ollama.chat(
        model='llama3.2',
        messages=history

    )
    # print("--------------------------------------------")
    # print(chat['message']['content'])
    return chat['message']['content']
# Task-specific prompt functions
def classify_chat(chat_history):
    # formatted_history =[{role: content} for role, content in chat_history]
    formatted_history = [{'role':'user','content' : rules_1}] +  chat_history
    # prompt = f"Classify the chat history to determine if an itinerary can be generated:\n\n{formatted_history}\n\n" \
    #          "Respond with '1' if there is enough information to generate an itinerary or '2' if more details are needed. "
    chat = generate_chat(formatted_history)
    # inputs = tokenizer(prompt, return_tensors="pt")
    # outputs = model.generate(**inputs, max_new_tokens=200)
    # response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    if '1' in chat[:3]:
        m_chat = generate_itinerary(chat_history)
        return m_chat
    elif '2' in chat[:3]:
        m_chat = generate_question(chat_history)
        return m_chat
    # elif '3' in chat[:3]:
        # m_chat = generate_weather(chat_history)
        
    return chat  # Extract '1' or '2'


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data["message"]
    print(user_message)
    # Store user message
    store_message("User", user_message)
    prompt_history.append({'role':'user','content':user_message})
    # Retrieve and classify chat history
    chat_history = get_chat_history()
    chat_message = classify_chat(prompt_history)
    # print("classification: ",chat_message)
    # if '1' in classification[0:3]:
    #     # Generate itinerary based on chat history
    #     itinerary = generate_itinerary(chat_history)
    #     response_message = f"Here's your itinerary:\n{itinerary}"
    # else:
    #     # Prompt user for more information
    #     # response_message = "Could you provide more details, such as the city to visit, available timings, budget, and interests?"
    #     response_message = classification

    # Store bot response
    prompt_history.append({'role':'assistant','content':chat_message})


    return {"reply": chat_message}
