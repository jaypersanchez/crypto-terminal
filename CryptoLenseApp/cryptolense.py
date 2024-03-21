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

# Function to close the application
def close_application():
    root.destroy()

# Set up the GUI
root = tk.Tk()
root.title("Semantic Search")
root.geometry("800x600")  # Adjust the size of the application window as needed

# Query input
query_frame = tk.Frame(root)
query_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

tk.Label(query_frame, text="Enter your query:").pack(side=tk.LEFT, padx=(0, 10))
query_entry = tk.Entry(query_frame, width=50)
query_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# Search button
search_button = tk.Button(query_frame, text="Search", command=perform_search)
search_button.pack(side=tk.LEFT, padx=(10, 0))

# Close application button
close_button = tk.Button(root, text="Close", command=close_application)
close_button.pack(fill=tk.X, padx=10, pady=(5, 10))

# Results display area
results_display = scrolledtext.ScrolledText(root)
results_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))

root.mainloop()
