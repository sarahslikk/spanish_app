import numpy as np
import pandas as pd
import unicodedata
import re
import string
data = pd.read_csv(
    'sentence_pairs.tsv',
    delimiter='\t',
    names=['English', 'Column 2', 'Spanish'],
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

    spanish_sentence = data.loc[random_row, 'Spanish']
    english_sentence = data.loc[random_row, 'English']
    #print('Translate this sentence to English: ' + spanish_sentence)
    user_translation = input('Translate this sentence to English: ' + spanish_sentence + '\n')

    print(check_answer_function(user_translation, english_sentence))
    #the print('Translation: ', english_sentence)
    again_check = input('Again? Y to continue, N to go to main menu, anything else to quit.\nChoice: ')
    if again_check.lower() == 'y':
        return give_spanish_sentence(data)
    elif again_check.lower() == 'n':
        return ask_user()
    else:
        return print('Ending program, thanks for studying!')

def give_english_sentence(data):
    random_row = data.sample(n=1).index[0]
    spanish_sentence = data.loc[random_row, 'Spanish']
    english_sentence = data.loc[random_row, 'English']
    user_translation = input('Translate this sentence to Spanish: ' + english_sentence + '\n')

    print(check_answer_function(user_translation, spanish_sentence))
    again_check = input('Again? Y to continue, N to go to main menu, anything else to quit.\nChoice: ')
    if again_check.lower() == 'y':
        return give_english_sentence(data)
    elif again_check.lower() == 'n':
        return ask_user()
    else:
        return 'Ending program, thanks for studying!'

def ask_user():
    option = input('Choose an option: \n1. English to Spanish \n2. Spanish to English \n3. Search for a specific word\nType 1, 2, or 3 only or anything else to quit\nChoice: ')
    if option == '1':
        give_english_sentence(df)
    elif option == '2':
        give_spanish_sentence(df)
    elif option == '3':
        search_word()
    else: 
        return print('That is an incorrect choice. Please only type 1 or 2')

def search_word(word=''):
    word = normalize(input('Please enter a single word or phrase to search for. Only that exact phrase/word will be searched (case insensitive)\nChoice: '))
    df['NormalizedColumn'] = df['Spanish'].apply(normalize)
    filtered_df = df[df['NormalizedColumn'].str.contains(rf'\b{word}\b', case=False, na=False)]
    max_rows = 5
    filtered_df = filtered_df.drop(columns=['NormalizedColumn'])
    random_selection = filtered_df.sample(n=min(len(filtered_df), max_rows), random_state=42)
    print(random_selection)

    user_request = input('Would you like to see more? Y or N. N to return to main menu. Type anything else to quit\nChoice: ').lower()
    if user_request == 'y':
        try:
            more_selection = filtered_df.sample(n=min(len(filtered_df), max_rows), random_state=None)
            print(more_selection)
            search_word()  # Call again to allow repeated searches
        except ValueError:
            print("No more rows to display!")
            search_word()
    elif user_request == 'n':
        ask_user()
    else:
        return print('Thanks!')


ask_user()

