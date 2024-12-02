#!/usr/bin/env python3
from OntologyMapper.graph import GraphDesigner
from Scraper.crawler import Crawler
from Scraper.scraper import Scraper
from Utils.fileWriter import DataWriter
from DataEngineering.dataEng import DataEng
from DataEngineering.dataVisual import DataVisual
from Classifier.classifier import Classifier
from Scraper.ocr import OCR
from OntologyMapper.ontologyMapper import OntologyMapper
from sysValues import SysValues

import sys
import os
import pandas as pd
from datetime import date
import re

clf = None
today = date.today().strftime('%B-%d-%Y')
files = []

def writeFile(data, path, df=True):
    writer = DataWriter()
    if(df):
        writer.set_pandas_df(data)
        writer.write_csv(path)
    else:
        writer.write_json(path, data)

def readFiles(path):
    if os.path.isdir(path):
        global files
        files = os.listdir(path)

def checkIfScanned(file):
    if(file + ".json" in files):
        return True
    else:
        return False

def crawl(mainUrl="https://weiterbildungsportal.rlp.de"):
    crawler = Crawler(mainUrl)
    crawler.get_page(crawler.domainUrl)
    crawler.url_extractor()

    for url in crawler.courseListUrlQue:
        crawler.set_current_url("/"+url)
        while crawler.currentUrl is not None :
            crawler.get_page(crawler.domainUrl+crawler.currentUrl)
            crawler.addvt_url_extractor()
            crawler.get_next_page()

    scraper = Scraper(mainUrl)
    for url in crawler.urlQueue: 
        scraper.get_page(scraper.domainUrl+url)
        scraper.url_extractor()
        scraper.scrape()

    titles = []
    description = []
    description2 = []
    for obj in scraper.data:
        titles.append(obj['title'])
        description.append(obj['description'])
        description2.append(obj['description2'])
            
            
    title = pd.DataFrame(list(zip(titles, ['title' for i in range(len(titles))])),
                columns =['data', 'class'])
    desc = pd.DataFrame(list(zip(description, ['description' for i in range(len(description))])),
                columns =['data', 'class'])
    desc2 = pd.DataFrame(list(zip(description2, ['description2' for i in range(len(description2))])),
                columns =['data', 'class'])

    df = pd.concat([title, desc, desc2])

    writeFile(df, "/Users/manendraranathunga/Documents/Thesis/df_" + today + ".csv")

def dataCleanUp():
    dataEng = DataEng("/Users/manendraranathunga/Documents/Thesis/df_January-07-2024.csv")
    dataEng.print_data()
    dataEng.get_abschluss()
    dataEng.get_beschreibung()
    dataEng.get_ansprechpartner()
    dataEng.get_telefon()
    dataEng.get_fax()
    dataEng.get_email()
    dataEng.get_dauer()
    dataEng.get_ziel()
    dataEng.get_zielgruppe()
    dataEng.get_termin()
    dataEng.get_voraussetzung()
    dataEng.get_unterichtsart()
    dataEng.get_titles()
    df = dataEng.pack_data()

    writeFile(df, "/Users/manendraranathunga/Documents/Thesis/df_eng_January-07-2024.csv")

def dataVisualNSampling():
    dataVis = DataVisual("/Users/manendraranathunga/Documents/Thesis/df_eng_January-07-2024.csv")
    dataVis.gen_wordCloud()
    dataVis.gen_barPlot()
    df = dataVis.data_normalization()

    writeFile(df, "/Users/manendraranathunga/Documents/Thesis/df_down_samp__no_title_January-07-2024.csv")

def trainClassifier():
    df = pd.read_csv("/Users/manendraranathunga/Documents/Thesis/df_down_samp__no_title_January-07-2024.csv", sep='\t')
    print("CSV Loading Complete !")
    clf = Classifier()
    clf.set_up()
    print("Classifier Setup Complete !")
    df["clean_text"] = df.data.map(clf.process_text)
    print("Text Cleaning Complete !")
    vector1 = clf.generate_initial_vector(df["clean_text"])
    print("Vectorization Complete !")
    classLabels = df['label']
    X_train, X_test, y_train, y_test = clf.get_test_train_split(vector1, classLabels)
    print("Train/Test Data Split Complete !")
    # clf.trainVotingClassifier(X_train, y_train)
    clf.train(X_train, y_train)
    print("Training Complete !")
    # clf.save_model("/Users/manendraranathunga/Documents/Thesis/models/", "VOTE_down_tfidf_no_title_January-07-2024_JUL19", "VOTE_down_tfidf_vec_no_title_January-07-2024_JUL19")
    clf.save_model(SysValues.MODEL_FOLDER_PATH.value, SysValues.CLASSIFIER_NAME.value, SysValues.VECTOR_NAME.value)
    print("Saving Model Complete !")
    y_pred = clf.predict(X_test)
    clf.calculate_scores(y_test, y_pred)
    print("Score Calculations Complete !")

