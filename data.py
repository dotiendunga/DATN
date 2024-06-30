# import openpyxl
# import haversine as hs

# # Mở file Excel
# def distance_target(current_position,target_position):
#     try:
#         wb = openpyxl.load_workbook('line_point.xlsx')
#         sheet = wb['sheetdata']  # Thay 'sheetdata' bằng tên sheet cần đọc
#     except FileNotFoundError:
#         print("Không tìm thấy tệp Excel tại đường dẫn đã chỉ định.")
#     # Khởi tạo biến để lưu giá trị từ hai cột
#     column_values = []
#     # Đọc các giá trị từ sheet và tính khoảng cách
#     for row in sheet.iter_rows(values_only=True, min_row=3, max_row=sheet.max_row):
#         column_values.append((float(row[1]), float(row[2])))
#     # Tìm điểm trên dải tọa độ gần nhất
#     nearest_coord = min(column_values, key=lambda coord: hs.haversine(current_position, coord))
#     # Xác định chỉ mục của điểm gần nhất trong danh sách line_coords
#     index_of_nearest = column_values.index(nearest_coord)

#     # Tìm điểm trên dải tọa độ gần nhất
#     target_coord = min(column_values, key=lambda coord: hs.haversine(target_position, coord))
#     # Xác định chỉ mục của điểm gần nhất trong danh sách line_coords
#     index_of_target = column_values.index(target_coord)
#     total =0.0
#     for i in range(min(index_of_nearest, index_of_target),max(index_of_nearest, index_of_target)):
#         distance = hs.haversine(column_values[i], column_values[i + 1])
#         path_1 = map_widget.set_path([marker_2.position, marker_3.position, (52.57, 13.4), (52.55, 13.35)])
#         total+=distance
#     return total
