# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15CUMUn98iY1NyR-k_-vqE8vaTkqdSRwd
"""

from google.colab import files
uploaded = files.upload()

!pip install anndata

import anndata as ad
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Carga el archivo .h5ad
adata = ad.read_h5ad('1c2d14d8-32d4-41be-b38d-ba975ad10efa.h5ad')

# Extraer las coordenadas UMAP usando la clave 'X_UMAP'
umap_coords = adata.obsm['X_UMAP']

# Extraer el identificador de cluster
cluster_ids = adata.obs['cluster_id']
print(cluster_ids.head())  # Mostrar los primeros identificadores de cluster

# Crear un DataFrame con UMAP coords y cluster_id
df = pd.DataFrame(umap_coords, columns=['UMAP1', 'UMAP2'])
df['cluster_id'] = cluster_ids.values

# Mostrar las primeras filas del DataFrame combinado
print(df.head())

# Crear la figura
plt.figure(figsize=(10, 8))

# Graficar los puntos usando seaborn
sns.scatterplot(x='UMAP1', y='UMAP2', hue='cluster_id', data=df, palette='tab10', s=100, edgecolor='k')


# Dibujar el hull convexo para cada cluster
def all_same_side(p1, p2, points):
    side = None
    for p in points:
        cross_product = (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0])
        if cross_product != 0:
            if side is None:
                side = np.sign(cross_product)
            elif np.sign(cross_product) != side:
                return False
    return True

def brute_force_convex_hull(points):
    n = len(points)
    hull = []
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            if all_same_side(p1, p2, points):
                hull.append(p1)
                hull.append(p2)
    hull = np.unique(hull, axis=0)
    return hull

# Colores para cada cluster
palette = sns.color_palette("tab10", n_colors=df['cluster_id'].nunique())

# Dibujar el hull convexo para cada cluster
for cluster_id in df['cluster_id'].unique():
    cluster_points = df[df['cluster_id'] == cluster_id][['UMAP1', 'UMAP2']].values
    print(f"Cluster ID: {cluster_id}, Puntos: {cluster_points.shape[0]}")
    hull = brute_force_convex_hull(cluster_points)
    print(f"Cluster ID y puntos unicos dentro del Hull: {cluster_id}: {len(hull)}")

    if len(hull) > 0:
        hull_points = np.array(hull)
        plt.fill(np.append(hull_points[:, 0], hull_points[0, 0]),
                 np.append(hull_points[:, 1], hull_points[0, 1]),
                 color=palette[cluster_id % len(palette)], alpha=0.3)

# Agregar título y leyenda
plt.title('UMAP Clustering with Convex Hulls')
plt.legend(title='Cluster ID')
plt.show()


df = pd.DataFrame(umap_coords, columns=['UMAP1', 'UMAP2'])
df['cluster_id'] = cluster_ids.values
plt.figure(figsize=(8, 6))
sns.scatterplot(x='UMAP1', y='UMAP2', hue='cluster_id', data=df, palette='tab10')
plt.title('UMAP Clustering')
plt.show()

