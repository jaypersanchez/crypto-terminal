"""
This clustering approach lets you explore patterns or groupings in your data 
based on open_price and avg_volume without directly predicting close_price. 
After clustering, analyzing the close_price within each cluster might reveal interesting insights, 
such as certain clusters having higher or lower average close_price values.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data_path = "../data/sol_exchange_data_yearly.csv"
df = pd.read_csv(data_path)

# Assuming df is your DataFrame
X = df[['open_price', 'avg_volume']]

# Applying K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

# Adding the cluster labels to your DataFrame
df['cluster'] = kmeans.labels_

# Analyzing close_price characteristics for each cluster
for i in df['cluster'].unique():
    cluster_close_price_mean = df[df['cluster'] == i]['close_price'].mean()
    print(f"Cluster {i} Close Price Mean: {cluster_close_price_mean}")
    
# Visualizing the clusters
sns.scatterplot(data=df, x='open_price', y='avg_volume', hue='cluster', palette='viridis')
plt.title('Clusters based on Open Price and Avg Volume')
plt.xlabel('Open Price')
plt.ylabel('Avg Volume')
plt.legend(title='Cluster')
plt.show()


