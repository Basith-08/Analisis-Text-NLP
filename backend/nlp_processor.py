import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import emoji
import string

class NLPProcessor:
    def __init__(self):
        """Initialize NLP Processor with required resources"""
        self._download_nltk_resources()

        # Indonesian stopwords
        try:
            self.stopwords_id = set(stopwords.words('indonesian'))
        except:
            self.stopwords_id = set()

        # Add custom Indonesian stopwords
        custom_stopwords = {
            'yang', 'dan', 'di', 'dari', 'ke', 'untuk', 'pada', 'dengan',
            'ini', 'itu', 'akan', 'adalah', 'atau', 'oleh', 'dalam', 'juga',
            'sih', 'nih', 'dong', 'deh', 'yah', 'lah', 'kah', 'banget', 'bgt',
            'gw', 'gue', 'lu', 'lo', 'aku', 'kamu', 'dia', 'mereka', 'kita',
            'nya', 'ku', 'mu', 'kak', 'ka', 'yg', 'dgn', 'utk', 'pd', 'tdk',
            'tapi', 'tp', 'ga', 'gak', 'ngga', 'nggak', 'udah', 'sudah',
            'aja', 'saja', 'sich', 'kok', 'wkwk', 'wkwkwk', 'haha', 'hehe',
            'hihi', 'huhu', 'the', 'a', 'an', 'of', 'to', 'in', 'for', 'on'
        }
        self.stopwords_id.update(custom_stopwords)

        # Initialize Sastrawi Stemmer for Indonesian
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()

    def _download_nltk_resources(self):
        """Download required NLTK resources"""
        resources = ['punkt', 'stopwords', 'punkt_tab']
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
            except LookupError:
                try:
                    nltk.download(resource, quiet=True)
                except:
                    pass

    def remove_emoji(self, text):
        """Remove emojis from text"""
        return emoji.replace_emoji(text, replace='')

    def clean_text(self, text):
        """Clean text by removing special characters, numbers, etc."""
        # Convert to lowercase
        text = text.lower()

        # Remove emojis
        text = self.remove_emoji(text)

        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)

        # Remove numbers
        text = re.sub(r'\d+', '', text)

        # Remove punctuation and special characters
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Remove extra whitespace
        text = ' '.join(text.split())

        return text.strip()

    def tokenize(self, text):
        """Tokenize text into words"""
        try:
            tokens = word_tokenize(text)
            return tokens
        except:
            # Fallback to simple split if tokenizer fails
            return text.split()

    def remove_stopwords(self, tokens):
        """Remove stopwords from tokens"""
        filtered_tokens = [token for token in tokens if token.lower() not in self.stopwords_id and len(token) > 2]
        return filtered_tokens

    def stem_tokens(self, tokens):
        """Apply stemming to tokens (optional)"""
        stemmed = [self.stemmer.stem(token) for token in tokens]
        return stemmed

    def preprocess(self, text, apply_stemming=False):
        """
        Complete preprocessing pipeline

        Args:
            text (str): Input text to preprocess
            apply_stemming (bool): Whether to apply stemming

        Returns:
            dict: Dictionary containing preprocessing results
        """
        # Step 1: Clean text
        cleaned = self.clean_text(text)

        # Step 2: Tokenize
        tokens = self.tokenize(cleaned)

        # Step 3: Remove stopwords
        filtered_tokens = self.remove_stopwords(tokens)

        # Step 4: Optional stemming
        if apply_stemming:
            filtered_tokens = self.stem_tokens(filtered_tokens)

        return {
            'original': text,
            'cleaned': cleaned,
            'tokens': tokens,
            'filtered_tokens': filtered_tokens
        }

# Test the processor
if __name__ == '__main__':
    processor = NLPProcessor()

    # Test text
    test_text = "Semoga tahun ini lulus UI aamiin 🤲 love it! ❤️"

    result = processor.preprocess(test_text)

    print("Original:", result['original'])
    print("Cleaned:", result['cleaned'])
    print("Tokens:", result['tokens'])
    print("Filtered:", result['filtered_tokens'])
