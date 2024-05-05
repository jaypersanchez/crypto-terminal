from datasets import load_dataset
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_dataset_updates(dataset_names):
    access_token = os.getenv('HUGGING_FACE_ACCESS_TOKEN')
    if not access_token:
        raise ValueError("HUGGING_FACE_ACCESS_TOKEN is not set in the environment variables")

    updates = {}
    for name in dataset_names:
        dataset = load_dataset(name, token=access_token)  # use_auth_token might be required for private datasets or rate limits
        #current_version = dataset.version
        print(dataset)
        # Here you would compare with previously stored version info
        updates[name] = "Check manually for version or changes" #current_version
    return updates

dataset_names = [
    'juanberasategui/Crypto_Tweets', 'LolorzoloL/crypto_news',
    'flowfree/crypto-news-headlines', 'mkly/crypto-sales-question-answers',
    'Aleereza/crypto-dataset', 'StephanAkkerman/crypto-charts',
    'Myashka/CryptoNews', 'Myashka/CryptoNews_50_50'
]

# Run the check
updates = check_dataset_updates(dataset_names)
print(updates)
