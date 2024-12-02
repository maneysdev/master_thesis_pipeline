#!/usr/bin/env python3

from .scraperMain import ScraperMain

class Scraper(ScraperMain):
    
    data = []
        
    def __init__(self, domainUrl):
        ScraperMain.__init__(self, domainUrl)
        
    def scrape(self):
        row = {}
        
        titleHtml = self.soup.find("h1", {"class": "wisyr_kurstitel"})
        if (titleHtml != None and titleHtml.text != None):
            row['title'] = titleHtml.text
        
        descriptionHtml = self.soup.find("div", {"itemprop": "description"})
        
        infoLists = ""
        
        if(descriptionHtml != None):
            infoParagraphs = descriptionHtml.findAll('p')
            infoLists = descriptionHtml.findAll('ul')
        else:
            infoParagraphs = ""
        
        row["description"] = infoParagraphs
        
        if infoLists != None: 
            row["description2"] = infoLists
        self.data.append(row)