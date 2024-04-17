import pandas as pd
from sklearn.preprocessing import StandardScaler
import nltk
import re
from langdetect import detect
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

# Check if the 'stopwords' dataset is already downloaded, if not download it
if not nltk.corpus.stopwords.words('english'):
    nltk.download('stopwords')

# Check if the 'punkt' tokenizer models are downloaded, if not download them
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


# Try to load the Spanish model, download if not found
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("Downloading the spaCy Spanish model...")
    spacy.cli.download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")



nlp = spacy.load("es_core_news_sm")
spanish_stopwords = stopwords.words('spanish')

def detect_languages(text):
    try:
        return detect(text)
    except:
        return None

def remove_non_ascii_except_accents(text):
    allowed_accents = 'áéíóúñ'
    pattern = f"[^{re.escape(allowed_accents)}\\w\\s]"
    return re.sub(pattern, '', text)

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word not in spanish_stopwords]
    return ' '.join(filtered_words)

def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])

def preprocess_data(df):
    # # Detect language and filter Spanish texts
    # df['language'] = df.apply(detect_languages)
    # df = df[df['language'] == 'es']
    # df.drop('language', axis=1, inplace=True)
    # print("x")
    # Text preprocessing steps
    df = df.apply(remove_non_ascii_except_accents)
    df = df.str.lower()
    df = df.apply(remove_punctuation)
    df = df.apply(remove_stopwords)
    df = df.apply(lemmatize_text)
    print(df)

    return df
