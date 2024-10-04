from collections import Counter

true_list = ['T','R','U','E']
love_list = ['L','O','V','E']

heart_list = [true_list,love_list]


def LoveCalculator_v2(first_name, last_name):
    love_numbers = []
    first_name = first_name.upper()
    last_name = last_name.upper()
    
    name = first_name + last_name
    print(name)
    name = Counter(name)
    for sub_list in heart_list:
        sum = 0
        for letter in sub_list:
            for key,value in name.items():
                if letter==key:
                    sum = sum + value
        love_numbers.append(sum)
    
    percentage = ""
    for i in love_numbers:
        i = str(i)
        percentage = percentage + i
    percentage = int(percentage)
    return percentage
    
def LoveEmoji(percentage):
    if percentage >= 0 and percentage <= 10:
        emoji = "💔"  # Broken heart
    elif percentage > 10 and percentage <= 20:
        emoji = "❤️"  # Red heart
    elif percentage > 20 and percentage <= 30:
        emoji = "💖"  # Sparkling heart
    elif percentage > 30 and percentage <= 40:
        emoji = "💞"  # Revolving hearts
    elif percentage > 40 and percentage <= 50:
        emoji = "💕"  # Two hearts
    elif percentage > 50 and percentage <= 60:
        emoji = "💗"  # Growing heart
    elif percentage > 60 and percentage <= 70:
        emoji = "💘"  # Heart with arrow
    elif percentage > 70 and percentage <= 80:
        emoji = "💓"  # Beating heart
    elif percentage > 80 and percentage <= 90:
        emoji = "💝"  # Heart with ribbon
    elif percentage > 90 and percentage <= 100:
        emoji = "❤️‍🔥"  # Heart on fire
    
    return emoji
