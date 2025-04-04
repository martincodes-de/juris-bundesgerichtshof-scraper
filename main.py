import time
import urllib.request
from bs4 import BeautifulSoup
import requests
import os

COURTS = [
    "1. Strafsenat",
    "2. Strafsenat",
    "3. Strafsenat",
    "4. Strafsenat",
    "5. Strafsenat",
    "6. Strafsenat",
]

TIMEOUT_PER_PAGE_IN_SECONDS = 2

def downloadPdf(url, storageDirectoryPath, storagePath, fileId):
    print("Versuche", fileId, "herunterzuladen")

    try:
        if not os.path.exists(storageDirectoryPath):
            os.makedirs(storageDirectoryPath)
    except Exception as e:
        print(f"Verzeichnisstruktur kann nicht erstellt werden: {storageDirectoryPath} {e}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(storagePath, 'wb') as pdf_file:
            pdf_file.write(response.content)

    except requests.exceptions.RequestException:
        print(f"Fehler beim Herunterladen des Aktenzeichens: {fileId}")


def getMaximumNumbersOfPages(sessionId):
    url = f"https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/list.py?Gericht=bgh&Art=en&sid={sessionId}"
    html = urllib.request.urlopen(url).read()
    scraper = BeautifulSoup(html, 'html.parser')

    pageNumberElements = scraper.find_all("td", {"class": "pagenumber"})

    if len(pageNumberElements) == 0:
        lastPageNumber = 0
    else:
        lastPageNumber = pageNumberElements[-1].find_all("a")[-1].get("href")[-1]

    return lastPageNumber


def downloadPage(sessionId, pageNumber):
    url = f"https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/list.py?Gericht=bgh&Art=en&sid={sessionId}&Seite={pageNumber}"
    html = urllib.request.urlopen(url).read()
    scraper = BeautifulSoup(html, 'html.parser')

    searchSubject = scraper.find("input", {"class": "SuchFormFeld", "name": "text"}).get("value").strip()
    searchFileId = scraper.find("input", {"class": "SuchFormFeld", "name": "az"}).get("value").strip()
    searchDate = scraper.find("input", {"class": "SuchFormFeld", "name": "datum"}).get("value").strip()

    if not searchSubject:
        searchSubject = "kein_betreff"

    if not searchFileId:
        searchFileId = "kein_aktenzeichen"

    if not searchDate:
        searchDate = "kein_datum"

    evenResults = scraper.find_all("tr", {"class": "roweven"})
    oddResults = scraper.find_all("tr", {"class": "rowodd"})
    allResults = evenResults + oddResults

    for result in allResults:
        court = result.find("td", {"class": "ESpruchk"}).get_text().strip()
        fileId = result.find("td", {"class": "EAz"}).find("a").get_text().strip()
        downloadPath = result.find("td", {"class": "EAz"}).find("a", {"type": "application/pdf"}).get("href")
        downloadUrl = "https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/" + downloadPath

        storageDirectory = os.path.join(os.getcwd(), "Download", f"{searchSubject}", f"{searchFileId}", f"{searchDate}")
        storagePath = os.path.join(storageDirectory, fileId.replace("/", "_") + ".pdf")

        if court not in COURTS:
            continue
        downloadPdf(downloadUrl, storageDirectory, storagePath, fileId)


if __name__ == '__main__':
    print("===", "SID eingeben", "===")
    SID = input("SID:")
    lastPageNumber = getMaximumNumbersOfPages(SID)
    for pageNumber in range(0, int(lastPageNumber) + 1):
        time.sleep(TIMEOUT_PER_PAGE_IN_SECONDS)
        print("===", "Starte Download Seite", pageNumber, "===")
        downloadPage(SID, pageNumber)
        print("===", "Ende Download Seite", pageNumber, "===")
        print("===", "Pause für", TIMEOUT_PER_PAGE_IN_SECONDS, "Sekunden", "===")
