from customtkinter import *
from tkinter import filedialog
import google.generativeai as genai
import google.api_core.exceptions  # Import error handling for Google API
import requests
import PyPDF2
from PIL import Image
from dotenv import load_dotenv
import os


# ========== Configure Gemini AI ==========
load_dotenv(dotenv_path="api.env")  # Load variables from .env file
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key="AIzaSyBWJmxjkV3kXnU24Mx2UUWABOA6Vw63rag")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You will get a PDF from the user. Read it and answer the questions the user asks from the uploaded PDF.",
)

chat_session = model.start_chat(history=[])

# ========== Read PDF Function ==========
def read_pdf(file_path):
    """Reads a PDF file and returns its text content."""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                try:
                    text += page.extract_text() or ''
                except Exception as ex:
                    print(f"Error extracting text from page: {ex}")
                    pass
            return text.strip()
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# ========== Backend Class ==========
class Backend:
    def __init__(self):
        self.files = []  # Store file paths
        self.pdf_texts = {}  # Store text with filenames

    def openfile(self):
        """Opens a file dialog to select multiple PDFs and stores their paths and content."""
        file_paths = filedialog.askopenfilenames(title="Select PDF Files", filetypes=[("PDF Files", "*.pdf")])
        
        if file_paths:
            self.files = file_paths  # Store file paths
            self.pdf_texts = {fp.split("/")[-1]: read_pdf(fp) for fp in file_paths}  # Store text with filenames
            
            # Display all selected files
            file_names = "\n".join(self.pdf_texts.keys())
            l3.configure(text=f"Selected Files:\n{file_names}")

    def ask_gemini(self, user_input):
        """Sends user query and all uploaded PDFs' content to Gemini AI with internet error handling."""
        if not self.pdf_texts:
            return "⚠️ No PDFs uploaded! Please upload files first."

        # Check internet connection before making API request
        try:
            requests.get("https://www.google.com", timeout=3)  # Check internet connectivity
        except requests.ConnectionError:
            return "⚠️ No internet connection! Please check your network and try again."

        # Prepare labeled text from PDFs
        labeled_texts = "\n\n".join([f"Document: {name}\n{text}" for name, text in self.pdf_texts.items()])
        prompt = f"The user has uploaded multiple PDFs. Below is their content:\n\n{labeled_texts}\n\nUser Question: {user_input}\n\nIndicate the document(s) you took the response from."

        try:
            response = chat_session.send_message(prompt)
            return response.text if response else "⚠️ No response received."

        except google.api_core.exceptions.GoogleAPIError as e:
            return f"⚠️ Network Error: {e.message if hasattr(e, 'message') else 'Check your internet connection!'}"

        except Exception:
            return "⚠️ Unexpected Error! Please try again later."



be = Backend()

# ========== Copy to Clipboard Function ==========
def copy_to_clipboard(copy_button, text):
    """Copies AI response to clipboard and temporarily replaces the copy button with '✔ Copied!'"""
    app.clipboard_clear()
    app.clipboard_append(text)
    app.update()

    # Change button text to "✔ Copied!"
    copy_button.configure(text="✔ Copied!", fg_color="transparent", text_color="#134074")
    
    # Restore copy button after 2 seconds
    copy_button.after(2000, lambda: copy_button.configure(Image=copy_icon,text="", fg_color="transparent"))

# ========== Insert Message Function ==========
def insert_message(chat_container, sender, message):
    """Inserts a message in a chat bubble format with an optional copy button."""
    
    # Set text alignment and color based on sender
    if sender == "user":
        fg_color = "white"  # White for user messages
        text_color = "black"
        anchor_side = "e"  # Right alignment
    else:
        fg_color = "#134074"  # Blue for AI messages
        text_color = "white"
        anchor_side = "w"  # Left alignment

    # Create a frame to hold both the message bubble & copy button
    msg_frame = CTkFrame(chat_container, fg_color="transparent")
    msg_frame.pack(fill="x", padx=20, pady=5, anchor=anchor_side)

    # Create a horizontal frame to contain both the message and copy button
    bubble_container = CTkFrame(msg_frame, fg_color="transparent")
    bubble_container.pack(side="left" if sender == "ai" else "right", padx=5, pady=5)

    # Create a label for the chat bubble
    bubble = CTkLabel(
        bubble_container,
        text=message,
        wraplength=700,
        justify="left",
        fg_color=fg_color,
        text_color=text_color,
        corner_radius=20,
        padx=20,
        pady=15,
        font=("Arial", 16)
    )
    bubble.pack(side="left", padx=5)

    # Add Copy Button only for AI responses
    if sender == "ai":
        global copy_icon
        copy_icon=CTkImage(light_image=Image.open("copy.png"),size=(30,30))
        copy_button = CTkButton(
            bubble_container,
            image=copy_icon,
            text="",
            width=60,
            height=40,
            fg_color="transparent",
            text_color="#134074",
            command=lambda: copy_to_clipboard(copy_button, message)  # Pass button reference
        )
        copy_button.pack(side="left", padx=5)

    chat_container.update_idletasks()
    chat_container._parent_canvas.yview_moveto(1.0)  # Scroll to latest message

