def are_jpg_files_identical_by_bytes(file1_path, file2_path, tolerance=0):
    """
    Проверяет, идентичны ли два JPG-файла побайтово.

    Args:
        file1_path: Путь к первому JPG-файлу.
        file2_path: Путь ко второму JPG-файлу.

    Returns:
        True, если файлы идентичны, False в противном случае.
    """
    try:
        with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
            return file1.read() == file2.read()
    except FileNotFoundError:
        return False  # Один или оба файла не найдены

file1 = ".\cloud_6.ply"
file2 = ".\cloud_7.ply"

tolerance = 0.001  # Допустимое отклонение (например, 1 мм)

if are_jpg_files_identical_by_bytes(file1, file2, tolerance):
    print("Файлы идентичны побайтово.")
else:
    print("Файлы не идентичны побайтово.")