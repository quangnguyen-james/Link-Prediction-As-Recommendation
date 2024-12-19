#-- Tính toán các chỉ số đặc trưng bài toán Link Prediction
#-- Những chỉ số này khai thác thông tin từ đồ thị để giúp mô hình học sâu nhận diện các mối quan hệ tiềm năng chính xác hơn
#-- Các chỉ số sẽ tính: Common Neighbors (CN), Jaccard Coefficient (JC), Adamic-Adar Index (AA)
#--                     Preferential Attachment (PA), Resource Allocation Index (RA), Shortest Path Distance
#-- Sau khi tính toán, dữ liệu lưu vào link_prediction_features.csv
#-- Dữ liệu sẽ dữ liệu đầu vào cho mô hình học sâu
#-- Input:  graph/processed_graph_with_communities.graphml
#           prepare_traindata/positive_edges.txt
#           prepare_traindata/negative_edges.txt
#-- Output: prepare_traindata/link_prediction_features.csv

import networkx as nx
import numpy as np
from itertools import islice

# 1. Đọc đồ thị GraphML
graphml_file = "graph/processed_graph_with_communities.graphml"
G = nx.read_graphml(graphml_file)

# 2. Đọc Positive và Negative edges
positive_edges = [tuple(map(str, line.strip().split("\t"))) for line in open("prepare_traindata/positive_edges.txt")]
negative_edges = [tuple(map(str, line.strip().split("\t"))) for line in open("prepare_traindata/negative_edges.txt")]

# 3. Tính chỉ số cho từng cặp cạnh
def calculate_features(G, edge_list):
    features = []
    for u, v in edge_list:
        if not G.has_node(u) or not G.has_node(v):
            continue
        
        # Common Neighbors
        cn = len(list(nx.common_neighbors(G, u, v)))
        
        # Jaccard Coefficient
        union_size = len(set(G.neighbors(u)).union(set(G.neighbors(v))))
        jc = cn / union_size if union_size > 0 else 0
        
        # Adamic-Adar Index
        aa = sum(1 / np.log(len(list(G.neighbors(w)))) for w in nx.common_neighbors(G, u, v) if len(list(G.neighbors(w))) > 1)
        
        # Preferential Attachment
        pa = len(list(G.neighbors(u))) * len(list(G.neighbors(v)))
        
        # Resource Allocation Index
        ra = sum(1 / len(list(G.neighbors(w))) for w in nx.common_neighbors(G, u, v) if len(list(G.neighbors(w))) > 0)
        
        # Shortest Path Distance
        try:
            sp = nx.shortest_path_length(G, source=u, target=v)
        except nx.NetworkXNoPath:
            sp = float('inf')  # Không có đường đi
        
        # Tổng hợp đặc trưng
        features.append({
            "u": u, "v": v,
            "CN": cn, "JC": jc, "AA": aa, "PA": pa, "RA": ra, "SP": sp
        })
    return features

# 4. Tính đặc trưng cho Positive và Negative edges
positive_features = calculate_features(G, positive_edges)
negative_features = calculate_features(G, negative_edges)

# 5. Lưu đặc trưng vào tệp
import pandas as pd

df_positive = pd.DataFrame(positive_features)
df_negative = pd.DataFrame(negative_features)

df_positive["label"] = 1  # Positive edges
df_negative["label"] = 0  # Negative edges

df_combined = pd.concat([df_positive, df_negative])
df_combined.to_csv("prepare_traindata/link_prediction_features.csv", index=False)

print("Đặc trưng đã lưu tại link_prediction_features.csv")
