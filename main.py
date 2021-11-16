from tkinter import *
from tkinter import ttk
from functions import *
from tkinter import filedialog
from tkinter import messagebox
import os


# ---------CHANGE HERE TO UPDATE AVAILABLE EVENT CATEGORIES---------
categories = ["Allgemein", "Eltern", "Schüler", "Unterrichtsfrei", ]


# ----DON'T CHANGE ANYTHING BELOW EVER!!!----
entries = []  # [["Test0", "Das ist ein Text BLABLABLA", "10-02-2021", "10:12:00", "10-02-2021", "10:15:00", False, [False, False, True, True]],
# ["Test1", "Das ist ein Text <br>BLABwadwLABLA</br>", "10-04-2021", "12:15:00", "10-06-2021", "10:30:00", True, [True, True, False, False]]]
db = cur = current_selection = sql_filepath = chkbtn_categories_vars = ""
chkbtn_categories = []
chkbtn_categories_vars = []
bool_new_event = False  # if true, current event is new and hasn't been saved yet


# ----TKINTER EVENTS----
def event_listbox_select(event):
    global bool_new_event
    global current_selection
    bool_new_event = False
    current_selection = len(lstbx_event_list.curselection())
    if (current_selection != 0):
        entry_controls_selector()

        #a, b, c, d, e, f, g, h = (Update_Curr_Entry(lstbx_event_list.curselection(), entries))

        update_screen(entries, ([int(a)
                      for a in lstbx_event_list.curselection()][0]))

    else:
        entry_controls_selector()


def event_export_entries():
    exportCSVFile(filedialog.asksaveasfilename(title="Exportieren...", initialdir='~/Documents', defaultextension=".csv",
                  filetype=(("Comma Separated Value", "*.csv"), ("All Files", "*.*"))), len(entries), entries, categories, root.winfo_x()+(root.winfo_width()/2), root.winfo_y()+(root.winfo_height()/2))


def event_new_entry():  # clear all input fields
    global bool_new_event
    ent_event_name.delete(0, END)
    txtbx_event_description.delete(1.0, END)
    ent_start_date.delete(0, END)
    ent_start_time.delete(0, END)
    ent_end_date.delete(0, END)
    ent_end_time.delete(0, END)
    bool_alldayevent.set(0)
    bool_new_event = True
    entry_controls_selector()


def event_save_entry():
    global entries
    global bool_new_event
    chkbtn_categories_var = []

    for i in range(0, len(chkbtn_categories_vars)):
        chkbtn_categories_var.insert(i, chkbtn_categories_vars[i].get())

    entries, bool_new_event = save_event(ent_event_name.get(), txtbx_event_description.get("1.0", END), ent_start_date.get(), ent_start_time.get(
    ), ent_end_date.get(), ent_end_time.get(), bool_alldayevent.get(), chkbtn_categories_var, entries, bool_new_event, lstbx_event_list.curselection())
    lstbx_event_list.delete(0, END)
    for i in range(0, len(entries)):
        lstbx_event_list.insert(END, entries[i][0])
    entry_controls_selector()
    set_entry_count()


def event_delete_entry():
    global entries
    if (len(lstbx_event_list.curselection()) != 0 and len(entries) > 0):
        entries = delete_curr_entry(lstbx_event_list.curselection(), entries)
        lstbx_event_list.delete(0, END)
        for i in range(0, len(entries)):
            lstbx_event_list.insert(END, entries[i][0])
    set_entry_count()


def event_delete_all():
    global entries
    if len(entries) > 0:
        delete_all(entries)
        entries = delete_all(entries)
        lstbx_event_list.delete(0, END)
    set_entry_count()


def event_create_database():
    global db
    global cur
    global sql_filepath
    db, cur, sql_filepath, ret = create_new_database(filedialog.asksaveasfilename(
        title="Datenbank erstellen...", initialdir='~/Documents', defaultextension=".db", filetype=(("Datenbanken", "*.db"), ("All Files", "*.*"))))
    if (ret == "success"):
        set_title()
        btn_create_new_db.state(['disabled'])
        btn_load_from_db.state(['disabled'])
        btn_save_to_db.state(['!disabled'])
        btn_close_db.state(['!disabled'])
        messagebox.showinfo("Datenbank erfolgreich erstellt",
                            "Die Datenbank wurde erfolgreich in " + sql_filepath + " erstellt!")


