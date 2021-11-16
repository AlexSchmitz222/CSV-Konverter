import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import time

print("OOPS. YOu have executed functions.py . Surely you wanted to execute main.py, right?")
# os.system("main.py")


def exportCSVFile(filepath: str, entry_count: int, entry_list: list, categories: list, main_center_x: int, main_center_y: int):
    if (filepath == ''):
        return

    pgbr_length = 220
    root_width = pgbr_length + 10
    root = Tk()
    root.grab_set()
    root.title("Event Exporter")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    root.iconbitmap(str(dir_path) + "\export_icon.ico")
    root.resizable(False, False)

    x = main_center_x - (root.winfo_width()/2)
    y = main_center_y
    root.geometry('%dx%d+%d+%d' % (root_width, 50, x, y))
    root.overrideredirect(1)

    frm_progressbar = ttk.Frame(root, borderwidth=(
        root_width-pgbr_length)/2, width=1, height=1)
    frm_progressbar.grid(column=1, row=1, sticky="N")

    last_pgbr = 0
    pgbr = ttk.Progressbar(frm_progressbar, orient=HORIZONTAL,
                           length=pgbr_length, mode="determinate", maximum=pgbr_length)
    pgbr.pack()

    lbl = ttk.Label(frm_progressbar,
                    text="Currently exporting Event X of Y Events.")
    lbl.pack()
    root.update()

    with open(filepath, "w") as filewrite:
        filewrite.write(
            "EVENT NAME,EVENT DESCRIPTION,START DATE,START TIME,END DATE,END TIME,ALL DAY EVENT?,CATEGORIES\n")
    with open(filepath, "a") as filewrite:
        for entry in range(entry_count):
            lbl.config(text="Currently Exporting Event " +
                       str(entry+1) + " of " + str(entry_count) + " Events.")
            root.update()
            for i in range(0, 8):
                if (i < 7):
                    filewrite.write('\"' + str(entry_list[entry][i]) + '\"')
                    if i < 7:
                        filewrite.write(",")
                elif (i == 7):
                    category_sel = list(entry_list[entry][i])
                    event_categories = []
                    for i in category_sel:
                        event_categories.append(categories[i])
                    filewrite.write('\"' + str(event_categories) + '\"')
                else:
                    return "fail"
            pgbr["value"] = last_pgbr+pgbr_length/entry_count
            last_pgbr = pgbr["value"]
            root.update()
            filewrite.write("\n")
    root.destroy()
    messagebox.showinfo("Events erfolgreich Exportiert",
                        'Alle Events wurden erfolgreich nach "' + filepath + '" exportiert')


#def Update_Curr_Entry(current_selection, entries):
#    index = ([int(a) for a in current_selection][0])
#    str_eventname = entries[index][0]
#    str_eventdescription = entries[index][1]
#    str_startdate = entries[index][2]
#    str_starttime = entries[index][3]
#    str_enddate = entries[index][4]
#    str_endtime = entries[index][5]
#    bool_alldayevent = entries[index][6]
#    list_categories = entries[index][7]
#    return str_eventname, str_eventdescription, str_startdate, str_starttime, str_enddate, str_endtime, bool_alldayevent, list_categories

#TODO: Bug, es werden keine bearbeiteten Events gespeichert!
def save_event(event_name: str, event_description: str, start_date: str, start_time: str, end_date: str, end_time: str, alldayevent: bool, categories: list, entries: list, new_event: bool, current_selection: tuple):
    # if (event_name!=0 and event_description!=0 and start_date!=0 and start_time!=0 and end_date!=0 and end_time!=0 and alldayevent=='false' and categories!=0 or event_name!=0 and event_description!=0 and start_date!=0 and end_date!=0 and  alldayevent=='true' and categories!=0):
    event = []
    event.extend([event_name, (event_description[: -1]),
                  start_date, start_time, end_date, end_time, alldayevent, categories])

    if (new_event == True):
        entries.append(event)
        not new_event
    else:
        if (len(current_selection) != 0):
            index = ([int(a) for a in current_selection][0])
            entries[index] = event
    return(entries, new_event)


def delete_curr_entry(current_selection: tuple, entries: list):
    if (len(entries) > 0):
        index = ([int(a) for a in current_selection][0])
        entries.pop(index)
        return entries


def delete_all(entries: list):
    query = messagebox.askyesno(
        "Wirklich...?", "Wirklich alle Events löschen?", icon='warning')
    if (query == True):
        entries.clear()
        return entries


def create_new_database(filepath):
    db = sqlite3.connect(filepath)
    cur = db.cursor()
    cur.execute(
        ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='entries' ''')
    if (cur.fetchone()[0] != 1):
        cur.execute(
            ''' CREATE TABLE entries (id, event_name, event_description, start_date, start_time, end_date, end_time, alldayevent, categories) ''')
        db.commit()
    sql_filepath = filepath
    return db, cur, sql_filepath, "success"


def open_existing_database(filepath, entries):
    query = messagebox.askyesno(
        "Wirklich...?", "Durch das Laden einer Datenbank gehen aktuell nicht gespeicherte Events verloren!\n Fortfahren?", icon='warning')
    if (query == True):
        db = sqlite3.connect(filepath)
        cur = db.cursor()
        sql_filepath = filepath
        cur.execute('''SELECT * FROM entries''')
    table = cur.fetchall()

    for row in table:
        entries.append([row[1], row[2], row[3], row[4],
                       row[5], row[6], row[7], row[8]])

    for i in range(0, len(entries)):
        splitter = entries[i][7].split(", ")
        splitter[0] = splitter[0][1:]
        splitter[len(splitter)-1] = splitter[len(splitter)-1][: -1]
        entries[i][7] = splitter
    return db, cur, sql_filepath, entries,  "success"


def save_existing_database(entries, db, cur):
    cur.execute(''' DELETE FROM entries''')
    for entry in range(0, len(entries)):
        cur.execute(''' INSERT INTO entries (id, event_name, event_description, start_date, start_time, end_date, end_time, alldayevent, categories)
                        VALUES (?,?,?,?,?,?,?,?,?)''', (str(entry), entries[entry][0], entries[entry][1], entries[entry][2], entries[entry][3], entries[entry][4], entries[entry][5], entries[entry][6], str(entries[entry][7])))
    db.commit()
    return "success"


def close_existing_database(db, cur):
    query = messagebox.askyesno(
        "Wirklich...?", "Datenbank wirklich schließen? \n Nicht gespeicherte Events gehen verloren.", icon='warning')
    if (query == True):
        db.close()
    return "success"
