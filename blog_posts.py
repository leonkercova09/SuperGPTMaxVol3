import requests
from bs4 import BeautifulSoup
import prompts

def get_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is not 200
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join(p.text for p in soup.find_all('p'))  # Extracts text from all <p> tags
        return text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_blog_summary_prompt(blog_url):
    blog_article = get_text_from_url(blog_url)
    if blog_article:
        prompt = prompts.blog_bullet_summary_prompt.format(
            MaxPoints="10", MinPoints="5", InputText=blog_article
        )
        return prompt
    else:
        return "Failed to fetch article."

