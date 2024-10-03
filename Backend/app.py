from flask import Flask, render_template, request, jsonify
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AI_Service')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))




from gemini import get_gemini_response
from WordIndex import Word_Pair_Index
from gemini_Guess import initialize_gemini,gemini_guess
from rock_gemini import initialize_gemini_rock, gemini_rock,get_gemini_item
from Rock_Paper_Scissor_Decision import RPSDecision
app = Flask(__name__, template_folder="../Frontend/templates", static_folder="../Frontend/static")

@app.route('/')
def home():
    return render_template('index.html')


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
    
    
    
    
    
    

if __name__ == "__main__":
    app.run(debug=True)