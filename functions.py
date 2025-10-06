import numpy as np
import pandas as pd
import dcor
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

def compare_centroids_distance_correlation_from_df(
    df: pd.DataFrame,
    sample_col: str = 'sample',
    dataset_col: str = 'dataset'
):
    """
    Compute distance correlation between sample centroids in a PCA/Harmony space
    provided as a DataFrame, using pre‑computed embeddings.

    Rule: dataset == 'CCLE' is cell line; else tumor.

    Args:
        df: DataFrame with columns for PCs (pc_cols), plus sample_col and dataset_col.
        sample_col: name of the column with sample IDs.
        dataset_col: name of the column with dataset labels (e.g. 'CCLE' or other).

    Returns:
        centroid_df: DataFrame with distance correlation matrix
                     (CCLE samples × Tumor samples).
        best_match: dict with keys 'CCLE', 'Tumor', 'Correlation' for the best pair.
    """
    pc_cols = [c for c in df.columns if c.startswith('PC')]
    emb = df[pc_cols + [sample_col, dataset_col]].copy()
    centroids = (
        emb
        .groupby(sample_col, observed=True)[pc_cols]
        .mean()
    )

    sample_to_ds = (
        emb
        .drop_duplicates(sample_col)
        .set_index(sample_col)[dataset_col]
    )

    ccle_centroids  = centroids.loc[sample_to_ds == 'CCLE']
    tumor_centroids = centroids.loc[sample_to_ds != 'CCLE']

    if ccle_centroids.empty or tumor_centroids.empty:
        raise ValueError("No CCLE or Tumor samples found with given criteria.")

    centroid_df = pd.DataFrame(
        index=ccle_centroids.index,
        columns=tumor_centroids.index,
        dtype=float
    )

    for ccle_s in tqdm(ccle_centroids.index, desc="Calculating distance correlations"):
        v1 = ccle_centroids.loc[ccle_s].values
        for tum_s in tumor_centroids.index:
            v2 = tumor_centroids.loc[tum_s].values
            try:
                centroid_df.at[ccle_s, tum_s] = dcor.distance_correlation(v1, v2)
            except Exception:
                centroid_df.at[ccle_s, tum_s] = np.nan

    clean = centroid_df.dropna(how='all', axis=0).dropna(how='all', axis=1)
    if clean.empty:
        raise ValueError("Distance correlation matrix is empty after cleaning.")

    max_idx = clean.stack().idxmax()
    best_match = {
        'CCLE':       max_idx[0],
        'Tumor':      max_idx[1],
        'Correlation': clean.loc[max_idx]
    }

    return centroid_df, best_match

def convert_to_long_format(centroid_df):
    """
    Converte o DataFrame wide para formato longo com colunas:
    CCLE, Primary Tumor, Distance Correlation
    """
    # Reset index para transformar o índice em coluna
    long_df = centroid_df.reset_index()
    
    # Verificar qual é o nome da coluna do índice
    index_col_name = long_df.columns[0]
    
    # Fazer o melt usando o nome correto da coluna
    long_df = long_df.melt(
        id_vars=index_col_name, 
        var_name='Primary Tumor', 
        value_name='Distance Correlation'
    )
    
    # Renomear a coluna do índice para 'CCLE'
    long_df = long_df.rename(columns={index_col_name: 'CCLE'})
    
    # Remover valores NaN e ordenar por correlação
    long_df = long_df.dropna(subset=['Distance Correlation'])
    return long_df.sort_values('Distance Correlation', ascending=False)

def plot_correlation_heatmap(centroid_matrix):
    """
    Plot a correlation heatmap.
    
    Parameters:
    -----------
    centroid_matrix : array-like
        Matrix data for the heatmap
    """
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(
        centroid_matrix,
        cmap='rocket',
        linecolor="lightgray",
        cbar_kws={"label": "Distance Correlation"},
        xticklabels=True,
        yticklabels=True
    )

    plt.xlabel("Tumor Samples", fontdict={'weight': 'bold'}, fontsize=22)
    plt.ylabel("CCLE Samples", fontdict={'weight': 'bold'}, fontsize=22)
    plt.xticks(fontsize=10, ha='right')
    plt.yticks(fontsize=10)

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label('Distance Correlation', fontsize=12, weight='bold')

    plt.tight_layout()
