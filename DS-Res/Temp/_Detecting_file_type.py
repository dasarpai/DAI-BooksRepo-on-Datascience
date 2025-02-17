import os
from PyPDF2 import PdfReader

def is_ebook(text):
    # Simple heuristic based on common ebook terms
    ebook_terms = ["chapter", "contents", "introduction", "author", "isbn", "publisher", "copyright"]
    text_lower = text.lower()
    return any(term in text_lower for term in ebook_terms)

def check_and_rename_and_move_pdfs(directory):
    # Create a "books" folder in the specified directory
    books_folder = os.path.join(directory, 'books')
    os.makedirs(books_folder, exist_ok=True)
    
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'rb') as file:
                    reader = PdfReader(file)
                    # Get the first few pages or first 5 pages to analyze
                    text = ""
                    for page_num in range(min(5, len(reader.pages))):
                        text += reader.pages[page_num].extract_text()
                    
                if is_ebook(text):
                    new_filename = filename.replace('.pdf', '_eBook.pdf')
                    new_filepath = os.path.join(books_folder, new_filename)
                    os.rename(filepath, new_filepath)
                    print(f"Renamed and moved: {filename} to {new_filepath}")
                else:
                    print(f"Not an ebook: {filename}")
            except Exception as e:
                print(f"Error reading file: {filename}, Error: {e}")

# Replace 'your_directory_path' with the path to your directory
directory_path = '.'
check_and_rename_and_move_pdfs(directory_path)
