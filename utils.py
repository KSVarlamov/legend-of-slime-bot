import pyautogui

def click(x, y):
    pyautogui.click(x, y)

def get_screenshot(region):
    return pyautogui.screenshot(region=region)
