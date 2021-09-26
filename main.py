from bs4 import BeautifulSoup
import csv

def main():
    soup = BeautifulSoup(open("./fall-league-2021"), 'html.parser')
    with open("out.csv", "w") as fp:
        w = csv.DictWriter(fp, fieldnames=["name","score"])
        w.writeheader()
        for x in soup.select(".ladder-row"):
            name = x.select(".arena-leaderboard-name")[0].text.strip().split()[0].strip()
            score = x.select(".arena-leaderboard-rating")[0].text.strip()
            score = int(score.replace(",", ""))
            w.writerow({"name": name, "score": score})

if __name__ == "__main__":
    main()
