import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Load cleaned data
df = pd.read_csv('cleaned_data.csv')

# Reference date for recency (1 day after the last purchase date)
reference_date = pd.to_datetime(df['InvoiceDate'].max()) + pd.Timedelta(days=1)

# Compute RFM metrics
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (reference_date - pd.to_datetime(x).max()).days,
    'InvoiceNo': 'nunique',
    'TotalPrice': 'sum'
}).reset_index()

# Rename columns
rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# Scale RFM values
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

# Determine optimal number of clusters (elbow method)
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(rfm_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method for Optimal Clusters')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.grid(True)
plt.tight_layout()
plt.show()

# Fit final model
kmeans = KMeans(n_clusters=4, random_state=42)  # Change k as needed
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

score = silhouette_score(rfm_scaled, rfm['Cluster'])
print(f"Silhouette Score: {score:.3f}")

# Visualize clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Cluster', palette='Set2')
plt.title('Customer Segments (Recency vs Monetary)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Display RFM with clusters
print(rfm.head())

