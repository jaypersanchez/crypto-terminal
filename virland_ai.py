import json
import random
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import sys
import subprocess

# Try to install the package
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sentence-transformers'])

from sentence_transformers import SentenceTransformer

def load_and_embed_responses(filename, model):
    with open(filename, 'r', encoding='utf-8') as file:
        responses = json.load(file)
    
    embeddings = model.encode(responses, convert_to_tensor=True)
    return responses, embeddings

# Initialize the model
model_st = SentenceTransformer('all-MiniLM-L6-v2')

# Preprocess and embed the responses
responses, response_embeddings = load_and_embed_responses('data/cleaned_bitcoin_tweets.json', model_st)
def load_responses():
    with open('data/cleaned_bitcoin_tweets.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    
def load_keywords(filename='data/crypto_keywords.txt'):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip().lower() for line in file if line.strip()]

def setup_model():
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    return tokenizer, model

'''def generate_response(model, tokenizer, user_input, chat_history_ids, keywords, responses):
    relevant_keywords = [kw for kw in keywords if kw in user_input.lower()]
    if relevant_keywords:
        # If relevant keywords are found, select a related tweet
        related_responses = [resp for resp in responses if any(kw in resp.lower() for kw in relevant_keywords)]
        if related_responses:
            return random.choice(related_responses), chat_history_ids  # Use a related tweet directly

    # General model-based response if no direct tweet is applicable
    keyword_phrase = " ".join(relevant_keywords) if relevant_keywords else "cryptocurrency blockchain"
    prompt_text = f"This conversation will focus on {keyword_phrase}: " + user_input + tokenizer.eos_token
    new_input_ids = tokenizer.encode(prompt_text, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        top_k=50
    )

    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids'''
def find_semantic_response(user_input, responses, embeddings, model_st):
    input_embedding = model_st.encode(user_input, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(input_embedding, embeddings)
    
    # Find the index of the response with the highest cosine similarity
    best_idx = torch.argmax(similarities)
    return responses[best_idx]

def generate_response(user_input, chat_history_ids, responses, response_embeddings, model_st):
    if chat_history_ids is not None:
        # Concatenate user input to the ongoing chat history for context
        user_input = chat_history_ids + " " + user_input
    
    # Find the best semantic response
    response = find_semantic_response(user_input, responses, response_embeddings, model_st)
    chat_history_ids = (chat_history_ids + " " + response) if chat_history_ids else response
    
    return response, chat_history_ids

def main():
    print("Hello, I'm Virland, your crypto assistant. Ask me anything about crypto!")
    
    # Load responses and pre-computed embeddings
    responses, response_embeddings = load_and_embed_responses('data/cleaned_bitcoin_tweets.json', model_st)
    
    chat_history_ids = None  # This will store the context of the conversation

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Virland: Goodbye!")
            break
        
        response, chat_history_ids = generate_response(user_input, chat_history_ids, responses, response_embeddings, model_st)
        print(f"Virland: {response}")

if __name__ == "__main__":
    main()
