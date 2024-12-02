#!/usr/bin/env python

import pandas as pd
import re

class DataEng:
    
    dataframe = pd.DataFrame()
    abschluss = []
    beschreibung = []
    inhalt = []
    ansprechpartner = []
    telefon = []
    fax = []
    email = []
    dauer = []
    ziel = []
    zielgruppe = []
    voraussetzung = []
    termin = []
    unterrichtsart = []
    titles = []
    
    def __init__(self, path):
        self.dataframe = pd.read_csv(path, sep='\t')
    
    def rem_html_amp(self, el):
        el = el.replace('&lt;', '<')
        el = el.replace('&gt;', '>')
        return el.replace('&amp;', '&')
    
    def print_data(self):

        print('###### title ######')
        print('\n')

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "title"):
                print(row['data'])
                print('\n')


        print('###### description ######')
        print('\n')

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                print(row['data'])
                print('\n')

        print('\n')
        print('###### description2 ######')
        print('\n')

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description2"):
                print(row['data'])
                print('\n')

    def get_abschluss(self):
        removeBTags = re.compile(r'<b(.*?)>')
        removeAbsStr = re.compile(r'abschluss:.+?</p>')

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('abschluss:' in data):
                    absch = re.search(removeAbsStr, data)
                    if(absch != None):
                        absch = absch.group()
                        sub_list = ['<br/>', '</b>', '</p>', '<i>', '</i>', '<li>', '</li>']
                        for sub in sub_list:
                            absch = absch.replace(sub, '')
                        absch = absch.replace("<p>zielgruppe:", "")
                        absch = self.rem_html_amp(absch)
                        absch = re.sub(removeBTags, "", absch)
                        self.abschluss.append(absch)

                        replace = {"class" : row['class'], "data" : data.replace(absch, "")}
                        self.dataframe.loc[index] = replace

    def get_ansprechpartner(self):
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('ansprechpartner' in data):
                    result = re.search('ansprechpartner:(.*?)<br/>', data)
                    if(result != None):
                        ansP = str(result.group(1))
                        sub_list = ['</b>', '</i>']
                        for sub in sub_list:
                            ansP = ansP.replace(sub, '')
                        ansP = self.rem_html_amp(ansP)
                        if(ansP != ''):
                            self.ansprechpartner.append("ansprechpartner:" + ansP)
                            replace = {"class" : row['class'], "data" : data.replace(result.group(), "")}
                            self.dataframe.loc[index] = replace
            
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description2"):
                data = str(row['data']).lower()
                if('ansprechpartner' in data):
                    result2 = re.search('ansprechpartner:(.*?)<br/>', data)
                    if(result2 != None):
                        ansP = str(result2.group(1))
                        sub_list = ['</b>', '</i>']
                        for sub in sub_list:
                            ansP = ansP.replace(sub, '')
                        ansP = self.rem_html_amp(ansP)
                        if(ansP != ''):
                            self.ansprechpartner.append("ansprechpartner:" + ansP)
                            replace = {"class" : row['class'], "data" : data.replace(result2.group(), "")}
                            self.dataframe.loc[index] = replace

    def get_telefon(self):
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('telefon' in data):
                    result = re.search('telefon:(.*?)<br/>', data)
                    if(result != None):
                        tel = str(result.group(1))
                        sub_list = ['</b>', '</i>']
                        for sub in sub_list:
                            tel = tel.replace(sub, '')
                        tel = self.rem_html_amp(tel)
                        if(tel != ''):
                            self.telefon.append("telefon:" + tel)
                            replace = {"class" : row['class'], "data" : data.replace(result.group(), "")}
                            self.dataframe.loc[index] = replace  
                    
            
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description2"):
                data = str(row['data']).lower()
                if('telefon' in data):
                    result2 = re.search('telefon:(.*?)<br/>', data)
                    if(result2 != None):
                        tel = str(result2.group(1))
                        sub_list = ['</b>', '</i>']
                        for sub in sub_list:
                            tel = tel.replace(sub, '')
                        tel = self.rem_html_amp(tel)
                        if(tel != ''):
                            self.telefon.append("telefon:" + tel)
                            replace = {"class" : row['class'], "data" : data.replace(result2.group(), "")}
                            self.dataframe.loc[index] = replace
     
    def get_fax(self):
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description2"):
                data = str(row['data']).lower()
                if('fax' in data):
                    result = re.search('fax:(.*?)<br/>', data)
                    if(result != None):
                        faxNo = str(result.group(1))
                        sub_list = ['</b>', '</i>']
                        for sub in sub_list:
                            faxNo = faxNo.replace(sub, '')
                        faxNo = self.rem_html_amp(faxNo)
                        if(faxNo != ''):
                            self.fax.append("fax:" + faxNo)
                            replace = {"class" : row['class'], "data" : data.replace(result.group(), "")}
                            self.dataframe.loc[index] = replace    

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('fax' in data):
                    result2 = re.search('fax:(.*?)<br/>', data)
                    if(result2 != None):
                        faxNo = str(result2.group(1))
                        sub_list = ['</b>', '</i>']
                        for sub in sub_list:
                            faxNo = faxNo.replace(sub, '')
                        faxNo = self.rem_html_amp(faxNo)
                        if(faxNo != ''):
                            self.fax.append("fax:" + faxNo)
                            replace = {"class" : row['class'], "data" : data.replace(result2.group(), "")}
                            self.dataframe.loc[index] = replace

    def get_email(self):
        removeATags = re.compile(r'<a(.*?)>')

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('email' in data):
                    result = re.search('email:(.*?)<br/>', data)
                    if(result != None):
                        eml = str(result.group(1))
                        sub_list = ['</b>', '<i>', '</i>', '</a>']
                        for sub in sub_list:
                            eml = eml.replace(sub, '')
                        eml = re.sub(removeATags, "", eml)
                        eml = self.rem_html_amp(eml)
                        if(eml != ''):
                            self.email.append("email:" + eml)  
                            replace = {"class" : row['class'], "data" : data.replace(result.group(), "")}
                            self.dataframe.loc[index] = replace

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description2"):
                data = str(row['data']).lower()
                if('email' in data):
                    result2 = re.search('email:(.*?)<br/>', data)
                    if(result2 != None):
                        eml = str(result2.group(1))
                        sub_list = ['</b>', '<i>', '</i>', '</a>']
                        for sub in sub_list:
                            eml = eml.replace(sub, '')
                        eml = re.sub(removeATags, "", eml)
                        eml = self.rem_html_amp(eml)
                        if(eml != ''):
                            self.email.append("email:" + eml)
                            replace = {"class" : row['class'], "data" : data.replace(result2.group(), "")}
                            self.dataframe.loc[index] = replace  
    
    def get_dauer(self):
        dauStr = re.compile(r'<b> dauer:(.*)?</p>,')
        voraussetzungStr = r'^(.*?)(?:voraussetzung:|$)'


        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('dauer:' in data):
                    result1 = re.search(dauStr, data)
                    if(result1 != None):
                        dauerB = str(result1.group())
                        if(dauerB != None):
                            dauerBVorRm = re.match(voraussetzungStr, dauerB)
                            if dauerBVorRm:
                                dauerBStr = dauerBVorRm.group(1)                        
                                sub_list = ['<li>', '<b>', '</b>', '<p>', '</p>', ',']
                                for sub in sub_list:
                                    dauerBStr = dauerBStr.replace(sub, '')

                                self.dauer.append(dauerBStr)
                                replace = {"class" : row['class'], "data" : data.replace(result1.group(), "")}
                                self.dataframe.loc[index] = replace

        gesDauStr = re.compile(r'<li>gesamtdauer:(.*)?')
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description2"):
                data = str(row['data']).lower()
                if('dauer:' in data):
                    result = re.search(gesDauStr, data)
                    if(result != None):
                        dauerLi = str(result.group())
                        sub_list = ['<li>', '<b>', '</b>', '<p>', '</p>', ',']
                        for sub in sub_list:
                            dauerLi = dauerLi.replace(sub, '')
                        self.dauer.append(dauerLi)
                        replace = {"class" : row['class'], "data" : data.replace(result.group(), "")}
                        self.dataframe.loc[index] = replace

    def get_ziel(self):
        zielMatchStr = re.compile(r'ziel:(.*?)</p>,')
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('ziel:' in data):
                    result = re.search(zielMatchStr, data)
                    if(result != None):
                        zielStr = str(result.group())
                        sub_list = ['<b>', '</b>', '<p>', '</p>', ',', '<i>', '</i>', '<br/>']
                        for sub in sub_list:
                            zielStr = zielStr.replace(sub, '')
                        zielStr = self.rem_html_amp(zielStr)
                        self.ziel.append(zielStr)
                        replace = {"class" : row['class'], "data" : data.replace(result.group(), "")}
                        self.dataframe.loc[index] = replace
                
        lehrGZielMatchStr = re.compile(r'lehrgangsziel:(.*?)</p>,')
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('lehrgangsziel:' in data):
                    result1 = re.search(lehrGZielMatchStr, data)
                    if(result1 != None):
                        lehrGZielStr = str(result1.group())
                        sub_list = ['<b>', '</b>', '<p>', '</p>', ',', '<i>', '</i>', '<br/>']
                        for sub in sub_list:
                            lehrGZielStr = lehrGZielStr.replace(sub, '')
                        lehrGZielStr = self.rem_html_amp(lehrGZielStr)
                        self.ziel.append(lehrGZielStr)
                        replace = {"class" : row['class'], "data" : data.replace(result1.group(), "")}
                        self.dataframe.loc[index] = replace   

    def get_zielgruppe(self):
        removeBTags = re.compile(r'<b(.*?)>')
        zielGruppeMatchStr = re.compile(r'zielgruppe:(.*?)</p>')

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('zielgruppe:' in data):
                    result1 = re.findall(zielGruppeMatchStr, data)
                    result1 = 'zielgruppe:'+ result1[0]
                    sub_list = ['<b>', '</b>', '<p>', '</p>', '<i>', '</i>', '\x95\t']
                    for sub in sub_list:
                        result1 = result1.replace(sub, '')
                    
                    if "inhalt:" in result1:
                            result1 = result1[:result1.index("inhalt:")]
                    if "vorkenntnisse:" in result1:
                            result1 = result1[:result1.index("vorkenntnisse:")]
                    if "zielsetzung:" in result1:
                            result1 = result1[:result1.index("zielsetzung:")]
                    if "ansprechpartner:" in result1:
                            result1 = result1[:result1.index("ansprechpartner:")]
                    if "referent/in:" in result1:
                            result1 = result1[:result1.index("referent/in:")]
                    if "voraussetzungen:" in result1:
                            result1 = result1[:result1.index("voraussetzungen:")]
                            
                    sub_list = ['<b>', '</b>', '<p>', '</p>', '<i>', '</i>', '\x95\t']
                    for res in result1.split('<br/>'):
                        if(res.strip() != ""):
                            res = res.replace(sub, '')
                            res = re.sub(removeBTags, "", res)
                            self.zielgruppe.append(res)

                    replace = {"class" : row['class'], "data" : data.replace(result1, "")}
                    self.dataframe.loc[index] = replace

    # Must be called before get_voraussetzung()
    def get_termin(self):
        termStr = re.compile(r'<br/><br/>[0-9]+ termin.+?uhr<br/><br/>')
        termStr2 = re.compile(r'<br/><br/>(\d+ termin\(e\))<br/><br/>((.*?) uhr)<br/><br/>')
        termMatchStr3 = re.compile(r'bewerbungstermin:(.*?),')

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('termin:' in data):
                    result1 = re.findall(termMatchStr3, data)
                    if(len(result1) > 0):
                        result1 = 'bewerbungstermin:'+ result1[0]
                        resultTer = result1
                        sub_list = ['<b>', '</b>', '<p>', '</p>']
                        for sub in sub_list:
                            resultTer = resultTer.replace(sub, '')
                        self.termin.append(resultTer)
                        replace = {"class" : row['class'], "data" : data.replace(result1, "")}
                        self.dataframe.loc[index] = replace
                            
                if('termin(e)' in data):
                    resultTerm2 = re.search(termStr2, data)
                    if(resultTerm2 != None):
                        ter2 = resultTerm2.group()
                        for ln in ter2.split('<br/>'):
                            if(ln.strip() != ""):
                                self.termin.append(ln)
                        replace = {"class" : row['class'], "data" : data.replace(ter2, "")}
                        self.dataframe.loc[index] = replace
                    
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description2"):
                data = str(row['data']).lower()
                if('termin' in data):
                    t = re.search(termStr, data)
                    if(t != None):
                        ter = t.group()
                        for ln in ter.split('<br/>'):
                            if(ln.strip() != ""):
                                self.termin.append(ln)
                        replace = {"class" : row['class'], "data" : data.replace(ter, "")}
                        self.dataframe.loc[index] = replace

    def get_voraussetzung(self):
        vorausMatchStr = re.compile(r'voraussetzung:(.*?)</p>')

        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('voraussetzung:' in data):
                    result1 = re.findall(vorausMatchStr, data)
                    result1 = 'voraussetzung:'+ result1[0]
                        
                    if "ansprechpartner:" in result1:
                        result1 = result1[:result1.index("ansprechpartner:")]
                            
                    if "inhalt:" in result1:
                        result1 = result1[:result1.index("inhalt:")]
                        
                    sub_list = ['<b>', '</b>', '<p>', '</p>', '</a>', '<i>', '</i>', 
                                        '<ul>', '</ul>', '<li>', '</li>', '<br/>' '</']
                        
                    for line in re.split(r'<br/>|<li>',result1):
                        result1Repl = line
                        for sub in sub_list:
                            result1Repl = result1Repl.replace(sub, '')
                        result1Repl = self.rem_html_amp(result1Repl)
                            
                        if "<<a href" in result1Repl:
                            result1Repl = result1Repl[:result1Repl.index("<<a href")]
                            
                        self.voraussetzung.append(result1Repl)
                    replace = {"class" : row['class'], "data" : data.replace(result1, "")}
                    self.dataframe.loc[index] = replace

        vorausMatchStr2 = re.compile(r'teilnahmevoraussetzungen:(.*?)(?:</p>|;)')
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('teilnahmevoraussetzungen:' in data):
                    result1 = re.findall(vorausMatchStr2, data)
                    if(len(result1) > 0):
                        result1 = 'teilnahmevoraussetzungen:'+ result1[0]
                        for voraus in re.split('<br/>|<li>', result1):
                            sub_list = ['<b>', '</b>', '<p>', '</p>', '</a>', '<i>', '</i>', 
                                    '<ul>', '</ul>', '<li>', '</li>', '<br/>']
                            for sub in sub_list:
                                voraus = voraus.replace(sub, '')
                            voraus = self.rem_html_amp(voraus)
                            self.voraussetzung.append(voraus)
                    replace = {"class" : row['class'], "data" : data.replace(result1, "")}
                    self.dataframe.loc[index] = replace
                            
        vorausMatchStr3 = re.compile(r'technische voraussetzung:(.*?)</p>')
        vorausMatchStr4 = re.compile(r'technische voraussetzungen:(.*?)</p>')
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('technische voraussetzung' in data):
                    result1 = re.findall(vorausMatchStr3, data)
                    if(len(result1) > 0):
                        result1 = 'technische voraussetzung:'+ result1[0]
                        for voraus in result1.split('<br/>'):
                            voraus = self.rem_html_amp(voraus)
                            self.voraussetzung.append(voraus)
                        replace = {"class" : row['class'], "data" : data.replace(result1, "")}
                        self.dataframe.loc[index] = replace

                    result2 = re.findall(vorausMatchStr4, data)
                    if(len(result2) > 0):
                        result2 = 'technische voraussetzungen:'+ result2[0]
                        for voraus in result2.split('<br/>'):
                            voraus = self.rem_html_amp(voraus)
                            self.voraussetzung.append(voraus)
                        replace = {"class" : row['class'], "data" : data.replace(result2, "")}
                        self.dataframe.loc[index] = replace   

    def get_unterichtsart(self):
        unterichtartMatchStr = re.compile(r'unterrichtsart(.*?)(</p>)(.*?)(</p>)')
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                if('unterrichtsart' in data):
                    u = re.search(unterichtartMatchStr, data)
                    sub_list = ['</b>', '<p>', '</p>']
                    ustr = u[0]
                    for sub in sub_list:
                        ustr = ustr.replace(sub, '')

                    self.unterrichtsart.append(ustr)            


    def get_titles(self):
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "title"):
                self.titles.append(row['data'])

    def get_beschreibung(self):
        removeBTags = re.compile(r'<b(.*?)>')
        removeATags = re.compile(r'<a(.*?)>')
        removeUlTags = re.compile(r'<ul(.*?)>')
        removeLiTags = re.compile(r'<li(.*?)>')
        removeVorStr = re.compile(r'voraussetzungen:(.*)')
        removeAbsStr = re.compile(r'abschlüsse:(.*)')
        zgAbsStr = re.compile(r'zielgruppe:(.*)')
        removeTermStr = re.compile(r'<br/><br/>[0-9]+ termin.+?:[0-9][0-9]')
        inhaltStr = re.compile(r'((\w+|^|)inhalte:)')
        vorKntStr = re.compile(r'(vorkenntnisse:[^.]+).')
        inhAnyStr = re.compile(r'\s(.*?)inhalte:')

        sub_list = ['<p>', '</p>', '<b>', '</b>', '<i>', '</i>', '</a>', '<ul>', '</ul>', '<li>', '</li>']

            
        for index, row in self.dataframe.iterrows():
            if(row['class'] == "description"):
                data = str(row['data']).lower()
                for p in data.split("<p>"):
                    if('inhalte:' in p):
                        inhalteLst = re.findall(inhaltStr, p)
                        inhWord = inhalteLst[0][0]
                        pW = p.split(inhWord)
                        
                        if(pW[0] != ""):
                            besch = re.sub(removeBTags, "", pW[0])
                            besch = re.sub(removeVorStr, "", besch)
                            
                            sub_list = ['<p>', '</p>', '<b>', '</b>', '<i>', '</i>', '</a>', '<ul>', '</ul>', '<li>', '</li>']
                            for sub in sub_list:
                                besch = besch.replace(sub, '')
                            for ln in besch.split('<br/>'):
                                if(ln.strip() != ""):
                                    ln = re.sub(removeATags, "", ln.strip())
                                    ln = re.sub(removeUlTags, "", ln)
                                    ln = re.sub(removeLiTags, "", ln)
                                    self.beschreibung.append(ln)
                        
                        if(len(pW)> 1 and pW[1] != ""):
                            combWd = inhWord + " " + pW[1]
                            combWd = re.sub(removeTermStr, "", combWd)
                            vorkntStr = re.search(vorKntStr, combWd)
                            if(vorkntStr != None):
                                self.beschreibung.append(vorkntStr.group())
                                combWd = combWd.replace(vorkntStr.group(), '')
                            for ln2 in combWd.split('<br/>'):
                                if(ln2.strip() != ""):
                                    inh = re.sub(removeAbsStr, "", ln2)
                                    inh = re.sub(zgAbsStr, "", inh)
                                    for sub in sub_list:
                                        inh = inh.replace(sub, '')
                                        
                                    for ln3 in inh.split(' - '):
                                        ln3 = re.sub(removeATags, "", ln3.strip())
                                        ln3 = re.sub(removeUlTags, "", ln3)
                                        ln3 = re.sub(removeLiTags, "", ln3)
                                        self.inhalt.append(ln3)

    def pack_data(self):
        titleDf = pd.DataFrame(list(zip(self.titles, ['Titel' for i in range(len(self.titles))])),
               columns =['data', 'class'])

        termineDf = pd.DataFrame(list(zip(self.termin, ['Termine' for i in range(len(self.termin))])),
                    columns =['data', 'class'])

        voraussetzungDf = pd.DataFrame(list(zip(self.voraussetzung, ['Voraussetzungen' for i in range(len(self.voraussetzung))])),
                    columns =['data', 'class'])

        zielgruppeDf = pd.DataFrame(list(zip(self.zielgruppe, ['Zielgruppe' for i in range(len(self.zielgruppe))])),
                    columns =['data', 'class'])

        zielDf = pd.DataFrame(list(zip(self.ziel, ['Ziele' for i in range(len(self.ziel))])),
                    columns =['data', 'class'])

        dauerDf = pd.DataFrame(list(zip(self.dauer, ['Dauer' for i in range(len(self.dauer))])),
                    columns =['data', 'class'])

        emailDf = pd.DataFrame(list(zip(self.email, ['Email' for i in range(len(self.email))])),
                    columns =['data', 'class'])

        faxDf = pd.DataFrame(list(zip(self.fax, ['Fax' for i in range(len(self.fax))])),
                    columns =['data', 'class'])

        telefonDf = pd.DataFrame(list(zip(self.telefon, ['Telefon' for i in range(len(self.telefon))])),
                    columns =['data', 'class'])

        ansprechpartnerDf = pd.DataFrame(list(zip(self.ansprechpartner, ['Ansprechpartner' for i in range(len(self.ansprechpartner))])),
                    columns =['data', 'class'])

        inhaltDf = pd.DataFrame(list(zip(self.inhalt, ['Inhalt' for i in range(len(self.inhalt))])),
                    columns =['data', 'class'])

        beschreibungDf = pd.DataFrame(list(zip(self.beschreibung, ['Beschreibung' for i in range(len(self.beschreibung))])),
                    columns =['data', 'class'])

        abschlussDf = pd.DataFrame(list(zip(self.abschluss, ['Abschluss' for i in range(len(self.abschluss))])),
                    columns =['data', 'class'])
        
        unterrichtsartDf = pd.DataFrame(list(zip(self.unterrichtsart, ['Unterrichtsart' for i in range(len(self.unterrichtsart))])),
                    columns =['data', 'class'])

        df = pd.concat([titleDf, termineDf, voraussetzungDf, zielgruppeDf, zielDf, dauerDf, emailDf, faxDf, telefonDf, ansprechpartnerDf, inhaltDf, 
                        beschreibungDf, abschlussDf, unterrichtsartDf])
        
        return df.sample(frac = 1)