from bs4 import BeautifulSoup
import urllib3
import certifi
Wordlist = [line.rstrip('\n') for line in open("Text.txt")]
print(Wordlist)
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
for w in Wordlist:
    r = http.request('GET', "https://dictionary.cambridge.org/dictionary/english/" + w)
    page = r.data
    soup = BeautifulSoup(page, "html.parser")
    if soup.find('span', attrs={"class": "eg"}) != None:
        defn = soup.find('span', attrs={"class": "eg"}).get_text().replace(":", "")
        print(defn)
    else:
        print()
