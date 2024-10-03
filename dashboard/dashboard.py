import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Fungsi untuk memuat data dari file di komputer (otomatis tanpa upload)
def load_data(file_path):
    hour_df = pd.read_csv('main.csv')
    
    # Pilih kolom yang diinginkan untuk korelasi
    variables_x = ['temp', 'atemp', 'hum', 'windspeed']  # Sesuaikan nama kolom dengan dataset
    variables_y = ['casual', 'registered', 'cnt']
    
    # Menghitung korelasi hanya antara variabel-variabel yang diinginkan
    correlation_matrix = hour_df[variables_y + variables_x].corr().loc[variables_y, variables_x]
    
    return hour_df, correlation_matrix

# Fungsi visualisasi (seperti yang sebelumnya)
def plot_average_users_per_day(hour_df):
    grouped_data = hour_df.groupby('weekday')['cnt'].mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=grouped_data.index, y=grouped_data.values, marker='o', ax=ax)
    
    ax.set_title('Average Users Per Day in 2011-2012', fontsize=14)
    ax.set_xlabel('Weekday (0=Sunday, 6=Saturday)', fontsize=12)
    ax.set_ylabel('Average Users', fontsize=12)
    ax.grid(True)
    
    st.pyplot(fig)

def plot_average_users_per_month(hour_df):
    grouped_data = hour_df.groupby('mnth')['cnt'].mean()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    # Plot untuk casual users
    sns.lineplot(data=hour_df, x='mnth', y='casual', marker='o', label='Casual Users', color='orange')
    # Plot untuk registered users
    sns.lineplot(data=hour_df, x='mnth', y='registered', marker='o', label='Registered Users', color='green')
    # Plot untuk total users (cnt)
    sns.lineplot(data=hour_df, x='mnth', y='cnt', marker='o', label='Total Users (cnt)', color='blue')
    
    ax.set_title('Average Users per Month in 2011-2012', fontsize=14)
    ax.set_xlabel('Month (1=January, 12=December)', fontsize=12)
    ax.set_ylabel('Average Users', fontsize=12)
    ax.grid(True)
    
    st.pyplot(fig)

def plot_users_by_season(hour_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='cnt', data=hour_df, ax=ax)
    
    ax.set_title('Average Total Users by Season in 2011-2012')
    ax.set_xlabel('Season')
    ax.set_ylabel('Average Count')
    
    st.pyplot(fig)

def plot_correlation_heatmap(correlation_matrix):
    # Visualisasi matriks korelasi dengan heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
    
    ax.set_title('Correlation Matrix between Selected Variables')
    ax.set_xlabel('Weather Conditions')
    ax.set_ylabel('Users')
    
    st.pyplot(fig)

# Main function to layout the dashboard
def dashboard(hour_df, correlation_matrix):
    st.title('User Analysis Dashboard')
    
    col1, col2 = st.columns(2)
    
    with col1:
        plot_average_users_per_day(hour_df)
    
    with col2:
        plot_users_by_season(hour_df)
    
    with col1:
        plot_average_users_per_month(hour_df)
    
    with col2:
        plot_correlation_heatmap(correlation_matrix)

# Load data and run dashboard
file_path = 'main.csv'  # Sesuaikan dengan path file Anda
hour_df, correlation_matrix = load_data(file_path)

if hour_df is not None:
    dashboard(hour_df, correlation_matrix)
else:
    st.write("File not found or invalid.")
