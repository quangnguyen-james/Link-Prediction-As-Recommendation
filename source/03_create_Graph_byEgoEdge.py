import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Đường dẫn tới thư mục chứa các file ego
base_path = r"dataset\ego-Facebook\facebook\facebook"  # Thay đổi thành đường dẫn thực tế

# Tạo đồ thị tổng hợp và thêm nhãn
combined_graph = nx.Graph()

# Hàm xử lý từng nhóm ego
def process_ego_group(ego_id):
    print(f"Processing ego: {ego_id}")

    # Đường dẫn tới các file
    edge_list_file = os.path.join(base_path, f"{ego_id}.edges")

    # Đọc file .edges và xây dựng đồ thị
    graph = nx.read_edgelist(edge_list_file, nodetype=int)

    # Thêm cạnh từ đồ thị của ego vào đồ thị tổng hợp
    combined_graph.add_edges_from(graph.edges)

    # Gán nhãn cho các nút trong đồ thị của ego
    for node in graph.nodes:
        if "ego_group" not in combined_graph.nodes[node]:
            combined_graph.nodes[node]["ego_group"] = []
        combined_graph.nodes[node]["ego_group"].append(ego_id)

    print(f"Ego {ego_id} processed with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")

# Lặp qua tất cả các nhóm ego
for file in os.listdir(base_path):
    if file.endswith(".edges"):
        ego_id = file.split(".")[0]
        process_ego_group(ego_id)

# Chuyển đổi danh sách `ego_group` thành chuỗi để tương thích với GraphML
for node in combined_graph.nodes:
    if "ego_group" in combined_graph.nodes[node]:
        combined_graph.nodes[node]["ego_group"] = ",".join(map(str, combined_graph.nodes[node]["ego_group"]))

# Xuất đồ thị tổng hợp sang định dạng GraphML
graph_path = "graph"
output_graphml_file = os.path.join(graph_path, "combined_graph.graphml")
nx.write_graphml(combined_graph, output_graphml_file)
print(f"Combined graph saved to {output_graphml_file}")

# Phân tích đồ thị tổng hợp
print(f"Number of nodes in combined graph: {combined_graph.number_of_nodes()}")
print(f"Number of edges in combined graph: {combined_graph.number_of_edges()}")

# Tính và hiển thị phân phối bậc
degree_sequence = sorted([d for n, d in combined_graph.degree()], reverse=True)
plt.figure(figsize=(10, 6))
plt.hist(degree_sequence, bins=50, color='blue', alpha=0.7)
plt.title("Degree Distribution for Combined Graph")
plt.xlabel("Degree")
plt.ylabel("Count")
plt.show()

print("Processing complete!")
