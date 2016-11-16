from bs4 import BeautifulSoup


def get_page(url):
    try:
        import urllib
        return urllib.request.urlopen(url).read()
    except:
        return ""


url = "http://www.howstat.com.au/cricket/Statistics/Matches/MatchListCountry_T20.asp?A=IND"
print('getting and parsing url source code')
page = BeautifulSoup(get_page(url), 'html.parser')
# print(page.prettify())
# print(page.title.string)

matchTags = page.find_all(attrs={'class': 'LinkNormal'})
# print(matchTags)

matchCodes = []
print('getting match codes')
# print(matchTags[0].attrs)
for matchTag in matchTags:
    matchCode = matchTag.attrs['href'].split('=')[1]
    matchCodes.append(matchCode)

# print(len(matchCodes))

print('saving list as .pkl format')
import pickle

f = open('India_T20_matchcodes.pkl', 'wb')
pickle.dump(matchCodes, f)
f.close()
