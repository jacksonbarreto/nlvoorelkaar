from controllers.logincontroller import LoginController
from view.loginview import LoginView


class WindowsManagerConfig:
    def __init__(self, root_window):
        self.root_window = root_window

    def get_config(self):
        return {
            "LoginView": (LoginView, [],
                          {"root_window": self.root_window,
                           "login_controller": LoginController(),
                           "next_window": "HomeWindow"
                           })
        }