def event_load_database():
    global db
    global cur
    global sql_filepath
    global entries
    db, cur, sql_filepath, entries, ret = open_existing_database(filedialog.askopenfilename(
        title="Datenbank öffnen...", initialdir='~/Documents', defaultextension=".db", filetype=(("Datenbanken", "*.db"), ("All Files", "*.*"))), entries)
    
    current_selection = lstbx_event_list.curselection()
    if (current_selection == ()):
        current_selection = 0
    else:
        current_selection = ([int(a) for a in current_selection][0])
    update_screen(entries, current_selection)
    if (ret == "success"):
        set_title()
        btn_create_new_db.state(['disabled'])
        btn_load_from_db.state(['disabled'])
        btn_save_to_db.state(['!disabled'])
        btn_close_db.state(['!disabled'])


def event_save_database():
    global db
    global cur
    global entries
    ret = save_existing_database(entries, db, cur)
    if (ret == "success"):
        messagebox.showinfo("Erfolgreich...",
                            "Alle Events wurden erfolgreich gespeichert!")


def event_close_database():
    global db
    global cur
    ret = close_existing_database(db, cur)
    if (ret == "success"):
        btn_create_new_db.state(['!disabled'])
        btn_load_from_db.state(['!disabled'])
        btn_save_to_db.state(['disabled'])
        btn_close_db.state(['disabled'])
        messagebox.showinfo("Erfolgreich...",
                            "Die Datenbank wurde erfolgreich geschlossen!")


def set_title():
    global sql_filepath
    if (sql_filepath == ""):
        root.title("JSG Kalender Tool")
    else:
        root.title("JSG Kalender Tool - " + sql_filepath)


def set_entry_count():
    global entries
    lbl_event_count.config(text=str(len(entries)) + " Events")


def entry_controls_selector():
    global current_selection
    global bool_new_event
    if (bool_new_event == True):
        btn_delete_entry.state(['disabled']) #disabled
        btn_delete_all.state(['disabled']) #disabled
    else:
        btn_delete_entry.state(['!disabled']) #active
        btn_delete_all.state(['!disabled']) #active

    if (current_selection != 0):
        btn_save_entry.state(['!disabled']) #active
        btn_delete_entry.state(['!disabled']) #active
    else:
        btn_save_entry.state(['disabled']) #disabled
        btn_delete_entry.state(['disabled']) #disabled


def update_screen(entries, current_selection):

    str_eventname = entries[current_selection][0]
    str_eventdescription = entries[current_selection][1]
    str_startdate = entries[current_selection][2]
    str_starttime = entries[current_selection][3]
    str_enddate = entries[current_selection][4]
    str_endtime = entries[current_selection][5]
    bool_alldayevent_ = entries[current_selection][6]
    list_categories = entries[current_selection][7]

    ent_event_name.delete(0, END)
    ent_event_name.insert(0, str_eventname)

    txtbx_event_description.delete(1.0, END)
    txtbx_event_description.insert(1.0, str_eventdescription)

    ent_start_date.delete(0, END)
    ent_start_date.insert(0, str_startdate)

    ent_start_time.delete(0, END)
    ent_start_time.insert(0, str_starttime)

    ent_end_date.delete(0, END)
    ent_end_date.insert(0, str_enddate)

    ent_end_time.delete(0, END)
    ent_end_time.insert(0, str_endtime)

    if (bool_alldayevent_ == True):
        bool_alldayevent.set(1)
    else:
        bool_alldayevent.set(0)

    for i in range(0, (len(list_categories)-1)):
        if (list_categories[i] == True):
            chkbtn_categories_vars[i].set(1)
        else:
            chkbtn_categories_vars[i].set(0)

    lstbx_event_list.delete(0, END)
    for i in range(0, len(entries)):
        lstbx_event_list.insert(END, entries[i][0])

# -MAIN PROGRAM------------------------------------------


root = Tk()
set_title()
dir_path = os.path.dirname(os.path.realpath(__file__))
root.iconbitmap(str(dir_path) + "\icon.ico")
root.resizable(False, False)

frm_curr_event = ttk.Frame(root, relief="groove",
                           borderwidth=5, width=600, height=100)
frm_curr_event.grid(column=1, row=1, sticky="N")

lbl_event_name = ttk.Label(frm_curr_event, text="Name")
lbl_event_name.grid(column=1, row=1, sticky="W")

ent_event_name = ttk.Entry(frm_curr_event, width=50)
ent_event_name.grid(column=1, columnspan=2, row=2, sticky="W")


lbl_event_description = ttk.Label(frm_curr_event, text="Beschreibung")
lbl_event_description.grid(column=1, row=3, sticky="W")

txtbx_event_description = Text(
    frm_curr_event, height=10, width=38, relief="raised")
txtbx_event_description.grid(column=1, columnspan=2, row=4, sticky="W")


lbl_start_date = ttk.Label(frm_curr_event, text="Start Datum (DD-MM-YYYY)")
lbl_start_date.grid(column=1, row=5, sticky="W")

ent_start_date = ttk.Entry(frm_curr_event)
ent_start_date.grid(column=1, row=6, sticky="W")


