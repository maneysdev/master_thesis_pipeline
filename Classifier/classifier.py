#!/usr/bin/env python

from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn.metrics import precision_score, recall_score, confusion_matrix, classification_report, accuracy_score, f1_score
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
from Classifier.sequencer import Sequencer
import gensim
from sklearn.decomposition import PCA


import numpy as np
import joblib
import re
import string


class Classifier:
    
    stemmer = None
    analyzer = None
    vectorizer = None
    classifier = None
    
    def __init__(self):
        pass
    
    def stemmed_words(self, doc):
        return (self.stemmer.stem(w) for w in self.analyzer(doc))
    
    def set_up(self):
        self.stemmer = SnowballStemmer('german')
        self.analyzer = TfidfVectorizer().build_analyzer()
        self.vectorizer = TfidfVectorizer(stop_words=stopwords.words('german'), analyzer=self.stemmed_words, ngram_range=(1,3))
        #self.vectorizer = CountVectorizer(stop_words='german', analyzer=self.stemmed_words)
    
    def w2v_stemmer(self, doc):
        stemmer = SnowballStemmer("german")
        tokens = word_tokenize(doc)
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return " ".join(stemmed_tokens)
    
    def process_text(self, text):
        text = str(text).lower()
#         text = re.sub(r'[^a-zA-Z ]+', '', text) #ignored because of termin
        text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
        text = " ".join(text.split())
        # text = self.w2v_stemmer(text)
        return text
    
    def generate_w2v(self, data):
        model = gensim.models.Word2Vec(data,
                 vector_size=100
                 # Size is the length of our vector.
                )
        
        # model.wv.most_similar("free")
        sequencer = Sequencer(all_words = [token for seq in data for token in seq],
              max_words = 1000,
              seq_len = 30,
              embedding_matrix = model.wv
             )
        
        x_vecs = np.asarray([sequencer.textToVector(" ".join(seq)) for seq in data])
        print(x_vecs.shape)
        
        pca_model = PCA(n_components=100)
        pca_model.fit(x_vecs)
        print("Sum of variance ratios: ",sum(pca_model.explained_variance_ratio_))
        
        x_comps = pca_model.transform(x_vecs)
        x_comps.shape
        return x_comps
    
    
    
    def generate_initial_vector(self, data):
        return self.vectorizer.fit_transform(data)
    
    def generate_vector(self, data):
        return self.vectorizer.transform(data)
    
    def get_test_train_split(self, dataVector, classLabels):
        return train_test_split(dataVector, classLabels, test_size=0.33, random_state=42)

    def train(self, X_train, y_train):
        self.classifier = svm.SVC(kernel='rbf', C=30, probability=True)
        # self.classifier = svm.SVC(kernel='rbf', C=30, probability=True, decision_function_shape='ovr')
        # self.classifier = svm.SVC(kernel='linear')
        # self.classifier = svm.SVC(kernel='poly', random_state=50, class_weight='balanced')
        # self.classifier = MultinomialNB() #Accuracy 98.32%
        # self.classifier = KNeighborsClassifier(n_neighbors=3)
        # self.classifier = tree.DecisionTreeClassifier(criterion='entropy', max_leaf_nodes=20)
        # self.classifier = RandomForestClassifier(n_estimators=200, random_state=50) 
        self.classifier.fit(X_train, y_train)

    def trainVotingClassifier(self, X_train, y_train):
        model1 = svm.SVC(kernel='rbf', class_weight='balanced', C=30, probability=True)
        model2 = RandomForestClassifier(n_estimators=30, random_state=30)
        model3 = tree.DecisionTreeClassifier()
        # model3 = MultinomialNB()

        # Create a Voting Classifier (Soft Voting)
        self.classifier = VotingClassifier(estimators=[('svc', model1), ('randF', model2), ('dTree', model3)], voting='soft')

        # Fit the Voting Classifier on the training data
        self.classifier.fit(X_train, y_train)
    
    def predict(self, inputVector):
        return self.classifier.predict(inputVector)
    
    def predict_prob(self, inputVector):
        return self.classifier.predict_proba(inputVector)
    
    def classifier_accuracy(self, testActual, pred):
        accuracy = accuracy_score(testActual, pred)
        print("Accuracy: {:.2f}%".format(accuracy * 100))
        
    def calculate_scores(self, y_test, prediction):
        print ('Accuracy: {:.2f}%'.format(accuracy_score(y_test, prediction) * 100 ))
        print ('Recall: {:.2f}%'.format(recall_score(y_test, prediction, average="weighted", zero_division=1) * 100 ))
        print ('Precision: {:.2f}%'.format(precision_score(y_test, prediction, average="weighted", zero_division=1) * 100 ))
        print ('F1 score: {:.2f}%'.format(f1_score(y_test, prediction, average="weighted", zero_division=1) * 100 ))
        
        print ('\n clasification report:\n', classification_report(y_test,prediction))
        print ('\n confussion matrix:\n',confusion_matrix(y_test, prediction))
        
    def save_model(self, path, classifierName, vectorName):
        
        joblib.dump(self.classifier, path + classifierName + ".joblib")
        joblib.dump(self.vectorizer, path + vectorName + ".joblib")
        
    def load_model(self, path, classifierName, vectorName):
        self.classifier = joblib.load(path + classifierName + ".joblib")
        self.vectorizer = joblib.load(path + vectorName + ".joblib")
        
        