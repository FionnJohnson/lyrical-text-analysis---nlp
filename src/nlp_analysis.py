import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re


stop_words = set(stopwords.words('english'))
analyzer = SentimentIntensityAnalyzer()

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


# Joins song lyrics into one big string
def join_lyrics(album_series):
    album_lyrics = []

    for song in album_series:
        album_lyrics.append(song)

    album_lyrics = " ".join(album_lyrics)
    return album_lyrics


# Joins song lyrics into one big string then performs tokenization, returning a list
def tokenize(album_series):
    album_lyrics = []

    for song in album_series:
        album_lyrics.append(song)

    album_lyrics = " ".join(album_lyrics)
    tokens = word_tokenize(album_lyrics.lower())
    return tokens


# Stop word removal, filters out stopwords from the corpus module and custom word list,
# also removes words that are less than 3 letters and contain any numbers.
def stop_word_rem(tokens):
    custom_stopwords = ('like na see wan yet one know oh ooh get gon hey way '
                        'time yeah thing comin look something nothing tell').split()

    filtered_tokens = [word for word in tokens if
                       word not in stop_words and
                       word not in custom_stopwords and
                       len(word) > 2 and
                       word.isalpha()]      # isalpha() checks if the characters are from a-z
    return filtered_tokens


# Returns the top nouns from the list of lemmatized tokens
def top_nouns(lemmatized_tokens):
    pos_tags = nltk.pos_tag(lemmatized_tokens)
    interesting_words = [word for word, tag in pos_tags if tag.startswith('NN')]
    return Counter(interesting_words).most_common(12)


# Calculates and returns the sentiment score from a text
def get_sentiment(text):
    score = analyzer.polarity_scores(text)
    sentiment = score['compound']
    return sentiment

# Calculates vocabulary richness using the first 500 words from each album
def type_token_ratio(lyrics):
    filtered_lyrics = []
    for word in lyrics:
        cleaned_word = re.sub(r'[^a-zA-Z]', '', word).lower()
        if cleaned_word != "":
            filtered_lyrics.append(cleaned_word)

    sample_size = 500
    lyric_sample = filtered_lyrics[:sample_size]
    lemmatized_sample = [lemmatizer.lemmatize(word) for word in lyric_sample]
    unique_words = set(lemmatized_sample)

    return len(unique_words) / sample_size