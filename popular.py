from email.policy import default
from bs4 import BeautifulSoup
import requests

mov_lst = []

try:
    source = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm') # get most popular movies site
    source.raise_for_status() # throw an exception if address is invalid

    soup = BeautifulSoup(source.text, 'html.parser')
    
    movies = soup.find('tbody', class_='lister-list').find_all('tr')

    for movie in movies:
        html_movie = movie.find('td', class_ = 'titleColumn')

        name = html_movie.a.text

        rank = html_movie.get_text(strip = True).split(')')[1].split('(')[0].strip('\n').strip(',')
        
        year = html_movie.span.text.strip('(').strip(')')

        change = html_movie.find('div', class_ = 'velocity').text.split('\n(')[1].strip('\n').strip(')').replace(",", "")
        if change == 'no change':
            change = 0

        change_html = html_movie.find('div', class_ = 'velocity').span
        
        sign = 0
        if change_html != None:
            if change_html.find('span', class_ = 'global-sprite titlemeter up') != None:
                sign = 1
            else:
                sign = -1
        print(f"{rank}. \t{name} ({year}) {int(sign) * int(change)}")
        mov_lst.append({"rank": rank, "name": name, "year": year, "sign": sign, "change": change})
        
except Exception as e:
    print(e)

#print("welcome to Pick a Movie Generator!")
#print("The top 100 movies are here to get picked!")
#ans = input("If that's too much, would you like to shorten the range?").casefold()
