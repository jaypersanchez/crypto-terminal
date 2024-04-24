import json
import re

def clean_tweet(tweet):

   # Determine the tweet text based on the input type
    if isinstance(tweet, dict):
        tweet_text = tweet.get('Text', '')  # Fetches 'Text' or defaults to an empty string
        if tweet_text is None:  # Debugging line to check if None is somehow passed
            print("Unexpected None for 'Text' key, setting to empty string.")
            tweet_text = ''
    elif isinstance(tweet, str):
        tweet_text = tweet
    else:
        print(f"Unsupported tweet type: {type(tweet)}")  # Prints the type if it's neither dict nor str
        return None  # Return None if the content is not in expected format
    
    # Now apply cleaning operations on tweet_text, which should be a string
    if tweet_text is not None:
        tweet_text = re.sub(r"http\S+|www\S+|https\S+", "", tweet_text)  # Remove URLs
        tweet_text = re.sub(r"@\w+", "", tweet_text)  # Remove mentions
        tweet_text = re.sub(r"#\S+", "", tweet_text)  # Remove hashtags
        tweet_text = re.sub(r"\\u[\dA-Fa-f]+", "", tweet_text)  # Remove unicode characters
        tweet_text = re.sub(r"\n", " ", tweet_text)  # Replace new lines with space
        tweet_text = re.sub(r"[^\w\s]", "", tweet_text)  # Remove special characters
        return tweet_text.strip()

# Load the dataset
tweets = []
with open('../../data/combined_crypto_data.json', 'r', encoding='utf-8') as file:
    for line in file:
        try:
            # Each line contains one JSON object
            tweet = json.loads(line)
            tweets.append(tweet)
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {line[:100]}")  # Truncated to avoid too long printouts

# Clean the tweets
cleaned_tweets = [clean_tweet(tweet) for tweet in tweets if tweet is not None]
cleaned_tweets = [tweet for tweet in cleaned_tweets if tweet]  # Filter out empty results

# Save the cleaned tweets to a new JSON file
if cleaned_tweets:
    with open('../../data/cleaned_bitcoin_tweets.json', 'w', encoding='utf-8') as file:
        json.dump(cleaned_tweets, file, indent=4)
    print(f"Cleaned tweets have been saved to cleaned_bitcoin_tweets.json. Total: {len(cleaned_tweets)}")
else:
    print("No tweets were cleaned or all cleaned tweets were empty.")
