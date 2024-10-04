from collections import Counter

def Word_Pair_Index(word):
    word = list(word)
    choosen_word = Counter(word)
    count_more = []
    count_one = []

    for key,value in choosen_word.items():
        if value>1:
            count_more.append(key)
        else:
            count_one.append(key)

    letters_with_index = {}

    total_list = [count_more,count_one]

    for sub in total_list:
          for letter_with_count_more in sub:
                count = []
                for index in range(len(word)):
                    if letter_with_count_more == word[index]:
                        count.append(index)
                    
                    letters_with_index[letter_with_count_more] = count
    return letters_with_index