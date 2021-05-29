import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import collections


class TextCleaner:
    def __init__(self, to_clean):
        self.to_clean = to_clean
        self.settings = self.get_settings()
        self.lang_settings = {
            'english': {'active': True, 'words': set(stopwords.words('english'))},
            'french' : {'active': True, 'words': set(stopwords.words('french'))},
            'italian': {'active': True, 'words': set(stopwords.words('italian'))},
            'spanish': {'active': True, 'words': set(stopwords.words('spanish'))}}
        self.stopwords = self.create_stopwords()

    def get_settings(self):
        return {
            'remove_punctuation': {'active': True, 'action': self.remove_punctuation},
            'lower_case':         {'active': True, 'action': self.lowerize},
            'remove_stopword':    {'active': True, 'action': self.remove_stopwords},
            'stemming':           {'active': False, 'action': self.stemming},
            'too_long':           {'active': True, 'action': self.too_long}
        }

    def clean_text(self):
        tokens = self.tokenize(self.to_clean)

        for k, params in self.settings.items():

            if params['active']:
                tokens = params['action'](tokens)
            
        return tokens

    @staticmethod
    def tokenize(text):
        return word_tokenize(text)

    @staticmethod
    def remove_punctuation(tokens):
        future_tokens = []
        whitelist = string.ascii_letters + ' ' + "'" + 'éèàçùëê'
        for text in tokens:      
            try:
                future_tokens.append(''.join(character for character in text if character in whitelist))
            except TypeError as e:
                print(f'Error removing punctuation from token:\n{e}')
        return future_tokens

    @staticmethod
    def lowerize(tokens):
        return [w.lower() for w in tokens]

    def remove_stopwords(self, tokens):
        return [w for w in tokens if w not in self.stopwords]

    @staticmethod
    def stemming(tokens):
        porter = PorterStemmer()
        return [porter.stem(word) for word in tokens]

    @staticmethod
    def too_long(tokens):
        return [w for w in tokens if len(w) < 13]

    def create_stopwords(self):
        white_list = []
        black_list = ['moreshow', 'plus', 'team', 'work' 'experience', 'esperienza', 'conoscenza', 'clients', 'expérience', 'équipe', 'équipes', 'lavoro', 'business']

        stop_words = set(black_list)
        for v in self.lang_settings.values():
            if v['active']:
                stop_words = set.union(stop_words, v['words'])
        stop_words = [w for w in stop_words if w not in white_list]
        return stop_words

def token_freq(tokens):
    counter = collections.Counter(tokens)
    return counter.most_common(11)[1:]

def detect_lang(text):
    lang = {
        'english': {'count': 0, 'words': set(stopwords.words('english'))},
        'french' : {'count': 0, 'words': set(stopwords.words('french'))},
        'italian': {'count': 0, 'words': set(stopwords.words('italian'))},
        'spanish': {'count': 0, 'words': set(stopwords.words('spanish'))}}

    for k, v in lang.items():
        for w in v['words']:
            if w in text:
                v['count'] += 1
        # print(k, v['count'])
    detected_lang = sorted(lang, key=lambda x: lang[x]['count'], reverse=True)[0]
    return detected_lang

def lang_freq(text_list):
    lang_used = []
    for text in text_list:
        lang_used.append(detect_lang(text))
    return collections.Counter(lang_used)



if __name__ == '__main__':
    text_list = ["you gotta be proud of this result", 'hello darkness my old friend', 'boujour, tu veux du paté', 'perfetto facciamo cosi']
    print(lang_freq(text_list))
