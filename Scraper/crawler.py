#!/usr/bin/env python3

from .scraperMain import ScraperMain

class Crawler(ScraperMain):
    
    courseListUrlQue = []
    urlQueue = []
    
    def __init__(self, domainUrl):
        ScraperMain.__init__(self, domainUrl)
        
    def url_extractor(self):
        menus = self.soup.find("ul", {"class": "dropdown dropdown-horizontal"})
        courseMenuList = menus.select('ul > li')[1].select('ul > li > a')
        for i, courseCat in enumerate(courseMenuList):
            if i > 0 and courseCat['href'] != "javascript:;":
                self.courseListUrlQue.append(courseCat['href'])
                        
    def addvt_url_extractor(self):
        dataTable = self.soup.find("table", {"class": "wisy_list wisyr_kursliste"})
        if(dataTable != None):
            for i, row in enumerate(dataTable.find_all('tr')):
                if i > 0:
                    self.urlQueue.append(row.find_all('td')[0].find('a')['href'])
                    # print(row.find_all('td')[0].find('a')['href'])
    
    def get_next_page(self):
        if (self.soup.find("a", {"class": "wisy_paginate_next"})) is not None :
            self.currentUrl = (self.soup.find("a", {"class": "wisy_paginate_next"})['href'])[1:] 
            print(self.currentUrl)
        else:
            self.currentUrl = None
