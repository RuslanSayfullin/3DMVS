
import open3d as o3d

# Загрузка файла .ply
pcd = o3d.io.read_point_cloud(".\cloud_1.ply")

# Проверка, правильно ли загружены данные
if pcd.is_empty():
    print("Не удалось загрузить .ply файл")
else:
    # Отображение облака точек
    o3d.visualization.draw_geometries([pcd])