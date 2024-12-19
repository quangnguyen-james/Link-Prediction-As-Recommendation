# Chuyển đổi dữ liệu sang cặp cạnh (Edge Pair)
# Định dạng dữ liệu cần có hai tệp:
# Positive edges: Các cạnh thực sự tồn tại trong đồ thị.
# Negative edges: Các cặp nút không có cạnh, được tạo ra để làm dữ liệu huấn luyện hoặc kiểm tra.

import os
import networkx as nx

# 1. Đọc đồ thị GraphML
graphml_file = "graph/processed_graph_with_communities.graphml"
G = nx.read_graphml(graphml_file)

# 2. Lấy danh sách cạnh (positive edges)
positive_edges = list(G.edges())

# 3. Tạo negative edges (các cạnh không liên kết)
# Lấy các cặp không liên kết với điểm số cao theo Adamic-Adar
print("Đang tính điểm Adamic-Adar...")
adamic_adar_scores = nx.adamic_adar_index(G)

# Chọn số lượng bằng positive_edges
negative_edges = []
for u, v, score in adamic_adar_scores:
    if len(negative_edges) >= len(positive_edges):  # Dừng khi đủ số lượng
        break
    if not G.has_edge(u, v) and u != v:  # Đảm bảo không phải là self-loop
        negative_edges.append((u, v))

# 4. Tạo thư mục lưu trữ nếu chưa có
os.makedirs("prepare_traindata", exist_ok=True)

# 5. Lưu cặp cạnh vào tệp
print("Đang xử lý và lưu positive_edges.txt...")
with open("prepare_traindata/positive_edges.txt", "w") as pos_file:
    for edge in positive_edges:
        pos_file.write(f"{edge[0]}\t{edge[1]}\n")

print("Đang xử lý và lưu negative_edges.txt...")
with open("prepare_traindata/negative_edges.txt", "w") as neg_file:
    for edge in negative_edges:
        neg_file.write(f"{edge[0]}\t{edge[1]}\n")

print("Positive edges và Negative edges đã được lưu thành công.")