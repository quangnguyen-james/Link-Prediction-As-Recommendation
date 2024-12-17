#--- Đọc facebook_combined.txt để tạo đồ thị nền:
#--- Đồ thị này sẽ được xem là đồ thị tổng quát và đầy đủ nhất.
#--- Tích hợp facebook_combined.txt: Thông tin từ các ego được bổ sung vào đồ thị tổng hợp.
#--- Tích hợp thông tin từ các file <ego>:
#--- Thêm đặc trưng nút (.feat, .egofeat).
#--- Gắn nhãn cạnh từ file .circles.
#--- Xuất toàn bộ dữ liệu (đồ thị, đặc trưng, nhãn cạnh, ma trận kề) ra file trung gian:
#--- Tạo ma trận đặc trưng và kề cho từng ego và tổng hợp.
#--- Lưu đồ thị tổng hợp: Tạo combined_graph.edges và combined_adjacency_matrix.csv.
#--- Phục vụ các bước phân tích hoặc học sâu tiếp theo.
import os
import pandas as pd
import networkx as nx
import numpy as np

# Đọc file facebook_combined.txt để xây dựng đồ thị tổng hợp
def read_combined_graph(file_path):
    return nx.read_edgelist(file_path, nodetype=int)

# Đọc file .edges để xây dựng đồ thị
def read_edges(edges_file):
    return nx.read_edgelist(edges_file, nodetype=int)

# Đọc file .feat và .egofeat để tạo ma trận đặc trưng nút
def read_features(feat_file, egofeat_file, ego_id):
    # Đọc file .feat và chuyển thành DataFrame
    feat_df = pd.read_csv(feat_file, delimiter=' ', header=None)
    feat_df.index = [f"{ego_id}_{i}" for i in feat_df.index]  # Gắn nhãn nút với ego_id

    # Đọc file .egofeat và chuyển thành danh sách
    egofeat = np.loadtxt(egofeat_file)

    # Đồng bộ số cột
    if len(egofeat) < feat_df.shape[1]:
        # Nếu thiếu, thêm giá trị 0
        egofeat = np.append(egofeat, [0] * (feat_df.shape[1] - len(egofeat)))
    elif len(egofeat) > feat_df.shape[1]:
        # Nếu dư, chỉ giữ số cột cần thiết
        egofeat = egofeat[:feat_df.shape[1]]

    # Thêm ego node vào DataFrame
    feat_df.loc[f"{ego_id}_ego"] = egofeat

    return feat_df

# Đọc file .featnames để gán nhãn cho các đặc trưng
def read_featnames(featnames_file):
    featnames = {}
    with open(featnames_file, "r") as f:
        for line in f:
            index, name = line.strip().split(" ", 1)
            featnames[int(index)] = name
    return featnames

