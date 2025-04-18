import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from datetime import timedelta

st.set_page_config(page_title="📊 RFM Customer Segmentation", layout="wide")
st.title("📊 Customer Segmentation using RFM Analysis")

# Automatically load the cleaned CSV file
try:
    df = pd.read_csv('cleaned_data.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    reference_date = df['InvoiceDate'].max() + timedelta(days=1)

    # Compute RFM features
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    }).reset_index()

    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

    # Scale RFM features
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

    st.sidebar.header("Clustering Options")
    k = st.sidebar.slider("Select number of clusters (k)", 2, 10, 4)

    # Fit KMeans
    kmeans = KMeans(n_clusters=k, random_state=42)
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

    # Silhouette Score
    score = silhouette_score(rfm_scaled, rfm['Cluster'])
    st.markdown(f"**Silhouette Score:** `{score:.3f}`")

    # Visualizations
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Cluster', palette='Set2', ax=ax1)
    ax1.set_title('Customer Segments (Recency vs. Monetary)')
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=rfm, x='Frequency', y='Monetary', hue='Cluster', palette='Set1', ax=ax2)
    ax2.set_title('Customer Segments (Frequency vs. Monetary)')
    st.pyplot(fig2)

    st.subheader("Sample of RFM Table with Cluster Labels")
    st.dataframe(rfm.head())

except FileNotFoundError:
    st.error("❌ 'cleaned_data.csv' not found. Please make sure the file exists in the same directory as the app.")