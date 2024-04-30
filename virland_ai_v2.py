'''
This embedding process is for Virlan AI.  Update this constantly with new extracted data
to keep Virlan very knowledgeable about every Web3, Crypto and Blockchain.
'''
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from sentence_transformers import SentenceTransformer, util
import requests
import nltk
from nltk.corpus import wordnet as wn

def intent_forecasting(user_input, detail=None):
    # Implementation
    return "Forecasting response based on: " + str(detail)

def intent_sentiment(user_input, detail=None):
    # Implementation
    return "Sentiment analysis response."

# Ensure all other intent functions follow the same pattern:
def intent_investment_advice(user_input, detail=None):
    # Implementation
    return "Investment advice response."

def intent_portfolio_management(user_input, detail=None):
    # Implementation
    return "Portfolio management response."

def intent_technical_analysis(user_input, detail=None):
    # Implementation
    return "Technical analysis response."

def intent_transaction_queries(user_input, detail=None):
    # Implementation
    return "Transaction queries response."

def intent_economic_impact(user_input, detail=None):
    # Implementation
    return "Economic impact response."

def intent_education_questions(user_input, detail=None):
    # Implementation
    return "Education questions response."

def intent_news_updates(user_input, detail=None):
    # Implementation
    return "News and updates response."

def intent_compliance_legal(user_input, detail=None):
    # Implementation
    return "Compliance and legal issues response."

def intent_general(user_input, detail=None):
    # Implementation
    return "General inquiry response."

def intent_market_trends(user_input, detail=None):
    # Implementation
    return "Market Trend"    

# Mapping of intents to functions
intent_function_mapping = {
    "forecast": intent_forecasting,
    "sentiment": intent_sentiment,
    "investment_advice": intent_investment_advice,
    "portfolio_management": intent_portfolio_management,
    "technical_analysis": intent_technical_analysis,
    "transaction_queries": intent_transaction_queries,
    "economic_impact": intent_economic_impact,
    "education_questions": intent_education_questions,
    "news_updates": intent_news_updates,
    "compliance_legal": intent_compliance_legal,
    "general": intent_general,
    "market_trends_and_forecasts": intent_market_trends
}

def dispatch_intent(user_input, intent_keywords):
    intent, detail = determine_intent(user_input, intent_keywords)
    print(f"dispatch_intent {intent, detail}")
    # Get the appropriate function from the mapping
    function_to_call = intent_function_mapping.get(
        intent, 
        lambda user_input, detail=None: "I'm not sure how to respond to that. Can you ask something else?"
    )

    # Call the function and pass the user input and any necessary details
    return function_to_call(user_input, detail)
    
def determine_intent(user_input, intent_keywords):
    user_input_lower = user_input.lower()
    detected_categories = set()

    words = user_input_lower.split()
    for i in range(len(words) - 1):
        bi_gram = ' '.join(words[i:i+2])
        if bi_gram in intent_keywords:
            detected_categories.update(intent_keywords[bi_gram])

    for word in words:
        if word in intent_keywords:
            detected_categories.update(intent_keywords[word])

    print("Detected Categories:", detected_categories)  # Debug output

    for priority_category in [
        "Market Trends and Forecasts", "Sentiment Analysis", "Investment Advice and Decisions",
        "Portfolio Management", "Technical Analysis", "Transaction and Trading Queries",
        "Economic Impact and Analysis", "Educational Questions", "News and Updates",
        "Compliance and Legal"
    ]:
        if priority_category in detected_categories:
            return priority_category.lower().replace(" ", "_"), None
    return "general", None
   
def main():
    global intent_keywords
    intent_keywords = load_intent_keywords('data/financial_intent_prompts.json')   
    print("Hello, I'm Virland, your crypto assistant. Ask me anything about crypto!")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Virland: Goodbye!")
            break

        # Dispatch query based on intent
        response = dispatch_intent(user_input, intent_keywords)
        print(f"Virland: {response}")

def download_nltk_resources():
    try:
        # Try to find the WordNet data
        nltk.data.find('corpora/wordnet')
    except LookupError:
        # If not found, download it
        nltk.download('wordnet')
import json

def load_intent_keywords(json_file_path):
    with open(json_file_path, 'r') as file:
        categories = json.load(file)
    intent_keywords = {}
    for category, questions in categories.items():
        for question in questions:
            words = question.lower().split()
            for i in range(len(words) - 1):
                phrase = ' '.join(words[i:i+2])
                intent_keywords.setdefault(phrase, set()).add(category)
            for word in words:
                intent_keywords.setdefault(word, set()).add(category)
    return intent_keywords

        
if __name__ == "__main__":
    download_nltk_resources()
    # Pass globally
    main()
