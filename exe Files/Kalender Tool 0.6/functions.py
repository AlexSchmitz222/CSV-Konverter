import sqlite3


def exportCSVFile(filepath: str, entry_count: int, entry_list: list, categories: list):
    if (filepath == ''):
        return
    with open(filepath, "w") as filewrite:
        filewrite.write(
            "EVENT NAME,EVENT DESCRIPTION,START DATE,START TIME,END DATE,END TIME,ALL DAY EVENT?,CATEGORIES\n")
    with open(filepath, "a") as filewrite:
        for entry in range(entry_count):
            for i in range(0, 8):
                if (i < 7):
                    filewrite.write('\"' + str(entry_list[entry][i]) + '\"')
                    if i < 7:
                        filewrite.write(",")
                elif (i == 7):
                    category_sel = list(entry_list[entry][i])
                    print(category_sel)
                    event_categories = []
                    for i in category_sel:
                        print(categories[i])
                        event_categories.append(categories[i])
                    filewrite.write('\"' + str(event_categories) + '\"')
                else:
                    return

            filewrite.write("\n")


def Update_Curr_Entry(cur_sel, entries):
    index = ([int(a) for a in cur_sel][0])
    str_eventname = entries[index][0]
    str_eventdescription = entries[index][1]
    str_startdate = entries[index][2]
    str_starttime = entries[index][3]
    str_enddate = entries[index][4]
    str_endtime = entries[index][5]
    bool_alldayevent = entries[index][6]
    str_categories = entries[index][7]
    return str_eventname, str_eventdescription, str_startdate, str_starttime, str_enddate, str_endtime, bool_alldayevent, str_categories


def save_event(event_name: str, event_description: str, start_date: str, start_time: str, end_date: str, end_time: str, alldayevent: bool, categories: tuple, entries: list, new_event: bool, cur_sel: tuple):
    # if (event_name!=0 and event_description!=0 and start_date!=0 and start_time!=0 and end_date!=0 and end_time!=0 and alldayevent=='false' and categories!=0 or event_name!=0 and event_description!=0 and start_date!=0 and end_date!=0 and  alldayevent=='true' and categories!=0):
    print(new_event)
    # print(event_name + " , " + event_description + " , " + start_date + " , " + start_time + " , " + end_date + " , " + end_time + " , " + str(alldayevent) + " , " + str(event_categories) + " , " + )
    event = []
    new_event_categories = []
    event.extend([event_name, (event_description[: -1]),
                  start_date, start_time, end_date, end_time, alldayevent, categories])

    if (new_event == 'true'):
        entries.append(event)
        not new_event
    else:
        if (len(cur_sel) != 0):
            index = ([int(a) for a in cur_sel][0])
            entries[index] = event
    return(entries)


def delete_curr_entry(cur_sel: tuple, entries: list):
    if (len(entries) > 0):
        index = ([int(a) for a in cur_sel][0])
        entries.pop(index)
        return entries


def delete_all(entries: list):
    entries.clear()
    return entries

def create_new_database(filepath):
    print(filepath)
    
def open_existing_database(filepath):
    print(filepath)

def save_existing_database(filepath,entries):
    print(filepath)