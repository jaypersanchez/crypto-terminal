import tkinter as tk
from tkinter import scrolledtext
from semantic_query_module import semantic_search  # Adjust the import path as necessary

# Function to handle search
def perform_search():
    user_query = query_entry.get()
    results = semantic_search(user_query)
    # Clear the existing results
    results_display.delete(1.0, tk.END)
    # Display new results
    for result in results:
        results_display.insert(tk.END, result + "\n\n")

# Set up the GUI
root = tk.Tk()
root.title("Semantic Search")

# Query input
tk.Label(root, text="Enter your query:").pack(pady=(10, 0))
query_entry = tk.Entry(root, width=50)
query_entry.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Search", command=perform_search)
search_button.pack(pady=(5, 10))

# Results display area
results_display = scrolledtext.ScrolledText(root, width=60, height=10)
results_display.pack(pady=(0, 10))

root.mainloop()
