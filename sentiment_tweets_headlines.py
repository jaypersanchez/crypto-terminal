import pandas as pd
from io import StringIO
import sys

# Initialize an empty list to store each line's data
data = []

# Open the file and read line by line
with open('data/cleaned_crypto_data.json', 'r') as file:
    for i, line in enumerate(file):
        if i % 100 == 0:
            # Print a status message every 100 lines
            sys.stdout.write(f"\rProcessing line {i}...")
            sys.stdout.flush()
        
        # Wrap the line string in a StringIO object
        sio = StringIO(line)
        data.append(pd.read_json(sio, lines=True))
print("\nFinished processing.")
# Concatenate all the data into a single DataFrame
df = pd.concat(data, ignore_index=True)
print(df.head())

