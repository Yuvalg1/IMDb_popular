from email.policy import default
from bs4 import BeautifulSoup
import requests
import random

mov_lst = []

def print_dict(x):
    print("{0}. \t{1} ({2}) Change: {3} Rating: {4}".format(x["rank"], x["name"], x["year"], int(x["sign"]) * int(x["change"]), x["rating"]))

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

        rating = movie.find('td', class_ = 'ratingColumn imdbRating').strong

        if rating == None:
            rating = 0.0
        else:
            rating = float(rating.text)

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
        mov_lst.append({"rank": rank, "name": name, "year": year, "sign": sign, "change": change, "rating": rating})
except Exception as e:
    print(e)


suggested = mov_lst

print("welcome to Pick a Movie Generator!")
print("The top 100 movies are here to get picked!")

ans = input("If that's too much, would you like to shorten the range? y/n ").casefold()
if ans == 'y':
    print('pick a range between [1, 100]: ')
    a = max(min(int(input()) - 1, 100), 0)
    b = max(min(int(input()), 100), 0)
    suggested = suggested[a : b]

ans = input('would you like to pick the range of the release year? y/n ').casefold()
if ans == 'y':
    seq = [x['year'] for x in suggested]
    minYear = int(min(seq))
    maxYear = int(max(seq))
    print(f'pick a range between [{minYear}, {maxYear}]: ')
    a = max(min(int(input()), maxYear), minYear)
    b = max(min(int(input()), maxYear), minYear)
    suggested = [x for x in suggested if a < int(x['year']) < b]

ans = input('would you like to pick the range of rating? y/n ').casefold()
if ans == 'y':
    print(f'pick a range between [0, 10]: ')
    a = float(max(min(float(input()), 10), 0))
    b = float(max(min(float(input()) + 0.1, 10), 0))
    suggested = [x for x in suggested if a < float(x['rating']) < b]

ans = input("Would you like a personal suggestion? y/n ").casefold()
if ans == 'y':
    print_dict(suggested[random.randint(0, len(suggested))])
else:
    [print_dict(x) for x in suggested]