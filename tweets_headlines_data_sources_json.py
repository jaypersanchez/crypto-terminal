'''
This routine extracts crypto news headlines and crypto related tweets
directly from Huggingface.  
'''
from datasets import load_dataset
import pandas as pd

# Load the datasets
crypto_tweets = load_dataset('juanberasategui/Crypto_Tweets')
crypto_news = load_dataset('LolorzoloL/crypto_news')
crypto_news_headlines = load_dataset('flowfree/crypto-news-headlines')

# Convert to Pandas DataFrames
df_crypto_tweets = crypto_tweets['train'].to_pandas()
df_crypto_news = crypto_news['train'].to_pandas()
df_crypto_news_headlines = crypto_news_headlines['train'].to_pandas()

# Combine the DataFrames
combined_df = pd.concat([df_crypto_tweets, df_crypto_news, df_crypto_news_headlines], ignore_index=True)

# Save to JSON
combined_df.to_json('data/combined_crypto_data.json', orient='records', lines=True)
