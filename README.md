# AI Productivity Hub

A Generative AI-powered productivity application designed to help individuals and teams work smarter. This application simplifies daily tasks, automates repetitive workflows, and improves overall efficiency using Generative AI.

## Features

- **Document Summarizer**: Quickly extract key points from long texts. Uses the `sshleifer/distilbart-cnn-12-6` model to generate concise summaries.
- **Email & Content Generator**: Draft emails or generate ideas efficiently. Uses the `distilgpt2` model to generate text based on a given prompt.
- **Meeting Notes Summarizer**: Turn your raw meeting notes into concise summaries, making it easier to identify action items and key takeaways.
- **Task Extractor**: Extract actionable tasks and to-dos from a paragraph of text.

## Requirements

Ensure you have Python 3.8+ installed. You can install the required dependencies using:

```bash
pip install -r requirements.txt
```

## How to Run

1. Clone this repository.
2. Install the required dependencies.
3. Run the application using Streamlit:

```bash
streamlit run app.py
```

4. Open the provided local URL in your web browser to access the AI Productivity Hub.

## Technical Details

- **Framework**: Streamlit
- **AI Models**: Hugging Face Transformers (`distilbart-cnn-12-6` for summarization, `distilgpt2` for text generation)
- **Backend**: PyTorch
