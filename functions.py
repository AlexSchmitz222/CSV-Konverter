
def exportCSVFile(filepath: str, entry_count: int, entry_list: list):
    if (filepath == ''):
        return
    with open(filepath, "w") as filewrite:
        filewrite.write(
            "EVENT NAME,EVENT DESCRIPTION,START DATE,START TIME,END DATE,END TIME,ALL DAY EVENT?,CATEGORIES\n")
    with open(filepath, "w") as filewrite:
        for entry in range(entry_count):
            for i in range(0, 8):
                filewrite.write('\"' + str(entry_list[entry][i]) + '\"')
                if i < 7:
                    filewrite.write(",")
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


def save_new_event(event_name: str, event_description: str, start_date: str, start_time: str, end_date: str, end_time: str, alldayevent: bool, event_categories: tuple, entries: list, categories: list):
    # if (event_name!=0 and event_description!=0 and start_date!=0 and start_time!=0 and end_date!=0 and end_time!=0 and alldayevent=='false' and categories!=0 or event_name!=0 and event_description!=0 and start_date!=0 and end_date!=0 and  alldayevent=='true' and categories!=0):
    #print(event_name + " , " + event_description + " , " + start_date + " , " + start_time + " , " + end_date + " , " + end_time + " , " + str(alldayevent) + " , " + str(event_categories))
    new_event = []
    new_event_categories = []
    new_event.extend([event_name, (event_description[: -1]),
                     start_date, start_time, end_date, end_time, alldayevent])
    for i in event_categories:
        new_event_categories.append(categories[i])
    new_event.append(new_event_categories)
    print(new_event)
    entries.append(new_event)
    return(entries)


def delete_curr_entry(cur_sel: tuple, entries: list):
    if (len(entries) > 0):
        index = ([int(a) for a in cur_sel][0])
        entries.pop(index)
        return entries


def delete_all(entries: list):
    entries.clear()
    return entries
