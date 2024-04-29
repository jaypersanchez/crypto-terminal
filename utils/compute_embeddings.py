import json
from sentence_transformers import SentenceTransformer
import torch
import psycopg2
import numpy as np
from dotenv import load_dotenv
import os
import sys
import time
import logging

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(filename='embedding_process.log', level=logging.INFO)
logging.info("Starting process...")

def test_database_connection(db_params):
    try:
        # Attempt to connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        # Perform a simple query (optional)
        cur.execute("SELECT 1")
        # Close the connection
        cur.close()
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"An error occurred while testing the database connection: {e}")
        return False
    
def compute_and_save_embeddings(source_file, db_params):
    
    if not test_database_connection(db_params):
        print("Failed to connect to the database. Please check your connection parameters.")
        return
    else:
        print(f"Connection success, proceeding with vector creation")
    
def compute_and_save_embeddings(source_file, db_params):
    if not test_database_connection(db_params):
        print("Failed to connect to the database. Please check your connection parameters.")
        return
    else:
        print("Connection success, proceeding with vector creation")
        
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
        
        # Prepare for batch processing
        total_responses = len(responses)
        BATCH_SIZE = 1000  # Define a suitable batch size
        start_time = time.time()

        # Process and insert data in batches
        for batch_start in range(0, total_responses, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, total_responses)
            batch = [(responses[i], embeddings[i].tolist()) for i in range(batch_start, batch_end)]
            cur.executemany("INSERT INTO virland_vector (tweet_text, embedding) VALUES (%s, %s)", batch)
            conn.commit()  # Commit after each batch

            # Update the status on the same line in the console
            elapsed_time = time.time() - start_time
            records_per_second = batch_end / elapsed_time if elapsed_time > 0 else 0
            eta = ((total_responses - batch_end) / records_per_second) if records_per_second > 0 else 0
            #sys.stdout.write(f"\rProcessed {batch_end} of {total_responses} - Speed: {records_per_second:.2f} records/s, ETA: {eta:.2f} s")
            logging.info(f"\rProcessed {batch_end} of {total_responses} - Speed: {records_per_second:.2f} records/s, ETA: {eta:.2f} s")
            sys.stdout.flush()
        
        cur.close()
        conn.close()
        print("\nEmbeddings saved successfully to the database.")
    
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        if 'conn' in locals():
            conn.rollback()

# Database parameters (modify these with your actual credentials)
db_params = {
    'dbname': os.getenv('DBNAME'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': 'localhost'
}


compute_and_save_embeddings('../data/cleaned_bitcoin_tweets.json', db_params)
