from Utils.LoggingManager.loggingmanager import LogginManager
from routing.windowsmanager import WindowManager
from view import windows as win
from view.windowsmanagerconfig import WindowsManagerConfig

if __name__ == '__main__':
    LogginManager().config()

    root_window = win.start_window()

    windows_manager = WindowManager(WindowsManagerConfig(root_window).get_config())
    windows_manager.go_to_window("LoginView")


    # win.set_login_screen(root_window)

    root_window.mainloop()
