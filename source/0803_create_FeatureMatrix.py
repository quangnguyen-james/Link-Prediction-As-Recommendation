#-- Tạo ma trận đặc trưng (Node2Vec) - Node Embedding
#-- Lưu thông tin dưới cả 2 dạng CSV và TXT (node_embeddings) để tùy trường hợp huấn luyện sau phụ thuộc loại nào
from node2vec import Node2Vec
import networkx as nx
import pandas as pd
from gensim.models.callbacks import CallbackAny2Vec
import os

# Callback để theo dõi tiến trình Word2Vec
class ProgressCallback(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        print(f"Epoch {self.epoch + 1} started...")

    def on_epoch_end(self, model):
        print(f"Epoch {self.epoch + 1} finished.")
        self.epoch += 1

try:
    # Tạo thư mục lưu trữ nếu chưa tồn tại
    output_dir = "prepare_traindata"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Đọc đồ thị từ file GraphML
    graphml_file = "graph/processed_graph_with_communities.graphml"
    G = nx.read_graphml(graphml_file)

    # 2. Tạo Node2Vec
    node2vec = Node2Vec(G, dimensions=128, walk_length=30, num_walks=200, workers=4)

    # 3. Huấn luyện mô hình Node2Vec
    print("Bắt đầu huấn luyện Word2Vec...")
    model = node2vec.fit(window=10, min_count=1, batch_words=4, callbacks=[ProgressCallback()])
    print("Huấn luyện Node2Vec hoàn thành!")

    # 4. Lưu vector đặc trưng vào file CSV
    node_embeddings = {node: model.wv[node] for node in G.nodes()}
    df_embeddings = pd.DataFrame.from_dict(node_embeddings, orient="index")
    df_embeddings.index.name = "node"
    df_embeddings.to_csv(f"{output_dir}/node_embeddings.csv", index=True)

    # 5. Lưu vector đặc trưng vào file TXT
    embeddings_file = f"{output_dir}/node_embeddings.txt"
    with open(embeddings_file, "w") as f:
        for node in G.nodes():
            embedding = model.wv[str(node)]
            embedding_str = "\t".join(map(str, embedding))
            f.write(f"{node}\t{embedding_str}\n")

    print("Node2Vec embeddings đã được lưu.")
except FileNotFoundError as e:
    print(f"Lỗi: Không tìm thấy file {e.filename}")
except ValueError as e:
    print(f"Lỗi giá trị: {e}")
except Exception as e:
    print(f"Lỗi không xác định: {e}")
