from bs4 import BeautifulSoup

import globals.globals as gl
from globals.globals import SessionSingleton as ss, url_logout, url_login_page, url_login


def login(root_window):
    root_window.error_label.configure(text="")
    if fast_login(root_window):
        from view.windows import set_main_screen
        set_main_screen(root_window)
    else:
        root_window.error_label.configure(text="Login failed, please try again.")


def fast_login(root_window):
    response = ss.get_session().get(url_login_page, headers=gl.headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': '_csrf_token'})['value']
    data = {'_csrf_token': csrf_token, '_username': root_window.username_entry.get(),
            '_password': root_window.password_entry.get(), '_remember_me': 'on'}

    response = ss.get_session().post(url_login, data=data, headers=gl.headers)
    if response.status_code == 200 and response.url == 'https://www.nlvoorelkaar.nl/mijn-pagina/berichten?authentication=success':
        return True
    else:
        return False


def logout():
    response = ss.get_session().get(url_logout, headers=gl.headers)

    if response.status_code == 302:
        return True
    else:
        return False
