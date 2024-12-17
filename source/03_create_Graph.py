#--- XÂY DỰNG ĐỒ THỊ TỔNG HỢP DỰA TRÊN DỮ LIỆU ĐẦU VÀO facebook_combined.txt
#--- Tạo label cho từng Node theo ego - Mỗi nút sẽ được gán một nhãn hoặc một màu dựa trên cụm (ego) mà nó thuộc về.
#--- Mỗi cụm là một ego graph từ các file .edges. Dựa vào các file này, xác định được các nút thuộc từng ego.
#--- Tạo file đồ thị GraphML, có thể sử dụng trong các công cụ khác (như Gephi, Cytoscape) để phân tích và trực quan hóa nâng cao.

import networkx as nx
import os
# Đường dẫn lưu đồ thị
dataset_path = r"dataset\ego-Facebook"

# Đọc đồ thị từ facebook_combined.txt
G_combined = nx.read_edgelist(r"dataset\ego-Facebook\facebook_combined.txt\facebook_combined.txt", nodetype=int)

# Đường dẫn folder chứa các file .edges
edges_directory = r"dataset\ego-Facebook\facebook\facebook"

# Mapping: node -> ego_id
node_to_ego = {}

# Lặp qua tất cả file .edges để xác định ego
for filename in os.listdir(edges_directory):
    if filename.endswith(".edges"):
        ego_id = int(filename.split(".")[0])  # Lấy ego ID từ tên file
        filepath = os.path.join(edges_directory, filename)
        
        # Đọc ego graph
        ego_graph = nx.read_edgelist(filepath, nodetype=int)
        
        # Gán ego_id cho các nút trong ego graph
        for node in ego_graph.nodes():
            if node in node_to_ego:
                # Nếu một nút thuộc nhiều ego, thêm vào danh sách
                node_to_ego[node].append(ego_id)
            else:
                node_to_ego[node] = [ego_id]

# Gán ego_id làm thuộc tính cho các nút trong đồ thị G_combined
for node in G_combined.nodes():
    G_combined.nodes[node]["ego"] = ",".join(map(str, node_to_ego.get(node, [])))

# Lưu đồ thị thành file GraphML
nx.write_graphml(G_combined, f"{dataset_path}/facebook_combined.graphml")
print("Đã lưu đồ thị vào file facebook_combined.graphml")
