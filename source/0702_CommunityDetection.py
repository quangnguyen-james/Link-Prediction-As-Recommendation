import networkx as nx
import community  
import matplotlib.pyplot as plt

# 1. Đọc đồ thị từ tệp GraphML
graphml_file = "graph/processed_graph.graphml"
G = nx.read_graphml(graphml_file)

# 2. Phân tích cộng đồng bằng Louvain
partition = community.best_partition(G)

# 3. Số lượng cộng đồng
num_communities = len(set(partition.values()))
print(f"Số lượng cộng đồng: {num_communities}")

# 4. Thêm thuộc tính cộng đồng vào đồ thị
nx.set_node_attributes(G, partition, "community")

# 5. Lưu đồ thị đã gắn nhãn cộng đồng (nếu cần)
output_graphml_file = "graph/processed_graph_with_communities.graphml"
nx.write_graphml(G, output_graphml_file)
print(f"Đồ thị đã gắn nhãn cộng đồng được lưu tại: {output_graphml_file}")

# 6. Vẽ đồ thị với màu sắc theo cộng đồng
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Bố trí đồ thị
colors = [partition[str(node)] for node in G.nodes()]  # Đảm bảo đúng kiểu dữ liệu của node
nx.draw(
    G,
    pos,
    node_color=colors,
    cmap=plt.cm.tab20,
    node_size=30,
    with_labels=False,
    edge_color="lightgray",
)
plt.title("Phân tích cộng đồng bằng Louvain")
plt.show()
