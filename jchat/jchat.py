import openai

openai.api_key="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"

def get_response(prompt_text):
    response = openai.Completion.create(
      engine="gpt-3.5-turbo-0125",  # Choose the model
      prompt=prompt_text,
      temperature=0.7,
      max_tokens=150,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["\n", " Human:", " AI:"]
    )
    return response.choices[0].text.strip()

# Loop so user can start chatting with JChat
print("Chat with the bot! Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    response = get_response(f"Human: {user_input}\nAI:")
    print("AI:", response)

