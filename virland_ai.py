'''
This embedding process is for Virlan AI.  Update this constantly with new extracted data
to keep Virlan very knowledgeable about every Web3, Crypto and Blockchain.
'''
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from sentence_transformers import SentenceTransformer, util

def load_responses_and_embeddings():
    try:
        with open('data/cleaned_bitcoin_tweets.json', 'r', encoding='utf-8') as file:
            responses = json.load(file)
        model_st = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model_st.encode(responses, convert_to_tensor=True)
        return responses, embeddings
    except FileNotFoundError:
        print("File not found, please check the path to your data file.")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

def setup_model():
    try:
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        model = GPT2LMHeadModel.from_pretrained("gpt2")
        return tokenizer, model
    except Exception as e:
        print(f"Failed to load models: {e}")
        exit()

def find_semantic_response(user_input, responses, embeddings, model_st):
    input_embedding = model_st.encode(user_input, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(input_embedding, embeddings)
    best_idx = torch.argmax(similarities)
    return responses[best_idx]

def main():
    print("Hello, I'm Virland, your crypto assistant. Ask me anything about crypto!")
    
    # Load responses and pre-computed embeddings once when the program starts
    responses, response_embeddings = load_responses_and_embeddings()
    model_st = SentenceTransformer('all-MiniLM-L6-v2')

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Virland: Goodbye!")
            break
        
        response = find_semantic_response(user_input, responses, response_embeddings, model_st)
        print(f"Virland: {response}")

if __name__ == "__main__":
    main()
