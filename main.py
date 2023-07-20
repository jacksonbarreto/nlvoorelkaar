import os

import config.settings as gl
import logging

from controllers.logincontroller import LoginController
from view import windows as win
from view.loginview import LoginView

if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    info_handler = logging.FileHandler('logs/info.log')
    info_handler.setLevel(logging.INFO)

    error_handler = logging.FileHandler('logs/error.log')
    error_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    root_window = win.start_window()
    # ctk frame
    import customtkinter as ctk
    frame_ctk_tmp = ctk.CTkFrame(root_window)
    log_v = LoginView(root_window, LoginController(), frame_ctk_tmp)
    log_v.load_screen()

    #win.set_login_screen(root_window)

    root_window.mainloop()
