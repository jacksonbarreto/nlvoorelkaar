from view.loginview import LoginView

config = {
    "LoginView": (LoginView, [],
                  {"root_window": root_window,
                   "login_controller": LoginController(),
                   "next_window": "HomeWindow"}
                  )
}