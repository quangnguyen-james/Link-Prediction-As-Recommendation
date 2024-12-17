# Link-Prediction-As-Recommendation
Bài nghiên cứu phân tích Link Prediction as Recommendation 
Bộ dữ liệu sử dụng: ego-facebook
1. Phân tích bộ dữ liệu:
    - File: <ego>.edges
        + Mỗi dòng đại diện cho một cạnh (edge) giữa hai nút (node).
        + Cấu trúc: node1 node2.
        + Là tệp quan trọng nhất, chứa toàn bộ thông tin về mạng xã hội ego.
    - File: <ego>.circles:
        + Chứa thông tin về các nhóm (circles) mà ego đã xác định.
        + Dòng đầu là tên của nhóm (circle).
        + Các số tiếp theo là danh sách các nút (node IDs) thuộc nhóm đó.
    - File: <ego>.egofeat
        + Chứa vector đặc trưng của ego.
        + Một dòng với các giá trị đặc trưng (features) cho ego.
    - File: <ego>.feat
        + Chứa vector đặc trưng của tất cả các nút khác (neighbors của ego).
        + Mỗi dòng tương ứng với một nút; Dạng: feature1 feature2 ....
    - File: <ego>.featnames:
        + Cung cấp tên của các đặc trưng trong tệp .egofeat và .feat.
        + Mỗi dòng mô tả một đặc trưng, ví dụ: Feature_1, Feature_2
    - File: facebook_combined.txt
        + Mạng xã hội kết hợp của toàn bộ các ego trong bộ dữ liệu.
        + Tương tự .edges, mỗi dòng chứa một cạnh node1 node2.

