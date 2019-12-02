import os
from bs4 import BeautifulSoup

archivo = input("Path del archivo (html): ")
html = open(archivo,'r')
soup = BeautifulSoup(html,'lxml')


# kill all script and style elements
for script in soup(["style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text(separator='\n', strip=True)

#print(soup.get_text(separator=']'))


# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.split("\n"))
print (lines)
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

print(text)


f = open ("state.txt", "w")
f.write(text)
f.close()

f1 = open('state.txt', 'r')
f2 = open('state.txt.tmp', 'w')
for line in f1:
    f2.write(line.replace('\n', ' '))
f1.close()
f2.close()

f1 = open('state.txt.tmp', 'r')
f2 = open('state.txt', 'w')
for line in f1:
    f2.write(line.replace(']', '] \n'))
f1.close()
f2.close()

f1 = open('state.txt', 'r')
f2 = open('state.txt.tmp', 'w')
for line in f1:
    f2.write(line.replace(':', ''))
f1.close()
f2.close()

f1 = open('state.txt.tmp', 'r')
f2 = open('state.txt', 'w')
for line in f1:
    f2.write(line.replace('Reachability/Coverability Graph Information', ''))
f1.close()
f2.close()

os.remove("state.txt.tmp")