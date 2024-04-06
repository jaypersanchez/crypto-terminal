import tkinter as tk
from tkinter import scrolledtext, Toplevel, LabelFrame, Label, Button
from datetime import datetime
from modules.semantic_query_module import semantic_search  # Adjust the import path as necessary
from polygon_analytics.analyticsroutines.matic_current_price import get_current_price

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

# Function to open the popup window and display current prices
def show_current_prices():
    popup = Toplevel(root)
    popup.title("Current Prices")
    # Adjust the geometry for more space
    popup.geometry("400x250")  # Increased height to accommodate date

    # Make the popup modal
    popup.grab_set()

    try:
        # Assuming get_current_price returns a tuple (price, market_cap, volume)
        price, market_cap, volume = get_current_price()

        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Formatting the data for display
        info_text = f"${price} as of {current_date}\n" \
                    f"${market_cap}\n" \
                    f"${volume}"

        # Use a LabelFrame for a more structured layout
        info_frame = LabelFrame(popup, text="MATIC Information", font=('Helvetica', 12))
        info_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Display the formatted information in a label inside the frame
        info_label = Label(info_frame, text=info_text, font=('Helvetica', 12), justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)

    except Exception as e:
        # Error handling
        error_label = Label(popup, text="Failed to fetch current prices", font=('Helvetica', 12))
        error_label.pack(pady=20)
        print(f"Error: {e}")  # Log the error to console for debugging


    # Button to close the popup
    close_popup_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_popup_button.pack(pady=(0, 10))
    # This will block interaction with the main window until the popup is closed
    popup.wait_window()
    
# Set up the GUI
root = tk.Tk()
root.title("Virland Financials")
# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the size of the application window to be the entire screen
root.geometry(f"{screen_width}x{screen_height}")

# Query input
query_frame = tk.Frame(root)
query_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

tk.Label(query_frame, text="Ask Virland:").pack(side=tk.LEFT, padx=(0, 10))
query_entry = tk.Entry(query_frame, width=50)
query_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# Search button
search_button = tk.Button(query_frame, text="Ask", command=perform_search)
search_button.pack(side=tk.LEFT, padx=(10, 0))

# Close application button
close_button = tk.Button(root, text="Close", command=close_application)
close_button.pack(fill=tk.X, padx=10, pady=(5, 10))

# Add a "Current Prices" button to the main window
current_prices_button = tk.Button(root, text="Current Prices", command=show_current_prices)
current_prices_button.pack(fill=tk.X, padx=10, pady=(0, 5))

# Results display area
results_display = scrolledtext.ScrolledText(root)
results_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))





root.mainloop()
