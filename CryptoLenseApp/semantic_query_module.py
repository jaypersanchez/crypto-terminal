# Import necessary libraries at the beginning of your script
import psycopg2
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings
    
def semantic_search(query):
    # Your existing setup code...
    # Convert query to embedding
    query_embedding = get_embedding(query)
    
    # Convert the NumPy array to a Python list
    query_embedding_list = query_embedding.tolist()
    
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(dbname="semantic", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()
    
    # Prepare your SQL query. This example uses L2 norm for simplicity.
    sql = """
    SELECT id, instruction, input, output, vector,
    (SELECT sqrt(sum(power(vector[series.idx] - unnested.query_element, 2))) 
    FROM generate_series(1, array_length(vector, 1)) AS series(idx),
        unnest(%s::float[]) WITH ORDINALITY AS unnested(query_element, idx)
    WHERE series.idx = unnested.idx) AS distance
    FROM tweet_sentiments
    ORDER BY distance ASC
    LIMIT 5;
    """
    
    # Execute the query with the query vector
    cur.execute(sql, (query_embedding_list,))
    
    # Fetch results
    results = cur.fetchall()
    # Instead of printing results, store them in a list and return it
    fetched_results = []
    for row in results:
        #fetched_results.append(f"ID: {row[0]}, Instruction: {row[1]}, Input: {row[2]}, Output: {row[3]}, Distance: {row[5]}")
        fetched_results.append(f"Input: {row[2]}, Output: {row[3]}")
    # Return the list of results
    return fetched_results

# Now, semantic_search returns a list of strings representing the search results.
