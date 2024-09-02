import re
import random
from collections import Counter

# function to read a txt file
def read_txt(txt_file: str):
    with open(txt_file) as file:
        content = file.read()
    return content

def parse_content(content: str) -> str:
    # remove non alphanumeric characters
    parsed_content = re.sub(r'[^a-zA-Z0-9 ]', '', content)
    return parsed_content

# return a dict: {(word1, word2, word3): ['word4', 'words4', 'word5']}
def trigram(content: str) -> dict:
    result = {}
    # split the content into a list using empty space as a delimter
    word_list = content.split(' ')
    # get length of the word_list 
    length =len(word_list)

    for i in range(2, length):
        if i < length - 1:
            # tuple with 3 words as keys
            key = (word_list[i - 2], word_list[i - 1], word_list[i])

            # if key is not in the result dict add key with value of next word on list 
            # else append to list
            if key not in result.keys():
                result[key] = [word_list[i + 1]] 
            else:
                result[key].append(word_list[i + 1])

    return result

# return a dict: {('word1, 'word2', 'word3'): {'word4':2, 'word5':1}}
def trigram_count(trigram:dict):
    result = {}
    # use the Counter function to get count of each key
    for key in trigram.keys():
        result[key] = dict(Counter(trigram[key]))

    return result

# generate random text using complied data of length $length
def generate_trigram_text(trigram:dict, length=10) -> str:

    # use a random trigram key as start point
    trigram_key = random.choice(list(trigram.keys()))
    words = list(trigram_key) # convert random choice to list

    # iterate until the list variable words length is less than variable length
    while length > len(words):
        if trigram_key in trigram.keys():
            # get value from trigram value with structure of trigram_probability function
            count = trigram[trigram_key]
            # get the next_word as a random choice based on the weights
            next_word = random.choices(list(count.keys()), weights=count.values(), k=1)[0]
            # append next_word to words
            words.append(next_word)
            # get new trigram key
            trigram_key = tuple(words[-3:])
        else:
            # break if key not in trigram
            break

    return ' '.join(words)

# calculate probability of word apprearing after trigram
def trigram_probability(trigram: dict, trigram_count: dict ,trigram_key: tuple, next_word: str):
    if trigram_key in trigram_count.keys() and trigram_key in trigram.keys():
        if next_word in trigram_count[trigram_key].keys():
            probability = trigram_count[trigram_key][next_word] / len(trigram[trigram_key])
            print(f"probability of {next_word} coming after {trigram_key} is {probability}")
        else:
            print(f"probability of {next_word} coming after {trigram_key} is 0")
    else:
        print(f"Key Error: invalid Key {trigram_key}")

if __name__ == "__main__":
    # take a test file as a corpus
    content = read_txt('words.txt')
    
    # parse content variable
    content = parse_content(content)

    # create a trigram
    trigram_list = trigram(content)
    
    # generate a dict with values as weigthed next_words
    trigram_count = trigram_count(trigram_list)

    print(generate_trigram_text(trigram_count, 15))
    trigram_probability(trigram_list, trigram_count, ('The', 'quick', 'brown'), 'dame')
