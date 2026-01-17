import numpy as np
import torch
from torch_geometric.data import Data, DataLoader
from scipy.sparse import csr_matrix

class GraphDataset:
    def __init__(self, split='train', use_text_only=True):
        self.edges = np.loadtxt("data/gossipcop/A.txt", delimiter=",", dtype=int)
        self.node_graph_id = np.load("data/gossipcop/node_graph_id.npy")
        self.graph_labels = np.load("data/gossipcop/graph_labels.npy")

        if use_text_only:
            features = np.load("data/gossipcop/new_spacy_feature.npz")
        else:
            features = np.load("data/gossipcop/new_content_feature.npz")
        sparse = csr_matrix(
            (features["data"], features["indices"], features["indptr"]),
            shape=tuple(features["shape"])
        )
        self.node_features = torch.tensor(sparse.toarray(), dtype=torch.float)

        if split == 'train':
            self.graph_ids = np.load("data/gossipcop/train_idx.npy")
        elif split == 'val':
            self.graph_ids = np.load("data/gossipcop/val_idx.npy")
        elif split == 'test':
            self.graph_ids = np.load("data/gossipcop/test_idx.npy")
        else:
            raise ValueError("split must be one of train/val/test")

    def build_graph(self, g_id):
        nodes = np.where(self.node_graph_id == g_id)[0]
        mask = np.isin(self.edges[:,0], nodes) & np.isin(self.edges[:,1], nodes)
        edge_index = self.edges[mask]
        node_map = {node:i for i,node in enumerate(nodes)}
        edge_index = np.array([[node_map[u], node_map[v]] for u,v in edge_index]).T
        edge_index = torch.tensor(edge_index, dtype=torch.long)
        x = self.node_features[nodes]
        y = torch.tensor([self.graph_labels[g_id]], dtype=torch.float)
        from torch_geometric.data import Data
        return Data(x=x, edge_index=edge_index, y=y)

    def get_loader(self, batch_size=128, shuffle=True):
        from torch_geometric.data import DataLoader
        dataset = [self.build_graph(g) for g in self.graph_ids]
        return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
