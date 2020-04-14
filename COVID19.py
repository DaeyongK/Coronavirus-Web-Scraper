import requests
import time
from bs4 import BeautifulSoup
import csv
stats = {
        "Cases": 0,
        "Deaths": 0,
        "Recovers": 0,
        "Chance of Death": 0,
        "Cases per Minute": 0,
        "Time": 0
}
previousNum = 0
def getStats(previousNum):
    decimal = str(stats["Chance of Death"]).find(".")
    decimal2 = str(stats["Cases per Minute"]).find(".")
    stats["Chance of Death"] = float(str((stats["Deaths"]/stats["Cases"]*100))[0:decimal+3])
    stats["Cases per Minute"] = float(str((stats["Cases"]-previousNum)/60)[0:decimal+3])
    stats["Time"] = time.asctime()
    for things in stats:
        print(things+": "+ str(stats[things]))
while True:
    caseList = []
    thingList = []
    which = 0
    r = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(r.text, "html.parser")
    for i in soup.find_all("div", attrs={"class": "maincounter-number"}):
        caseList.append(int(i.text.strip().replace(",","")))
    for x in stats:
        stats[x] = caseList[which]
        which = which + 1
        if x == "Recovers":
            break
    getStats(previousNum)
    for x in stats:
        thingList.append(stats[x])
    with open("coronavirus_stats.csv", "a") as df:
        csv_writer = csv.writer(df, delimiter = ",")
        csv_writer.writerow(thingList)
    previousNum = stats["Cases"]
    time.sleep(3600)
    
