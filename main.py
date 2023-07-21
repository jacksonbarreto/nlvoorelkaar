from Utils.LoggingManager.LoggingManager import LogginManager
from controllers.logincontroller import LoginController
from view import windows as win
from view.loginview import LoginView

if __name__ == '__main__':
    LogginManager().config()

    root_window = win.start_window()

    # ctk frame
    import customtkinter as ctk
    frame_ctk_tmp = ctk.CTkFrame(root_window)
    log_v = LoginView(root_window, LoginController(), frame_ctk_tmp)
    log_v.load_screen()

    #win.set_login_screen(root_window)

    root_window.mainloop()
