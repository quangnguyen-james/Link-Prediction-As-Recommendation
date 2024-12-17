#--- Tích hợp dữ liệu từ các file EGO
#--- Bao gồm dữ liệu từ các file file .edgelist, .feat, .egofeat, .featname làm bộ dữ liệu đặc trưng
#--- Đây là bộ dữ liệu đầy đủ để sử dụng cho phân tích SNA và học sâu
#--- Sau khi tích hợp lưu dữ liệu thành 2 file nodes và edges, dưới dạng CSV (trong thư mục preprocessing)

import os
import numpy as np
import pandas as pd

# Đường dẫn tới thư mục chứa các file ego
base_path = r"dataset\ego-Facebook\facebook\facebook"  

# Kiểm tra xem đường dẫn có hợp lệ không
if not os.path.isdir(base_path):
    raise NotADirectoryError(f"The specified base path is not a directory: {base_path}")

# Danh sách lưu trữ thông tin nút và cạnh
nodes_data = []
edges_data = []

def process_ego_group(ego_id):
    print(f"Processing ego: {ego_id}")

    # Đường dẫn tới các file
    edge_list_file = os.path.join(base_path, f"{ego_id}.edges")
    feat_file = os.path.join(base_path, f"{ego_id}.feat")
    egofeat_file = os.path.join(base_path, f"{ego_id}.egofeat")
    featname_file = os.path.join(base_path, f"{ego_id}.featnames")

    # Kiểm tra file .edges có tồn tại không
    if not os.path.isfile(edge_list_file):
        print(f"Edge list file not found for ego {ego_id}. Skipping.")
        return

    # Đọc file .edges và thêm thông tin cạnh
    with open(edge_list_file, "r") as f:
        for line in f:
            source, target = map(int, line.strip().split())
            edges_data.append({"source": source, "target": target, "ego_group": ego_id})

    # Gắn nhãn đặc trưng từ file .featname
    feature_names = []
    if os.path.isfile(featname_file):
        with open(featname_file, "r") as f:
            feature_names = [line.strip().split(' ', 1)[1] for line in f.readlines()]

    # Đọc file .feat và thêm thông tin nút
    if os.path.isfile(feat_file):
        feat_data = np.loadtxt(feat_file)
        for i, feature_vector in enumerate(feat_data):
            feature_dict = {feature_names[j] if j < len(feature_names) else f"feature_{j}": feature_vector[j] for j in range(len(feature_vector))}
            feature_dict.update({"node_id": int(i), "ego_group": ego_id})
            nodes_data.append(feature_dict)

    # Đọc file .egofeat và thêm thông tin nút ego
    if os.path.isfile(egofeat_file):
        egofeat_data = np.loadtxt(egofeat_file).tolist()
        feature_dict = {feature_names[j] if j < len(feature_names) else f"feature_{j}": egofeat_data[j] for j in range(len(egofeat_data))}
        feature_dict.update({"node_id": int(ego_id), "ego_group": ego_id})
        nodes_data.append(feature_dict)

    print(f"Ego {ego_id} processed.")

# Lặp qua tất cả các nhóm ego
for file in os.listdir(base_path):
    file_path = os.path.join(base_path, file)
    if os.path.isfile(file_path) and file.endswith(".edges"):
        ego_id = file.split(".")[0]
        process_ego_group(ego_id)

# Lưu thông tin nút và cạnh vào file CSV
preprocessing_path ="preprocessing"
output_nodes_file = os.path.join(preprocessing_path, "processed_nodes.csv")
output_edges_file = os.path.join(preprocessing_path, "processed_edges.csv")

nodes_df = pd.DataFrame(nodes_data)
nodes_df.to_csv(output_nodes_file, index=False)
print(f"Node attributes saved to {output_nodes_file}")

edges_df = pd.DataFrame(edges_data)
edges_df.to_csv(output_edges_file, index=False)
print(f"Edge list saved to {output_edges_file}")

print("Processing complete!")
