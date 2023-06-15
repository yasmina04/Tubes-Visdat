import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import requests
import plotly
import geopandas as gpd

from streamlit_option_menu import option_menu

# st.title('Visualisasi Persebaran Upah Minimum Rakyat di Indonesia')
with st.sidebar:
    choose = option_menu('UMR Visualization',["Chart","Growth","Data Frame"])
    

def dataframe() :
    st.write("""### Indonesian Salary by Region (1997-2022)""")
    df = pd.read_csv("Indonesian Salary by Region (1997-2022).csv")
    df
    st.write("""### Summary Data""")
    st.write(df.describe())
    
def chart() :
    df = pd.read_csv("Indonesian Salary by Region (1997-2022).csv")
    i = df[df.REGION=="INDONESIA"].index
    df = df.drop(i)
    provlist = df.REGION.unique().tolist()
    daftarprov = st.multiselect("Pilih provinsi",provlist)

    st.write("""### Menampilkan UMR Provinsi: {}""".format(", ".join(daftarprov)))

    dfs = {prov: df[df["REGION"] == prov] for prov in daftarprov}
    fig = go.Figure()
    for prov, df in dfs.items():
        fig = fig.add_trace(go.Scatter(x=df["YEAR"], y=df["SALARY"], name=prov))
    
    fig.update_layout(
    xaxis=dict(
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
    )
    st.plotly_chart(fig)

def barchart():
    df = pd.read_csv("Indonesian Salary by Region (1997-2022).csv")
    df_indo = df[df.REGION=="INDONESIA"]
    fig = px.bar(df_indo, x='YEAR',y='SALARY',
                 hover_data=['SALARY'],
                 color='SALARY',
                 text_auto='.2s',
                 )
    st.plotly_chart(fig)


def growth() :
    df = pd.read_csv("Indonesian Salary by Region (1997-2022).csv")

    df_indo = df[df.REGION=="INDONESIA"].reset_index()
    df_indo = df_indo.drop(['index'],axis=1)

    i = df[df.REGION=="INDONESIA"].index
    df = df.drop(i)

    salary_growth = [0]
    
    for i in range(1,len(df_indo)):
        salary_growth.append(df_indo["SALARY"][i]-df_indo["SALARY"][i-1])

    df_indo["salary_growth"]=salary_growth
    st.write("""### Tabel Pertumbuhan Rata - Rata UMR Indonesia""")
    df_indo

    st.write("""### Line Chart Pertumbuhan Rata - Rata UMR Indonesia""")
    fig1 = px.line(df_indo, x='YEAR',
                   y='salary_growth',
                   hover_data=['salary_growth'],
                 )
    fig1.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            
    )
    )

    st.plotly_chart(fig1)


    st.write("""### Bar Chart UMR Indonesia Per Provinsi """)
    fig2 = px.bar(df, x='REGION',
                  y="SALARY",
                  color="REGION",
                  animation_frame="YEAR",
                  range_y=[0,4766460],
                  width=700,
                  height=690
                  
                  )
    
    fig2.update_layout(updatemenus=[dict(type='buttons',
                  showactive=False,
                  y=-0.45,
                  x=-0.1,
                  xanchor='left',
                  yanchor='bottom')
                        ])

   
    fig2['layout']['sliders'][0]['pad']=dict(r= 70, t= 135)

    
    st.plotly_chart(fig2)


if choose == 'Chart' or choose == '':
    st.title("""Line Chart Upah Minimum Rakyat (UMR) Indonesia""") #menampilkan halaman utama
    chart()
    st.write("""## Bar Chart Rata-Rata Upah Minimum Rakyat Indonesia Tahun 1997-2022""")
    barchart()  
        
    
elif choose  == 'Growth':
    st.title("""Pertumbuhan UMR Indonesia""") #menampilkan judul halaman mapping
    growth()

elif choose  == 'Data Frame':
    st.title("""Data Frame Upah Minuimum Rakyat Indonesia Tahun 1997-2022""") #menampilkan judul halaman dataframe
    dataframe()





