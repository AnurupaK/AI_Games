import sys
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, StopCandidateException
import re

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key for Google Generative AI is not set in the environment variables.")

# Configure the Google Generative AI library with the API key
genai.configure(api_key=api_key)

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 100,
    "response_mime_type": "text/plain",
}

# Define safety settings
safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# Initialize the chat session globally
chat_session_gemini_v2 = None

def initialize_gemini_love(your_name, partner_name, percentage):
    global chat_session_gemini_v2
    instruction = f"""
      You are an AI designed to calculate the love compatibility between two people.
      The user's name is {your_name}, and their partner's name is {partner_name}. 
      Their love compatibility score is {percentage}%.

      Create a fun and lovable statement about their relationship in not more than 2 lines. 
      Be creative with the statements and everytime statements should be deifferent.
      Don't give boring and same responses.
       
      Strictly follow the format:
      Love: **Insert a playful or heartwarming statement about their relationship here with emoji**
      The message needs to me within ** **
    """
    
    gemini_v2 = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=instruction,
        safety_settings=safety_settings
    )
    
    chat_session_gemini_v2 = gemini_v2.start_chat(history=[])

def gemini_calculate_love(prompt):
    try:
        if chat_session_gemini_v2 is None:
            return "Oops! Gemini session not initialized."
        
        pattern = r'Love:\s*\*\*(.+)\*\*'
        response = chat_session_gemini_v2.send_message(prompt)
        print("RAW TEXT:", response.text)
        
        match = re.search(pattern, response.text)
        if match:
             feedback_message = match.group(1)
             return feedback_message
        else:
            return False
    
    except StopCandidateException:
        return False

# Initialize the love compatibility
# initialize_gemini_love('Anu', 'Vishnu', 100)
# result = gemini_calculate_love('What is the status of love?')
# print(result)
