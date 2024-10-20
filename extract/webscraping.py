import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_css(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to load page, status code: {response.status_code}")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    inline_css = []
    for attribute in soup.find_all(lambda tag: tag.has_attr('style')):
        print(attribute.name)
        # inline_css += style.get_text() + '\n'
        inline_css.append(attribute['style'])
    
     # Extract linked CSS from <link> tags and fetch their content
    linked_css = []
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            # Handle relative URLs
            if not href.startswith('http'):
                href = requests.compat.urljoin(url, href)
            try:
                css_response = requests.get(href)
                a = urlparse(href)
                fileName = os.path.basename(a.path)
                if css_response.status_code == 200:
                    with open(f"webPage/css/{fileName}", 'w', encoding='utf-8') as file:
                        file.write(css_response.text)
                    linked_css.append(fileName)
                else:
                    print(f"Failed to load CSS file: {href}, status code: {css_response.status_code}")
            except Exception as e:
                print(f"Error fetching CSS file: {href}, error: {e}")
                
    print("Linked CSS:\n", linked_css)
    print("Inline CSS:\n", inline_css)

    return inline_css,linked_css


def download_website(url, statusCode):
    if not os.path.exists("webPage/css"): 
        os.makedirs("webPage/css") 
   
    response = requests.get(url)
    if response.status_code == statusCode:
        soup = BeautifulSoup(response.content, 'html.parser')
        with open('webPage/index.html', 'w', encoding='utf-8') as file:
            file.write(str(soup))
        # return str(soup)
    extract_css(url)
    else:
        print(
            f"Failed to download website. Status code: {response.status_code}")


if __name__ == '__main__':
  download_website("https://",200)
