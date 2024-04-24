import json
import re

def clean_tweet(tweet):
    tweet = re.sub(r"http\S+|www\S+|https\S+", "", tweet)  # Remove URLs
    tweet = re.sub(r"@\w+", "", tweet)  # Remove mentions
    tweet = re.sub(r"#\S+", "", tweet)  # Remove hashtags
    tweet = re.sub(r"\\u[\dA-Fa-f]+", "", tweet)  # Remove unicode characters
    tweet = re.sub(r"\n", " ", tweet)  # Replace new lines with space
    tweet = re.sub(r"[^\w\s]", "", tweet)  # Remove special characters
    return tweet.strip()

# Load the dataset
with open('../../data/bitcoin_tweets.json', 'r', encoding='utf-8') as file:
    tweets = json.load(file)

# Clean the tweets
cleaned_tweets = [clean_tweet(tweet) for tweet in tweets]

# Save the cleaned tweets to a new JSON file
with open('../../data/cleaned_bitcoin_tweets.json', 'w', encoding='utf-8') as file:
    json.dump(cleaned_tweets, file, indent=4)

print("Cleaned tweets have been saved to cleaned_bitcoin_tweets.json")
