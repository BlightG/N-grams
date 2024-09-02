import re
import random
from collections import Counter

# function to read a txt file
def read_txt(txt_file: str):
    with open(txt_file) as file:
        content = file.read()
    return content

def parse_content(content):
    parsed_content = re.sub(r'[^a-zA-Z0-9 ]', '', content)
    return parsed_content

def bigram(content: str):
    result = {}
    word_list = content.split(' ')
    length = len(word_list)
    for i in range(1, length):
        if i < length - 1:
            key = (word_list[i - 1], word_list[i])
            if key not in result.keys():
                result[key] = [word_list[i + 1]]
            else:
                result[key].append(word_list[i + 1])
    return result 

def trigram(content: str):
    result = {}
    word_list = content.split(' ')
    length =len(word_list)
    for i in range(2, length):
        if i < length - 1:
            key = (word_list[i - 2], word_list[i - 1], word_list[i])
            if key not in result.keys():
                result[key] = [word_list[i + 1]] 
            else:
                result[key].append(word_list[i + 1])
    return result

def bigram_probability(bigram:dict):
    result = {}
    for key in bigram.keys():
        result[key] = dict(Counter(bigram[key]))
    return result

def trigram_probability(trigram:dict):
    result = {}
    for key in trigram.keys():
        result[key] = dict(Counter(trigram[key]))
    return result

def generate_trigram_text(trigram:dict, bigram, length=10):
    trigram_key = random.choice(list(trigram.keys())) # choose random key as a starting point
    words = list(trigram_key) # convert random choice to list
    # print(words)
    while length > len(words):
        if trigram_key in trigram.keys():
            count = trigram[trigram_key]
            next_word = random.choices(list(count.keys()), weights=count.values(), k=1)[0]
            words.append(next_word)
            trigram_key = tuple(words[-3:])
#            print(words)
#            print('trigram_key:', list(trigram_key))
        else:
            break

    return ' '.join(words)

if __name__ == "__main__":
    # take a test file as a corpus
    content = read_txt('words.txt')
    
    # parse content variable
    content = parse_content(content)

    # create a bigram
    content2 = bigram(content)
    content3 = trigram(content)
    
    bigram_count = bigram_probability(content2)
    trigram_count = trigram_probability(content3)

    print(generate_trigram_text(trigram_count, bigram_count, 15))
