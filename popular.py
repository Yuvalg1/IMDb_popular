from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm') # get most popular movies site

source.raise_for_status() # throw an exception if address is invalid