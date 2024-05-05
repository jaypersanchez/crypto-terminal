# Creating a vector database for semantic search involves several steps, including setting up PostgreSQL with vector extension (if you plan to use vector search capabilities), processing your text data to create embeddings, and then inserting these embeddings into PostgreSQL. Below is a step-by-step guide including Python code. Note that this guide assumes you're using PostgreSQL 12 or later with the pgvector extension for vector search, which you might need to install separately.

## Install Required Libraries
`
pip install psycopg2-binary transformers torch
`
## Setup PostgreSQL with pgvector

1. Install PostgreSQL and pgvector. Check pgvector's documentation for specific instructions on adding it to your PostgreSQL setup.

2. Create a database and enable pgvector extension:

`
CREATE DATABASE mydatabase;
\c mydatabase;
CREATE EXTENSION pgvector;
`

3. Create a table to store your text and its vector representation:
`
CREATE TABLE text_embeddings (
    id SERIAL PRIMARY KEY,
    text TEXT,
    scam BOOLEAN,
    embedding VECTOR(768) -- Assuming using BERT which generates 768-dimensional vectors
);
`

4. Prepare Text Data and Generate Embeddings
Using Python, process your text data to create embeddings. This example uses BERT from the Hugging Face transformers library.
`from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd
import psycopg2

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings.tolist()

# Load your data
df = pd.read_json('./data/cleaned_crypto_data.json', lines=True)

# Generate embeddings
df['embedding'] = df['Cleaned_Text'].apply(get_embedding)
`
5. Insert Data into PostgreSQL
`# Connect to your PostgreSQL database
conn = psycopg2.connect(dbname='mydatabase', user='username', password='password')
cur = conn.cursor()

# Insert data
for index, row in df.iterrows():
    text = row['Cleaned_Text']
    scam = row['Scam']
    embedding = row['embedding']
    cur.execute("INSERT INTO text_embeddings (text, scam, embedding) VALUES (%s, %s, %s)", (text, scam, embedding))

conn.commit()
cur.close()
conn.close()
`

6. Querying the Database for Semantic Search
You can now query your database for similar texts based on vector similarity. pgvector supports various distance metrics like L2 or cosine similarity.
`SELECT text FROM text_embeddings
ORDER BY embedding <-> vector(your_query_vector)
LIMIT 10;
`

