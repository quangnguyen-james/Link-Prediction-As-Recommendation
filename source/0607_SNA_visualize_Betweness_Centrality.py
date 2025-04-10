import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.colors as mcolors

# Đọc đồ thị từ file .graphml
graph_path = r"graph\processed_graph.graphml"
G = nx.read_graphml(graph_path)

# Tính Degree Centrality
betweenness_centrality = nx.betweenness_centrality(G)

# Phát hiện cụm bằng Greedy Modularity
communities = list(greedy_modularity_communities(G))

# Tạo mapping từ nút đến cụm
node_to_community = {}
for i, community in enumerate(communities):
    for node in community:
        node_to_community[node] = i

# Gán màu sắc cho từng cụm
colors = list(mcolors.TABLEAU_COLORS.values())
color_map = [colors[node_to_community[node] % len(colors)] for node in G.nodes]

# Tạo đối tượng ScalarMappable cho Betweenness Centrality
sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=min(betweenness_centrality.values()), vmax=max(betweenness_centrality.values())))
sm.set_array([])  # ScalarMappable cần một mảng, nhưng ở đây ta không cần nó.

# Vẽ đồ thị
plt.figure(figsize=(20, 16))
pos = nx.spring_layout(G, k=0.05)

# Vẽ các nút với kích thước theo Betweenness Centrality và màu sắc theo cụm
nodes = nx.draw_networkx_nodes(
    G, pos,
    node_size=[v * 1500 for v in betweenness_centrality.values()],
    node_color=list(betweenness_centrality.values()),  # Dùng giá trị Betweennesscentrality cho màu sắc
    cmap=plt.cm.plasma,  # Liên kết cmap với ScalarMappable
    alpha=0.9
)
nx.draw_networkx_edges(G, pos, alpha=0.5)
#nx.draw_networkx_labels(G, pos, font_size=10)

# Thêm thanh màu (Colorbar) cho Betweenness Centrality
cbar = plt.colorbar(nodes, label="Betweenness Centrality")

# Hiển thị đồ thị
plt.title("Graph with Betweenness Centrality (Size) and Communities (Color)")
plt.axis("off")
plt.show()
