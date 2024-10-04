import re
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, StopCandidateException
import re
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key for Google Generative AI is not set in the environment variables.")


genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 100,
    "response_mime_type": "text/plain",
}


safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
}

# riddle = "What can fill a room but takes up no space?"
# answer ="light"


chat_session_gemini_riddle = None

def initialize_gemini_riddle(riddle,answer):
    global chat_session_gemini_riddle
    
    instruction = f"""
        The AI is tasked with checking the user's answer to a riddle that has already been presented. 
        The user is allowed a maximum of 5 attempts to guess the correct answer. 
        For each incorrect answer, the AI will provide feedback, letting the user know how many attempts are remaining. 
        If the user provides the correct answer within the 5 attempts, the AI will confirm the correct answer and stop checking further guesses. 
        If the user exhausts all 5 attempts without providing the correct answer, the AI will inform them that they are out of attempts and reveal the correct answer. 
        The AI will then conclude the current check. Do use emojis and the feedbacks should be fun.
        The riddle is: {riddle}
        Answer of the riddle is: {answer}
        
        Follow the feedback format strictly
        
        Feedback:**your feedback statement**
        The feedback statement must be within ** **. Be very very careful with the format and strictly follow the format
        
        Example of the format. This is one example format you need to generate different varieties of responses.
        
        Feedback:**positive or negative statement with emoji.**
        
        Strictly vary your positive or negative responses everytime. Player will pass the attempts to you. 
        Please carefully maintain the number of attempts. The user has 5 attempts to guess the word for the riddle.
    """
    
    gemini_riddle = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=instruction,
        safety_settings=safety_settings
    )
    
    chat_session_gemini_riddle = gemini_riddle.start_chat(history=[])


def Gemini_riddle(prompt):
    try:
        
        pattern = r'Feedback:\s*\*\*(.+)\*\*'
        response = chat_session_gemini_riddle.send_message(prompt)
        print("RAW TEXT:", response.text)
        
        match = re.search(pattern, response.text)
        if match:
             feedback_message = match.group(1)
             return feedback_message
        else:
            return False
        
    except Exception as e:
        return False
        
    
# initialize_gemini_riddle(riddle,answer)

# while True:
#    user =  input("Tell the answer: ")
#    bot = Gemini_riddle(f"The answer is {user}")
#    print("Bot:",bot)
   
    
