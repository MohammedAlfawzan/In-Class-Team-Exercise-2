import wikipedia
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import os

def convert_to_str(obj):
  # Your existing convert_to_str function
  pass

def safe_filename(title):
  # Add an indented block of code here
  pass

def dl_and_save(topic, search_term):
  try:
    page = wikipedia.page(topic, auto_suggest=False)
    references = convert_to_str(page.references)
    dir_name = f"wiki_dl/{search_term}"
    os.makedirs(dir_name, exist_ok=True)
    file_name = f"{dir_name}/{safe_filename(page.title)}.txt"
    
    with open(file_name, 'w', encoding='utf-8') as file:
      file.write(references)
  except Exception as e:
    print(f"An error occurred with {topic}: {e}")

# Sequential implementation
if __name__ == "__main__":
  user_input = input("Enter a search term: ")
  search_term = user_input if len(user_input) >= 4 else "generative artificial intelligence"
  
  dl_and_save("topic1", search_term)

  # Threaded implementation
  with ThreadPoolExecutor() as executor:
    executor.submit(dl_and_save, "topic2", search_term)

  # Process-based implementation
  with ProcessPoolExecutor() as executor:
    executor.submit(dl_and_save, "topic3", search_term)
