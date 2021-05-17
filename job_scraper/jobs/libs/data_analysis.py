import nltk
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer





class TextCleaner:
    def __init__(self, to_clean):
        self.stopwords = self.create_stopwords()
        self.to_clean = to_clean
        self.settings = self.get_settings()

    def get_settings(self):
        return {
            'remove_punctuation': {'activated': True,  'action': self.remove_punctuation},
            'lower_case':         {'activated': True,  'action': self.lowerize},
            'remove_stopword':    {'activated': True,  'action': self.remove_stopwords},
            'stemming':           {'activated': False, 'action': self.stemming}
        }

    def clean_text(self):
        tokens = self.tokenize(self.to_clean)

        for k, params in self.settings.items():

            if params['activated']:
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
    def create_stopwords():
        white_list = []
        lang_settings = {
            'english': {'active': True, 'words': set(stopwords.words('english'))},
            'french': {'active': True, 'words': set(stopwords.words('french'))},
            'italian': {'active': True, 'words': set(stopwords.words('italian'))},
            'spanish': {'active': True, 'words': set(stopwords.words('spanish'))}
        }
        stop_words = set()
        for v in lang_settings.values():
            if v['active']:
                stop_words = set.union(stop_words, v['words'])
        stop_words = [w for w in stop_words if w not in white_list]
        return stop_words

# https://stackoverflow.com/questions/2161752/how-to-count-the-frequency-of-the-elements-in-an-unordered-list

if __name__ == '__main__':
    TextCleaner('lol').create_stopwords()