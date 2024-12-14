import numpy as np
import pandas as pd
import unicodedata
import re
import string
data = pd.read_csv(
    'sentence_pairs.tsv',
    delimiter='\t',
    names=['Column 1', 'Column 2', 'Column 3'],
    chunksize=1000,
    on_bad_lines='skip'  
)
df = pd.concat(data, ignore_index=True)
df = df.drop('Column 2', axis=1)

#print(df.head(10))
translator = str.maketrans('','', string.punctuation)

def normalize(input):
    output = ''.join(c for c in unicodedata.normalize('NFD', input)
                             if unicodedata.category(c) != 'Mn')
    
    return output


def check_answer_function(user_answer, correct_answer):
    return correct_answer 
    
def give_spanish_sentence(data):
    random_row = data.sample(n=1).index[0]

    spanish_sentence = data.loc[random_row, 'Column 3']
    english_sentence = data.loc[random_row, 'Column 1']
    #print('Translate this sentence to English: ' + spanish_sentence)
    user_translation = input('Translate this sentence to English: ' + spanish_sentence + '\n')

    print(check_answer_function(user_translation, english_sentence))
    #the print('Translation: ', english_sentence)

def give_english_sentence(data):
    random_row = data.sample(n=1).index[0]
    spanish_sentence = data.loc[random_row, 'Column 3']
    english_sentence = data.loc[random_row, 'Column 1']
    user_translation = input('Translate this sentence to Spanish: ' + english_sentence + '\n')

    print(check_answer_function(user_translation, spanish_sentence))

def ask_user():
    option = input('Choose an option: \n1. English to Spanish \n2. Spanish to English \n Type 1 or 2 only\nChoice: ')
    if option == '1':
        give_english_sentence(df)
    if option == '2':
        give_spanish_sentence(df)
    else: 
        return 'That is an incorrect choice. Please only type 1 or 2'
    
ask_user()
