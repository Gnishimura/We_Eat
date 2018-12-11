from pymongo import MongoClient
from bs4 import BeautifulSoup

we_eat_client = MongoClient()
we_eat_db = we_eat_client['we_eat']
website_collection = we_eat_db['websites']
review_collection = we_eat_db['reviews']

# To run this file and compile reviews into a database: db = collect_reviews(website_collection)

def parse_review(review, alias):
    r = {}
    r['alias'] = alias
    r['username'] = review.select_one('li.user-name').text.strip()
    r['href'] = review.select_one('li.user-name a').attrs['href']
    r['userid'] = r['href'].partition('?userid=')[2]
    r['rating'] = float(review.select_one('div.i-stars').attrs['title'].partition(' ')[0])
    r['date'] = review.select_one('span.rating-qualifier').text.strip()
    r['review_text'] = review.select_one('div.review-content p').text
    return r

def save_review(review_data):
    review_collection.delete_many({
        'alias': review_data['alias'],
        'userid': review_data['userid']
    })
    review_collection.insert_one(review_data)

def collect_reviews(website_collection):
    for website in website_collection.find():
        url = website['url']
        alias = url.rpartition('/')[2]
        html = website['html']
        soup = BeautifulSoup(html, 'html.parser')
        reviews = soup.select('div.review')
        for review in reviews[1:]:
            review_data = parse_review(review, alias)
            save_review(review_data)
