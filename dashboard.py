import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df = pd.read_csv('day.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
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

st.header('Pengaruh Cuaca')
weather = df.groupby('weathersit')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather, ax=ax)
ax.set_title('Rata-rata penyewaan sepeda berdasarkan kondisi cuaca')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Rental')
st.pyplot(fig)

st.header('Tren Musiman')
seasonal = df.groupby(['mnth', 'season'])['cnt'].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='mnth', y='cnt', hue='season', data=seasonal, ax=ax2)
ax2.set_title('Tren sewa sepeda berdasarkan musim')
ax2.set_xlabel('Bulan')
ax2.set_ylabel('Rata-rata Rental')
st.pyplot(fig2)

st.header('Data yang sudah di filter')
filter = df[(df['season'] == select_season) & (df['weathersit'] == select_weather)]
st.dataframe(filter)