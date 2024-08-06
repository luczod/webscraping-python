# pip install PyMuPDF requests
import fitz  # PyMuPDF
import requests
import os

def extract_links_from_pdf(pdf_path):
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

def download_files(links, download_folder):
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
    pdf_path = "file.pdf"  # Replace with your PDF file path
    download_folder = "downloaded_audios"

    links = extract_links_from_pdf(pdf_path)
    download_files(links, download_folder)