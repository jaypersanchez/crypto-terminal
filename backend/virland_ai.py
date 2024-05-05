import json
import random
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def load_responses():
    with open('data/cleaned_bitcoin_tweets.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def setup_model():
    # Load pre-trained GPT-2 model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    return tokenizer, model

def generate_response(model, tokenizer, user_input):
    # Encode user input and add the EOS token
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Generate a response sequence
    chat_history_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

def main():
    print("Hello, I'm Virland, your crypto assistant. Ask me anything about crypto!")
    responses = load_responses()  # Load preprocessed tweets as potential responses
    tokenizer, model = setup_model()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Virland: Goodbye!")
            break
        
        # Use GPT-2 model to generate a response
        response = generate_response(model, tokenizer, user_input)
        print(f"Virland: {response}")

if __name__ == "__main__":
    main()
