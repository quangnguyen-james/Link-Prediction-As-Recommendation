#--- PHÂN TÍCH CÁC CHỈ SỐ MẠNG (SNA)
#--- Số nút và số cạnh
#--- Mật độ mạng
#--- Bậc trung bình
#--- Hệ số cụm trung bình
#--- Đường kính mạng
#--- Độ trung tâm (degree centrality, closeness centrality, betweenness centrality)
#--- Liên thông (connected components)
#--- Số cụm (community detection)
#--- Sau khi tính toán sẽ lưu ra file network_metrics.txt
import networkx as nx
import os

# Đường dẫn tới file GraphML
input_graphml_file = r"graph\processed_graph.graphml"

# Kiểm tra sự tồn tại của file
if not os.path.exists(input_graphml_file):
    raise FileNotFoundError(f"File not found: {input_graphml_file}")

# Đọc đồ thị từ file GraphML
G = nx.read_graphml(input_graphml_file)

# Tính các chỉ số mạng
def calculate_network_metrics(graph):
    metrics = {}
    
    # Số nút và số cạnh
    metrics["num_nodes"] = graph.number_of_nodes()
    metrics["num_edges"] = graph.number_of_edges()
    
    # Mật độ mạng
    metrics["density"] = nx.density(graph)
    
    # Bậc trung bình
    degrees = [deg for _, deg in graph.degree()]
    metrics["average_degree"] = sum(degrees) / len(degrees)
    
    # Hệ số cụm trung bình
    metrics["average_clustering_coefficient"] = nx.average_clustering(graph)
    
    # Đường kính mạng (nếu đồ thị liên thông)
    if nx.is_connected(graph):
        metrics["diameter"] = nx.diameter(graph)
    else:
        metrics["diameter"] = "Not applicable (graph not connected)"
    
    # Độ trung tâm
    metrics["degree_centrality"] = nx.degree_centrality(graph)
    metrics["closeness_centrality"] = nx.closeness_centrality(graph)
    metrics["betweenness_centrality"] = nx.betweenness_centrality(graph)
    
    # Liên thông
    metrics["is_connected"] = nx.is_connected(graph)
    if not metrics["is_connected"]:
        components = nx.connected_components(graph)
        metrics["num_connected_components"] = len(list(components))
    
    # Phát hiện số cụm (sử dụng Louvain hoặc Girvan-Newman)
    try:
        import community as community_louvain
        partition = community_louvain.best_partition(graph)
        metrics["num_communities"] = len(set(partition.values()))
    except ImportError:
        metrics["num_communities"] = "Louvain library not available"
    
    return metrics

# Tính toán chỉ số và in kết quả
network_metrics = calculate_network_metrics(G)

print("Network Metrics:")
for metric, value in network_metrics.items():
    print(f"{metric}: {value}")

# Ghi các chỉ số ra file
output_metrics_file = "processed_result/network_metrics.txt"
with open(output_metrics_file, "w") as f:
    for metric, value in network_metrics.items():
        f.write(f"{metric}: {value}\n")

print(f"Network metrics saved to {output_metrics_file}")
