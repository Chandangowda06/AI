import PyPDF2
import nltk

# Download the nltk punkt package if not already installed
# nltk.download('punkt')

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize an empty list to store the sentences
        sentences = []

        # Iterate through all pages in the PDF
        for page_number in range(len(pdf_reader.pages)):
            # Get the page
            page = pdf_reader.pages[page_number]
            
            # Extract text from the page
            text = page.extract_text()

            # Tokenize the text into sentences
            page_sentences = nltk.sent_tokenize(text)

            # Remove newline characters from each sentence
            page_sentences = [sentence.replace('\n', ' ') for sentence in page_sentences]

            # Append the sentences to the list
            sentences.extend(page_sentences)

    return sentences



