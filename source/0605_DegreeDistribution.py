import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os

# Đường dẫn tới file GraphML
input_graphml_file = r"graph\processed_graph.graphml"

# Kiểm tra sự tồn tại của file
if not os.path.exists(input_graphml_file):
    raise FileNotFoundError(f"File not found: {input_graphml_file}")

# Đọc đồ thị từ file GraphML
G = nx.read_graphml(input_graphml_file)

# Tính phân phối bậc nút
degrees = [deg for _, deg in G.degree()]
degree_counts = np.bincount(degrees)
degree_values = np.nonzero(degree_counts)[0]

# Chuyển sang thang log-log
plt.figure(figsize=(10, 6))
plt.scatter(degree_values, degree_counts[degree_values], c='b', alpha=0.6, edgecolor='k')
plt.xscale('log')
plt.yscale('log')
plt.title("Degree Distribution (Log-Log Scale)")
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

# Lưu biểu đồ
output_plot_file = "processed_result/degree_distribution_processed_graph.png"
plt.savefig(output_plot_file)
plt.show()

print(f"Degree distribution plot saved to {output_plot_file}")
