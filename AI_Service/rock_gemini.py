import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, StopCandidateException
import re
load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key for Google Generative AI is not set in the environment variables.")

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

instruction1 = """
     You are playing rock paper scissor game with an user. The user will randomly select one of the following options: rock, paper, or scissors. 
     Your task is to also choose one of the three.

        Strictly follow the format:

        Choosen_Item:**rock**
        or
        Choosen_Item:**paper**
        or
        Choosen_Item:**scissor**
"""

gemini_choosing= genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=instruction1,
    safety_settings=safety_settings
)

chat_gemini_choose = gemini_choosing.start_chat(history=[])

def get_gemini_item():
    try:
        response = chat_gemini_choose.send_message("Choose any one: rock or paper or scissor")
        # print("Raw Text:",response.text)
        pattern = r"Choosen_Item:\*\*(rock|paper|scissor)\*\*"
        match = re.search(pattern, response.text)
        if match:
            choice = match.group(1)
            # print(f"AI chose: {choice}")
            return choice
        else:
            return "rock"
    except StopCandidateException:
        return "rock"

chat_session_gemini_rock = None

def initialize_gemini_rock(ai_item):
    global chat_session_gemini_rock
    instruction = f"""
        You are a helpful AI assitant who give feedback on rock paper scissor game.
        AI has choosen {ai_item}.
        
        Game rules (follow it very strictly):

        Rock beats Scissors (Rock > Scissors)
        Scissors beats Paper (Scissors > Paper)
        Paper beats Rock (Paper > Rock)
        
        Give feedback in the following format strictly:
        Feedback:**Some positive or negative feedback with some emoji.**
        
        The feedback statement needs to be strictly within ** **.
        
        
    """
    
    gemini_rock = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=instruction,
        safety_settings=safety_settings
    )
    print("INSTRUCTION: ",instruction)
    chat_session_gemini_rock = gemini_rock.start_chat(history=[])

def gemini_rock(user_item):
    try:
        pattern = r'Feedback:\s*\*\*(.+)\*\*'
        
        response = chat_session_gemini_rock.send_message(user_item)
        print("RAW TEXT:",response.text)
        match = re.search(pattern, response.text)
        if match:
             feedback_message = match.group(1)
            #  print("Feedback test to return: ",feedback_message)
             return feedback_message
        else:
            return False
    except StopCandidateException:
        return False