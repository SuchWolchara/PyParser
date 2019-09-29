import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

base_url = 'https://www.yelp.com/biz/imperio-taqueria-san-jose-2?osq=import.io'

def py_parser(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)

    reviews = []
    urls = []
    urls.append(base_url)

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')

        try:
            pagination = soup.find_all('div', attrs={'class': 'lemon--div__373c0__1mboc pagination-link-container__373c0__XX_T4 border-color--default__373c0__2oFDT'})
            count = int(pagination[-1].text)

            for i in range(1, count):
                url = f'https://www.yelp.com/biz/imperio-taqueria-san-jose-2?osq=import.io&start={i * 20}'

                if url not in urls:
                    urls.append(url)

        except:
            pass

        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'itemprop': 'review'})

            for div in divs:
                name = div.find('meta', attrs={'itemprop': 'author'})['content']
                stars = div.find('meta', attrs={'itemprop': 'ratingValue'})['content']
                date = div.find('meta', attrs={'itemprop': 'datePublished'})['content']
                comment = div.find('p', attrs={'itemprop': 'description'}).text

                reviews.append({
                    'name': name,
                    'stars': stars,
                    'date': date,
                    'comment': comment
                })

            print(len(reviews))

    else:
        print('ERROR')

    return reviews

def file_writer(reviews):
    with open('parsed_reviews.csv', 'w', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Number:', 'Username:', 'Score:', 'Date:', 'Review:'))
        i = 1

        for review in reviews:
            a_pen.writerow((i, review['name'], review['stars'], review['date'], review['comment']))
            i += 1

reviews = py_parser(base_url, headers)
file_writer(reviews)