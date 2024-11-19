# pip install PyMuPDF requests
import fitz  # PyMuPDF
import requests
import os

def extract_links_from_pdf(pdf_path: str) -> list[str]:
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Extract links
    links = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        link_dicts = page.get_links()
        for link in link_dicts:
            if 'uri' in link:
                links.append(link['uri'])

    pdf_document.close()
    return links

def download_files(links: str, download_folder: str) -> None:
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    # List[start:stop:step]
    for link in links[::2]: 
        try:
            response = requests.get(link)
            response.raise_for_status()  # Ensure we notice bad responses
            file_name = os.path.join(download_folder, link.split("/")[-1]+".ext")
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {link}: {e}")

if __name__ == "__main__":
    # pdf_path = "file.pdf"  # Replace with your PDF file path
    # download_folder = "downloaded_audios"
    decks = []
    for root, dirs, files in os.walk('dir'):
        for file in files:
            if 'Deck' in file:
                decks.append(file)

    for pdf_file in decks:
        print(pdf_file)
        print(pdf_file[:7])
        download_folder = f"downloaded_audios/{pdf_file[:7]}"
        links = extract_links_from_pdf(pdf_file)
        download_files(links, download_folder)