# crawler/dianping_spider.py
import requests
from bs4 import BeautifulSoup
import pandas as pd


def crawl_attractions(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    attractions = []

    # 根据实际网页结构调整选择器
    for attraction in soup.select('.list-item'):
        name = attraction.select_one('.title').get_text(strip=True)
        rating = attraction.select_one('.score').get_text(strip=True) if attraction.select_one('.score') else '无评分'
        reviews = attraction.select_one('.review-count').get_text(strip=True) if attraction.select_one(
            '.review-count') else '无评论'

        attractions.append({
            'name': name,
            'rating': rating,
            'reviews': reviews,
        })

    return attractions


def save_to_excel(attractions, filename='attractions.xlsx'):
    df = pd.DataFrame(attractions)
    df.to_excel(filename, index=False)
