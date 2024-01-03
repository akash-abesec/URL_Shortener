# pyshorteners is a python library which can reduce the url size
import pyshorteners
URL = input('Enter the url: ')
def shortenurl(URL):
    s = pyshorteners.Shortener()
    print(s.tinyurl.short(URL))
shortenurl(URL)



