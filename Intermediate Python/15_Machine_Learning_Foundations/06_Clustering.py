from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

RANDOM_STATE: int = 42


class GeneExpressionClusterer:
    """Groups biological samples into phenotype clusters based on gene-expression profiles."""

    def __init__(self, data: pd.DataFrame, n_clusters: int = 3) -> None:
        self.data: pd.DataFrame = data.copy()
        self.feature_columns: list[str] = ["gene_expression_a", "gene_expression_b", "gene_expression_c"]
        self.n_clusters: int = n_clusters
        self.scaler: StandardScaler = StandardScaler()
        self.model: KMeans = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10)
        self.scaled_features: pd.DataFrame | None = None
        self.labels: pd.Series | None = None

    def scale_features(self) -> pd.DataFrame:
        features = self.data[self.feature_columns]
        scaled_array = self.scaler.fit_transform(features)
        self.scaled_features = pd.DataFrame(scaled_array, columns=self.feature_columns, index=features.index)
        return self.scaled_features

    def fit_clusters(self) -> pd.Series:
        if self.scaled_features is None:
            raise RuntimeError("Features must be scaled before clustering.")
        cluster_labels = self.model.fit_predict(self.scaled_features)
        self.labels = pd.Series(cluster_labels, index=self.data.index, name="cluster")
        return self.labels

    def evaluate_clustering(self) -> float:
        if self.scaled_features is None or self.labels is None:
            raise RuntimeError("Clustering must be fit before evaluation.")
        return float(silhouette_score(self.scaled_features, self.labels))

    def cluster_summary(self) -> pd.DataFrame:
        if self.labels is None:
            raise RuntimeError("Clustering must be fit before summarizing.")
        summary_frame = self.data[self.feature_columns].copy()
        summary_frame["cluster"] = self.labels
        return summary_frame.groupby("cluster")[self.feature_columns].mean()

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S01", "gene_expression_a": 2.1, "gene_expression_b": 0.8, "gene_expression_c": 1.2},
                {"sample_id": "S02", "gene_expression_a": 2.4, "gene_expression_b": 0.9, "gene_expression_c": 1.4},
                {"sample_id": "S03", "gene_expression_a": 1.9, "gene_expression_b": 0.7, "gene_expression_c": 1.1},
                {"sample_id": "S04", "gene_expression_a": 6.3, "gene_expression_b": 5.8, "gene_expression_c": 6.1},
                {"sample_id": "S05", "gene_expression_a": 6.7, "gene_expression_b": 6.1, "gene_expression_c": 6.4},
                {"sample_id": "S06", "gene_expression_a": 6.0, "gene_expression_b": 5.5, "gene_expression_c": 5.9},
                {"sample_id": "S07", "gene_expression_a": 3.9, "gene_expression_b": 3.4, "gene_expression_c": 3.6},
                {"sample_id": "S08", "gene_expression_a": 4.2, "gene_expression_b": 3.6, "gene_expression_c": 3.8},
                {"sample_id": "S09", "gene_expression_a": 3.7, "gene_expression_b": 3.2, "gene_expression_c": 3.5},
                {"sample_id": "S10", "gene_expression_a": 2.3, "gene_expression_b": 0.9, "gene_expression_c": 1.3},
                {"sample_id": "S11", "gene_expression_a": 6.5, "gene_expression_b": 5.9, "gene_expression_c": 6.2},
                {"sample_id": "S12", "gene_expression_a": 4.0, "gene_expression_b": 3.5, "gene_expression_c": 3.7},
                {"sample_id": "S13", "gene_expression_a": 2.0, "gene_expression_b": 0.6, "gene_expression_c": 1.0},
                {"sample_id": "S14", "gene_expression_a": 6.4, "gene_expression_b": 5.7, "gene_expression_c": 6.0},
                {"sample_id": "S15", "gene_expression_a": 3.8, "gene_expression_b": 3.3, "gene_expression_c": 3.6},
                {"sample_id": "S16", "gene_expression_a": 2.2, "gene_expression_b": 0.8, "gene_expression_c": 1.2},
                {"sample_id": "S17", "gene_expression_a": 6.8, "gene_expression_b": 6.2, "gene_expression_c": 6.5},
                {"sample_id": "S18", "gene_expression_a": 4.1, "gene_expression_b": 3.7, "gene_expression_c": 3.9},
            ]
        )

        clusterer = GeneExpressionClusterer(data, n_clusters=3)
        clusterer.scale_features()
        labels = clusterer.fit_clusters()

        print("Cluster assignments:\n", labels)
        print("Silhouette score:", clusterer.evaluate_clustering())
        print("Cluster summary (mean expression):\n", clusterer.cluster_summary())


if __name__ == "__main__":
    GeneExpressionClusterer.run()
