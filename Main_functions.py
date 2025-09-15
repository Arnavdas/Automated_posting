
# import json
from bs4 import BeautifulSoup, Comment
import requests

def save_dict(dictionary, filename='dict.pkl')-> None:
    if type(filename) != str:
        print(f"{filename} is not a string type, enter a str type")
    if filename.endswith(".pkl"):
        import pickle
        with open(filename, 'wb') as file:
            pickle.dump(dictionary, file)
    else:
        print(f"Cant save {filename} yet, bcz of different format")

def get_file_info(file_pth)-> None:
  import os, time
  print(f"File name passed : {file_pth}\n")
  stats = os.stat(file_pth)

  if os.path.exists(file_pth):
    file_size = os.path.getsize(file_pth)
    print(f'{file_pth} size :')
    print(f"{file_size} Bytes")
    print(f"{round(file_size/1024, 2)} Kbs")
    print(f"{round(file_size/(1024*1024), 2)} Mbs")
    print("Last modified:", time.ctime(stats.st_mtime))
    print("Last accessed :", time.ctime(stats.st_atime))
    print("Created :", time.ctime(stats.st_ctime))
  else:
    print(f"{file_pth} not found")

def get_size_of_dataframe(dff, show_detailed=False, return_size_in_kbs=False)-> None:
  '''
  dff : pandas dataframe
  '''
  # Get size in bytes, convert to KB
  size_in_kb = dff.memory_usage(deep=True).sum() / 1024  # Bytes to KB
  size_in_mb = size_in_kb / (1024*1024)  # Bytes to MB
  if return_size_in_kbs:
    return round(size_in_kb, 2)

  print(f"DataFrame size: {size_in_kb:.2f} Kbs OR {size_in_mb:.2f} Mbs \n")
  
  if show_detailed:
    # Detailed column-wise memory usage in KB
    print("column wise space distribution : \n")
    column_sizes = dff.memory_usage(deep=True) / 1024
    for column, size in column_sizes.items():
        print(f"{column}: {size:.2f} Kbs")

def scrape_web_page(logger, url='https://odishatv.in/odisha/bhubaneswar'):
    # url+='/15' # For next page

    try:
        # Send a request to the Wikipedia main page
        # Adding a user agent to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract different sections from the main page
        results = {}

        return results, soup

    except requests.RequestException as e:
      logger.debug(f"Error occurred while scraping: {e}")
      print(f"Error occurred while scraping: {e}")
      return None, None

# Main Funcs :

# error_dict = {'random_key' : 'testing'}

def scrape_web_page(logger, url='https://odishatv.in/odisha/bhubaneswar'):
    # url+='/15' # For next page

    try:
        # Send a request to the Wikipedia main page
        # Adding a user agent to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract different sections from the main page
        results = {}

        return results, soup

    except requests.RequestException as e:
      logger.debug(f"Error occurred while scraping: {e}")
      print(f"Error occurred while scraping: {e}")
      return None, None

def separate_elements(webpg_obj, logger, debug=False):

  webpg_obj_list = webpg_obj.find_all('div', {'class':'listing-result-news'})

  if len(webpg_obj_list) > 0:
    if debug:
      print(f"Found {len(webpg_obj_list)} news items")

    news_items_dict, idx = {}, 0

    for item in webpg_obj_list:# Loop for extracting all imp elements

      if debug:
        display(item)

      news_items_dict[idx] = {}

      # Extracting news_link, pic_link & Title :
      try:
        news_items_dict[idx]['news_link'] = item.find('a').get('href')
      except Exception as ee:
        news_items_dict[idx]['news_link'] = None
        logger.debug(f"Error occured while extracting news link : {ee}")
        if debug:
          print(f'Exception occured while drawing the href element or the link : {str(ee)}')

      # Extracting pic link :
      try:
        news_items_dict[idx]['pic_link'] = item.find('img').get('data-src')
      except Exception as ee:
        news_items_dict[idx]['pic_link'] = None
        logger.debug(f"Error occured while extracting pic link : {ee}")
        if debug:
          print(f'Exception occured while drawing pic link : {str(ee)}')

      # Extracting Subtitle :
      try:
        news_items_dict[idx]['Subtitle'] = item.find('p').get_text()
      except Exception as ee:
        news_items_dict[idx]['Subtitle'] = None
        logger.debug(f"Error occured while extracting Subtitle : {ee}")
        if debug:
          print(f'Exception occured while drawing Subtitle : {str(ee)}')

      # Extracting Title :
      try:
        news_items_dict[idx]['Title'] = item.find('h5').get_text()
      except Exception as ee:
        news_items_dict[idx]['Title'] = None
        logger.debug(f"Error occured while extracting Title : {ee}")
        if debug:
          print(f'Exception occured while drawing Title : {str(ee)}')

      comments = item.find_all(string=lambda text: isinstance(text, Comment))

      # Extracting datepublished :
      news_items_dict[idx]['DatePublished'] = None
      try:
        for c in comments:
          if "li" in c:
              # print(c.strip())
              inner_soup = BeautifulSoup(c, "html.parser")
              date_text = inner_soup.get_text(strip=True)
              # print(type(date_text), date_text)
              if (('am'in date_text.lower()) or ('pm' in date_text.lower())) and ('ist' in date_text.lower()):
                news_items_dict[idx]['DatePublished'] = date_text
                if debug:
                  print('drawn date text',date_text)
                break
      except Exception as ee:
        news_items_dict[idx]['DatePublished'] = None
        logger.debug(f"Error occured while extracting DatePublished : {ee}")
        if debug:
          print(f'Exception occured while drawing DatePublished : {str(ee)}')

      # Extracting ArticleBody, Author Name & Author profile (if available) :
      _, inner_tmp = scrape_web_page(logger, news_items_dict[idx]['news_link'])

      # Extracting ArticleBody :
      p_wo_class = [p.get_text(strip=True) for p in inner_tmp.find_all("p", class_=False)]
      if debug:
        display('p_wo_class', p_wo_class)
      if len(p_wo_class) > 0:
        news_items_dict[idx]['ArticleBody'] = " ".join(p_wo_class)
      else:
        news_items_dict[idx]['ArticleBody'] = None
        logger.debug(f"Error occured while extracting ArticleBody : {ee}")
        if debug:
          print(f'Exception occured while drawing ArticleBody : {str(ee)}')

      # Extracting Author :
      try:
        author = inner_tmp.find('span', {'class':'otv-auth__name'}).get_text(strip=True)
        news_items_dict[idx]['Author'] = author
      except Exception as ee:
        news_items_dict[idx]['Author'] = None
        logger.debug(f"Error occured while extracting Author : {ee}")
        if debug:
          print(f'Exception occured while drawing Author : {str(ee)}')

      # Extracting Author Webpage :
      for ff in inner_tmp.find_all('span'):
        # print(ff)
        try:
          href_txt = ff.find('a').get('href')
          if (not(author is None)) and (author.lower() in href_txt.lower()):
            news_items_dict[idx]['Author'] = None
            break
          else:
            news_items_dict[idx]['AuthorWebpage'] = href_txt
        except Exception as ee:
          href_txt = None
          logger.debug(f"Error occured while extracting Author Webpage : {ee}")
          if debug:
            print(f'Exception occured while drawing Author Webpage : {str(ee)}')

      # index increment for next news item :
      idx+=1
  else:
    print("No news items found, which implies maybe there's some change in webpage elemental structure")
    news_items_dict = None

  return news_items_dict
