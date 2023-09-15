import streamlit as st
import PyPDF2
import openai
import os

# Initialize OpenAI API with your key
openai.api_key = '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'

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Read PDF
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
    return text

# Dividing text into smaller chunks
def divide_text(text, section_size):
    sections = []
    start = 0
    end = section_size
    while start < len(text):
        section = text[start:end]
        sections.append(section)
        start = end
        end += section_size
    return sections

# Create Anki cards
def create_anki_cards(pdf_text):
    SECTION_SIZE = 1000
    divided_sections = divide_text(pdf_text, SECTION_SIZE)
    generated_flashcards = ''
    for i, text in enumerate(divided_sections):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Create Anki flashcards with the provided text using the format: question;answer (next line) question;answer etc. Keep the question and the corresponding answer on the same line:\n{text}"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.3,
            max_tokens=2048
        )

        response_from_api = response['choices'][0]['message']['content']
        generated_flashcards += response_from_api

        if i == 0:
            break

    with open("flashcards.txt", "w") as f:
        f.write(generated_flashcards)

# Streamlit app
def main():
    st.title("Anki Flashcard Generator")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        pdf_text = read_pdf(uploaded_file)
        st.text("PDF Successfully Uploaded!")
        if st.button("Generate Anki Flashcards"):
            create_anki_cards(pdf_text)
            st.success("Anki flashcards have been generated and saved to 'flashcards.txt'")
            st.download_button(label="Download Flashcards", data=open('flashcards.txt', 'rb').read(), key='download_button')

if __name__ == "__main__":
    main()
