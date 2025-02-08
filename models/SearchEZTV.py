import requests
from bs4 import BeautifulSoup

class SearchEZTV:
    BASE_URL = "https://eztv.io"
    SEARCH_URL_TPL = "/search/{}"

    def search(self, search_string):    
        posts = []
        search_url = self.BASE_URL + self.SEARCH_URL_TPL.format(search_string)
        data = BeautifulSoup(requests.get(search_url).content, 'html.parser').select('table.forum_header_border > tr.forum_header_border')
        
        for row in data:
            cols = row.select('td')
            title = cols[1].text.replace('\n', '').strip()
            info = "{}/forum/{}".format(self.BASE_URL, cols[1].select('a')[0]['href'])
            dl = "{}/forum/{}".format(self.BASE_URL, cols[2].select('a')[0]['href'])
            size = cols[3].text
            date = cols[4].text
                    
            posts.append({'title': title, 'info': info, 'dl': dl, 'size': size, 'date': date})

        for post in posts:
            yield post
