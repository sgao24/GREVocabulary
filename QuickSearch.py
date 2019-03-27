from bs4 import BeautifulSoup
import urllib3
import certifi
import datetime
currentDT = datetime.datetime.now()
WordList = [line.rstrip('\n') for line in open("Text.txt")]
print(WordList)
print()
Total = len(WordList)
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
A = []
for w in WordList:
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

    if soup.find('span', attrs={"class": "pron"}):
        pron = soup.find('span', attrs={"class": "pron"}).get_text()
        if pron.find('.') != -1:
            pron = pron.replace('.', '')
        if pron.find('·') != -1:
            pron = pron.replace('·', '')
        A[-1]["Pronunciation"] = pron

    if soup.find('b', attrs={"class": "def"}):
        defn = soup.find('b', attrs={"class": "def"}).get_text().replace(":", "")
        A[-1]["Definition"] = defn

    if soup.find('span', attrs={"class": "eg"}):
        eg = soup.find('span', attrs={"class": "eg"}).get_text().replace(":", "")
        A[-1]["Example"] = eg

    percent = len(A) / Total * 100
    print("Done " + str(len(A)) + "/" + str(Total) + "     " + str(round(percent, 1)) + "%")

# output
file = open("Output/" + currentDT.strftime("%Y-%m-%d %H_%M_%S") + ".txt", "w", encoding='utf-8')
for dic in A:
    file.write(dic["Word"] + "\t" +
               dic["Pronunciation"] + "\t" +
               dic["Definition"] + "\t" +
               dic["Example"] + "\n")
file.close()
print("File successfully saved to Output/" + currentDT.strftime("%Y-%m-%d %H_%M_%S") + ".txt")