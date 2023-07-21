
class WindowManager:
    def __init__(self, config):
        self.current_window = None
        self.config = config # { "LoginWindow": (LoginWindow, [arg1, arg2], {"key": "value"}), "AnotherWindow": (AnotherWindow, [arg3, arg4], {}),}

    def go_to_window(self, window_name):
        if self.current_window is not None:
            self.current_window.destroy()
        window_class, args, kwargs = self.config[window_name]
        self.current_window = window_class(*args, **kwargs)
        self.current_window.load_screen()