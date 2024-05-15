import nltk
import os 
import string 
import re
import pandas as pd
from nltk.corpus import cmudict
df = pd.read_csv('csvfiles/input.csv')
df['POSITIVE SCORE'] = ''
df['NEGATIVE SCORE'] = ''
df['POLARITY SCORE'] = ''
df['SUBJECTIVITY SCORE'] = ''
df['AVG SENTENCE LENGTH'] = ''
df['PERCENTAGE OF COMPLEX WORDS'] = ''
df['FOG INDEX'] = ''
df['AVG NUMBER OF WORDS PER SENTENCE'] = ''
df['COMPLEX WORD COUNT'] = ''
df['WORD COUNT'] = ''
df['SYLLABLES PER WORD'] = ''
df['PERSONAL PRONOUNS'] = ''
df['AVG WORD LENGTH'] = ''
def read_stop_words(directory):
    stop_words = set()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file:
            stop_words.update(set(word.strip() for word in file.readlines()))
    return stop_words
def read_positive_negative_words(score_dir, file_name):
    pos_nev_words = set()
    with open(os.path.join(score_dir, file_name), 'r') as file:
        pos_nev_words.update(set(word.strip() for word in file.readlines()))
    return pos_nev_words
d = cmudict.dict()
def syllable_count(word):
    if word.lower() in d:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]])
    else:
        return max(1, len(word) // 3)
def count_personal_pronouns(text):
    pattern = r'\b(?!US\b)\b(?:I|we|my|ours|us)\b'
    personal_pronouns = re.findall(pattern, text, flags=re.IGNORECASE) 
    return len(personal_pronouns)
def filer(article_Dir, stop_words, positive_words, negative_words):
    for article_file in os.listdir(article_Dir):
        positive_score = 0
        negative_score = 0
        with open(os.path.join(article_Dir, article_file), 'r', encoding='utf-8') as f:
            raw = f.read()
            word_tokens = nltk.word_tokenize(raw)
            filtered_tokens = [word for word in word_tokens if word.lower() not in stop_words]
            filtered_text = ' '.join(filtered_tokens)
            for score_check in filtered_tokens:
                if score_check in positive_words:
                    positive_score += 1 
                elif score_check in negative_words:
                    negative_score -= 1
            negative_score = abs(negative_score)
            try: 
                var_minus = float(positive_score - negative_score)
                var_plus = float(positive_score + negative_score)
                polarity_score = (var_minus/var_plus) + 0.000001
                total_words = [tot for tot in filtered_tokens if tot not in string.punctuation]
                subjectivity_score = var_plus/(len(total_words) + 0.000001)
                total_sen = nltk.sent_tokenize(raw)
                avg_sen_len = len(total_words)/len(total_sen)
                comp_word = [word for word in total_words if syllable_count(word) >= 2]
                perc_comp_word = len(comp_word)/len(total_words)
                fog_index = 0.4 * (avg_sen_len + perc_comp_word)
                max_syllable = max([syllable_count(word) for word in total_words])
                personal_pron = count_personal_pronouns(raw)
                word_len = [len(word) for word in total_words]
                avg_word_len = sum(word_len)/len(total_words)
                article_file1 = article_file.split('.txt')[0]
                df.loc[df['URL_ID'] == article_file1, 'POSITIVE SCORE'] = positive_score
                df.loc[df['URL_ID'] == article_file1, 'NEGATIVE SCORE'] = negative_score
                df.loc[df['URL_ID'] == article_file1, 'POLARITY SCORE'] = polarity_score
                df.loc[df['URL_ID'] == article_file1, 'SUBJECTIVITY SCORE'] = subjectivity_score
                df.loc[df['URL_ID'] == article_file1, 'AVG SENTENCE LENGTH'] = avg_sen_len
                df.loc[df['URL_ID'] == article_file1, 'PERCENTAGE OF COMPLEX WORDS'] = perc_comp_word
                df.loc[df['URL_ID'] == article_file1, 'FOG INDEX'] = fog_index
                df.loc[df['URL_ID'] == article_file1, 'AVG NUMBER OF WORDS PER SENTENCE'] = avg_sen_len
                df.loc[df['URL_ID'] == article_file1, 'COMPLEX WORD COUNT'] = len(comp_word)
                df.loc[df['URL_ID'] == article_file1, 'WORD COUNT'] = len(total_words)
                df.loc[df['URL_ID'] == article_file1, 'SYLLABLES PER WORD'] = max_syllable
                df.loc[df['URL_ID'] == article_file1, 'PERSONAL PRONOUNS'] = personal_pron
                df.loc[df['URL_ID'] == article_file1, 'AVG WORD LENGTH'] = avg_word_len
                df.to_csv('csvfiles/output.csv', index=False)
                print('%s:  updated'%(article_file))
                print('-----------------------------------')
            except:
                article_file1 = article_file.split('.txt')[0]
                df.loc[df['URL_ID'] == article_file1, 'POSITIVE SCORE'] = 0
                df.loc[df['URL_ID'] == article_file1, 'NEGATIVE SCORE'] = 0
                df.loc[df['URL_ID'] == article_file1, 'POLARITY SCORE'] = 0
                df.loc[df['URL_ID'] == article_file1, 'SUBJECTIVITY SCORE'] = 0
                df.loc[df['URL_ID'] == article_file1, 'AVG SENTENCE LENGTH'] = 0
                df.loc[df['URL_ID'] == article_file1, 'PERCENTAGE OF COMPLEX WORDS'] = 0
                df.loc[df['URL_ID'] == article_file1, 'FOG INDEX'] = 0
                df.loc[df['URL_ID'] == article_file1, 'AVG NUMBER OF WORDS PER SENTENCE'] = 0
                df.loc[df['URL_ID'] == article_file1, 'COMPLEX WORD COUNT'] = 0
                df.loc[df['URL_ID'] == article_file1, 'WORD COUNT'] = 0
                df.loc[df['URL_ID'] == article_file1, 'SYLLABLES PER WORD'] = 0
                df.loc[df['URL_ID'] == article_file1, 'PERSONAL PRONOUNS'] = 0
                df.loc[df['URL_ID'] == article_file1, 'AVG WORD LENGTH'] = 0
                df.to_csv('csvfiles/output.csv', index=False)
                print('%s:  page not found'%(article_file))
                print('-----------------------------------')

article_Dir = "extracted_articles"
stop_words = read_stop_words("StopWords")
positive_words = read_positive_negative_words("MasterDictionary", "positive-words.txt")
negative_words = read_positive_negative_words("MasterDictionary", "negative-words.txt")
filer(article_Dir, stop_words, positive_words, negative_words)