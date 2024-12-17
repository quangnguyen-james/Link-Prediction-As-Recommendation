import os
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community


G = nx.read_edgelist(r"dataset\ego-Facebook\facebook_combined.txt\facebook_combined.txt", nodetype=int)
# In thông tin cơ bản về đồ thị
print(f"Số nút trong facebook_combined: {G.number_of_nodes()}")
print(f"Số cạnh trong facebook_combined: {G.number_of_edges()}")

density = nx.density(G)
print(f"Mật độ mạng: {density:.4f}")

# 2. Phân bố bậc
degrees = [d for _, d in G.degree()]
print(f"Bậc trung bình: {sum(degrees) / len(degrees):.2f}")

# Phân phối bậc
plt.hist(degrees, bins=30, color="skyblue", edgecolor="black")
plt.title("Degree Distribution")
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.show()

# 3. Tính chất kết nối
is_connected = nx.is_connected(G)
print(f"Mạng liên thông: {is_connected}")
if not is_connected:
    num_components = nx.number_connected_components(G)
    print(f"Số thành phần liên thông: {num_components}")
if is_connected:
    diameter = nx.diameter(G)
    print(f"Đường kính mạng: {diameter}")

# 4. Tính chất cụm
avg_clustering = nx.average_clustering(G)
print(f"Hệ số cụm trung bình: {avg_clustering:.4f}")

# 5. Tính chất trung tâm
degree_centrality = nx.degree_centrality(G)
most_connected = max(degree_centrality, key=degree_centrality.get)
print(f"Nút có độ trung tâm cao nhất (degree centrality): {most_connected} với giá trị {degree_centrality[most_connected]:.4f}")

# 6. Phân cụm
communities = community.greedy_modularity_communities(G)
print(f"Số cụm phát hiện: {len(communities)}")