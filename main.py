from bs4 import BeautifulSoup
import csv
import re
from dateutil.parser import parse
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
plt.rcParams["figure.figsize"] = (8, 8)


def formatData():
    with open("scrape.html") as f:
        soup = BeautifulSoup(f, "html.parser")
        entryList = soup.find("history-entries-list")
        entries = entryList.find_all(
            "history-entry", {"ng-repeat": "entry in $ctrl.entries"})
        print("Found {} entries".format(len(entries)))

        with open("data.csv", "w") as data:
            writer = csv.writer(data, delimiter='\t', lineterminator='\n')
            currentDate = ""
            for entry in entries:
                date = entry.find(
                    "time", {"class": "history-entry-day ng-binding ng-scope"})
                if date is not None:
                    currentDate = re.sub(
                        ' +', ' ', date.text.strip().replace("\n", ""))
                    # print(currentDate)
                time = entry.find(
                    "time", {"class": "history-entry-metadata-time ng-binding"}).text
                dateTime = parse(currentDate+" "+time)
                # print(dateTime)
                changes = entry.find_all(
                    "li", {"class": "history-entry-change ng-scope"})
                processedChanges = []
                for change in changes:
                    processedChanges.append(
                        re.sub(' +', ' ', change.text.replace("\n", " ").strip()))
                writer.writerow([dateTime, processedChanges])

def dateGraph(showLines=True):
    dataMap = {}
    with open("data.csv", "r") as data:
        csvreader = csv.reader(data, delimiter='\t', lineterminator='\n')
        for row in csvreader:
            date = parse(row[0]).date()
            if date in dataMap.keys():
                dataMap[date] += 1
            else:
                dataMap[date] = 1
    fig, ax = plt.subplots()
    ax.bar(dataMap.keys(), dataMap.values())
    if showLines:
        plt.axvline(x=datetime(2022, 3, 22, 13, 50),
                    color='r', label='Ende Facharbeit')
        plt.axvline(x=datetime(2022, 1, 24, 23, 20),
                    color='g', label='Start Facharbeit')
        plt.axvline(x=datetime(2022, 2, 22, 13, 50),
                    color='y', label='Sprechstunde')
        plt.axvline(x=datetime(2022, 3, 14, 11, 50),
                    color='c', label='gA Klausuren')
        plt.axvline(x=datetime(2022, 2, 24, 11, 50),
                    color='c')
        plt.axvline(x=datetime(2022, 1, 7, 18, 00),
                    color='m', label='Abgabe des Exposés')

        plt.legend(loc='upper left')
    plt.gcf().autofmt_xdate()

    plt.ylabel("Anzahl an Bearbeitungen")
    fig.savefig("dateGraph"+(""if showLines else "Raw") +
                ".png", bbox_inches='tight')
    plt.show()


