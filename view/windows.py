import json
import math
import random
import logging
import time
import urllib

import customtkinter as ctk
from controllers import logincontrollerold as lc
from controllers.logincontrollerold import logout, fast_login
from config.settings import SessionSingleton as ss, url_autocomplete
from config.settings import url_volunteer, headers, minimum_time, maximum_time, delay_to_start_sending
from bs4 import BeautifulSoup


def center_window(root_window):
    root_window.update_idletasks()
    width = root_window.winfo_width()
    height = root_window.winfo_height()
    x = (root_window.winfo_screenwidth() // 2) - (width // 2)
    y = (root_window.winfo_screenheight() // 2) - (height // 2)
    root_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def start_window():
    root_window = ctk.CTk()
    root_window.title("NL Voor Elkaar Manager")
    root_window.geometry("600x300")
    return root_window


def set_login_screen(root_window):
    width = 400
    height = 300
    root_window.geometry(f'{width}x{height}')
    root_window.title(f'{root_window.title()} - Login')
    root_window.resizable(False, False)
    frame = ctk.CTkFrame(root_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    username_label = ctk.CTkLabel(frame, text="E-mail")
    username_label.grid(row=0, column=0, sticky="ew", padx=10, pady=4)  # Add some padding
    username_entry = ctk.CTkEntry(frame, width=200)
    username_entry.configure(justify='center')
    username_entry.grid(row=1, column=0, padx=20)
    username_entry.insert(0, 'zodoende@asdasd.nl')

    password_label = ctk.CTkLabel(frame, text="Password")
    password_label.grid(row=2, column=0, sticky="ew", padx=10, pady=4)  # Add some padding
    password_entry = ctk.CTkEntry(frame, show="*", width=200)
    password_entry.configure(justify='center')
    password_entry.grid(row=3, column=0, padx=20)
    password_entry.insert(0, '6ocTtr$675RS')

    root_window.username_entry = username_entry
    root_window.password_entry = password_entry

    login_button = ctk.CTkButton(frame, text="Login", command=lambda: lc.login(root_window))
    login_button.grid(row=4, column=0, pady=30)

    error_label = ctk.CTkLabel(frame, text="", text_color="red")
    error_label.grid(row=5, column=0, sticky="ew", padx=10, pady=4)  # Add some padding
    root_window.error_label = error_label
    center_window(root_window)


def send_message(tab_view, root_window):
    if root_window.volunteers_ids is None:
        return
    total_recipients = len(root_window.volunteers_ids)
    if total_recipients > 0:
        loading_frame = ctk.CTkFrame(tab_view.tab("Send Messages"))
        loading_frame.grid(row=0, column=0, columnspan=3, rowspan=2, sticky="nsew")
        loading_frame.grid_rowconfigure(0, weight=1)
        loading_frame.grid_columnconfigure(0, weight=1)

        inner_frame = ctk.CTkFrame(loading_frame)
        inner_frame.grid(row=0, column=0, columnspan=3, rowspan=2, sticky="nsew", padx=0, pady=0)
        inner_frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid_rowconfigure(0, weight=2)
        inner_frame.grid_rowconfigure(3, weight=2)

        dummy_row = ctk.CTkLabel(inner_frame, text='')
        dummy_row.grid(row=0, column=0, sticky="nsew")
        dummy_row1 = ctk.CTkLabel(inner_frame, text='')
        dummy_row1.grid(row=3, column=0, sticky="nsew")

        progress_bar = ctk.CTkProgressBar(inner_frame, width=400)
        progress_bar.grid(row=1, column=0)

        percent_var = ctk.StringVar()
        percent_label = ctk.CTkLabel(inner_frame, textvariable=percent_var, )
        percent_label.grid(row=2, column=0, sticky="nsew", pady=(5, 0))

        progress_bar.set(0)
        current_recipient = 1
        logout()
        percent_var.set(f"Messaging will start in {int(delay_to_start_sending)} seconds.")
        tab_view.update_idletasks()
        time.sleep(delay_to_start_sending)
        for volunteer_id in root_window.volunteers_ids:
            fast_login(root_window)
            sent = False
            url = url_volunteer + str(volunteer_id) + '?showMessage=1'
            response = ss.get_session().get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                message_token = soup.find('input', {'name': 'message[_token]'})['value']
                message_loaded = soup.find('input', {'name': 'message[loaded]'})['value']
                data = {
                    'message[body]': root_window.message.get("1.0", "end-1c"),
                    'message[phoneNumber]': root_window.phone.get(),
                    'message[dusdat]': '',
                    'message[_token]': message_token,
                    'message[loaded]': message_loaded}

                # response = ss.get_session().post(url, data=data, headers=headers)
                if response.status_code == 200:
                    progress = current_recipient / len(root_window.volunteers_ids)
                    progress_bar.set(progress)
                    percent_var.set(f"Messages Sent: {current_recipient} out of {len(root_window.volunteers_ids)}.")
                    tab_view.update_idletasks()
                    inner_frame.update_idletasks()
                    current_recipient += 1
                    sent = True
                else:
                    logging.error(f"Error sending message to volunteer: {volunteer_id} | "
                                  f"Response text: {response.text}")

            else:
                logging.error(f"Error getting volunteer page: {volunteer_id} | Response text: {response.text}")

            logout()
            if sent and volunteer_id != root_window.volunteers_ids[-1]:
                time.sleep(random.uniform(minimum_time, maximum_time))

        root_window.volunteers_ids = []
        root_window.send_button.configure(state="disabled")
        root_window.message.delete("1.0", "end-1c")
        root_window.phone.set('')
        loading_frame.grid_forget()


def on_message_change(root_window):
    total_characters = len(root_window.message.get("1.0", "end-1c"))
    if total_characters > 3 and hasattr(root_window, 'volunteers_ids') and root_window.volunteers_ids is not None \
            and len(root_window.volunteers_ids) > 0:
        root_window.send_button.configure(state="normal")
    else:
        root_window.send_button.configure(state="disabled")


def set_main_screen(root_window):
    width = 1300
    height = 700
    root_window.geometry(f'{width}x{height}')
    root_window.title(f'{root_window.title()} - Main')
    root_window.resizable(False, False)

    root_window.checkbox_vars = {}

    tab_view = ctk.CTkTabview(root_window)
    tab_view.pack(fill="both", expand=True)
    tab_view.add("Send Messages")
    tab_view.add("Reminders")
    tab_view.tab("Send Messages").focus_set()
    tab_view.tab("Send Messages").grid_columnconfigure(0, weight=1)
    tab_view.tab("Reminders").grid_rowconfigure(0, weight=1)

    # Send Messages tab
    ## Category
    category_pratical_frame = ctk.CTkFrame(tab_view.tab("Send Messages"))
    category_pratical_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    category_pratical_frame.grid_columnconfigure(0, weight=1)
    pratical_label = ctk.CTkLabel(category_pratical_frame, text="Category")
    pratical_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

    categories_options = [
        {"id": "categories_11", "text": "Maatje, buddy & gezelschap", "value": "11"},
        {"id": "categories_10", "text": "Activiteiten\xadbegeleiding", "value": "10"},
        {"id": "categories_19", "text": "Klussen buiten & tuin", "value": "19"},
        {"id": "categories_32", "text": "Taal & lezen", "value": "32"},
        {"id": "categories_5", "text": "Administratie & receptie", "value": "5"},
        {"id": "categories_25", "text": "Begeleiding & coaching", "value": "25"},
        {"id": "categories_17", "text": "Bestuur & organisatie", "value": "17"},
        {"id": "categories_8", "text": "Boodschappen", "value": "8"},
        {"id": "categories_39", "text": "Collecte & inzamelacties", "value": "39"},
        {"id": "categories_4", "text": "Computerhulp & ICT", "value": "4"},
        {"id": "categories_31", "text": "Creativiteit & muziek", "value": "31"},
        {"id": "categories_29", "text": "Dierenverzorging", "value": "29"},
        {"id": "categories_49", "text": "Financiën & fondsenwerving", "value": "49"},
        {"id": "categories_9", "text": "Gastvrijheid & horeca", "value": "9"},
        {"id": "categories_50", "text": "Hulp bij armoede", "value": "50"},
        {"id": "categories_51", "text": "In een winkel", "value": "51"},
        {"id": "categories_38", "text": "Juridisch", "value": "38"},
        {"id": "categories_48", "text": "Klussen binnen", "value": "48"},
        {"id": "categories_2", "text": "Koken & maaltijden", "value": "2"},
        {"id": "categories_14", "text": "Marketing & communicatie", "value": "14"},
        {"id": "categories_46", "text": "Media & design", "value": "46"},
        {"id": "categories_18", "text": "Projectcoördinatie", "value": "18"},
        {"id": "categories_7", "text": "Schoonmaak", "value": "7"},
        {"id": "categories_3", "text": "Techniek & reparatie", "value": "3"},
        {"id": "categories_47", "text": "Training & scholing", "value": "47"},
        {"id": "categories_1", "text": "Vervoer & transport", "value": "1"}
    ]
    set_categories(categories_options, category_pratical_frame, root_window.checkbox_vars, tab_view, root_window)

    ## Theme
    theme_frame = ctk.CTkFrame(tab_view.tab("Send Messages"))
    theme_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    theme_frame.grid_columnconfigure(1, weight=1)
    theme_label = ctk.CTkLabel(theme_frame, text="Theme")
    theme_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

    theme_options = [
        {"id": "themes_12", "text": "Zorg", "value": "12"},
        {"id": "themes_9", "text": "Sociaal & welzijn", "value": "9"},
        {"id": "themes_8", "text": "Sport & beweging", "value": "8"},
        {"id": "themes_11", "text": "Tuin, dieren & natuur", "value": "11"},
        {"id": "themes_1", "text": "Belangenbehartiging & goede doelen", "value": "1"},
        {"id": "themes_2", "text": "Duurzaamheid & milieu", "value": "2"},
        {"id": "themes_3", "text": "Evenementen & festivals", "value": "3"},
        {"id": "themes_4", "text": "Kunst & cultuur", "value": "4"},
        {"id": "themes_5", "text": "Noodhulp", "value": "5"},
        {"id": "themes_6", "text": "Onderwijs & educatie", "value": "6"},
        {"id": "themes_7", "text": "Politiek", "value": "7"},
        {"id": "themes_10", "text": "Religie & zingeving", "value": "10"}
    ]
    set_categories(theme_options, theme_frame, root_window.checkbox_vars, tab_view, root_window)

    ## Location
    location_frame = ctk.CTkFrame(tab_view.tab("Send Messages"))
    location_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    location_label = ctk.CTkLabel(location_frame, text="Location")
    location_label.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=5)
    location_frame.grid_columnconfigure(0, weight=1)
    location_frame.grid_columnconfigure(1, weight=1)

    root_window.location = ctk.StringVar()
    location_label = ctk.CTkLabel(location_frame, text="find the city or postal code")
    location_label.grid(row=1, column=0, sticky="w", pady=(0, 3), padx=5)
    location_entry = ctk.CTkEntry(location_frame, textvariable=root_window.location)
    location_entry.bind("<Return>", lambda event: on_location_change(event, tab_view, root_window, option_menu))
    location_entry.bind("<KeyRelease>", lambda event: on_location_change(event, tab_view, root_window, option_menu))
    location_entry.grid(row=2, column=0, sticky="nsew", padx=5)

    root_window.location_options = []
    optionmenu_label = ctk.CTkLabel(location_frame, text="Select the City or Postal Code")
    optionmenu_label.grid(row=1, column=1, sticky="w", pady=(0, 3), padx=5)
    option_menu = ctk.CTkOptionMenu(location_frame, values=root_window.location_options,
                                    command=lambda event: on_location_option_change(event, tab_view, root_window))
    option_menu.set("No results found")
    option_menu.grid(row=2, column=1, sticky="nsew", pady=(0, 3), padx=(10, 5))

    root_window.distance = ctk.IntVar(value=1)
    text_distance = ctk.StringVar()
    text_distance.set("Current Distance: 1 km")

    def update_distance_label(*args):
        text_distance.set(f"Current Distance: {str(root_window.distance.get())} km")

    root_window.distance.trace_add("write", update_distance_label)
    distance_label = ctk.CTkLabel(location_frame, text="Distance (km)")
    distance_label.grid(row=3, column=0, sticky="w", pady=(15, 3), padx=5)

    slider_frame = ctk.CTkFrame(location_frame)
    slider_frame.grid(row=4, column=0, sticky="nsew", padx=5)

    start_label = ctk.CTkLabel(slider_frame, text="1 km ")
    start_label.pack(side="left")

    distance_entry = ctk.CTkSlider(slider_frame, from_=1, to=50, variable=root_window.distance)
    distance_entry.bind("<ButtonRelease-1>", lambda event: on_distance_change(event, tab_view, root_window))
    distance_entry.pack(side="left", ipady=3, expand=True, fill="x")
    distance_entry.configure(state="disabled")
    root_window.distance_entry = distance_entry
    end_label = ctk.CTkLabel(slider_frame, text="50 km")
    end_label.pack(side="left")

    current_value_label = ctk.CTkLabel(location_frame, textvariable=text_distance)
    current_value_label.grid(row=5, column=0, sticky="w", pady=(3, 0), padx=5)

    ## Total Volunteers
    total_volunteers_frame = ctk.CTkFrame(tab_view.tab("Send Messages"))
    total_volunteers_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    total_volunteers_label = ctk.CTkLabel(total_volunteers_frame, text="Total Volunteers")
    total_volunteers_label.grid(row=0, column=0, sticky="w", pady=(15, 3))

    root_window.total_volunteers = ctk.IntVar()
    total_volunteers = ctk.CTkLabel(total_volunteers_frame, textvariable=root_window.total_volunteers)
    total_volunteers.grid(row=1, column=2, sticky="w", pady=(0, 3))

    capture_all_volunteers_button = ctk.CTkButton(total_volunteers_frame, text="Capture All Volunteers",
                                                  command=lambda: capture_all_volunteers(tab_view, root_window))
    capture_all_volunteers_button.grid(row=2, column=2, sticky="w", pady=(0, 3))

    ## Message
    message_frame = ctk.CTkFrame(tab_view.tab("Send Messages"))
    message_frame.grid(row=0, column=2, sticky="nsew", rowspan=2, padx=10, pady=10)
    message_frame.grid_columnconfigure(2, weight=4)
    message_label = ctk.CTkLabel(message_frame, text="Message")
    message_label.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=(5, 0))

    root_window.message = ctk.StringVar()

    message_entry = ctk.CTkTextbox(message_frame, width=380, height=450)
    root_window.message = message_entry
    message_entry.grid(row=1, column=0, sticky="nsew", ipady=3, padx=10)
    message_entry.bind("<KeyRelease>", lambda event: on_message_change(root_window))

    root_window.phone = ctk.StringVar()
    phone_label = ctk.CTkLabel(message_frame, text="Phone Number")
    phone_label.grid(row=2, column=0, sticky="w", pady=(15, 3))
    phone_entry = ctk.CTkEntry(message_frame, textvariable=root_window.phone)
    phone_entry.grid(row=3, column=0, sticky="nsew", ipady=3, padx=10)

    send_button = ctk.CTkButton(message_frame, text="Send", command=lambda: send_message(tab_view, root_window))
    root_window.send_button = send_button
    send_button.grid(row=4, column=0, sticky="nsew", pady=(15, 0), padx=10)
    send_button.configure(state="disabled")

    # center_window(root_window)


def set_categories(categories, categories_frame, checkbox_vars, tab_view, root_window):
    rows_per_column = 13

    for i, category in enumerate(categories):
        column, row = divmod(i, rows_per_column)

        var = ctk.StringVar()
        checkbox = ctk.CTkCheckBox(categories_frame, text=category["text"], variable=var, onvalue=category["value"],
                                   offvalue="", command=lambda: on_filter_change(tab_view, root_window))
        checkbox.grid(row=row + 1, column=column, sticky="w", ipady=3, padx=(0, 38))

        checkbox_vars[category["id"]] = var


def on_filter_change(tab_view, root_window):
    loading_frame = ctk.CTkFrame(tab_view.tab("Send Messages"))
    loading_frame.grid(row=0, column=0, columnspan=3, rowspan=2, sticky="nsew", padx=10, pady=10)
    loading_frame.grid_rowconfigure(0, weight=1)
    loading_frame.grid_columnconfigure(0, weight=1)
    progress_bar = ctk.CTkProgressBar(loading_frame)
    progress_bar.grid(row=0, column=0)
    progress_bar.start()

    def stop_and_close():
        progress_bar.stop()
        loading_frame.grid_forget()

    total_volunteers = get_total_volunteers(root_window)
    root_window.total_volunteers.set(total_volunteers)
    root_window.volunteers_ids = None
    # Schedule stop_and_close to be run after 30000 milliseconds (30 seconds)
    loading_frame.after(500, stop_and_close)


def on_location_change(event, tab_view, root_window, option_menu):
    try:
        if len(root_window.location.get()) >= 3:
            url = url_autocomplete + root_window.location.get()
            response = ss.get_session().get(url, headers=headers)
            data = json.loads(response.text)

            if len(data) == 0:
                option_menu.configure(values=[])
                option_menu.set("No results found")
                root_window.location_ids_types = {}
            else:
                data.sort(key=lambda item: item['score'], reverse=True)
                root_window.location_options = data

                locales = {
                    f"{item['name']} ({item['subtitle']})" if item['subtitle'] and item['subtitle'] != 'Postcode' else item[
                        'name']: item for item in data}
                option_menu.configure(values=list(locales.keys()))
                option_menu.set(list(locales.keys())[0])
                root_window.location_ids_types = {
                    f"{item['name']} ({item['subtitle']})" if item['subtitle'] and item['subtitle'] != 'Postcode' else item[
                        'name']: (item['id'], item['type'], item['subtitle']) for item in data
                }

    except Exception as e:
        logging.error(e)


def on_distance_change(event, tab_view, root_window):
    if root_window.distance_entry.cget('state') != "disabled":
        on_filter_change(tab_view, root_window)


def on_location_option_change(event, tab_view, root_window):
    root_window.location.set(event)
    if root_window.location_ids_types[event][0] is not None and root_window.location_ids_types[event][1] is not None:
        root_window.distance_entry.configure(state="disabled")
    else:
        root_window.distance_entry.configure(state="normal")
    on_filter_change(tab_view, root_window)


def get_total_volunteers(root_window):
    url = make_url(root_window)
    response = ss.get_session().get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    total_volunteers = soup.find('span', {'class': 'c-brush-underline__text'}).text
    return total_volunteers


def capture_all_volunteers(tab_view, root_window):
    if root_window.location_ids_types.get(root_window.location.get()) is None:
        return

    loading_frame = ctk.CTkFrame(tab_view.tab("Send Messages"))
    loading_frame.grid(row=0, column=0, columnspan=3, rowspan=2, sticky="nsew", padx=10, pady=10)
    loading_frame.grid_rowconfigure(0, weight=1)
    loading_frame.grid_columnconfigure(0, weight=1)
    volunteers_to_capture = int(root_window.total_volunteers.get())
    num_pages = 1 if volunteers_to_capture == 0 else math.ceil(volunteers_to_capture / 23)
    progress_bar = ctk.CTkProgressBar(loading_frame)
    progress_bar.grid(row=0, column=0)
    percent_var = ctk.StringVar()
    percent_label = ctk.CTkLabel(loading_frame, textvariable=percent_var)
    percent_label.grid(row=1, column=0)

    url = make_url(root_window)
    try:
        response = ss.get_session().get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        key = soup.find('input', {'name': 'key'})['value']
        url = f"{url}&key={key}"
    except Exception as e:
        logging.error(e)
        return

    root_window.volunteers_ids = []
    current_page = 1
    while True:
        page_url = f"{url}&p={current_page}&submitSearchForm=1#"
        response = ss.get_session().get(page_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        elements = soup.find_all(['article', 'section'])
        for element in elements:
            classes = set(element.get('class', []))
            if element.name == 'section' and {'c-results-banner', 'c-results-banner--center'}.issubset(classes):
                break

            if element.name == 'article' and {'c-card', 'c-card--offer', 'js-card'}.issubset(classes):
                anchor = element.find('a', {'class': 'c-card__anchor'})
                if anchor:
                    volunteer_id = anchor.get('id')
                    root_window.volunteers_ids.append(volunteer_id)

        next_button = soup.find('a', {'rel': 'next'})
        progress = current_page / num_pages
        progress_bar.set(progress)
        percent_var.set(f"{progress * 100:.1f}%")
        tab_view.update_idletasks()
        if next_button:
            current_page += 1
        else:
            break

    logging.info(f'Total volunteers captured: {len(root_window.volunteers_ids)}')
    logging.info(f'Captured volunteers: {root_window.volunteers_ids}')
    loading_frame.grid_forget()
    on_message_change(root_window)


def make_url(root_window):
    categories = []
    for key, var in root_window.checkbox_vars.items():
        if var.get():
            categories.append(f"categories%5B%5D={var.get()}")

    params = []
    if root_window.location.get():
        location = urllib.parse.quote(root_window.location.get())
        params.append(f"region%5Blocation%5D={location}")
        location_id = root_window.location_ids_types[root_window.location.get()][0] if \
            root_window.location_ids_types[root_window.location.get()][0] is not None else ''
        params.append(f"region%5Blocation_id%5D={location_id}")
        location_type = root_window.location_ids_types[root_window.location.get()][1] if \
            root_window.location_ids_types[root_window.location.get()][1] is not None else ''
        params.append(f"region%5Blocation_type%5D={location_type}")
        if root_window.location_ids_types[root_window.location.get()][2] == 'Postcode':
            params.append(f"region%5Brange%5D={root_window.distance.get()}")

    if categories:
        params.extend(categories)

    if params:
        return f"{url_volunteer}?{'&'.join(params)}"
    else:
        return url_volunteer
