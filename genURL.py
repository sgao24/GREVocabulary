Wordlist = [line.rstrip('\n') for line in open("Text.txt")]
for w in Wordlist:
    print('<a href="https://dictionary.cambridge.org/dictionary/english/' + w + '">' + w + '</a></br>')