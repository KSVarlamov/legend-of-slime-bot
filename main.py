import time
import importlib
import os
import config
import pygetwindow as gw

# Найти окно BlueStacks
def find_bluestacks_window():
    for window in gw.getWindowsWithTitle(config.BLUESTACKS_TITLE):
        return window._rect.left, window._rect.top
    return None, None

# Загрузить модули из папки modules
def load_modules():
    modules = []
    module_files = [f[:-3] for f in os.listdir("modules") if f.endswith(".py") and f != "__init__.py"]

    for module_name in module_files:
        try:
            module = importlib.import_module(f"modules.{module_name}")
            print(f"Загружаем: {module_name}")  # <--- ВЫВОДИТЬ ИМЕНА МОДУЛЕЙ
            
            if hasattr(module, "name") and hasattr(module, "description") and hasattr(module, "run") and hasattr(module, "interval"):
                modules.append(module)
            else:
                print(f"Модуль {module_name} не имеет всех необходимых атрибутов!")
        except Exception as e:
            print(f"Ошибка загрузки {module_name}: {e}")

    return modules


def main():
    print("Поиск окна BlueStacks...")
    x, y = find_bluestacks_window()
    
    if x is None:
        print("Ошибка: окно BlueStacks не найдено!")
        return
    
    print(f"BlueStacks найден! Координаты: {x}, {y}")
    
    print("\nЗагрузка модулей...")  # <-- Здесь исправлено

    modules = load_modules()

    if not modules:
        print("Не найдено ни одного модуля.")
        return

    print("\nЗагруженные модули:")
    for mod in modules:
        print(f"- {mod.name}: {mod.description} (Интервал: {mod.interval} сек.)")

    print("\nБот запущен!")  # <-- Здесь тоже проверил

    # Основной цикл работы
    while True:
        for mod in modules:
            print(f"\nЗапуск модуля: {mod.name}")
            mod.run()  # Выполнение модуля
            print(f"Ожидание {mod.interval} секунд перед следующим модулем...")
            time.sleep(mod.interval)


if __name__ == "__main__":
    main()
