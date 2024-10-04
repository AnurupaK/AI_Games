import sys
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, StopCandidateException
import re
load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AI_Service')))

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key for Google Generative AI is not set in the environment variables.")

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
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
}

# Initialize the chat session globally
chat_session_gemini_v2 = None

def initialize_gemini(word):
    global chat_session_gemini_v2
    instruction = f"""
        You are a helpful assistant guiding the user in a word-guessing game. The user is trying to guess letters for the word '{word}'. For each letter the user guesses, you need to provide feedback.
        
        Strictly follow the format:
        If the guessed letter is correct:
        Feedback: **some positive feedback but with emoji and do mention the letter.**

        If the guessed letter is incorrect:
        Feedback: **some negative feedback but with emoji and do mention the letter.**
        
        Please check the word strictly and then only give your feedbacks. And do give different feedbacks everytime.
        Be very careful with tracking all the letters the user guess and then only give proper feedbacks.
        Note the Feedback statement needs to be within ** ** with Feedback: before
    """
    
    gemini_v2 = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=instruction,
        safety_settings=safety_settings
    )
    # print("INSTRUCTION: ",instruction)
    chat_session_gemini_v2 = gemini_v2.start_chat(history=[])

def gemini_guess(letter_input):
    try:
        if chat_session_gemini_v2 is None:
            # raise ValueError("Gemini chat session is not initialized. Call initialize_gemini(word) first.")
            return "Oops! The word is in the baking. Lets start the game😎"
        pattern = r'Feedback:\s*\*\*(.+)\*\*'
        
        response = chat_session_gemini_v2.send_message(letter_input)
        print("RAW TEXT:",response.text)
        match = re.search(pattern, response.text)
        if match:
             feedback_message = match.group(1)
             print("Feedback test to return: ",feedback_message)
             return feedback_message
        else:
            return 0
    except StopCandidateException:
        return 0


# initialize_gemini("apple")



# while True:
#     user_letter = input("Guess: ")
#     bot = gemini_guess(user_letter)
#     print('Bot:',bot)