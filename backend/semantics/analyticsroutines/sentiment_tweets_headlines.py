'''
This sentiment analysis loads partial data for the purpose of illustration of sentiment analysis.
Uses Matplotlib for visual illustration
'''
import pandas as pd
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt

# Function to calculate sentiment
def calculate_sentiment(text):
    try:
        return TextBlob(text).sentiment.polarity
    except:
        return None

# Initialize an empty list to store data
data = []

# Open the file and read line by line
with open('./data/cleaned_crypto_data.json', 'r') as file:
    for i, line in enumerate(file):
        if i >= 1000:  # Stop after reading 1000 lines
            break
        # Convert line into dictionary and append to the list
        try:
            data_dict = eval(line)  # Consider using json.loads(line) for JSON strings
            data.append(data_dict)
        except:
            continue  # Skip lines that can't be converted

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)

# Clean the 'Cleaned_Text' column to ensure it's a string
df['Cleaned_Text'] = df['Cleaned_Text'].astype(str)

# Apply the sentiment analysis
df['Sentiment'] = df['Cleaned_Text'].apply(calculate_sentiment)

# Drop rows with None sentiment
df.dropna(subset=['Sentiment'], inplace=True)

# Calculate and print the average sentiment
average_sentiment = df['Sentiment'].mean()
print(f"Average Sentiment Polarity: {average_sentiment:.2f}")

# Optionally, explore the distribution of sentiments
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.hist(df['Sentiment'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Sentiment Polarity')
plt.xlabel('Sentiment Polarity')
plt.ylabel('Count')
plt.show()
