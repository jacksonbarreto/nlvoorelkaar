from Utils.LoggingManager.LoggingManager import LogginManager
from controllers.logincontroller import LoginController
from routing.windowsmanager import WindowManager
from view import windows as win
from view.loginview import LoginView

if __name__ == '__main__':
    LogginManager().config()

    root_window = win.start_window()
    config = {
        "LoginView": (LoginView, [],
                      {"root_window": root_window,
                       "login_controller": LoginController(),
                       "next_window": "HomeWindow"
                       })
    }

    windows_manager = WindowManager(config)
    windows_manager.go_to_window("LoginView")


    # win.set_login_screen(root_window)

    root_window.mainloop()
