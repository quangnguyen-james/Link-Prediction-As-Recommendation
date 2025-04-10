import pandas as pd
import networkx as nx

# Đường dẫn tới các tệp dữ liệu
positive_edges_file = "prepare_traindata/positive_edges.txt"
negative_edges_file = "prepare_traindata/negative_edges.txt"
features_file = "prepare_traindata/link_prediction_features.csv"
adjacency_matrix_file = "prepare_traindata/combined_adjacency_matrix.csv"
node_embeddings_file = "prepare_traindata/node_embeddings.csv"

# Đọc dữ liệu
print("Đang kiểm tra tính nhất quán của dữ liệu...\n")

try:
    # 1. Kiểm tra positive_edges và negative_edges
    print("Đọc và kiểm tra positive_edges và negative_edges...")
    positive_edges = pd.read_csv(positive_edges_file, sep="\t", header=None, names=["source", "target"])
    negative_edges = pd.read_csv(negative_edges_file, sep="\t", header=None, names=["source", "target"])
    
    # Kiểm tra trùng lặp
    pos_duplicates = positive_edges.duplicated().sum()
    neg_duplicates = negative_edges.duplicated().sum()
    
    # Kiểm tra giao nhau giữa positive_edges và negative_edges
    intersection_edges = pd.merge(positive_edges, negative_edges, on=["source", "target"], how="inner")
    
    print(f"- Positive edges: {len(positive_edges)} cạnh, trùng lặp: {pos_duplicates}")
    print(f"- Negative edges: {len(negative_edges)} cạnh, trùng lặp: {neg_duplicates}")
    print(f"- Giao giữa positive_edges và negative_edges: {len(intersection_edges)} cạnh\n")

    # 2. Kiểm tra link_prediction_features
    print("Đọc và kiểm tra link_prediction_features.csv...")
    features = pd.read_csv(features_file)
    missing_labels = features["label"].isnull().sum()
    print(f"- Tổng số hàng: {len(features)}, nhãn bị thiếu: {missing_labels}\n")

    # 3. Kiểm tra adjacency_matrix
    print("Đọc và kiểm tra adjacency_matrix.csv...")
    adjacency_matrix = pd.read_csv(adjacency_matrix_file, index_col=0)
    adjacency_matrix.index = adjacency_matrix.index.astype(str) 
    adjacency_matrix.columns = adjacency_matrix.columns.astype(str)
    print(f"- Kích thước ma trận kề: {adjacency_matrix.shape}")
    if not (adjacency_matrix.index.equals(adjacency_matrix.columns)):
        print("  ⚠️ Các hàng và cột của ma trận kề không đồng nhất!\n")
    else:
        print("  ✅ Ma trận kề có chỉ mục hàng và cột đồng nhất.\n")

    # 4. Kiểm tra node_embeddings
    print("Đọc và kiểm tra node_embeddings.csv...")
    node_embeddings = pd.read_csv(node_embeddings_file, index_col=0)
    embedding_dimensions = node_embeddings.shape[1]
    print(f"- Số nút: {node_embeddings.shape[0]}, số chiều vector: {embedding_dimensions}\n")

    # 5. Kiểm tra sự khớp giữa dữ liệu
    print("Kiểm tra khớp giữa dữ liệu...")
    graph_nodes = set(adjacency_matrix.index)
    feature_nodes = set(features["source"]).union(set(features["target"]))
    embedding_nodes = set(node_embeddings.index)

    # Xử lý các giá trị null trước khi thực hiện kiểm tra 
    feature_nodes = {str(node) for node in feature_nodes if pd.notnull(node)} 
    embedding_nodes = {str(node) for node in embedding_nodes if pd.notnull(node)}

    missing_in_graph = feature_nodes - graph_nodes
    missing_in_embeddings = feature_nodes - embedding_nodes

    print(f"- Nút trong feature nhưng không có trong ma trận kề: {len(missing_in_graph)}")
    print(f"- Nút trong feature nhưng không có trong embeddings: {len(missing_in_embeddings)}\n")
    
    #if missing_in_graph:
    #    print(f"  ⚠️ Các nút thiếu trong ma trận kề: {missing_in_graph}")
    #if missing_in_embeddings:
    #    print(f"  ⚠️ Các nút thiếu trong embeddings: {missing_in_embeddings}")
    
    print("Kiểm tra tính nhất quán hoàn tất.")
except Exception as e:
    print(f"Lỗi xảy ra: {e}")
