"""Importing Modules"""
import json
from io import BytesIO
import base64
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import numpy as np
from pandas import json_normalize
import streamlit as st

# In[2]:
def app_follow_data_extraction(endpoint_url, key):
    """Function to authenticate with AppFollow API and Extracting Data"""
    response = requests.get(endpoint_url, auth=HTTPBasicAuth(key, ""))
    return response.text
# In[2]:
def external_ids_fetcher(endpoint_url, key, os):
    """Function creates a dataframe for the extracted data"""
    try:
        response = requests.get(endpoint_url, auth=HTTPBasicAuth(key, ""))
        data = response.text
        # if response.status_code == 404:
        #     st.error('Please provide the correct API KEY')
        # if 'Bad request' in data:
        #     st.error('Please provide the API KEY in input')
        afjdata = json.loads(data)
        af_df = json_normalize(afjdata["apps_app"])
    except:
        st.stop()

    if os == 'ios':
        af_df = af_df[af_df["app.artist_name"].str.contains('skidos', case = False)]
        external_ids = af_df[['app.ext_id','app.title']]
        external_ids.reset_index(drop=True, inplace=True)
    elif os == 'android':
        af_df = af_df[af_df["app.ext_id"].str.contains('skidos', case = False)]
        external_ids = af_df['app.ext_id'].tolist()
    return external_ids
# In[3]:
def pre_processing_data(data):
    """Function for processing of data & creates a dataframe for the extracted data"""
    afjdata = json.loads(data)
    af_df = json_normalize(afjdata["keywords"])
    list_null = af_df['list'].iloc[0]
    if list_null:
        for i in af_df['list']:
            position_keywords = i
        dataframe = pd.DataFrame(position_keywords)
        dataframe.drop(labels=['score','difficulty','effectiveness'],axis=1, inplace = True)
        dataframe.rename(columns={'device':'Device','date':'Date','popularity':'Popularity',
                                  'pos':'Rank','kw':'Keyword','country':'Country'},
                         inplace = True)
        return dataframe
# In[4]:
def sorting_data(data):
    """Function for sorting of dataframe"""
    keyword_rank_1 = np.sum(data['Rank'] == 1)
    keyword_rank_2_to_5 = np.sum((data['Rank']>=2)&(data['Rank']<=5))
    keyword_rank_6_to_10 = np.sum((data['Rank']>=6)&(data['Rank']<=10))
    keyword_rank_11_to_20 = np.sum((data['Rank']>=11)&(data['Rank']<=20))
    keyword_rank_21_to_50 = np.sum((data['Rank']>=21)&(data['Rank']<=50))
    total_ranked_keywords = data['Rank'].count()
    high_volume_keyword = np.sum((data['Popularity']>=50)&((data['Rank']>=1)&
                                                           (data['Rank']<=20)))
    medium_volume_keyword = np.sum(((data['Popularity']>=30)&(data['Popularity']<=49))&
                                   ((data['Rank']>=1)&(data['Rank']<=15)))
    low_volume_keyword = np.sum(((data['Popularity']>=10)&(data['Popularity']<=29))&
                                ((data['Rank']>=1)&(data['Rank']<=10)))
    high_volume_keyword_list = data.loc[(data['Popularity']>=50)&
                                        ((data['Rank']>=1)&(data['Rank']<=20))]
    medium_volume_keyword_list = data.loc[((data['Popularity']>=30)&(data['Popularity']<=49))&
                                          ((data['Rank']>=1)&(data['Rank']<=15))]
    low_volume_keyword_list = data.loc[((data['Popularity']>=10)&(data['Popularity']<=29))&
                                       ((data['Rank']>=1)&(data['Rank']<=10))]
    dataframe = pd.DataFrame([keyword_rank_1,keyword_rank_2_to_5,keyword_rank_6_to_10,
                              keyword_rank_11_to_20,keyword_rank_21_to_50,total_ranked_keywords,
                              high_volume_keyword, medium_volume_keyword, low_volume_keyword],
                             index=['Keyword Rank = 1','Keyword Rank = 2 to 5',
                             'Keyword Rank = 6 to 10','Keyword Rank = 11 to 20',
                             'Keyword Rank = 21 to 50','Total Ranked Keywords',
                             'High Volume Keywords', 'Medium Volume Keywords',
                             'Low Volume Keywords'],
                             columns=['Count'])
    data = pd.concat([dataframe, high_volume_keyword_list,
                      medium_volume_keyword_list, low_volume_keyword_list],
                      keys=['Count', 'high_volume_keyword_list',
                      'medium_volume_keyword_list','low_volume_keyword_list'])
    data = data.reset_index()
    index_value = data[data['level_1']=='Low Volume Keywords'].index.values[0] + 1
    data.loc[index_value:, 'level_1'] = np.nan
    data.rename(columns={'level_0':'Keys','level_1':'Keyword_Ranks'}, inplace=True)
    data.set_index(['Keys','Keyword_Ranks'], inplace=True)
    return data

def to_excel(df):
    """Proccesses the data to be downloaded in a xlsx format
    in:  dataframe
    out: processed dataframe
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=True, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df,name):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    b64 = base64.b64encode(df)  # val looks like b'...'
    link = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{name}.xlsx">📥 Download {name} Result</a>' # decode b'abc' => abc
    # $('<a href="data:text/csv;base64,{b64}" download="{name}">')[0].click()
    dl_link = f"""
    <html>
    <head>
    <title>Start Auto Download file</title>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:application/octet-stream;base64,{b64.decode()}" download="{name}.xlsx">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link,link
