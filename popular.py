from bs4 import BeautifulSoup
import requests

try:
    source = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm') # get most popular movies site
    source.raise_for_status() # throw an exception if address is invalid

    soup = BeautifulSoup(source.text, 'html.parser')
    
    movies = soup.find('tbody', class_='lister-list').find_all('tr')

    for movie in movies:
        name = movie.find('td', class_ = 'titleColumn').a.text

        rank = movie.find('td', class_ = 'titleColumn').get_text(strip = True).split(')')[1].split('(')[0].strip('\n')
        
        year = movie.find('td', class_ = 'titleColumn').span.text.strip('(').strip(')')
        print(rank, '\t', name, year)
        
except Exception as e:
    print(e)