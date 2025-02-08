# import logging
from requests import get
from bs4 import BeautifulSoup


class SearchRUTOR:    # Changed from SearchRutor to SearchRUTOR
    TRACKER_URL = "http://rutor.info"
    TRACKER_SEARCH_URL_TPL = "/search/0/0/000/0/"

    def search(self, search_string):
        """Search data on the web"""
        self.posts = []
        url = self.TRACKER_URL + self.TRACKER_SEARCH_URL_TPL + search_string
        data = BeautifulSoup(get(url).content, 'lxml').select('div#index > table > tr')
        for row in data[1:]:
            cols = row.select('td')
            title = cols[1].select('a')[2].text
            info = cols[1].select('a')[2].get('href')
            dl = cols[1].select('a')[1].get('href')
            # Check if it's a magnet link and use it directly
            if dl.startswith('magnet:'):
                dl_link = dl
            else:
                dl_link = f"{self.TRACKER_URL}/{dl}"
            size = cols[2].text if len(cols) == 4 else cols[3].text
            units = {'KB': 1024, 'MB': 1048576, 'GB': 1073741824}
            try:
                if size.split('\xa0')[1].upper() in units.keys():
                    size = int(float(size.split('\xa0')[0])) * units[size.split('\xa0')[1].upper()]
            except Exception as e:
                size = 0
            date = cols[0].text
            self.posts.append({
                'title': title.replace(r'<', ''),
                'info': f"{self.TRACKER_URL}/{info}",
                'dl': dl_link,  # Use the processed download link
                'size': size,
                'date': date
            })