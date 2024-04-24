import pandas as pd
import numpy as np
import re

# Assuming combined_crypto_data.json is your combined file
df = pd.read_json('data/combined_crypto_data.json', lines=True)

# Step 1: Consolidate Text Fields
df['Consolidated_Text'] = df['Text'].combine_first(df['text'])

# Step 2: Remove Nulls and Duplicates
df = df[df['Consolidated_Text'].notnull()].drop_duplicates(subset='Consolidated_Text')

# Step 3: Drop the 'Scam' label if not needed
# If you decide to keep it, ensure it's a binary integer column:
# df['Scam'] = df['Scam'].apply(lambda x: 1 if x == 1.0 else 0)
#df.drop(columns=['Scam', 'text', 'label'], inplace=True)
# Will keep the Scam label.  Since this may have an impact of general public sentiment
df.drop(columns=['text', 'label'], inplace=True)

# Step 4: Text Cleanup
def clean_text(text):
    """Basic text cleaning"""
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Remove special characters and numbers
    text = re.sub(r'[^A-Za-z\s]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove emojis by filtering out characters that fall outside the ASCII range
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove Reddit community references and slashes
    text = re.sub(r'\/r\/[^\s]+', '', text)  # Assuming the pattern is consistent
    # Optional: Remove any other specific patterns you've identified
    # e.g., removing backslashes which could be left from escaping characters
    text = text.replace('\\', '')
    return text

df['Cleaned_Text'] = df['Consolidated_Text'].apply(clean_text)

# Now your data is ready for sentiment analysis
print(df.head())

# Optionally save the cleaned data to a new JSON file for sentiment analysis
df.to_json('data/cleaned_crypto_data.json', orient='records', lines=True)
