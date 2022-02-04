# In[1]:
"""Importing Modules"""

import time
from datetime import date    
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from app_follow_functions import *


st.title('App follow data extractor')

# KEY = st.text_input('Access Key')
KEY = st.secrets["Key"]

DATE = st.date_input("Date")

st.write('Date selected:', DATE)

DEVICE = st.selectbox(
    'Device',
    ('ipad', 'iphone', 'android'))

st.write('Device selected:', DEVICE)

COUNTRY = st.selectbox(
    'Country',
    ('AL', 'DZ', 'AO', 'AI', 'AG', 'AR', 'AM', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BW', 'BR', 'BN', 'BG', 'BF', 'KH', 'CA', 'CV', 'KY', 'TD', 'CL', 'CN', 'CO', 'CG', 'CR', 'HR', 'CY', 'CZ', 'DK', 'DM', 'DO', 'EC', 'EG', 'SV', 'EE', 'SZ', 'FJ', 'FI', 'FR', 'GM', 'DE', 'GH', 'GR', 'GD', 'GT', 'GW', 'GY', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IE', 'IL', 'IT', 'JM', 'JP', 'JO', 'KZ', 'KE', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LR', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW', 'MY', 'ML', 'MT', 'MR', 'MU', 'MX', 'FM', 'MD', 'MN', 'MS', 'MZ', 'NA', 'NP', 'NL', 'NZ', 'NI', 'NE', 'NG', 'NO', 'OM', 'PK', 'PW', 'PA', 'PY', 'PE', 'PH', 'PG', 'PL', 'PT', 'QA', 'RO', 'RU', 'KN', 'LC', 'VC', 'ST', 'SA', 'SN', 'RS', 'SC', 'SL', 'SG', 'SK', 'SI', 'SB', 'ZA', 'ES', 'LK', 'SR', 'SE', 'CH', 'TW', 'TJ', 'TZ', 'TC', 'TH', 'TT', 'TN', 'TR', 'TM', 'AE', 'UG', 'UA', 'GB', 'US', 'UY', 'UZ', 'VE', 'VN', 'VG', 'YE', 'ZW')
    ,index=148)

st.write('Country selected:', COUNTRY)

if DATE == date.today():
    st.warning("Please change today's date")
    st.stop()
    
DATE = str(DATE)

time.sleep(7)
# agree = st.checkbox('Download All files Automatically',value=True)

# if agree:
#     st.write('All files will be downloaded, Please allow multiple downloads, when promted!')

if DEVICE == 'android':
    OS = 'android'
    APP_LIST_API = "http://api.appfollow.io/apps/app?apps_id=105810"
    # Android
    with st.spinner("Fecthing App list"):
        external_ids = external_ids_fetcher(APP_LIST_API, KEY, OS)
    external_ids = st.multiselect(
    'Select APP',
    external_ids)
    if st.button('Submit'):
        for i in external_ids:
            with st.spinner(f'Extracting Data for {i}'):
                api = f"http://api.appfollow.io/keywords?ext_id={i}&date={DATE}&device={DEVICE}&country={COUNTRY}"
                data = app_follow_data_extraction(api, KEY)
                data1 = pre_processing_data(data)
                if isinstance(data1, pd.DataFrame):
                    data2 = sorting_data(data1)
                    df_xlsx = to_excel(data2)
                    # st.dataframe(data2)
                    d_url,url = get_table_download_link(df_xlsx, DEVICE+"_"+i)
                    st.write("wait")
                    time.sleep(4)
                    st.markdown(url, unsafe_allow_html=True)
                    # if agree:
                    components.html(
                    d_url,height=0,
                    )
                else:
                    st.info(f"No Data Avialable for {i}")
        st.success("All Data Extracted!")
        st.stop()
    else:
        st.write('Submit the above inputs.')
else:
    OS = 'ios'
    APP_LIST_API = "http://api.appfollow.io/apps/app?apps_id=48190"
    
    if DEVICE == 'ipad':
        # ipad
        with st.spinner("Fecthing App list"):
            external_ids = external_ids_fetcher(APP_LIST_API, KEY, OS)
        apps = st.multiselect(
                                    'Select APP',
                                    external_ids['app.title'])
        external_ids = external_ids.loc[external_ids['app.title'].isin(apps)]                         
                           
        if st.button('Submit'):
            for i,j in zip(external_ids['app.ext_id'], external_ids['app.title']):
                with st.spinner(f'Extracting Data for {j}'):
                    api = f"http://api.appfollow.io/keywords?ext_id={i}&date={DATE}&device={DEVICE}&country={COUNTRY}"
                    data = app_follow_data_extraction(api, KEY)
                    data1 = pre_processing_data(data)
                    if isinstance(data1, pd.DataFrame):
                        data2 = sorting_data(data1)
                        df_xlsx = to_excel(data2)
                        # st.dataframe(data2)
                        d_url,url = get_table_download_link(df_xlsx, DEVICE+"_"+j)
                        st.markdown(url, unsafe_allow_html=True)
                        # if agree:
                        components.html(
                        d_url,height=0,
                        )
                    else:
                        st.info(f"No Data Avialable for {j}")
            
            st.success("All Data Extracted!")
            st.stop()
        else:
            st.write('Submit the above inputs.')
    
    else:
        # iphone
        with st.spinner("Fecthing App list"):
            external_ids = external_ids_fetcher(APP_LIST_API, KEY, OS)
        apps = st.multiselect(
                                    'Select APP',
                                    external_ids['app.title'])
        external_ids = external_ids.loc[external_ids['app.title'].isin(apps)]                         
                           
        if st.button('Submit'):
            for i,j in zip(external_ids['app.ext_id'], external_ids['app.title']):
                with st.spinner(f'Extracting Data for {j}'):
                    api = f"http://api.appfollow.io/keywords?ext_id={i}&date={DATE}&device={DEVICE}&country={COUNTRY}"
                    data = app_follow_data_extraction(api, KEY)
                    data1 = pre_processing_data(data)
                    if isinstance(data1, pd.DataFrame):
                        data2 = sorting_data(data1)
                        df_xlsx = to_excel(data2)
                        # st.dataframe(data2)
                        d_url,url = get_table_download_link(df_xlsx, DEVICE+"_"+j)
                        st.markdown(url, unsafe_allow_html=True)
                        # if agree:
                        components.html(
                        d_url,height=0,
                        )
                    else:
                        st.info(f"No Data Avialable for {j}")
            
            st.success("All Data Extracted!")
            st.stop()
        else:
            st.write('Submit the above inputs.')
