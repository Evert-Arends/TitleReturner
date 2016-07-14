# Safely return titles from web pages.
# Copyright for this script: Evert Arends
import requests
from bs4 import BeautifulSoup

SAFE = True  # Are valid SSL certs important to you, or not? To me they are. Set to false if you don't care.


class TitleReturner:
    def __init__(self):
        print ('Title requested.')

    def returnTitle(self, url):
        content = self._getContent(url)
        title = self._getTitle(content)

        if title:
            if len(title) > 30:
                return "Title contains to much characters."
            else:
                print title
                return title
        else:
            return "404 - Yeah, I'm not sure either."

    @staticmethod
    def _getContent(url):
        r = requests.get(url, timeout=5, stream=True, verify=SAFE)

        maxsize = 100000
        content = ''
        for chunk in r.iter_content(2048):
            content += chunk.encode('utf8')
            if '</title>' in content:
                r.close()
                return content.encode('utf8')
            if len(content) > maxsize:
                r.close()
                return ValueError('Response too large')

    @staticmethod
    def _getTitle(content):
        soup = BeautifulSoup(content, "html.parser")
        title = soup.title.string

        if title:
            return soup.title.string
        else:
            return ""

if __name__ == "__main__":
    T = TitleReturner()
    print T.returnTitle('') # url
