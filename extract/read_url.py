from urllib.parse import urlparse, parse_qsl
from pprint import pprint

def get_query_params_from_url(url: str) -> None:
    try:
      parsed_url = urlparse(url)
      path = parsed_url.path
      domain = parsed_url.netloc
      query_params = parse_qsl(parsed_url.query)
      print("domain =>", domain)
      print("path =>", path)
      pprint(query_params)
      return None
      
    except Exception as e:
      print(f"Error parsing URL: {e}")
      return None
    