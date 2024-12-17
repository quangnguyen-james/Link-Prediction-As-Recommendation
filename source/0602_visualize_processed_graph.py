import networkx as nx
import matplotlib.pyplot as plt
import random

# Đọc đồ thị từ file GraphML
G_combined = nx.read_graphml(r"graph\processed_graph.graphml")

# Tạo bảng màu ngẫu nhiên cho từng ego
ego_colors = {}
for node, data in G_combined.nodes(data=True):
    egos = data["ego"]  # Lấy danh sách ego của nút
    if egos:
        # Dùng ego đầu tiên để gán màu (nếu thuộc nhiều ego, chọn đại diện)
        ego_id = egos[0]
        if ego_id not in ego_colors:
            ego_colors[ego_id] = f"#{random.randint(0, 0xFFFFFF):06x}"

# Gán màu cho các nút
node_colors = [
    ego_colors[data["ego"][0]] if data["ego"] else "#CCCCCC"  # Màu mặc định cho nút không thuộc ego
    for _, data in G_combined.nodes(data=True)
]

# Trực quan hóa
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(G_combined, seed=42)  # Tùy chọn layout

nx.draw(
    G_combined,
    pos,
    node_color=node_colors,
    node_size=50,
    edge_color="#AAAAAA",
    with_labels=False
)

plt.title("Processed Graph - Colored by Ego Clusters", fontsize=16)
plt.show()
