import tkinter as tk
import win32gui
import win32api
import threading
import time
import pyautogui

selected_window = None

def get_running_windows():
    """현재 실행 중인 창의 제목을 가져옵니다."""
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        return True

    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def send_input_to_point(input_text, repetitions, interval):
    hwnd = selected_window[0]  # 선택된 창의 핸들을 가져옵니다.
    if hwnd:
        # 선택된 창에 포커스 이동
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)  # 포커스가 이동할 시간을 줍니다.

        # 클릭 이벤트 (창의 중앙으로 클릭)
        rect = win32gui.GetWindowRect(hwnd)
        x = (rect[0] + rect[2]) // 2
        y = (rect[1] + rect[3]) // 2
        pyautogui.click(x, y)  # pyautogui를 사용하여 클릭

        for _ in range(repetitions):
            # 텍스트 입력
            pyautogui.typewrite(input_text)  # pyautogui를 사용하여 텍스트 입력
            pyautogui.press('enter')  # 엔터키 입력
            time.sleep(interval)  # 주기 설정
    else:
        print("No foreground window found.")

def select_window(window_title):
    global selected_window
    for hwnd, title in running_windows:
        if title == window_title:
            selected_window = (hwnd, title)
            window_label.config(text=f"Selected Window: {title}")
            break

def start_typing():
    input_text = input_entry.get()
    repetitions = repeat_entry.get()
    interval = interval_entry.get()
    
    # 입력값 검증
    try:
        repetitions = int(repetitions)
        interval = float(interval)
    except ValueError:
        print("반복 횟수와 반복 주기는 숫자여야 합니다.")
        return

    if selected_window:
        print(f"Starting typing in: {selected_window[1]}")  # 디버깅 메시지
        threading.Thread(target=send_input_to_point, args=(input_text, repetitions, interval)).start()
    else:
        print("No window selected.")

# GUI 설정
root = tk.Tk()
root.title("자동 입력 프로그램")
root.geometry("400x400")

# 선택된 창 표시 라벨
window_label = tk.Label(root, text="Selected Window: None", font=("Arial", 12))
window_label.pack(pady=10)

# 현재 실행 중인 창 목록을 가져와서 드롭다운에 추가
running_windows = get_running_windows()
window_titles = [title for hwnd, title in running_windows]

# 드롭다운 목록
selected_window_var = tk.StringVar(root)
selected_window_var.set("Select a window")  # 기본값 설정
window_dropdown = tk.OptionMenu(root, selected_window_var, *window_titles, command=select_window)
window_dropdown.pack(pady=10)

# 입력창 라벨
input_label = tk.Label(root, text="입력할 문장", font=("Arial", 12))
input_label.pack(pady=10)

# 입력창
input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=10)

# 반복 횟수 라벨
repeat_label = tk.Label(root, text="반복 횟수", font=("Arial", 12))
repeat_label.pack(pady=10)

# 반복 횟수 입력창
repeat_entry = tk.Entry(root, width=10)
repeat_entry.pack(pady=10)

# 반복 주기 라벨
interval_label = tk.Label(root, text="반복 주기 (초)", font=("Arial", 12))
interval_label.pack(pady=10)

# 반복 주기 입력창
interval_entry = tk.Entry(root, width=10)
interval_entry.pack(pady=10)

# 시작 버튼
start_button = tk.Button(root, text="시작", command=start_typing)
start_button.pack(pady=20)

root.mainloop()