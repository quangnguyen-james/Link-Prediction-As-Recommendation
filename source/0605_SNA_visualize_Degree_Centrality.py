import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.colors as mcolors

# Đọc đồ thị từ file .graphml
graph_path = r"graph\processed_graph.graphml"
G = nx.read_graphml(graph_path)

# Tính Degree Centrality
degree_centrality = nx.degree_centrality(G)

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

# Tạo đối tượng ScalarMappable cho Degree Centrality
sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=min(degree_centrality.values()), vmax=max(degree_centrality.values())))
sm.set_array([])  # ScalarMappable cần một mảng, nhưng ở đây ta không cần nó.

# Vẽ đồ thị
plt.figure(figsize=(20, 16))
pos = nx.spring_layout(G)

# Vẽ các nút với kích thước theo Degree Centrality và màu sắc theo cụm
nodes = nx.draw_networkx_nodes(
    G, pos,
    node_size=[v * 1000 for v in degree_centrality.values()],
    node_color=list(degree_centrality.values()),  # Dùng giá trị degree_centrality cho màu sắc
    cmap=plt.cm.plasma,  # Liên kết cmap với ScalarMappable
    alpha=0.9
)
nx.draw_networkx_edges(G, pos, alpha=0.5)
#nx.draw_networkx_labels(G, pos, font_size=10)

# Thêm thanh màu (Colorbar) cho Degree Centrality
cbar = plt.colorbar(nodes, label="Degree Centrality")

# Hiển thị đồ thị
plt.title("Graph with Degree Centrality (Size) and Communities (Color)")
plt.axis("off")
plt.show()
