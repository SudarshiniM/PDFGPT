# PDFGPT

PDFGPT is a Python-based desktop application that allows you to interact with PDF documents using the power of Google's Gemini AI. It transforms static PDFs into dynamic knowledge sources, enabling you to ask questions and receive instant, context-aware answers.

## Features

* **AI-Powered Question Answering:** Get intelligent answers based on the content of your uploaded PDFs.
* **Multiple PDF Support:** Upload and query multiple PDFs simultaneously.
* **PDF Upload and Processing:** Easily upload and analyze your PDF documents.
* **Natural Language Processing:** Accurate extraction and interpretation of text from PDFs.
* **Interactive Chat Interface:** A user-friendly chat interface for conversational queries.
* **Context-Aware Responses:** Receive relevant answers, not just keyword matches.
* **Efficient Information Retrieval:** Quickly find the information you need, saving time and effort.
* **User-Friendly GUI:** Built with CustomTkinter for a modern look and feel.

## Prerequisites

* Python 3.x
* pip (Python's package installer)

## Installation

1.  Clone the repository to your local machine.
2.  Navigate to the project directory in your terminal.
3.  Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Setup

1.  **Create a `.env` file** in the same directory as `PDFGpt.py`.
2.  **Add your Gemini API key** to the `.env` file:

    ```
    GEMINI_API_KEY=YOUR_ACTUAL_API_KEY
    ```

    * Replace `YOUR_ACTUAL_API_KEY` with your actual Gemini API key.
    * **Important:** Do not put any quotes around the API key.

## Usage

1.  Run the `PDFGpt.py` script from your terminal:

    ```bash
    python PDFGpt.py
    ```

2.  The PDFGPT application window will open.
3.  Click the "Upload PDF" button to select the PDF files you want to query.
4.  Click "Read PDF" to process the uploaded PDFs.
5.  Switch to the chat interface to ask questions related to the content of the PDFs.
6.  Type your questions in the input box and press Enter or click the send button.
7.  PDFGPT will provide answers based on the PDF content.

##  Additional Notes

* Ensure you have a stable internet connection, as PDFGPT relies on the Gemini AI API.
* For optimal performance, avoid uploading extremely large PDF files. [cite: 7]


## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.txt) file for details.
