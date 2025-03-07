import pandas as pd
import matplotlib.pyplot as plt

def visualize_point_cloud(csv_file):
    """
    Читает CSV-файл с облаком точек (без заголовков) и визуализирует его.

    Аргументы:
        csv_file: Путь к CSV-файлу.
    """

    try:
        # Чтение CSV-файла в DataFrame, указываем, что нет заголовков
        df = pd.read_csv(csv_file, header=None)

        # Извлечение координат (столбцы по умолчанию: 0, 1, 2)
        x = df[0]
        y = df[1]
        z = df[2]

        # Визуализация
        plt.figure(figsize=(8, 6))

        # 3D-график
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, s=1)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Облако точек')

        plt.show()

    except FileNotFoundError:
        print(f"Ошибка: Файл '{csv_file}' не найден.")
    except KeyError as e:
        print(f"Ошибка: Столбец '{e}' не найден в CSV-файле.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Пример использования:
file_path = './Image_Cloud.csv'  # Замените на фактический путь к вашему файлу

visualize_point_cloud(file_path)