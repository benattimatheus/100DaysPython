import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇

file_path = "movies.txt"

response = requests.get(URL)
response.encoding = 'utf-8'

web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

titles = soup.find_all(name='h3', class_='title')

print(titles)

movies = []

# movies = [movie.getText() for movie in titles]

for titles in titles:
    title = titles.get_text()
    movies.append(title)

print(movies[::-1])

with open(file_path, "a") as file:
    for movie in movies[::-1]:
        file.write(movie + "\n")

# with open(file_path, "a") as file:
#     file.write("Hello World\n")