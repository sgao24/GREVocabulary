from bs4 import BeautifulSoup
import urllib3
import certifi
Wordlist = [line.rstrip('\n') for line in open("Text.txt")]
print(Wordlist)
Total = len(Wordlist)
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
A = []
for w in Wordlist:
    print("Searching " + w + " ...")
    A.append({
        "Word": w,
        "Pronunciation": "",
        "Definition": "",
        "Example": ""
    })
    r = http.request('GET', "https://dictionary.cambridge.org/dictionary/english/" + w)
    page = r.data
    soup = BeautifulSoup(page, "html.parser")
    if soup.find('span', attrs={"class": "pron"}) != None:
        pron = soup.find('span', attrs={"class": "pron"}).get_text()
        if pron.find('.') != -1:
            pron = pron.replace('.', '')
        if pron.find('·') != -1:
            pron = pron.replace('·', '')
        A[-1]["Pronunciation"] = pron
    if soup.find('b', attrs={"class": "def"}) != None:
        defn = soup.find('b', attrs={"class": "def"}).get_text().replace(":", "")
        A[-1]["Definition"] = defn
    if soup.find('span', attrs={"class": "eg"}) != None:
        eg = soup.find('span', attrs={"class": "eg"}).get_text().replace(":", "")
        A[-1]["Example"] = eg
    percent = len(A) / Total * 100
    print("Done " + str(len(A)) + "/" + str(Total) + "     " + str(round(percent, 1)) + "%")


file = open("Output.txt", "w", encoding='utf-8')

for dict in A:
    file.write(dict["Word"] + "\t" + dict["Pronunciation"] + "\t" + dict["Definition"] + "\t" + dict["Example"] + "\n")

file.close()