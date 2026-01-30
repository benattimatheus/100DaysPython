from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/news")

yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")
# print(soup.prettify())
# print(soup.title.string)

# article_tag = soup.find(selector= 'span a',class_='titleline', name='a')
# print(soup.find(name='span', class_='titleline'))
# print(article_tag)

span = soup.find('span', class_='titleline')
article_tag = span.find('a')

# print(article_tag)

article_text = article_tag.get_text()
article_link = article_tag.get('href')
article_upvote = soup.find('span', class_='score').get_text()

# print(article_text)
# print(article_link)
# print(article_upvote)

articles = soup.find_all('span', class_='titleline')

articles_text = []
articles_link = []
articles_upvote = []

for articles in articles:
    # print(articles)
    articles_tag = articles.find('a')
    # print(articles_tag)
    article_text = articles_tag.get_text()
    articles_text.append(article_text)
    # print(articles_text)
    article_link = articles_tag.get('href')
    articles_link.append(article_link)
    # print(articles_link)

articles_upvote = [int(score.getText().split()[0]) for score in soup.find_all(name='span', class_='score')]

print(articles_text)
print(articles_link)
print(articles_upvote)

largest_number = max(articles_upvote)
largest_index = articles_upvote.index(largest_number)

print(articles_text[largest_index])
print(articles_link[largest_index])
print(articles_upvote[largest_index])
# with open("website.html") as file:
#     contents = file.read()
#
# soup = BeautifulSoup(contents, 'html.parser')
# # print(soup.title)
# # print(soup.title.string)
# #
# # print(soup.prettify())
#
# all_anchor_tags = soup.find_all(name='a')
#
#
# for tag in all_anchor_tags:
#     # print(tag.getText())
#     print(tag.get("href"))
#
# heading = soup.find(name='h1', id='name')
# print(heading)
#
# section_heading = soup.find(name='h3', class_='heading')
# print(section_heading.getText())
#
# company_url = soup.select_one(selector='p a')
# print(company_url)
#
# name = soup.select_one(selector='#name')
# print(name)
#
# headings = soup.select(".heading")
# print(headings)