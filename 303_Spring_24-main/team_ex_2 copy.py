import wikipedia
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import os

def convert_to_str(obj):
    if isinstance(obj, list):
        return '\n'.join(obj)
    elif isinstance(obj, (str, int, float)):
        return str(obj)
    return ''

def safe_filename(title):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '_')
    return title

def dl_and_save(topic, search_term, mode):
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        references = convert_to_str(page.references)
        dir_name = f"wiki_dl/{mode}/{safe_filename(search_term)}"
        os.makedirs(dir_name, exist_ok=True)
        file_name = f"{dir_name}/{safe_filename(page.title)}.txt"
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(references)
        print(f"Saved references for '{page.title}' in {mode} mode to '{file_name}'")
    except Exception as e:
        print(f"An error occurred with '{topic}' in {mode}: {e}")

def download_and_save_all(search_term, mode):
    topics = wikipedia.search(search_term)
    if not topics:
        print(f"No results found for '{search_term}'.")
        return
    
    print(f"Found topics for '{search_term}': {topics}")

    if mode == 'sequential':
        for topic in topics:
            dl_and_save(topic, search_term, mode)
    elif mode == 'threaded':
        with ThreadPoolExecutor() as executor:
            executor.map(lambda topic: dl_and_save(topic, search_term, mode), topics)
    elif mode == 'process':
        with ProcessPoolExecutor() as executor:
            executor.map(lambda topic: dl_and_save(topic, search_term, mode), topics)

if __name__ == "__main__":
    user_input = input("Enter a search term: ")
    search_term = user_input.strip() if len(user_input.strip()) >= 4 else "generative artificial intelligence"
    
    modes = ['sequential', 'threaded', 'process']

    for mode in modes:
        print(f"\nSearching for and downloading pages related to '{search_term}' using {mode} mode...")
        start_time = time.time()
        download_and_save_all(search_term, mode=mode)
        print(f"Operation completed in {mode} mode in {time.time() - start_time} seconds.")
