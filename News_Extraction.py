# Create a log file :
import pandas as pd
import logging
import numpy as np

from Main_functions import scrape_web_page, separate_elements, get_size_of_dataframe

logging.basicConfig(
    level=logging.DEBUG,              # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
   handlers=[
        logging.StreamHandler(),               # console (stdout → Actions logs)
        logging.FileHandler("my_log.log")      # file (artifact later)
    ],
    force=True # This is done for colab env, bcz log format files are not created normally in colab
)

logger = logging.getLogger(__name__)

root_url_cur = 'https://odishatv.in/odisha/'
pages_to_draw = 2
# 15 is used below because in nxt_web_page_url_list variable as otv news lists extend in that way
visited_url_list, nxt_web_page_url_list = [], list(range(0, 15*pages_to_draw, 15))
news_city_dict = {}
print(f"Currently drawing from last {pages_to_draw} webapges starting with {root_url_cur} : \n")

try:# We del every time So that everytime we run, it will not store anything from prev runs
  del news_dff_all, news_dff_now, news_dict_now
except:
  pass

list_of_city = ['bhubaneswar', 'kendrapara', 'cuttack', 'rourkela', 'puri', 'kalahandi']
display_detailed = False # shows detailed list of Nans or errors inside the loop below

logging.info("Script started")

# News EXtraction loop starts :
for city in list_of_city:
  city_root_url_cur = root_url_cur + city

  logging.info(f"Current visiting {city} webpage : {city_root_url_cur}")
  print(f"Current visiting {city} webpage : {city_root_url_cur}")

  for ii in nxt_web_page_url_list:
    # print(ii)
    if ii==0:
      cur_url = city_root_url_cur
    else:
      cur_url = city_root_url_cur + '/' + str(ii)

    logging.info(f"Visiting now : {cur_url}")
    print(f"Visiting now : {cur_url}")

    _, obj = scrape_web_page(logger, cur_url)
    news_dict_now = separate_elements(obj, logger)
    visited_url_list.append(cur_url)
    del obj, cur_url

    # convert extracted info to Dataframes :
    for kk in news_dict_now:
      # print(kk)
      try:
        news_dff_now = pd.concat([news_dff_now, pd.Series(news_dict_now[kk]).to_frame().T], axis=0)
      except:
        news_dff_now = pd.Series(news_dict_now[kk]).to_frame().T

      news_dff_now = news_dff_now.reset_index(drop=True)
      # print('news_dff_now checks : ', news_dff_now.shape,)

      # # None/Nan Check : UNCOMMENT THIS SECTION ONLY IF U WISH TO CHECK MORE
      # if news_dff_now.isnull().sum().sum() > 0:
      #   print(f"Some Nones/Nans Detected : {news_dff_now.isnull().sum().sum()}")
      #   if display_detailed:
      #     display( news_dff_now.isnull().sum())

      # Duplicacy Check :
      if news_dff_now.duplicated().sum() > 0:
        logging.warning(f"\nNumber of duplicate rows : {news_dff_now.duplicated().sum()}\n")
        print(f"\nNumber of duplicate rows : {news_dff_now.duplicated().sum()}\n")

    # concat to Final Dataframe :
    try:
      news_dff_all = pd.concat([news_dff_all, news_dff_now], axis=0)
    except:
      news_dff_all = news_dff_now.copy()

    # Reset Index :
    news_dff_all = news_dff_all.reset_index(drop=True)
    logging.info(f"news_dff_all shape : {news_dff_all.shape}")
    print('news_dff_all shape : ', news_dff_all.shape,'\n')

    # None/Nan Check :
    if news_dff_all.isnull().sum().sum() > 0:
      logging.warning(f"Some Nones/Nans Detected : {news_dff_all.isnull().sum().sum()}")
      print(f"Some Nones/Nans Detected : {news_dff_all.isnull().sum().sum()}")
      if display_detailed:
        display(news_dff_all.isnull().sum())

    # Duplicacy Check :
    if news_dff_all.duplicated().sum() > 0:
      logging.warning(f"\nNumber of duplicate rows : {news_dff_all.duplicated().sum()}")
      print(f"\nNumber of duplicate rows : {news_dff_all.duplicated().sum()}, \n")

    del news_dff_now, news_dict_now

  news_city_dict[city] = news_dff_all.copy()
  # Size Check :
  # logging.info(f"{local_funcs_v2.get_size_of_dataframe(news_dff_all)}")
  # get_size_of_dataframe(news_dff_all)
  # Duplicacy Check :
  logging.info(f"Number of duplicate rows : {news_dff_all.duplicated().sum()}\n")
  print(f"Number of duplicate rows : {news_dff_all.duplicated().sum()}\n")

  del news_dff_all
