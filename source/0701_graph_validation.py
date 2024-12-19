import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os

# Đường dẫn tới file GraphML
input_graphml_file = r"graph\processed_graph.graphml"

# Kiểm tra sự tồn tại của file
if not os.path.exists(input_graphml_file):
    raise FileNotFoundError(f"File not found: {input_graphml_file}")

# Đọc đồ thị từ file GraphML
G = nx.read_graphml(input_graphml_file)

isolated_nodes = list(nx.isolates(G))
num_isolated_nodes = len(isolated_nodes)
num_self_loops = nx.number_of_selfloops(G)

print(f"Số nút cô lập: {num_isolated_nodes}")
print(f"Số cạnh tự kết nối: {num_self_loops}")