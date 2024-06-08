import customtkinter as ctk
import tkinter as tk

def send_message():
    message = user_input.get()
    chat_history.config(state=tk.NORMAL)  # Enable editing
    chat_history.insert(tk.END, f"You: {message}\n")
    chat_history.insert(tk.END, f"Chatbot: {message[::-1]}\n")
    chat_history.config(state=tk.DISABLED)  # Disable editing
    user_input.delete(0, tk.END)

# Create the main application window
app = ctk.CTk()

# Set window title and size
app.title("CustomTkinter Chatbot")
app.geometry("400x400")

# Change background color of the app
app.config(bg="lightgrey")

# Create a frame for the chat history with a custom border
chat_frame = ctk.CTkFrame(app, bd=2, relief=tk.SUNKEN)  # Add border and relief
chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Add padding

# Create a text widget to display the chat history with custom font and colors
chat_history = tk.CTkTextbox(chat_frame, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 10))  # Change font and colors
chat_history.pack(fill=tk.BOTH, expand=True)

# Create a scrollbar for the chat history with custom colors
scrollbar = ctk.CTkScrollbar(chat_frame, bg="lightgrey", troughcolor="grey", activebackground="darkgrey")  # Change scrollbar colors
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the scrollbar to the chat history
chat_history.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=chat_history.yview)

# Create a frame for user input with a custom border
input_frame = ctk.CTkFrame(app, bd=2, relief=tk.GROOVE)  # Add border and relief
input_frame.pack(fill=tk.X, padx=5, pady=5)  # Add padding

# Create an entry widget for user input with custom font and colors
user_input = ctk.CTkEntry(input_frame, bg="white", fg="black", font=("Arial", 10))  # Change font and colors
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Create a button to send the message with custom colors and font
send_button = ctk.CTkButton(input_frame, text="Send", command=send_message, bg="lightblue", fg="black", font=("Arial", 10, "bold"))  # Change button colors and font
send_button.pack(side=tk.RIGHT)

# Bind the Enter key to send the message
app.bind("<Return>", lambda event: send_message())

# Run the application
app.mainloop()
