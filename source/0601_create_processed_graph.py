#--- XÂY DỰNG ĐỒ THỊ VỚI BỘ DỮ LIỆU SAU KHI TIỀN XỬ LÝ preprocessing\combined_graph.edges
#--- Tạo label cho từng Node theo ego - Mỗi nút sẽ được gán một nhãn hoặc một màu dựa trên cụm (ego) mà nó thuộc về.
#--- Dữ liệu tạo label lấy từ các file .edges trong thư mục processed_dataset
#--- Mỗi cụm là một ego graph từ các file .edges. Dựa vào các file này, xác định được các nút thuộc từng ego.
#--- Tạo file đồ thị GraphML, có thể sử dụng trong các công cụ khác (như Gephi, Cytoscape) để phân tích và trực quan hóa nâng cao.

import networkx as nx
import os

# Đường dẫn lưu đồ thị
dataset_path = "graph"

# Đọc đồ thị từ preprocessing\combined_graph.edges
G_combined = nx.read_edgelist(r"preprocessing\combined_graph.edges", nodetype=int)

# Đường dẫn folder chứa các file .edges
edges_directory = r"preprocessing\processed_dataset"

# Mapping: node -> ego_id
node_to_ego = {}

# Lặp qua tất cả file .edges để xác định ego
for filename in os.listdir(edges_directory):
    if filename.endswith(".edges"):
        ego_id = int(filename.split("_")[0])  # Lấy ego ID từ tên file
        filepath = os.path.join(edges_directory, filename)
        
        # Đọc ego graph
        ego_graph = nx.read_edgelist(filepath, nodetype=int)
        
        # Gán ego_id cho các nút trong ego graph
        for node in ego_graph.nodes():
            if node not in node_to_ego:
                node_to_ego[node] = ego_id  # Chỉ gán ego đầu tiên

# Gán ego_id làm thuộc tính cho các nút trong đồ thị G_combined
for node in G_combined.nodes():
    G_combined.nodes[node]["ego"] = str(node_to_ego.get(node, "None"))  # Gán giá trị ego đầu tiên hoặc "None" nếu không có

# Lưu đồ thị thành file GraphML
nx.write_graphml(G_combined, f"{dataset_path}/processed_graph.graphml")
print("Đã lưu đồ thị vào file processed_graph")