lbl_start_time = ttk.Label(frm_curr_event, text="Startzeit (HH:MM)")
lbl_start_time.grid(column=1, row=7, sticky="W")

ent_start_time = ttk.Entry(frm_curr_event)
ent_start_time.grid(column=1, row=8, sticky="W")


lbl_end_date = ttk.Label(frm_curr_event, text="End Datum (DD-MM-YYYY)")
lbl_end_date.grid(column=2, row=5, sticky="W")

ent_end_date = ttk.Entry(frm_curr_event)
ent_end_date.grid(column=2, row=6, sticky="W")


lbl_end_time = ttk.Label(frm_curr_event, text="Endzeit (HH:MM)")
lbl_end_time.grid(column=2, row=7, sticky="W")

ent_end_time = ttk.Entry(frm_curr_event)
ent_end_time.grid(column=2, row=8, sticky="W")

bool_alldayevent = BooleanVar()
chk_all_Day_event = ttk.Checkbutton(
    frm_curr_event, text="Ganztägiges Event?", variable=bool_alldayevent)
chk_all_Day_event.grid(column=1, row=9, sticky="W")

lbl_categories = ttk.Label(frm_curr_event, text="Kategorien")
lbl_categories.grid(column=1, row=10, sticky="W")

for i in range(0, len(categories)):
    chkbtn_categories.append(None)

    chkbtn_categories_vars.insert(i, BooleanVar())
    chkbtn_categories_vars[i].set(0)

    chkbtn_categories[i] = ttk.Checkbutton(
        frm_curr_event, text=categories[i], variable=chkbtn_categories_vars[i])
    if ((i % 2) == 0):
        if (i == 0):
            chkbtn_categories[i].grid(column=1, row=11, sticky="W")
        else:
            chkbtn_categories[i].grid(column=1, row=11+i, sticky="W")
    else:
        chkbtn_categories[i].grid(column=2, row=11+i-1, sticky="W")


frm_treelist = ttk.Frame(root, relief="groove",
                         borderwidth=5, width=200, height=100)
frm_treelist.grid(column=2, row=1, sticky="N")


entries_var = StringVar(value=[item[0] for item in entries])

lstbx_event_list = Listbox(frm_treelist, height=25,
                           width=31, listvariable=entries_var, relief="raised")
lstbx_event_list.pack()
lstbx_event_list.bind('<<ListboxSelect>>', event_listbox_select)


frm_entry_controls = ttk.Frame(relief="groove", borderwidth=5, width=200)
frm_entry_controls.grid(column=3, row=1, sticky="N")

btn_create_entry = ttk.Button(
    frm_entry_controls, text="Neues Event", width=20, command=event_new_entry)
btn_create_entry.pack()
# btn_create_entry.state(['disabled'])

btn_delete_entry = ttk.Button(
    frm_entry_controls, text="Event löschen", width=20, command=event_delete_entry)
btn_delete_entry.pack()
btn_delete_entry.state(['disabled'])

btn_save_entry = ttk.Button(
    frm_entry_controls, text="Event speichern", width=20, command=event_save_entry)
btn_save_entry.pack()
btn_save_entry.state(['disabled'])

btn_delete_all = ttk.Button(
    frm_entry_controls, text="Alle Events löschen", width=20, command=event_delete_all)
btn_delete_all.pack()

lbl_event_count = ttk.Label(
    frm_entry_controls, text=str(len(entries)) + " Events")
lbl_event_count.pack()


frm_controls = ttk.Frame(relief="groove", borderwidth=5, width=200)
frm_controls.grid(column=3, row=1, sticky="S")

btn_create_new_db = ttk.Button(
    frm_controls, text="Datenbank erstellen", width=20, command=event_create_database)
btn_create_new_db.pack()
# btn_create_new_db.state(['disabled'])

btn_load_from_db = ttk.Button(
    frm_controls, text="Datenbank laden", width=20, command=event_load_database)
btn_load_from_db.pack()
# btn_load_from_db.state(['disabled'])

btn_save_to_db = ttk.Button(
    frm_controls, text="Datenbank speichern", width=20, command=event_save_database)
btn_save_to_db.pack()
btn_save_to_db.state(['disabled'])

btn_close_db = ttk.Button(
    frm_controls, text="Datenbank schließen", width=20, command=event_close_database)
btn_close_db.pack()
btn_close_db.state(['disabled'])

# , command=event_import_entries)
btn_import = ttk.Button(frm_controls, text="Importieren", width=20)
btn_import.pack()
btn_import.state(['disabled'])

btn_export = ttk.Button(frm_controls, text="Exportieren",
                        width=20, command=event_export_entries)
btn_export.pack()
# btn_export.state(['disabled'])


root.mainloop()
