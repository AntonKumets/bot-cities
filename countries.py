# Импорт необходимых модулей
import matplotlib.pyplot as plt  # Импортируем модуль для создания и отображения графиков из библиотеки Matplotlib
import cartopy.crs as ccrs  # Импортируем модуль для работы с географическими проекциями из библиотеки Cartopy
import cartopy.feature as cfeature  # Импортируем модуль для работы с географическими объектами из библиотеки Cartopy

# Определяем функцию для создания контурной карты для заданного региона
def create_contour_map(region):
    # Создаем новый объект Figure и Axes с указанным размером и проекцией PlateCarree
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Устанавливаем экстент (пределы области) графика с помощью заданных координат
    ax.set_extent(region['extent'], ccrs.PlateCarree())
    
    # Добавляем географические объекты (береговые линии) на график
    ax.add_feature(cfeature.COASTLINE)
    
    # Добавляем географические объекты (границы стран) на график с определенным стилем линий
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Добавляем стандартное изображение карты мира на график
    ax.stock_img()
    
    # Сохраняем график в файл с именем, основанным на названии региона
    plt.savefig(f"{region['name'].replace(' ', '_')}.png")
    
    # Закрываем текущее изображение, чтобы освободить память
    plt.close()

# Список регионов для генерации карт
regions = [
    {'name': 'Africa', 'extent': [-20, 60, -40, 40]},  # Африка
    {'name': 'Canada', 'extent': [-140, -50, 40, 85]},  # Канада
    {'name': 'Japan', 'extent': [129, 146, 30, 46]},  # Япония
    {'name': 'China', 'extent': [73, 135, 18, 54]},  # Китай
    {'name': 'India', 'extent': [68, 90, 6, 37]},  # Индия
    {'name': 'Europe', 'extent': [-13, 30, 34, 77]},
    {'name': 'Brazil', 'extent': [-74, -28, 6, -36]}
]

# Создание карты для каждого региона из списка
for region in regions:
    create_contour_map(region)