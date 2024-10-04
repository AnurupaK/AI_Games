from flask import Flask, render_template, request, jsonify
import os
import sys
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AI_Service')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))




from gemini import get_gemini_response
from WordIndex import Word_Pair_Index
from gemini_Guess import initialize_gemini,gemini_guess
from rock_gemini import initialize_gemini_rock, gemini_rock,get_gemini_item
from Rock_Paper_Scissor_Decision import RPSDecision
from Love import LoveCalculator_v2,LoveEmoji
from gemini_love import initialize_gemini_love,gemini_calculate_love
from gemini_riddle import initialize_gemini_riddle, Gemini_riddle
from riddle_list import riddles

app = Flask(__name__, template_folder="../Frontend/templates", static_folder="../Frontend/static")

lives = 5

@app.route('/')
def home():
    return render_template('index.html')


##GAME HANGMAN
@app.route('/api/gemini', methods=['GET'])
def Gemini_Word_Make():
    global word
    word,hint = get_gemini_response() 
    # word = "appleyeihrev"
    word = word.upper()
    initialize_gemini(word)
    word_index_count = Word_Pair_Index(word) 
    return jsonify({'Word':word,'Hint':hint,'Word_Index_Counter':word_index_count})
      

@app.route('/api/guessed_letter', methods=['POST'])
def Letter():
    data = request.get_json()
    guess_letter = data['letter']
    message = gemini_guess(guess_letter)
    print(guess_letter)

    return jsonify({'letterUser':guess_letter,'message':message})



##GAME2 - ROCK PAPER SCISSOR
@app.route('/api/rock_paper_scissor',methods=['POST'])
def RockPaperScissor():
    data = request.get_json()
    user_item = data['item']
    print("User has choosen",user_item)
    ai_item = get_gemini_item()
    print("AI has choosen",ai_item)
    initialize_gemini_rock(ai_item)
    message = gemini_rock(user_item)
    print("AI MESSAGE:", message)
    
    
    user_item = user_item.strip()
    ai_item = ai_item.strip()

    decision_message = RPSDecision(user_item='rock',ai_item='paper')
    print(decision_message)
    
    if ai_item.lower()=='rock':
        ai_item = "🪨"
    elif ai_item.lower()=='paper':
        ai_item= "📄"
    else:
        ai_item = "✂️"
        
    if(message):
        return jsonify({'bot_item':ai_item,'message':message})
    else:
        return jsonify({'bot_item':ai_item,'message':decision_message})
    
    
#GAME3
@app.route('/api/lovePercentage',methods=['POST'])
def LoveCalculator():
    data = request.get_json()
    YourName = data['your_name']
    HisName = data['partner_name']
    print(YourName,HisName)
    percentage = LoveCalculator_v2(YourName,HisName)
    initialize_gemini_love(YourName,HisName,percentage)
    message = gemini_calculate_love("Whats the feedback about their relationship?")
    print(message)
    print(YourName,HisName)
    print(percentage)
    emoji = LoveEmoji(percentage)
    print(emoji)
    
    if(message):
        return jsonify({'percentage':percentage,'message':message,"emoji":emoji})
    else:
        message = f"{YourName} and {HisName}, every love story is unique, with its own twists and turns. Embrace the journey together, for love grows deeper with every moment shared! 💖✨"
        return jsonify({'percentage':percentage,'message':message,"emoji":emoji})
    
    
    
##GAME 4
@app.route('/api/riddleGenerate',methods=['GET'])
def Riddle_Generator():
    riddle_item = random.choice(list(riddles.items()))
    global riddle_sentence
    global answer
    global lives 
    lives = 5
    riddle_sentence = riddle_item[0]
    answer = riddle_item[1]
    return jsonify({'riddle':riddle_sentence,'answer':answer})

@app.route('/api/aiComment', methods=['POST'])
def Comment():
    data = request.get_json()
    global lives
    user_answer = data['answer_to_check']
    initialize_gemini_riddle(riddle=riddle_sentence,answer=answer)
    if (user_answer.lower().strip()!=answer.lower().strip()):
        lives = lives - 1
        default_answer = f"Almost! But that's not the answer. Would you like to guess again? 🤔💭. You have got {lives} attempts left"
        answer_status = 'no'
    else:
        default_answer = "Spot on! You've cracked the riddle! 🔍✨"
        answer_status = 'yes'
    print("Lives:",lives)
    input_text = f"The answer is {user_answer} and he has {lives} left"
    response = Gemini_riddle(input_text)
    print(response)
    
    
        
    if (response):
        return jsonify({'AIcomment':response,'answer_status':answer_status})
    else:
        return jsonify({'AIcomment':default_answer,'answer_status':answer_status})
    

    

if __name__ == "__main__":
    app.run(debug=True)