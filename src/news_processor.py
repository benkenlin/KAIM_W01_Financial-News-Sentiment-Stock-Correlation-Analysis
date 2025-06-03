import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from collections import Counter

# Ensure NLTK data is downloaded (run this once in your environment or a notebook)
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('vader_lexicon') # If you use VADER instead of TextBlob

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def load_financial_news_data(filepath='../data/processed/daily_aggregated_sentiment.csv'):
    """Loads the main financial news dataset."""
    try:
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'], utc=True)
        df['publication_day'] = df['date'].dt.normalize() # For daily aggregation
        print(f"Loaded financial news data from {filepath}")
        return df
    except FileNotFoundError:
        print(f"Error: News data file not found at {filepath}")
        return pd.DataFrame()

def preprocess_text(text):
    """Cleans and preprocesses text for analysis."""
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text) # Remove non-alphabetic chars
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2]
    return ' '.join(tokens)

def add_sentiment_score(df, text_col='headline', processed_text_col='processed_headline'):
    """Adds sentiment polarity score using TextBlob."""
    if processed_text_col not in df.columns:
        df[processed_text_col] = df[text_col].apply(preprocess_text)
    df['daily_avg_sentiment'] = df[processed_text_col].apply(lambda x: TextBlob(x).sentiment.polarity)
    return df

def get_common_keywords(df, text_col='processed_headline', top_n=50, n_gram=1):
    """Identifies common keywords (single words or n-grams)."""
    all_words = ' '.join(df[text_col].dropna()).split()
    if n_gram == 1:
        return Counter(all_words).most_common(top_n)
    elif n_gram > 1:
        from nltk.util import ngrams
        n_grams = ngrams(all_words, n_gram)
        return Counter(n_grams).most_common(top_n)
    return []

if __name__ == '__main__':
    print("Testing news_processor.py:")
    # Create a dummy news DataFrame for testing
    dummy_news_data = {
        'headline': [
            "Apple's strong earnings boost stock.",
            "Tesla new factory plans, shares jump.",
            "Google AI breakthrough rallies shares.",
            "Meta faces antitrust probe, stock drops.",
            "Apple Vision Pro launch sparks mixed reactions.",
            "Tesla recalls vehicles, shares fall."
        ],
        'url': ['url1','url2','url3','url4','url5','url6'],
        'publisher': ['Reuters','Bloomberg','Reuters','WSJ','CNBC','Bloomberg'],
        'date': [
            '2023-01-10 10:00:00-04:00', '2023-01-10 11:30:00-04:00',
            '2023-01-11 09:00:00-04:00', '2023-01-11 14:00:00-04:00',
            '2023-01-12 10:15:00-04:00', '2023-01-12 12:45:00-04:00'
        ],
        'stock': ['AAPL','TSLA','GOOG','META','AAPL','TSLA']
    }
    dummy_df_news = pd.DataFrame(dummy_news_data)
    dummy_df_news['date'] = pd.to_datetime(dummy_df_news['date'], utc=True)
    dummy_df_news['publication_day'] = dummy_df_news['date'].dt.normalize()

    processed_df_news = add_sentiment_score(dummy_df_news)
    print("\nProcessed News Data Head with Sentiment:")
    print(processed_df_news.head())

    print("\nTop 5 Common Words:")
    print(get_common_keywords(processed_df_news, top_n=5))

    print("\nTop 5 Common Bigrams:")
    print(get_common_keywords(processed_df_news, top_n=5, n_gram=2))