import networkx as nx
import os


G = nx.read_edgelist(r"dataset\ego-Facebook\facebook_combined.txt\facebook_combined.txt", nodetype=int)
# In thông tin cơ bản về đồ thị
print(f"Số nút trong facebook_combined: {G.number_of_nodes()}")
print(f"Số cạnh trong facebook_combined: {G.number_of_edges()}")

# Thư mục chứa các file .edges
dataset_path = r"dataset\ego-Facebook"
directory = r"dataset\ego-Facebook\facebook\facebook"

# Tạo một đồ thị tổng hợp
G = nx.Graph()

# Lặp qua từng file .edges và thêm các cạnh vào đồ thị
for filename in os.listdir(directory):
    if filename.endswith(".edges"):
        filepath = os.path.join(directory, filename)
        G.add_edges_from(nx.read_edgelist(filepath, nodetype=int).edges())

# Kiểm tra kết quả
print(f"Số nút trong combined graph: {G.number_of_nodes()}")
print(f"Số cạnh trong combined graph: {G.number_of_edges()}")
nx.write_edgelist(G, f"{dataset_path}/combined_graph.edges")
