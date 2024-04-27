import json
from sentence_transformers import SentenceTransformer
import torch
import psycopg2
import numpy as np
from dotenv import load_dotenv
import os
import sys 

# Load environment variables from .env file
load_dotenv()

def compute_and_save_embeddings(source_file, db_params):
    try:
        # Open the source file and load tweets
        with open(source_file, 'r', encoding='utf-8') as file:
            responses = json.load(file)
        
        # Initialize the Sentence Transformer model
        model_st = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model_st.encode(responses, convert_to_tensor=False)  # Convert to numpy array directly
        
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        # Insert each tweet and its corresponding embedding into the database
        total_responses = len(responses)
        # Insert each tweet and its corresponding embedding into the database
        for index, (response, embedding) in enumerate(zip(responses, embeddings), 1):
            # Ensure the embedding is in a format suitable for double precision array
            embedding_list = embedding.tolist()  # Convert numpy array to Python list
            cur.execute(
                "INSERT INTO tweet_embeddings (tweet, embedding) VALUES (%s, %s)",
                (response, embedding_list)
            )
            
            # Update the status on the same line in the console
            sys.stdout.write(f"\rProcessing {index} of {total_responses}...")
            sys.stdout.flush()
        
        # Commit the transaction and close the connection
        conn.commit()
        cur.close()
        conn.close()
        print("Embeddings saved successfully to the database.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()

# Database parameters (modify these with your actual credentials)
db_params = {
    'dbname': os.getenv('DBNAME'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': 'localhost'
}

compute_and_save_embeddings('../data/cleaned_bitcoin_tweets.json', db_params)
