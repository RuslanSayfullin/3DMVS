import open3d as o3d
import numpy as np

def compare_ply_files(file1, file2, tolerance=1e-6):
    """
    Сравнивает два .ply файла на основе координат точек.

    Args:
        file1: Путь к первому .ply файлу.
        file2: Путь ко второму .ply файлу.
        tolerance: Допустимое отклонение координат.

    Returns:
        True, если точечные облака "похожи" (в пределах допуска), False - иначе.
    """
    try:
        # 1. Загрузка файлов
        cloud1 = o3d.io.read_point_cloud(file1)
        cloud2 = o3d.io.read_point_cloud(file2)

        # 2. Сравнение количества точек
        if len(cloud1.points) != len(cloud2.points):
            print(f"Разное количество точек: {len(cloud1.points)} vs {len(cloud2.points)}")
            return False

        # 3. Сравнение координат (поиск ближайших точек)
        points1 = np.asarray(cloud1.points)
        points2 = np.asarray(cloud2.points)

        # Создаем структуру k-d tree для быстрого поиска ближайших соседей в cloud2
        pcd_tree = o3d.geometry.KDTreeFlann(cloud2)

        max_distance = 0.0
        for i, point1 in enumerate(points1):
            [k, idx, dist_sq] = pcd_tree.search_knn_vector_3d(point1, 1) # Ищем ближайшую точку в cloud2

            distance = np.sqrt(dist_sq[0]) # Расстояние до ближайшей точки
            max_distance = max(max_distance, distance)

        if max_distance <= tolerance:
            print("Точечные облака совпадают (в пределах допуска).")
            return True
        else:
            print(f"Точечные облака отличаются. Максимальное расстояние: {max_distance}")
            return False

    except Exception as e:
        print(f"Ошибка при сравнении файлов: {e}")
        return False

# Пример использования:
file1 = ".\cloud_1.ply"
file2 = ".\cloud_2.ply"
tolerance = 5  # Допустимое отклонение (например, 1 мм)

if compare_ply_files(file1, file2, tolerance):
    print("Файлы похожи.")
else:
    print("Файлы разные.")