def weekDayBar():
    LABELS = ["Montag", "Dienstag", "Mittwoch",
              "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    dataMap = {}
    with open("data.csv", "r") as data:
        csvreader = csv.reader(data, delimiter='\t', lineterminator='\n')
        for row in csvreader:
            date = parse(row[0]).weekday()
            if date in dataMap.keys():
                dataMap[date] += 1
            else:
                dataMap[date] = 1
    fig, ax = plt.subplots()
    ax.bar(dataMap.keys(), dataMap.values())
    plt.ylabel("Anzahl an Bearbeitungen")
    plt.xticks([i for i in range(7)], LABELS)
    fig.savefig("weekDayBar.png", bbox_inches='tight',)
    plt.show()

def hourBar():
    dataMap = {}
    with open("data.csv", "r") as data:
        csvreader = csv.reader(data, delimiter='\t', lineterminator='\n')
        for row in csvreader:
            date = parse(row[0]).hour
            if date in dataMap.keys():
                dataMap[date] += 1
            else:
                dataMap[date] = 1
    fig, ax = plt.subplots()
    ax.bar(dataMap.keys(), dataMap.values())
    plt.ylabel("Anzahl an Bearbeitungen")
    plt.xlabel("Stunde")
    fig.savefig("hourBar.png", bbox_inches='tight',)
    plt.show()

def weekDayHourMap():
    LABELS = ["Montag", "Dienstag", "Mittwoch",
              "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    dataList = [[0 for _ in range(24)] for _ in range(7)]
    with open("data.csv", "r") as data:
        csvreader = csv.reader(data, delimiter='\t', lineterminator='\n')
        for row in csvreader:
            date = parse(row[0])
            dataList[date.weekday()][date.hour] += 1

    fig, ax = plt.subplots()
    im = ax.imshow(dataList, cmap="Greens")
    ax.set_yticks([i for i in range(7)], LABELS)
    ax.set_xticks([i for i in range(24)], [i for i in range(24)])

    fig.colorbar(im, ax=ax, shrink=0.4)
    plt.xlabel("Stunde")
    fig.savefig("weekDayHourMap.png", bbox_inches='tight')
    plt.show()

translation = {
    "sec-conclusion": "Ausblick",
    "main": "Hauptdatei",
    "subsec-chaos": "Chaos",
    "subsec-exponential-instability": "Instabilität",
    "subsec-tbp-energy": "Energieerhaltung",
    "subsec-time-reversibility":"Zeitreversibilität",
    "subsec-ptbp":"Pyth. DKP",
    "subsec-tbp-momentum":"Impulserhaltung",
    "settings":"Einstellungen",
    "subsec-bulirsch-stoer":"Bulirsch-Stoer",
    "subsec-verlet-leapfrog":"Verlet-Leapfrog",
    "sec-comparison":"Vergleich",
    "subsec-euler":"Euler",
    "subsec-runge-kutta":"Runge-Kutta",
    "subsec-error":"Fehleranalyse",
    "sec-numerical":"Numerik",
    "subsec-hamilton":"Hamilton",
    "sec-appendix":"Anhang",
    "subsec-newton":"Newton",
    "sec-introduction":"Einleitung",
    "subsec-dgl-comparison":"DGL-Vergleich",
    "subsec-stepsize-comparison":"Schrittweiten-Vergleich",
    "titlepage":"Titelseite",
    "ref":"Bibliographie",
    "sec-symbol":"Symbole",
    "sec-algorithms":"Algorithmen",
    "subsec-euler-cromer":"Euler-Cromer",
    "sec-declaration":"Deklaration",
    "declaration":"Deklaration",
    "appendix":"Anhang",
    "introduction":"Einleitung",
    "conclusion":"Zusammenfassung",
    "references":"Bibliographie",
    "subsec-tbp":"DKP",
    "sec-physics":"Physik",
    "references":"Bibliographie",
    "expose":"Exposé",
}

def topicBar():
    dataMap = {

    }
    with open("data.csv", "r") as data:
        csvreader = csv.reader(data, delimiter='\t', lineterminator='\n')
        for row in csvreader:
            listOfFiles = row[1].replace("'","").replace("[","").replace("]","").strip().split(",")  
            for file in listOfFiles:
                if "Edited" in file:
                    processed = file.replace("Edited ","").strip()
                    if "/" in processed:
                        filename = processed.split("/")[-1].replace(".tex","").replace(".bib","")
                    else:
                        filename = processed.replace(".tex","").replace(".bib","")
                    if filename in translation.keys():
                        if translation[filename] in dataMap.keys():
                            dataMap[translation[filename]] += 1
                        else:
                            dataMap[translation[filename]] = 1
                    else:
                        print("No translation for: " + filename)
    fig, ax = plt.subplots()
    clean = {}
    for key in dataMap.keys():
            clean[key] = dataMap[key]
    ax.bar(clean.keys(), clean.values())
    plt.ylabel("Anzahl an Bearbeitungen")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3)
    fig.savefig("topicBar.png",)
    plt.show()
    
def exploreData():
    df = pd.read_csv("data.csv", sep='\t', header=None)
    df[0] = pd.to_datetime(df[0])
    #print("Found {} entries".format(len(df)))
    #print(df.head())
    print(df.describe(datetime_is_numeric=True))


# Formatieren der Daten
#formatData()
# Daten erkunden
#exploreData()
# Daten visualisieren
#dateGraph(False)
#dateGraph()
#weekDayBar()
#hourBar()
#weekDayHourMap()
topicBar()
