def RPSDecision(user_item, ai_item):
    if (user_item.lower() == 'rock') and (ai_item.lower() == 'paper'):
        return "🧻 AI covers your rock with paper! AI wins!"
    elif (user_item.lower() == 'rock') and (ai_item.lower() == 'scissor'):
        return "💥 You smash AI's scissors! You win!"
    elif (user_item.lower() == 'paper') and (ai_item.lower() == 'rock'):
        return "🧻 You wrap AI's rock in paper! Victory is yours!"
    elif (user_item.lower() == 'paper') and (ai_item.lower() == 'scissor'):
        return "✂️ AI cuts through your paper! AI wins!"
    elif (user_item.lower() == 'scissor') and (ai_item.lower() == 'paper'):
        return "✂️ You slice up AI's paper! You win!"
    elif (user_item.lower() == 'scissor') and (ai_item.lower() == 'rock'):
        return "💥 AI smashes your scissors with a rock! AI wins!"
    elif user_item.lower() == ai_item.lower():
        return "😲 It's a tie! Great minds think alike!"



# print(RPSDecision(user_item='rock',ai_item='paper'))