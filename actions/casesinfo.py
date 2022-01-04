from bs4 import BeautifulSoup
import requests, pytz, math
import datetime as dt
from threading import Thread


def getTimeZone(tz):
    melb_tz = pytz.timezone(tz)
    now = dt.datetime.now()
    now_adj = now.astimezone(melb_tz)
    timeAdj = now_adj.strftime("%B %d, %Y %I:%M %p")
    return timeAdj


def getVicWebSoup():
    base = "https://www.coronavirus.vic.gov.au/"
    response = requests.get(base)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def getNSWWebSoup():
    base = "https://www.health.nsw.gov.au/Infectious/covid-19/Pages/default.aspx"
    response = requests.get(base)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


class CovidCases(Thread):
    def __init__(self):
        super().__init__()
        self.vic_soup = getVicWebSoup()
        self.nsw_soup = getNSWWebSoup()

    def outputVic(self):
        melbCases = self.vic_soup.find_all(
            "div", class_="ch-daily-update__statistics-item-text"
        )[4].text
        time = getTimeZone("Australia/Melbourne")
        return (
            melbCases
            + " cases acquired in Victoria (Last 24 hours) (Last updated: "
            + time
            + ")"
        )

    def vicProgressBar(self):
        vaxProgressText = self.vic_soup.find_all(
            "div", class_="ch-daily-update__statistics-item-text"
        )[1].text
        vaxStr = float(vaxProgressText.strip("%"))
        full = False
        if vaxStr >= 90:
            denom = 100
        elif vaxStr >= 80:
            denom = 90
        if vaxStr >= 99:
            full = True
        fillCount = vaxStr / denom * 20
        roundCount = math.floor(fillCount)
        block = "\u25a0"
        emptyBlock = "\u25a1"
        progressBar = roundCount * block + (20 - roundCount) * emptyBlock
        if full == True:
            progressResult = "gg"
        else:
            progressResult = (
                "VIC - Fully vaccinated: "
                + progressBar
                + " "
                + vaxProgressText
                + " / "
                + str(denom)
                + "%"
            )
        return progressResult

    def outputNSW(self):
        time = getTimeZone("Australia/Melbourne")
        NSWCases = self.nsw_soup.find_all("span", class_="number")[0].text
        return (
            NSWCases
            + " cases acquired in NSW (Last 24 hours) (Last updated: "
            + time
            + ")"
        )

    def run(self):
        victoria_cases = self.outputVic()
        vic_progress_bar = self.vicProgressBar()
        nsw_cases = self.outputNSW()
        return [vic_progress_bar, victoria_cases, nsw_cases]
