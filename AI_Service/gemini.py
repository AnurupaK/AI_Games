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

instruction = """
    You are an AI designed to generate a word and a related hint for a word-guessing game. Generate a word from a variety of interesting things. 
    Your output should follow this format strictly:

    Word: apple
    Hint: Fun one line hint with an emoji at the end
    Ensure that you generate random words along with appropriate hints for the game.
   
"""


gemini = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=instruction,
    safety_settings=safety_settings
)


chat_session_gemini = gemini.start_chat(history=[])

def get_gemini_response(prompt="Give me a word and I will guess it"):
    response  = chat_session_gemini.send_message(prompt)
    pattern = r"Word:\s*(\w+)\s*Hint:\s*(.*)"
    print("Raw Response")
    print(response.text)

    match = re.search(pattern, response.text)

    if match:
        word = match.group(1)  
        hint = match.group(2)  
        print("Word:", word)
        print("Hint:", hint)
    else:
        word = "apple"
        hint = "Red or green, crunchy and sweet, a healthy snack you’d love to eat."
    return word,hint





        
   
    
