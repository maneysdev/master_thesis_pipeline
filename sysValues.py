from enum import Enum
import os

"""SysValues will store the global enums.
SysValues file can be imported globally within the project.

Author: manendra
Version: 1.0
"""
class SysValues(Enum):
    # MODEL_FOLDER_PATH = "{}/".format(os.path.abspath("./models/")) 
    # CLASSIFIER_NAME= "VOTE_down_tfidf_no_title_January-07-2024"
    # VECTOR_NAME= "VOTE_down_tfidf_vec_no_title_January-07-2024"
    MODEL_FOLDER_PATH = "{}/".format(os.path.abspath("./models/")) 
    # CLASSIFIER_NAME= "RF__tfidf_07_01_24"
    # VECTOR_NAME= "RF__tfidf_vec_07_01_24"
    # CLASSIFIER_NAME= "VOTE_down_tfidf_no_title_January-07-2024_JUL19"
    # VECTOR_NAME= "VOTE_down_tfidf_vec_no_title_January-07-2024_JUL19"
    
    # CLASSIFIER_NAME= "RF_down_tfidf_no_title_January-07-2024_JUL19"
    # VECTOR_NAME= "RF_down_tfidf_vec_no_title_January-07-2024_JUL19"
    
    CLASSIFIER_NAME= "SVM_RBF_down_tfidf_no_title_January-07-2024_JUL19"
    VECTOR_NAME= "SVM_RBF_down_tfidf_vec_no_title_January-07-2024_JUL19"
    
    # CLASSIFIER_NAME= "SVM_RBF_down_w2v_no_title_January-07-2024_JUL19"
    # VECTOR_NAME= "SVM_RBF_down_w2v_vec_no_title_January-07-2024_JUL19"
    
    # CLASSIFIER_NAME= "SVM_RBF_down_tfidf_no_title_January-07-2024_JUL19_ovo"
    # VECTOR_NAME= "SVM_RBF_down_tfidf_vec_no_title_January-07-2024_JUL19_ovo"
    
    # CLASSIFIER_NAME= "SVM_poly_down_tfidf_no_title_January-07-2024_JUL19"
    # VECTOR_NAME= "SVM_poly_down_tfidf_vec_no_title_January-07-2024_JUL19"
    
    # CLASSIFIER_NAME= "DTREE_down_tfidf_no_title_January-07-2024_JUL19"
    # VECTOR_NAME= "DTREE_down_tfidf_vec_no_title_January-07-2024_JUL19"
    
    # CLASSIFIER_NAME= "KNN_down_tfidf_no_title_January-07-2024_JUL19"
    # VECTOR_NAME= "KNN_down_tfidf_vec_no_title_January-07-2024_JUL19"
    
    # CLASSIFIER_NAME= "NB_down_tfidf_no_title_January-07-2024_JUL19"
    # VECTOR_NAME= "NB_down_tfidf_vec_no_title_January-07-2024_JUL19"
    
    DATA_WRITE_PATH= r"/Users/manendraranathunga/Documents/Thesis/predictions/SVM/new2/"
    CHROME_DRIVER= r"/opt/homebrew/bin/chromedriver"
    TESSERACT= r""
    
