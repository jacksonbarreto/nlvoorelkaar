import globals.globals as gl
import logging
from view import windows as win

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    info_handler = logging.FileHandler('info.log')
    info_handler.setLevel(logging.INFO)

    error_handler = logging.FileHandler('error.log')
    error_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    root_window = win.start_window()
    win.set_login_screen(root_window)

    root_window.mainloop()
