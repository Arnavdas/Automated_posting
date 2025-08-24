

from bs4 import BeautifulSoup
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

def separate_elements(webpg_obj, logger, debug=False):

  webpg_obj_list = webpg_obj.find_all('div', {'class':'listing-result-news'})

  if len(webpg_obj_list) > 0:
    if debug:
      print(f"Found {len(webpg_obj_list)} news items")

    news_items_dict, idx = {}, 0

    for item in webpg_obj_list:# Loop for extracting all imp elements
      news_items_dict[idx] = {}

      # Extracting news_link, pic_link & Title :
      try:
        news_items_dict[idx]['news_link'] = item.find('a').get('href')
      except Exception as ee:
        news_items_dict[idx]['news_link'] = None
        logger.debug(f"Error occured while extracting news link : {ee}")
        if debug:
          print(f'Exception occured while drawing the href element or the link : {str(ee)}')

      try:
        news_items_dict[idx]['pic_link'] = item.find('img').get('data-src')
      except Exception as ee:
        news_items_dict[idx]['pic_link'] = None
        logger.debug(f"Error occured while extracting pic link : {ee}")
        if debug:
          print(f'Exception occured while drawing pic link : {str(ee)}')

      try:
        news_items_dict[idx]['Title'] = item.find('p').get_text()
      except Exception as ee:
        news_items_dict[idx]['Title'] = None
        logger.debug(f"Error occured while extracting Title : {ee}")
        if debug:
          print(f'Exception occured while drawing title : {str(ee)}')

      # Extracting from inside the news_link
      if news_items_dict[idx]['news_link'] is not None:
        _, obj_tmp = scrape_web_page(news_items_dict[idx]['news_link'])

        try:
          news_items_dict[idx]['author'] = obj_tmp.find('meta', attrs={'name': 'author'}).get("content")
        except Exception as ee:
          news_items_dict[idx]['author'] = None
          logger.debug(f"Error occured while extracting author : {ee}")
          if debug:
            print(f'Exception occured while drawing author : {str(ee)}')

        try:# Extracting articleBody & datePublished :
          tmp = obj_tmp.find('script', attrs={"type":"application/ld+json"})
          tmp_1 = tmp.getText()
          # print(tmp_1)
          # print(idx, json.loads(tmp_1.replace('\n', '').replace('\r', ''))['datePublished'])
          try: # Extract datePublished :
            news_items_dict[idx]['datePublished'] = json.loads(tmp_1.replace('\n', '').replace('\r', ''))['datePublished']
          except Exception as ee:
            news_items_dict[idx]['datePublished'] = None
            logger.debug(f"Error occured while extracting datePublished : {ee}")
            if debug:
              print(f'Exception occured while drawing datePublished : {str(ee)}')

          try: # Extract articleBody :
            news_items_dict[idx]['articleBody'] = json.loads(tmp_1.replace('\n', '').replace('\r', ''))['articleBody']
          except Exception as ee:
            news_items_dict[idx]['articleBody'] = None
            logger.debug(f"Error occured while extracting articleBody : {ee}")
            if debug:
              print(f'Exception occured while drawing articleBody : {str(ee)}')

        except Exception as ee: # exception block for attrs={"type":"application/ld+json"} :
          news_items_dict[idx]['datePublished'], news_items_dict[idx]['articleBody'] = None, None
          logger.debug(f"Error occured while extracting datePublished & articleBody : {ee}")
          if debug:
            print(f'Exception occured while drawing datePublished & articleBody : {str(ee)}')

      idx+=1
  else:
    print("No news items found, which implies maybe there's some change in webpage elemental structure")
    news_items_dict = None

  return news_items_dict
