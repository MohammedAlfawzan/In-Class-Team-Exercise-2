import wikipedia
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import os

def convert_to_str(obj):
    if isinstance(obj, list):
        return '\n'.join(obj)
    return ''

def safe_filename(title):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '_')
    return title

def dl_and_save(topic, search_term):
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        references = convert_to_str(page.references)
        dir_name = f"wiki_dl/{safe_filename(search_term)}"
        os.makedirs(dir_name, exist_ok=True)
        file_name = f"{dir_name}/{safe_filename(page.title)}.txt"
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(references)
        print(f"Saved references for '{page.title}' to '{file_name}'")
    except wikipedia.exceptions.PageError:
        print(f"No page found for '{topic}'")
    except wikipedia.exceptions.DisambiguationError as error:
        print(f"Disambiguation error for '{topic}', options are: {error.options}")
    except Exception as e:
        print(f"An error occurred with '{topic}': {e}")

def download_and_save_all(search_term):
    topics = wikipedia.search(search_term)
    if not topics:
        print(f"No results found for '{search_term}'.")
        return
    
    print(f"Found topics for '{search_term}': {topics}")

    for topic in topics:
        dl_and_save(topic, search_term)

if __name__ == "__main__":
    user_input = input("Enter a search term: ")
    search_term = user_input.strip()
    
    if len(search_term) < 4:
        print("Search term is too short, defaulting to 'generative artificial intelligence'.")
        search_term = "generative artificial intelligence"
    
    print(f"Searching for and downloading pages related to '{search_term}'...")
    start_time = time.time()
    download_and_save_all(search_term)
    print(f"Operation completed in {time.time() - start_time} seconds.")
