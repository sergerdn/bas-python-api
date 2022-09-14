import time

import psutil
import win32con
import win32gui
import win32process


def windows_is_visible(pid):
    def enum_handler(hwnd, data):
        if win32process.GetWindowThreadProcessId(hwnd)[1] == data[0] and win32gui.IsWindowVisible(hwnd):
            data[1] = True

    data = [pid, False]
    win32gui.EnumWindows(enum_handler, data)
    return data[1]


def window_set_visible(pid):
    def get_hwnds_for_pid(pid):
        def callback(hwnd, hwnds):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds

    handles = get_hwnds_for_pid(pid)
    if len(handles) > 0:
        wnd_handle = handles[0]
        win32gui.ShowWindow(wnd_handle, win32con.SW_SHOWNORMAL)
        return True

    return False


if __name__ == '__main__':
    process_name = "Worker.exe"


    def set_visible(pid):
        if windows_is_visible(pid):
            print(f"has visible window: {pid}")
        else:
            print(f"does not have visible window: {pid}")
            print(window_set_visible(pid))


    while 1:
        for proc in psutil.process_iter():
            if process_name in proc.name():
                pid = proc.pid
                set_visible(pid)

        time.sleep(1)
