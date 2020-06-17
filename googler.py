import argparse
import requests
import webbrowser
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="This program makes a Google search with your 'query' and opens the first 'n' result(s) on default browser.", epilog="ex: python3 googler.py 'how to make cupcake' 4", usage="python3 googler.py [-h] query n")
parser.add_argument("query", type=str, help="search query")
parser.add_argument("num", type=int, help="number of links to open (default=3)", nargs='?', default=3)

args = parser.parse_args()
q = args.query
n = args.num

print("Googling...")
res = requests.get(f"https://www.google.com/search?q={q}")
res.raise_for_status()

all_links = []

soup = BeautifulSoup(res.text, "lxml")
divs = soup.findAll("div", class_="kCrYT")
for div in divs:
  links = div.findAll("a")
  for link in links:
    result = link["href"].split("&")[0].split("=")[1]
    if "http://" in result or "https://" in result and result not in all_links:
      all_links.append(result)

len_all_links = len(all_links)

if len_all_links == 0:
  print("Sorry, I could not find any results :(")
  exit()
elif n > len_all_links:
  print(f"I could find only {len_all_links} result(s)")
  n = len_all_links

for link in all_links:
  print(link)

for i in range(n):
  webbrowser.open(all_links[i])