# ========== Main App Window ==========
app = CTk()
app.title("PDFGPT")
w, h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry("%dx%d+0+0" % (w, h))
app.resizable(False, False)
app.state("zoomed")

frame1 = app
frame2 = app

# ========== Frame Switching Functions ==========
def delete():
    """Removes all widgets from the current frame before switching."""
    for widget in app.winfo_children():
        widget.pack_forget()

def progressbar():
    read.configure(state="disabled")
    """Displays a progress bar before switching to the chat window."""
    progress_label = CTkLabel(frame1, text="Reading...", text_color="white", font=("Raleway", 15, "bold"))
    progress_label.pack(pady=(40, 2))

    progress = CTkProgressBar(frame1, mode="determinate", progress_color="White")
    progress.pack(pady=10)
    progress.start()

    progress.after(2000, lambda: [progress.destroy(), show_window2()])

# ========== Window 1 ==========
def show_window1():
    """Displays the PDF upload window."""
    delete()
    frame1.configure(fg_color='#134074')
    #frame1.state("zoomed")
    
    CTkLabel(frame1, text="📄 PDFGPT", text_color="white", font=("Raleway", 80, "bold"), pady=50).pack()
    CTkLabel(frame1, text="Ask and get answers from your PDF", text_color="white", font=("Raleway", 30)).pack()
    CTkLabel(frame1, text="Upload the PDF to be read", text_color="white", font=("Raleway", 18), pady=30).pack()

    global l3
    l3 = CTkLabel(frame1, text="No file selected", text_color="white")
    l3.pack()

    if be.pdf_texts:
        file_names = "\n".join(be.pdf_texts.keys())
        l3.configure(text=f"Selected Files:\n{file_names}")

   
    upload=CTkButton(frame1, text="Upload PDF", fg_color='#E5E4E2', text_color="black", border_width=3, border_color="white", hover_color='#E5E4E2', command=be.openfile)
    upload.pack(pady=10)
    global read
    read=CTkButton(frame1, text="Read PDF", fg_color='#E5E4E2', text_color="black", border_width=3, border_color="white", hover_color='#E5E4E2', command=progressbar)
    read.pack(pady=10)
# ========== Window 2 ==========
def show_window2():
    """Displays the chat interface and loads past messages."""
    delete()
    frame2.configure(fg_color="#E5E4E2")
    frame2.state("zoomed")

    CTkLabel(frame2, text="📄 PDFGPT", text_color="#134074", font=("Arial", 50, "bold"), pady=10).pack()
    
    #back button
    back_btn = CTkButton(frame2, text="Back", height=30, width=30, fg_color="#134074", command=show_window1)
    back_btn.pack(anchor="nw", padx=10)

    #chat interface
    chat_main_frame = CTkFrame(frame2, fg_color="transparent")
    chat_main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    chat_container = CTkScrollableFrame(chat_main_frame, fg_color="transparent", width=900, height=450)
    chat_container.pack(fill="both", expand=True)

    input_frame = CTkFrame(chat_main_frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=10, pady=5)

    #entry box
    global entry_box
    entry_box = CTkEntry(input_frame, width=700, height=50, placeholder_text="Type your question here...")
    entry_box.pack(side="left", padx=10, fill="x", expand=True)
    entry_box.bind("<Return>", lambda event: send_message(chat_container)) 
    
    #send button
    send_icon=CTkImage(light_image=Image.open("send_icon.png"),size=(30,30))
    btn_send = CTkButton(input_frame,width=30, height=50,image=send_icon, text="",fg_color="#134074", command=lambda: send_message(chat_container))
    btn_send.pack(side="right", padx=10)

    global copy_label
    copy_label = CTkLabel(frame2, text="", text_color="green", font=("Arial", 14))
    copy_label.pack()

# ========== Send Message Function ==========
def send_message(chat_container,event=None):
    """Handles sending user input and displaying AI responses."""
    user_input = entry_box.get().strip()
    if not user_input:
        return

    insert_message(chat_container, "user", user_input)
    entry_box.delete(0, END)

    ai_response = be.ask_gemini(user_input)

    insert_message(chat_container, "ai", ai_response)

# ========== Initialize Windows ==========
show_window1()
app.mainloop()