def readNewData(mainUrl="https://weiterbildungsportal.rlp.de"):

    clf = Classifier()
    clf.set_up()
    # gD = GraphDesigner()
    # onTMap = OntologyMapper(gD)
    # onTMap.load()
    # print("mapper loaded")
    # clf.load_model("/Users/manendraranathunga/Documents/Thesis/models/", "SVM_RBF_FULL_tfidf_" + today, "SVM_RBF_FULL_tfidf_vec_" + today)
    clf.load_model(SysValues.MODEL_FOLDER_PATH.value, SysValues.CLASSIFIER_NAME.value, SysValues.VECTOR_NAME.value)

    crawler = Crawler(mainUrl)
    # crawler.currentUrl = "/search/?q=Datum%3Aheute"
    # crawler.currentUrl = "/search?qs=Java&qf=datum%3Aheute&filter_datum_von=heute&filter_preis=&filter_preis_von=&filter_preis_bis=1000&filter_bei=&filter_dauer_von=&filter_dauer_bis=&filter_tageszeit=&filter_foerderung=&filter_zielgruppe=&filter_qualitaetszertifikat=&filter_unterrichtsart=&filter_order=b"
    # crawler.currentUrl = "/search?qs=Philosophie+Religion&qf=datum%3Aheute&filter_datum_von=heute&filter_preis=&filter_preis_von=&filter_preis_bis=&filter_bei=Koblenz&filter_km=&filter_dauer_von=&filter_dauer_bis=&filter_tageszeit=&filter_foerderung=&filter_zielgruppe=&filter_qualitaetszertifikat=&filter_unterrichtsart=&filter_order=b"
    crawler.currentUrl = "/search?qs=Hauptschulabschluss&qf=&qtrigger=h"
    while crawler.currentUrl is not None :
        print(crawler.domainUrl+crawler.currentUrl)
        crawler.get_page(crawler.domainUrl+crawler.currentUrl)
        crawler.addvt_url_extractor()
        crawler.get_next_page()

    # crawler.urlQueue.append("/k1003976901?q=Datum%3Aheute")
    

    for url in crawler.urlQueue:

        idUrl = url 
        idUrl = idUrl.replace("%3A", "")
        id = re.sub(r'\D', '', idUrl)

        if(not checkIfScanned(id)):
            dataObj = {}
            dataObj["id"] = id
            dataObj["classifierOut"] = []
            print(crawler.domainUrl+url)
            ocr = OCR(crawler.domainUrl+url)
            lineOne = False
            for line in ocr.get_lines():
                stripped = line.strip()
                if(stripped != ""):
                    if(not lineOne):
                        data = {"actual_sentence": line.strip(), "predictions": [{"class": "Titel", "percentage": 1.0}]}
                        dataObj["classifierOut"].append(data)
                        lineOne = True
                    else:
                        stripped = clf.process_text(stripped)
                        stemmed = clf.stemmed_words(stripped)
                        stemmed_words_string = ' '.join(stemmed)
                        vector = clf.generate_vector([stemmed_words_string])
                        pred = clf.predict_prob(vector)[0]
                        classes = clf.classifier.classes_
                        
                        wrappedObj = [{"Class": x, "Percentage": y} for x, y in zip(classes, pred)]
                        sorted_data = sorted(wrappedObj, key=lambda x: x['Percentage'], reverse=True)
                        
                        # Get the first two objects
                        first_two = sorted_data[:2]

                        # Calculate the total of value2 for the remaining objects
                        remaining_total = sum(item['Percentage'] for item in sorted_data[2:])

                        # Create a new object with the total
                        result = {'Class': 'Unspecified', 'Percentage': remaining_total}

                        # Combine the first two objects with the new object
                        combined_data = first_two + [result]
                        
                        data = {"actual_sentence": line.strip(), "predictions": combined_data}
                        dataObj["classifierOut"].append(data)
            
            # onTMap.writeCourse(dataObj)
            #complete by adding the pred and saving them into files
            writeFile(dataObj, SysValues.DATA_WRITE_PATH.value + id +".json", False)
    print("Predicting new data complete !")
    

def default():
    print("Invalid Argument !")

def switch_case(case_value):
    switch_dict = {
        1: crawl,
        2: dataCleanUp,
        3: dataVisualNSampling,
        4: trainClassifier,
        5: readNewData,
    }

    # Get the function for the given case_value or default_case if not found
    selected_case = switch_dict.get(case_value, default)
    
    # Call the selected function and return the result
    result = selected_case()
    return result


#Enter one of the following numbers as an argument to execute the relevant command 
# Refer the switch case for the relevant argument

if __name__ == "__main__":

    readFiles(SysValues.DATA_WRITE_PATH.value)

    if len(sys.argv) > 1:
        switch_case(int(sys.argv[1]))
    else:
        print("Argument not provided !")


