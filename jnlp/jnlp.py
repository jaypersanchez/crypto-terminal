from textblob import TextBlob
from googletrans import Translator

text = "TextBlob is amazingly simple to use. What great fun!"
blob = TextBlob(text)

# Sentiment Analysis
print(blob.sentiment)
# Tokenization
print(blob.words)
print(blob.sentences)

# Part of speech tagging
print(blob.tags)

# Noun phrase extraction
print(blob.noun_phrases)

# Word Inflection and Lemmatization
print(blob.words[2].singularize())
print(blob.words[2].pluralize())

# Lemmatization
from textblob import Word
w = Word("running")
print(w.lemmatize("v"))  # Pass part of speech (verb)

# WordNet Integration
from textblob import Word
word = Word("platform")
print(word.definitions)

# Spelling correction
blob = TextBlob("I havv goood speling!")
print(blob.correct())

# Translation and Language Detection
translator = Translator()

# Detecting language
detection = translator.detect('Bonjour')
print(detection.lang)

# Translating text
translation = translator.translate('Bonjour', dest='en')
print(translation.text)
