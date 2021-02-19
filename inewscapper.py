#my output but no images
import urllib

from flask import Flask, render_template, request, json
import pandas as pd
import re
from IPython.core.display import HTML

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
def news():
    try:
        import requests
        from bs4 import BeautifulSoup
        news = []
        url = 'https://inshorts.com/en/read'
        reqs = requests.get(url)
        page_soup = BeautifulSoup(reqs.text, 'html.parser')
        news_title = []
        news_content = []
        news_picture1 = []
        news_picture = []
        for headline, article, pictures in zip(page_soup.find_all('div', class_=["news-card-title news-right-box"]),
                                                   page_soup.find_all('div',
                                                                      class_=["news-card-content news-right-box"]),
                                                   page_soup.find_all('div', class_=["news-card-image"])):
            news_title.append(headline.find('span', attrs={'itemprop': "headline"}).string)
            news_content.append(article.find('div', attrs={'itemprop': "articleBody"}).string)
            news_picture.append(str(pictures))

        news_picture1 = re.findall(r'(https://\S................................................................................................g)',str(news_picture))
        df1 = pd.DataFrame(news_title, columns=["Title"])
        df2 = pd.DataFrame(news_content, columns=["Content"])
        df3 = pd.DataFrame(news_picture1, columns=["Pictures"])
        df = pd.concat([df1, df2, df3], axis=1)
        data = df[0:10]

        filename_et = 'Data.csv'
        data.to_csv(filename_et)

        HTML(data.to_html('.\\templates\\index.html', escape=False, formatters=dict(Pictures=image_link_to_html_tag),justify='center'))


    except AssertionError as e:
        print(e)
def image_link_to_html_tag(image_link):
    return '<img src="'+ image_link + '" width="120" >'


if __name__ == "__main__":
    news()
    app.run(debug=True)
