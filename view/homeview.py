import math
from typing import Optional

from routing.windowsmanagerinterface import WindowManagerInterface
from services.servicemanagerinterface import ServiceManagerInterface
from view.baseview import BaseView
import customtkinter as ctk

from view.utilsgui import center_window


class HomeView(BaseView):
    def __init__(self, root_window: ctk.CTk, windows_manager: WindowManagerInterface,
                 service_manager: ServiceManagerInterface, specific_title: Optional[str] = None,
                 generic_title: Optional[str] = None, width: Optional[int] = None, height: Optional[int] = None):
        super().__init__(root_window, windows_manager)
        self.service_manager = service_manager
        self.service_manager.subscribe(self)
        self.generic_title = "NL Voor Elkaar Manager" if generic_title is None else generic_title
        self.specific_title = "Home" if specific_title is None else specific_title
        self.width = 1300 if width is None else width
        self.height = 700 if height is None else height
        self.widgets = []
        self.tab_view = ctk.CTkTabview(self.root_window)
        self.tab_names = ["Send Messages", "Reminders"]
        self.checkbox_vars = {}
        self.location = None
        self.location_options = []
        self.distance = None
        self.text_distance = None
        self.distance_entry = None
        self.total_volunteers = None
        self.message = None
        self.phone = None
        self.send_button = None
        self.percent_var = None
        self.loading_frame = None
        self.progress_bar = None
        self.option_menu = None
        self.location_ids_types = {}

    def configure_tab_view(self) -> None:
        self.tab_view.pack(fill="both", expand=True)
        self.tab_view.add("Send Messages")
        self.tab_view.add("Reminders")
        self.tab_view.tab("Send Messages").focus_set()
        self.tab_view.tab("Send Messages").grid_columnconfigure(0, weight=1)
        self.tab_view.tab("Reminders").grid_rowconfigure(0, weight=1)

    def configure_window_style(self) -> None:
        self.root_window.geometry(f'{self.width}x{self.height}')
        self.root_window.title(f'{self.generic_title} - {self.specific_title}')
        self.root_window.resizable(False, False)

    def load_screen(self):
        self.configure_window_style()
        self.configure_tab_view()
        self.create_categories_filter()
        self.create_theme_filter()
        self.create_location_filter()
        self.create_box_get_volunteers()
        self.create_message_frame()
        x = (self.root_window.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.root_window.winfo_screenheight() // 2) - (self.height // 2)
        self.root_window.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

    def create_categories_filter(self):
        category_frame = ctk.CTkFrame(self.tab_view.tab(self.tab_names[0]))
        category_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        category_frame.grid_columnconfigure(0, weight=1)
        self.widgets.append(category_frame)

        category_label = ctk.CTkLabel(category_frame, text="Category")
        category_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.widgets.append(category_label)

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
        self.set_categories(categories_options, category_frame)

    def create_theme_filter(self):
        theme_frame = ctk.CTkFrame(self.tab_view.tab(self.tab_names[0]))
        theme_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        theme_frame.grid_columnconfigure(1, weight=1)
        self.widgets.append(theme_frame)

        theme_label = ctk.CTkLabel(theme_frame, text="Theme")
        theme_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.widgets.append(theme_label)

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
        self.set_categories(theme_options, theme_frame)

    def set_categories(self, categories, categories_frame):
        rows_per_column = 13

        for i, category in enumerate(categories):
            column, row = divmod(i, rows_per_column)

            var = ctk.StringVar()
            checkbox = ctk.CTkCheckBox(categories_frame, text=category["text"], variable=var, onvalue=category["value"],
                                       offvalue="", command=lambda: self.on_filter_change())
            checkbox.grid(row=row + 1, column=column, sticky="w", ipady=3, padx=(0, 38))
            self.widgets.append(checkbox)

            self.checkbox_vars[category["id"]] = var

    def create_location_filter(self):
        location_frame = ctk.CTkFrame(self.tab_view.tab(self.tab_names[0]))
        location_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        location_frame.grid_columnconfigure(0, weight=1)
        location_frame.grid_columnconfigure(1, weight=1)
        self.widgets.append(location_frame)

        location_label = ctk.CTkLabel(location_frame, text="Location")
        location_label.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=5)
        self.widgets.append(location_label)

        self.location = ctk.StringVar()
        location_label = ctk.CTkLabel(location_frame, text="find the city or postal code")
        location_label.grid(row=1, column=0, sticky="w", pady=(0, 3), padx=5)
        self.widgets.append(location_label)

        location_entry = ctk.CTkEntry(location_frame, textvariable=self.location)
        location_entry.bind("<Return>", lambda event: self.on_location_change())
        location_entry.bind("<KeyRelease>", lambda event: self.on_location_change())
        location_entry.grid(row=2, column=0, sticky="nsew", padx=5)
        self.widgets.append(location_entry)

        optionmenu_label = ctk.CTkLabel(location_frame, text="Select the City or Postal Code")
        optionmenu_label.grid(row=1, column=1, sticky="w", pady=(0, 3), padx=5)
        self.widgets.append(optionmenu_label)

        option_menu = ctk.CTkOptionMenu(location_frame, values=self.location_options,
                                        command=lambda event: self.on_location_option_change(event))
        option_menu.set("No results found")
        option_menu.grid(row=2, column=1, sticky="nsew", pady=(0, 3), padx=(10, 5))
        self.option_menu = option_menu
        self.widgets.append(self.option_menu)

        self.create_distance_slider(location_frame)

    def create_distance_slider(self, location_frame):
        start_value = 2
        self.distance = ctk.IntVar(value=start_value)

        self.text_distance = ctk.StringVar()
        self.text_distance.set(f"Current Distance: {start_value} km")
        self.distance.trace_add("write", lambda name, index, mode: self.text_distance.set(
            f"Current Distance: {str(self.distance.get())} km"))

        current_value_label = ctk.CTkLabel(location_frame, textvariable=self.text_distance)
        current_value_label.grid(row=5, column=0, sticky="w", pady=(3, 0), padx=5)
        self.widgets.append(current_value_label)

        distance_label = ctk.CTkLabel(location_frame, text="Distance (km)")
        distance_label.grid(row=3, column=0, sticky="w", pady=(15, 3), padx=5)
        self.widgets.append(distance_label)

        slider_frame = ctk.CTkFrame(location_frame)
        slider_frame.grid(row=4, column=0, sticky="nsew", padx=5)
        self.widgets.append(slider_frame)

        start_label = ctk.CTkLabel(slider_frame, text="1 km ")
        start_label.pack(side="left")
        self.widgets.append(start_label)

        distance_entry = ctk.CTkSlider(slider_frame, from_=1, to=50, variable=self.distance)
        distance_entry.bind("<ButtonRelease-1>", lambda event: self.on_distance_change())
        distance_entry.pack(side="left", ipady=3, expand=True, fill="x")
        distance_entry.configure(state="disabled")
        self.distance_entry = distance_entry
        self.widgets.append(distance_entry)

        end_label = ctk.CTkLabel(slider_frame, text="50 km")
        end_label.pack(side="left")
        self.widgets.append(end_label)

    def create_box_get_volunteers(self):
        total_volunteers_frame = ctk.CTkFrame(self.tab_view.tab(self.tab_names[0]))
        total_volunteers_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.widgets.append(total_volunteers_frame)

        total_volunteers_label = ctk.CTkLabel(total_volunteers_frame, text="Total Volunteers")
        total_volunteers_label.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)
        self.widgets.append(total_volunteers_label)

        self.total_volunteers = ctk.StringVar()
        self.total_volunteers.set("0")
        total_volunteers_label = ctk.CTkLabel(total_volunteers_frame, font=("Arial", 30),
                                              textvariable=self.total_volunteers)
        total_volunteers_label.place(relx=0.5, rely=0.5, anchor="center")
        self.widgets.append(total_volunteers_label)

    def create_message_frame(self):
        message_frame = ctk.CTkFrame(self.tab_view.tab(self.tab_names[0]))
        message_frame.grid(row=0, column=2, sticky="nsew", rowspan=2, padx=10, pady=10)
        message_frame.grid_columnconfigure(2, weight=4)
        self.widgets.append(message_frame)

        message_label = ctk.CTkLabel(message_frame, text="Message")
        message_label.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=(5, 0))
        self.widgets.append(message_label)

        message_entry = ctk.CTkTextbox(message_frame, width=380, height=450)
        message_entry.grid(row=1, column=0, sticky="nsew", ipady=3, padx=10)
        message_entry.bind("<KeyRelease>", lambda event: self.on_message_change())
        self.message = message_entry
        self.widgets.append(message_entry)

        phone_label = ctk.CTkLabel(message_frame, text="Phone Number")
        phone_label.grid(row=2, column=0, sticky="w", pady=(15, 3))
        self.widgets.append(phone_label)

        self.phone = ctk.StringVar()
        phone_entry = ctk.CTkEntry(message_frame, textvariable=self.phone)
        phone_entry.grid(row=3, column=0, sticky="nsew", ipady=3, padx=10)
        self.widgets.append(phone_entry)

        send_button = ctk.CTkButton(message_frame, text="Send", command=lambda: self.pre_send_message())
        send_button.grid(row=4, column=0, sticky="nsew", pady=(15, 0), padx=10)
        send_button.configure(state="disabled")
        self.send_button = send_button
        self.widgets.append(self.send_button)

    def show_loading_screen(self, tab_view_index: int, randon: bool = True):
        loading_frame = ctk.CTkFrame(self.tab_view.tab(self.tab_names[tab_view_index]))
        loading_frame.grid(row=0, column=0, columnspan=3, rowspan=2, sticky="nsew")
        loading_frame.grid_rowconfigure(0, weight=1)
        loading_frame.grid_columnconfigure(0, weight=1)
        self.loading_frame = loading_frame

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
        self.progress_bar = progress_bar

        percent_var = ctk.StringVar()
        percent_label = ctk.CTkLabel(inner_frame, textvariable=percent_var, )
        percent_label.grid(row=2, column=0, sticky="nsew", pady=(5, 0))
        self.percent_var = percent_var

        if randon:
            self.progress_bar.start()
            self.percent_var.set("Loading...")

    def clean_loading_frame(self):
        self.loading_frame.grid_forget()
        self.progress_bar = None
        self.percent_var = None

    def destroy(self):
        for widget in self.widgets:
            if widget.winfo_exists():
                widget.destroy()
        self.tab_view.grid_forget()
        self.service_manager.unsubscribe(self)

    def on_filter_change(self):
        self.service_manager.get_amount_of_volunteer(self.checkbox_vars, self.location_ids_types, self.location.get(),
                                                     self.distance.get())
        self.show_loading_screen(0)

    def on_location_change(self):
        if len(self.location.get()) >= 3:
            self.service_manager.get_location_data(self.location.get())

    def on_location_option_change(self, event):
        self.location.set(event)
        if self.location_ids_types[event][0] is not None and self.location_ids_types[event][1] is not None:
            self.distance_entry.configure(state="disabled")
        else:
            self.distance_entry.configure(state="normal")
        self.on_filter_change()

    def on_distance_change(self):
        if self.distance_entry.cget('state') != "disabled":
            self.on_filter_change()

    def notify(self, service_id, data):
        if service_id == 'notify_location_auto_complete':
            self.update_option_menu(data)
        elif service_id == 'notify_amount_of_volunteer':
            self.update_amount_of_volunteer(data)
        elif service_id == 'notify_starting_messaging':
            self.update_message_starting(data)
        elif service_id == 'notify_get_volunteers':
            self.send_message(data)
        elif service_id == 'notify_progresse_get_volunteers':
            self.update_progress_bar_to_get_volunteers(data)
        elif service_id == 'notify_message_sent':
            self.update_message_sent()
        elif service_id == 'notify_progress_message_sending':
            self.update_progress_bar_to_message_sending(data)

    def update_option_menu(self, data):
        if len(data) == 0:
            self.option_menu.configure(values=[])
            self.option_menu.set("No results found")
            self.location_ids_types = {}
        else:
            data.sort(key=lambda item: item['score'], reverse=True)
            self.location_options = data

            locales = {
                f"{item['name']} ({item['subtitle']})" if item['subtitle'] and item['subtitle'] != 'Postcode' else
                item[
                    'name']: item for item in data}
            self.option_menu.configure(values=list(locales.keys()))
            self.option_menu.set(list(locales.keys())[0])
            self.location_ids_types = {
                f"{item['name']} ({item['subtitle']})" if item['subtitle'] and item['subtitle'] != 'Postcode' else
                item[
                    'name']: (item['id'], item['type'], item['subtitle']) for item in data
            }

    def update_amount_of_volunteer(self, data):
        self.total_volunteers.set(data)
        self.clean_loading_frame()

    def update_message_starting(self, data):
        self.percent_var.set(f"Messaging will start in {int(data)} seconds.")
        pass

    def pre_send_message(self):
        self.show_loading_screen(0, False)
        self.service_manager.get_volunteers(self.checkbox_vars, self.location_ids_types, self.location.get(),
                                            self.distance.get())

    def send_message(self, data):
        self.clean_loading_frame()
        self.show_loading_screen(0, False)
        self.service_manager.send_messages(self.root_window.username, self.root_window.password,
                                           self.message.get("1.0", "end-1c"), self.phone.get(), data)

    def update_progress_bar_to_get_volunteers(self, current_page: int):
        total_volunteers = int(self.total_volunteers.get().replace('.', ''))
        num_pages = 1 if total_volunteers == 0 else math.ceil(total_volunteers / 23)
        progress = current_page / num_pages
        self.percent_var.set(f"Getting volunteers... {progress * 100:.1f}%")
        self.progress_bar.set(progress)

    def update_message_sent(self):
        self.clean_loading_frame()
        self.clear_message_fields()

    def update_progress_bar_to_message_sending(self, data):
        total_volunteers = int(self.total_volunteers.get().replace('.', ''))
        self.percent_var.set(f"Messages Sent: {data} out of {self.total_volunteers.get()}.")
        self.progress_bar.set(data / total_volunteers)

    def clear_message_fields(self):
        self.message.delete("1.0", "end-1c")
        self.phone.set("")

    def on_message_change(self):
        total_characters = len(self.message.get("1.0", "end-1c"))
        if total_characters > 3:
            self.send_button.configure(state="normal")
        else:
            self.send_button.configure(state="disabled")
