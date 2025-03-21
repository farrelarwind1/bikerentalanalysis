import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df = pd.read_csv('day.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    season_mapping = {
        1: 'Spring',
        2: 'Summer',
        3: 'Fall',
        4: 'Winter'
    }
    df['season'] = df['season'].map(season_mapping)
    
    weather_mapping = {
        1: 'Clear',
        2: 'Mist',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Snow'
    }
    df['weathersit'] = df['weathersit'].map(weather_mapping)
    
    return df

df = load_data()





st.sidebar.header('Filter')
select_season = st.sidebar.selectbox('Musim', df['season'].unique())
select_weather = st.sidebar.selectbox('Cuaca', df['weathersit'].unique())

st.title('Bike Rental Analysis Dashboard')
st.markdown("""
Menganalisis pola rental sepeda berdasarkan tren cuaca dan musim
"""
    """
    By MC005D5Y1297 - Farrel Arsya Winarendra
    """
    )




st.header('Metrik')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rental", df['cnt'].sum())
with col2:
    st.metric("Rata-rata Rental per Hari", round(df['cnt'].mean()))
with col3:
    st.metric("Rental per Hari", df['cnt'].max())




# Visualisasi pertama
st.header('Dampak kondisi cuaca pada jumlah penyewaan sepeda')
weather = df.groupby('weathersit')['cnt'].sum().reset_index()
weather['cnt'] = weather['cnt'] / 1e6
fig, ax = plt.subplots(figsize=(10, 6))
plt.bar(weather['weathersit'], weather['cnt'], color=['green', 'blue', 'red'])
plt.title('Dampak kondisi cuaca pada jumlah penyewaan sepeda')
plt.xlabel('Kondisi cuaca')
plt.ylabel('Total sepeda yang di rental (million)')
plt.xticks(weather['weathersit'], labels=['Cerah', 'Kabut', 'Gerimis/Salju'])
st.pyplot(fig)

# Visualisasi kedua
st.header('Tren Musiman')
seasonal = df.groupby('season')['cnt'].sum().reset_index()
seasonal.columns = ['Musim', 'Total Rental']
fig2, ax2 = plt.subplots(figsize=(10, 6))
plt.bar(seasonal['Musim'], seasonal['Total Rental'] / 1e6, color=['green', 'red', 'yellow', 'blue'])
plt.title('Tren Musiman pada penyewaan sepeda')
plt.xlabel('Musim')
plt.ylabel('Total sepeda yang di rental (million)')
plt.xticks(seasonal['Musim'], labels=['Spring', 'Summer', 'Fall', 'Winter'])
st.pyplot(fig2)


st.header('Data yang sudah di filter')
filter = df[(df['season'] == select_season) & (df['weathersit'] == select_weather)]
st.dataframe(filter)