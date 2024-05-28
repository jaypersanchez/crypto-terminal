1. Run datasets_update.py.  This will check all the HuggingFace tweet sources for any data.  
Not really needed but just for curiousity
2. Run tweets_headlines_dat_sources_json.py to extract tweets from HuggingFace sources
and update json file
3. Run process_tweets_data.py to clean the data and save in the cleaned_bitcoin_tweets.json file
4. Run training_data.py that will update the MongoDB tweets that is used for Semantic search and 
AI training.  (THIS IS STILL UNDER CONSTRUCTION)