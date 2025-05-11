import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv('day.csv')
    hour_df = pd.read_csv('hour.csv')
    
    # Simple cleaning
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar
st.sidebar.title("Filter Data")
selected_year = st.sidebar.selectbox("Tahun", ['Semua', 2011, 2012])
selected_season = st.sidebar.selectbox("Musim", ['Semua', 'Spring', 'Summer', 'Fall', 'Winter'])

# Apply filters
if selected_year != 'Semua':
    day_df = day_df[day_df['yr'] == (selected_year - 2011)]
    hour_df = hour_df[hour_df['yr'] == (selected_year - 2011)]

if selected_season != 'Semua':
    season_map = {'Spring':1, 'Summer':2, 'Fall':3, 'Winter':4}
    day_df = day_df[day_df['season'] == season_map[selected_season]]
    hour_df = hour_df[hour_df['season'] == season_map[selected_season]]

# Main content
st.title("🚲 Bike Sharing Analysis Dashboard")
st.write("""
Analisis pola penggunaan sepeda berdasarkan dataset Bike Sharing (2011-2012)
""")

# Row 1: Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{day_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Harian", f"{day_df['cnt'].mean():.0f}")
with col3:
    st.metric("Puncak Penyewaan", f"{day_df['cnt'].max()}")

# Row 2: Charts
tab1, tab2, tab3 = st.tabs(["Trend Harian", "Pola Per Jam", "Pengaruh Cuaca"])

with tab1:
    st.subheader("Trend Penyewaan Harian")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=day_df, x='dteday', y='cnt', ax=ax)
    ax.set(xlabel="Tanggal", ylabel="Jumlah Penyewaan")
    st.pyplot(fig)

with tab2:
    st.subheader("Pola Penggunaan Per Jam")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=hour_df, x='hr', y='cnt', ci=None, ax=ax)
    ax.set(xlabel="Jam (0-23)", ylabel="Rata-rata Penyewaan")
    ax.set_xticks(range(0, 24, 2))
    st.pyplot(fig)

with tab3:
    st.subheader("Pengaruh Cuaca Terhadap Penyewaan")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Weather impact
    sns.boxplot(data=day_df, x='weathersit', y='cnt', ax=ax1)
    ax1.set(xlabel="Kondisi Cuaca", ylabel="Penyewaan", 
           title="Pengaruh Cuaca")
    
    # Temperature impact
    sns.scatterplot(data=day_df, x='temp', y='cnt', ax=ax2)
    ax2.set(xlabel="Temperatur (normalisasi)", ylabel="Penyewaan",
           title="Pengaruh Temperatur")
    
    st.pyplot(fig)

# Row 3: Raw Data
with st.expander("Lihat Data Mentah"):
    st.write("**Data Harian**")
    st.dataframe(day_df.head())
    st.write("**Data Per Jam**")
    st.dataframe(hour_df.head())

# Footer
st.markdown("---")
st.caption("Proyek Analisis Data - Dicoding | Created by Sekarlana")