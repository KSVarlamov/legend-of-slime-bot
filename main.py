import time
import importlib
import os
import threading
import config
import utils
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
            if hasattr(module, "name") and hasattr(module, "description") and hasattr(module, "run"):
                modules.append(module)
        except Exception as e:
            print(f"Ошибка загрузки {module_name}: {e}")

    return modules

# Запуск модулей в отдельных потоках
def run_module(module):
    while True:
        module.run()
        time.sleep(module.interval)

def main():
    print("Поиск окна BlueStacks...")
    x, y = find_bluestacks_window()
    
    if x is None:
        print("Ошибка: окно BlueStacks не найдено!")
        return
    
    print(f"BlueStacks найден! Координаты: {x}, {y}")
    
    print("\nЗагрузка модулей...")
    modules = load_modules()

    if not modules:
        print("Не найдено ни одного модуля.")
        return

    print("\nЗагруженные модули:")
    for mod in modules:
        print(f"- {mod.name}: {mod.description} (Интервал: {mod.interval} сек.)")

    # Запуск модулей в потоках
    for mod in modules:
        thread = threading.Thread(target=run_module, args=(mod,))
        thread.daemon = True
        thread.start()

    print("\nБот запущен!")
    while True:
        time.sleep(1)  # Главное меню в ожидании

if __name__ == "__main__":
    main()
