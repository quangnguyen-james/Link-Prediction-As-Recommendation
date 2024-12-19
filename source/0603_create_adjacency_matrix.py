#-- Tạo ma trận kề
import pandas as pd
import networkx as nx

# Đọc đồ thị từ file GraphML
graphml_file = "graph/processed_graph.graphml"
G = nx.read_graphml(graphml_file)

# 1. Lấy danh sách các node từ đồ thị
nodes = list(G.nodes)
print(f"✅ Số lượng node trong đồ thị: {len(nodes)}")

# 2. Tạo ma trận kề từ đồ thị
# Đảm bảo danh sách node khớp với đồ thị
nodes = list(G.nodes)
adjacency_matrix = nx.to_pandas_adjacency(G, nodelist=nodes, dtype=int)

rows = set(adjacency_matrix.index)
cols = set(adjacency_matrix.columns)

# Lấy chỉ mục chung nếu cần
common_indices = list(rows.intersection(cols))
adjacency_matrix = adjacency_matrix.loc[common_indices, common_indices]

# In metadata của đồ thị
#for node in G.nodes(data=True):
#    print(node)

# 3. Kiểm tra tính nhất quán của hàng và cột
rows = set(adjacency_matrix.index)
cols = set(adjacency_matrix.columns)

assert rows == cols, "⚠️ Hàng và cột vẫn không khớp!"

print(f"Số lượng hàng: {len(rows)}, Số lượng cột: {len(cols)}")
print(f"Danh sách hàng: {list(rows)[:10]}")  # Hiển thị 10 phần tử đầu tiên
print(f"Danh sách cột: {list(cols)[:10]}")  # Hiển thị 10 phần tử đầu tiên

missing_in_rows = cols - rows
missing_in_cols = rows - cols

if missing_in_rows or missing_in_cols:
    print(f"⚠️ Node thiếu trong hàng: {missing_in_rows}")
    print(f"⚠️ Node thiếu trong cột: {missing_in_cols}")
else:
    print("✅ Không có node nào bị thiếu.")

# Điền giá trị mặc định
adjacency_matrix.fillna(0, inplace=True)

# Loại bỏ các dòng hoặc cột không hợp lệ
adjacency_matrix = adjacency_matrix.loc[adjacency_matrix.index.intersection(adjacency_matrix.columns), 
                                         adjacency_matrix.index.intersection(adjacency_matrix.columns)]

# Kiểm tra lại
assert set(adjacency_matrix.index) == set(adjacency_matrix.columns), "Hàng và cột vẫn không khớp!"

if rows != cols:
    print("⚠️ Hàng và cột không đồng nhất. Đang xử lý...")
    common_indices = list(rows.intersection(cols))
    print(f"✅ Số lượng chỉ mục chung: {len(common_indices)}")
    adjacency_matrix = adjacency_matrix.loc[common_indices, common_indices]
else:
    print("✅ Hàng và cột của ma trận kề đồng nhất!")

# Kiểm tra kiểu dữ liệu trước khi lưu
print("Trước khi lưu:")
print(f"adjacency_matrix.index.dtype: {adjacency_matrix.index.dtype}")
print(f"adjacency_matrix.index.dtype: {adjacency_matrix.index.dtype}")

# 4. Lưu ma trận kề vào file CSV
output_file = "prepare_traindata/combined_adjacency_matrix.csv"
adjacency_matrix.index = adjacency_matrix.index.astype(str)
adjacency_matrix.columns = adjacency_matrix.columns.astype(str)
adjacency_matrix.index = adjacency_matrix.index.str.strip()
adjacency_matrix.columns = adjacency_matrix.columns.str.strip()
adjacency_matrix.to_csv(output_file, index=True)
print(f"✅ Ma trận kề đã được lưu tại: {output_file}")

# Đọc lại ma trận kề
adjacency_matrix = pd.read_csv("prepare_traindata/combined_adjacency_matrix.csv", index_col=0)

# Kiểm tra kiểu dữ liệu sau khi đọc
print("Sau khi đọc:")
print(f"adjacency_matrix.index.dtype: {adjacency_matrix.index.dtype}")
print(f"adjacency_matrix.index.dtype: {adjacency_matrix.index.dtype}")
