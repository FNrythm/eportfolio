import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import seaborn as sns

# Configurar el estilo de las gráficas
plt.style.use('default')

# Cargar y procesar el dataset Iris
iris = pd.read_csv('Unit06 iris.csv')
iris_features = iris.select_dtypes(include=[np.number])
scaler = StandardScaler()
iris_scaled = scaler.fit_transform(iris_features)

# Aplicar K-Means al dataset Iris
kmeans_iris = KMeans(n_clusters=3, random_state=42)
iris_clusters = kmeans_iris.fit_predict(iris_scaled)

# Aplicar PCA para visualización
pca = PCA(n_components=2)
iris_pca = pca.fit_transform(iris_scaled)

# Graficar clusters de Iris
plt.figure(figsize=(10, 6))
scatter = plt.scatter(iris_pca[:, 0], iris_pca[:, 1], c=iris_clusters, cmap='viridis')
plt.title('Iris Dataset Clustering Results')
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.colorbar(scatter)
plt.savefig('../../assets/images/iris_clusters.png', dpi=300, bbox_inches='tight')
plt.close()

# Cargar y procesar el dataset Wine
wine = pd.read_csv('Unit06 wine.csv')
wine_features = wine.select_dtypes(include=[np.number])
wine_scaled = scaler.fit_transform(wine_features)

# Aplicar K-Means al dataset Wine
kmeans_wine = KMeans(n_clusters=3, random_state=42)
wine_clusters = kmeans_wine.fit_predict(wine_scaled)

# Aplicar PCA para visualización
wine_pca = pca.fit_transform(wine_scaled)

# Graficar clusters de Wine
plt.figure(figsize=(10, 6))
scatter = plt.scatter(wine_pca[:, 0], wine_pca[:, 1], c=wine_clusters, cmap='viridis')
plt.title('Wine Dataset Clustering Results')
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.colorbar(scatter)
plt.savefig('../../assets/images/wine_clusters.png', dpi=300, bbox_inches='tight')
plt.close()

# Cargar y procesar el dataset WeatherAUS
weather = pd.read_csv('Unit06 weatherAUS.csv')
weather_features = weather.select_dtypes(include=[np.number])
weather_features = weather_features.fillna(weather_features.mean())
weather_scaled = scaler.fit_transform(weather_features)

# Calcular el método del codo para WeatherAUS
inertias = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(weather_scaled)
    inertias.append(kmeans.inertia_)

# Graficar el método del codo
plt.figure(figsize=(10, 6))
plt.plot(k_range, inertias, 'bo-')
plt.title('Elbow Method for WeatherAUS Dataset')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.grid(True)
plt.savefig('../../assets/images/weather_elbow.png', dpi=300, bbox_inches='tight')
plt.close() 