#!/usr/bin/env python3

import requests
from requests.adapters import HTTPAdapter, Retry
import os
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class ScraperMain:
    
    domainUrl = ''
    currentUrl = ''
    currentPage = ''
    soup = ''
    
    def __init__(self, domainUrl):
        self.domainUrl = domainUrl
        
    def set_current_url(self, currentUrl):
        self.currentUrl = currentUrl
        
    def get_page(self, url):
        s = requests.Session()
        retries = Retry(total=50,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

        s.mount('http://', HTTPAdapter(max_retries=retries))

        self.currentPage = s.get(url, verify=False)
        self.soup = BeautifulSoup(self.currentPage.text, 'html.parser')
        
    @abstractmethod
    def url_extractor(self):
        pass