# Đọc file .circles và xử lý thông tin cộng đồng
def process_circles(circles_file):
    circles = {}
    if os.path.exists(circles_file):
        with open(circles_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                circle_id = parts[0]
                nodes = list(map(int, parts[1:]))
                circles[circle_id] = nodes
    return circles

# Gắn nhãn các cạnh dựa trên file .circles
def label_edges_based_on_circles(graph, circles):
    edge_labels = {}
    for u, v in graph.edges():
        label = 0
        for circle in circles.values():
            if u in circle and v in circle:
                label = 1
                break
        edge_labels[(u, v)] = label
    return edge_labels

# Tạo ma trận kề từ đồ thị
def create_adjacency_matrix(graph):
    adj_matrix = nx.to_numpy_array(graph, nodelist=sorted(graph.nodes()))
    return adj_matrix

# Pipeline xử lý từng thư mục ego
def process_ego_files(edges_file, feat_file, egofeat_file, featnames_file, circles_file, ego_id, processed_dataset, combined_graph):
    # Đọc và xây dựng đồ thị ego
    G_ego = read_edges(edges_file)
    combined_graph.add_edges_from(G_ego.edges())  # Tích hợp vào đồ thị tổng hợp
    
    # Đọc và tích hợp đặc trưng nút
    features = read_features(feat_file, egofeat_file, ego_id)
    
    # Đọc nhãn đặc trưng
    featnames = read_featnames(featnames_file) if os.path.exists(featnames_file) else {}
    
    # Đọc và xử lý file .circles
    circles = process_circles(circles_file) if os.path.exists(circles_file) else {}
    
    # Gắn nhãn cạnh
    edge_labels = label_edges_based_on_circles(G_ego, circles)
    
    # Tạo ma trận kề
    adjacency_matrix = create_adjacency_matrix(G_ego)
    
    # Lưu kết quả ra các file trung gian
    nx.write_edgelist(G_ego, os.path.join(processed_dataset, f"{ego_id}_processed.edges"))
    features.to_csv(os.path.join(processed_dataset, f"{ego_id}_features.csv"), index_label="node")
    pd.DataFrame.from_dict(featnames, orient="index", columns=["feature_name"]).to_csv(
        os.path.join(processed_dataset, f"{ego_id}_featnames.csv"), index_label="feature_id"
    )
    pd.DataFrame(list(edge_labels.items()), columns=["Edge", "Label"]).to_csv(
        os.path.join(processed_dataset, f"{ego_id}_edge_labels.csv"), index=False
    )
    np.savetxt(os.path.join(processed_dataset, f"{ego_id}_adjacency_matrix.csv"), adjacency_matrix, delimiter=",")

# Xử lý toàn bộ thư mục chính
def process_all_ego_folders(data_dir, processed_dataset, output_dir, combined_graph_file):
    # Tạo thư mục processed_dataset nếu chưa tồn tại
    os.makedirs(processed_dataset, exist_ok=True)  

    # Đọc đồ thị tổng hợp từ facebook_combined.txt
    combined_graph = read_combined_graph(combined_graph_file)

    # Lấy danh sách các ego_id từ các file trong thư mục
    ego_ids = set(f.split('.')[0] for f in os.listdir(data_dir) if '.' in f)
    
    for ego_id in ego_ids:
        print(f"Processing ego_id: {ego_id}")  # In thông báo ego đang xử lý
        
        # Xây dựng đường dẫn cho các file liên quan đến ego
        edges_file = os.path.join(data_dir, f"{ego_id}.edges")
        feat_file = os.path.join(data_dir, f"{ego_id}.feat")
        egofeat_file = os.path.join(data_dir, f"{ego_id}.egofeat")
        featnames_file = os.path.join(data_dir, f"{ego_id}.featnames")
        circles_file = os.path.join(data_dir, f"{ego_id}.circles")
        
        # Kiểm tra sự tồn tại của các file cần thiết trước khi xử lý
        if os.path.exists(edges_file) and os.path.exists(feat_file) and os.path.exists(egofeat_file):
            process_ego_files(
                edges_file, feat_file, egofeat_file, featnames_file, circles_file,
                ego_id, processed_dataset, combined_graph
            )
        else:
            print(f"Skipping ego_id {ego_id} due to missing files.")
    
    # Lưu đồ thị tổng hợp và ma trận kề
    nx.write_edgelist(combined_graph, os.path.join(output_dir, "combined_graph.edges"))
    adjacency_matrix = create_adjacency_matrix(combined_graph)
    np.savetxt(os.path.join(output_dir, "combined_adjacency_matrix.csv"), adjacency_matrix, delimiter=",")
    print("Completed processing all ego files!")

# Chạy pipeline
if __name__ == "__main__":
    data_dir = r"dataset\ego-Facebook\facebook\facebook"
    processed_dataset = r"preprocessing\processed_dataset"
    output_dir = "preprocessing"
    combined_graph_file = r"dataset\ego-Facebook\facebook_combined.txt\facebook_combined.txt"
    process_all_ego_folders(data_dir, processed_dataset, output_dir, combined_graph_file)
