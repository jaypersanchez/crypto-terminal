import json
import random
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

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

def generate_response(model, tokenizer, user_input, chat_history_ids, keywords, responses):
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
    return response, chat_history_ids

def main():
    print("Hello, I'm Virland, your crypto assistant. Ask me anything about crypto!")
    responses = load_responses()  # Load preprocessed tweets as potential responses
    keywords = load_keywords()  # Load the list of crypto keywords
    tokenizer, model = setup_model()

    chat_history_ids = None  # Initialize chat history

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Virland: Goodbye!")
            break

        response, chat_history_ids = generate_response(model, tokenizer, user_input, chat_history_ids, keywords, responses)
        print(f"Virland: {response}")

if __name__ == "__main__":
    main()
