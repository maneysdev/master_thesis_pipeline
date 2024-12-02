#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np

class DataVisual:

    dataframe = pd.DataFrame()

    def __init__(self, path):
        self.dataframe = pd.read_csv(path, sep='\t')
        self.dataframe.info()
        self.dataframe.rename(columns={'class':'label'}, inplace=True)
        self.dataframe.head()
        self.dataframe.describe()
        self.dataframe.groupby('label').describe().T

    def gen_wordCloud(self):
        df3 = self.dataframe.copy()
        aggregation_functions = {'data': 'sum'}
        df_new = df3.groupby(df3['label']).aggregate(aggregation_functions)
        df4 = pd.DataFrame(df_new)

        headings = list(set(df3['label'].tolist()))
        headings.sort()

        x, y = np.ogrid[:1000, :1000]
        mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
        mask = 255 * mask.astype(int)

        wordcloud = WordCloud(background_color="white", mask=mask, contour_width=0.5, 
                            contour_color="black",  max_font_size=100, random_state=42,
                            colormap="Dark2")

        i=1 
        for row in df4:
            for ln in df4[row]:
        #         Create and generate a word cloud image:
                wordcloud = WordCloud().generate(ln)
                plt.subplot(5, 4, i)
                # Display the generated image:
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.title(headings[i-1])
                plt.axis("off")
                i=i+1
                
            plt.show()

    def gen_barPlot(self):
        df2 = self.dataframe.copy()
        label = df2.groupby("label")

        # Summary statistic of all labels
        label.describe()

        plt.figure(figsize=(15,10))
        label.size().sort_values(ascending=False).plot.bar()
        plt.xticks(rotation=50)
        plt.title("Original data")
        plt.xlabel("Label")
        plt.ylabel("Number of Words")
        plt.show()

    #This must be modified as per the data set
    def data_normalization(self):
        df5 = self.dataframe.copy()

        dfCopy = self.dataframe.copy()

        # Identify the first occurrences and the last occurrences
        first_occurrences = ~dfCopy.duplicated(keep='first')
        last_occurrences = ~dfCopy.duplicated(keep='last')

        # Filter the DataFrame to keep both first and last occurrences
        df5 = dfCopy[first_occurrences | last_occurrences]

        # Reset the index of the resulting DataFrame
        df5 = df5.reset_index(drop=True)

        # df5 = df.copy().drop_duplicates(keep="first", subset=["data"]) 
        len(df5)
        print(df5.sort_values("data"))


        # In[11]:


        # Groupby by label
        label2 = df5.groupby("label")

        # Summary statistic of all labels
        label2.describe()


        # In[12]:


        plt.figure(figsize=(15,10))
        label2.size().sort_values(ascending=False).plot.bar()
        plt.xticks(rotation=50)
        plt.title("Duplicates excluded from the original data")
        plt.xlabel("Label")
        plt.ylabel("Number of Data Points")
        plt.show()


        # In[13]:


        print(df5.groupby('label').size())
        print('\n\n')
        print('Ziele')
        print(df5.groupby('label').size()['Ziele'])


        # In[14]:


        inhaltDf = df5.sample(n = df5.groupby('label').size()['Ziele'], random_state = 44)
        # inhaltDf
        print(inhaltDf.groupby('label').size())


        # In[15]:


        df6 = None
        for name, group in df5.groupby('label'):
            if(str(name) == "Inhalt"):
                df6 = pd.DataFrame(group).sample(frac = 1)
                
        df6


        # In[16]:


        df_filterd=df5.copy().groupby('label').filter(lambda x:(x.name != 'Inhalt'))
        df_filterd


        # In[17]:


        inhaltDf = df6.sample(n = df5.groupby('label').size()['Ziele'], random_state = 44)
        # inhaltDf
        print(inhaltDf.groupby('label').size())
        inhaltDf


        # In[18]:


        downsampled = [df_filterd, inhaltDf]
        downsampledDF = pd.concat(downsampled)
        downsampledDF


        # In[19]:


        downsampledDF.groupby('label').describe().T


        # In[20]:


        nan_rows = downsampledDF[downsampledDF.isna().any(axis=1)]
        print(len(nan_rows))
        downsampledDF=downsampledDF.dropna()


        # In[21]:


        # Groupby by label
        label3 = downsampledDF.groupby("label")

        # Summary statistic of all labels
        label3.describe()


        # In[22]:


        plt.figure(figsize=(15,10))
        label3.size().sort_values(ascending=False).plot.bar()
        plt.xticks(rotation=50)
        plt.title("Downsampled data")
        plt.xlabel("Label")
        plt.ylabel("Number of Data Points")
        plt.show()


        # In[23]:


        # downsampledDF = downsampledDF.astype({'data':'string', 'label':'string'})

        # downsampledDF['text_length'] = downsampledDF['data'].apply(len)

        # downsampledDF['label_type'] = downsampledDF['label'].map({'Titel':0, 'Inhalt':1, 'Ziele':2, 'Voraussetzungen':3, 'Abschluss':4, 'Dauer':5, 'Zielgruppe':6, 'Termine':7, 'Beschreibung':8, 'Ansprechpartner':9, 'Telefon':10, 'Email':11, 'Fax':12})
        # df_label = downsampledDF['label_type'].values
        # downsampledDF
        # print("Unique values count : "+ str(downsampledDF['label'].nunique()))


        # In[24]:


        # df7 = self.dataframe.copy()
        # not fully downsampled just duplicates excluded
        # df7 = df5
        # df7 = self.dataframe.copy().drop_duplicates()

        df7 = df5
        df7.drop(df7[df7['label'] == "Titel"].index, inplace=True) #removes title
        print(df7)
        df7=df7.dropna()
        df7 = df7.astype({'data':'string', 'label':'string'})
        df7['text_length'] = df7['data'].apply(len)

        df7['label_type'] = df7['label'].map({'Titel':0, 'Inhalt':1, 'Ziele':2, 'Voraussetzungen':3, 'Abschluss':4, 'Dauer':5, 'Zielgruppe':6, 'Termine':7, 'Beschreibung':8, 'Ansprechpartner':9, 'Telefon':10, 'Email':11, 'Fax':12})
        df_label = df7['label_type'].values
        df7.head()
        print("Unique values count : "+ str(df7['label'].nunique()))


        # In[25]:

        return df7
    
    