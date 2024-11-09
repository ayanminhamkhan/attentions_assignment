import streamlit as st
import requests

# Set the FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000/chat"

# Streamlit UI setup
st.title("Travel Itinerary Chatbot")
st.write("Enter your details for a customized travel itinerary!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat input area
user_input = st.text_input("You:", key="user_input")

if st.button("Send") or st.session_state.get("submit"):
    # Send user message to the backend
    response = requests.post(BACKEND_URL, json={"message": user_input})
    response_data = response.json()

    # Store user message and bot reply in session state
    st.session_state["messages"].append(("User", user_input))
    st.session_state["messages"].append(("Bot", response_data["reply"]))

    # Clear input field
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = ""

# Display chat history
for role, message in st.session_state["messages"]:
    st.write(f"**{role}:** {message}")
