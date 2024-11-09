# Attentions Assignment

This application provides a streamlined itinerary planning experience using a chat-based interface. The app has a **Streamlit frontend** that connects to a **FastAPI backend** with multiple Large Language Model (LLM) agents powered by **Ollama’s LLaMA 3.2**.

## Installation Requirements

To run the app, make sure you have the following dependencies installed. You can install them all at once with this command:

```bash
pip install fastapi sqlite3 ollama requests streamlit uvicorn
```

## Running the Application

1. **Start the Backend Server**  
   Open a terminal, navigate to the project folder, and run:  
   ```bash
   uvicorn backend:app --reload
   ```
3. **Start the Frontend**  
   Open another terminal in the same folder, and run:  
   ```bash
   streamlit run ./frontend.py
   ```

   If you encounter an error when the window loads, simply reload it.

## How the App Works

The frontend is a standard **Streamlit** window that allows users to interact with the backend server. Each session holds only **one chat sequence**. To start a new conversation, you’ll need to restart or reload the backend.

The backend contains multiple LLM agents running on **LLaMA 3.2** via **Ollama**, each specializing in a specific function:
- One agent directs the flow by deciding which other agents to use.
- Two additional agents gather further information and generate itinerary details.

## Features & Future Enhancements

Due to time constraints, some functions were not implemented. Here are ideas for future additions:

1. **User Login and Chat Storage**  
   Adding a login feature and chat storage would allow users to store and retrieve chat history. This could be easily implemented with an additional Streamlit window, utilizing the existing database to store all conversations by user.

2. **Weather Information**  
   After generating an itinerary, the app could call a weather API to fetch weather details for each location.

3. **Map Integration**  
   Using a map API, we could display city maps and visually indicate travel paths.

4. **Enhanced Prompt Engineering**  
   Further prompt engineering could improve response quality. Additional agents could be added to perform specialized functions and refine the itinerary based on user input. Additionally, using different models for each agent could enhance functionality.
