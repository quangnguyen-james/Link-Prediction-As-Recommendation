#-- Lỗi: hàng và cột của ma trận kề không đồng nhất
import pandas as pd

# Đọc lại ma trận kề
adjacency_matrix = pd.read_csv("prepare_traindata/combined_adjacency_matrix.csv", index_col=0, dtype=str)
adjacency_matrix.index = adjacency_matrix.index.astype(str) 
adjacency_matrix.columns = adjacency_matrix.columns.astype(str)

# Xác minh tính đồng nhất
print("Kích thước ma trận:", adjacency_matrix.shape)
assert set(adjacency_matrix.index) == set(adjacency_matrix.columns), "Hàng và cột không khớp!"
print("✅ Ma trận kề đã đồng nhất và sẵn sàng sử dụng.")
