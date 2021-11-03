
def exportCSVFile(filepath: str, entry_count: int, entry_list: list):
    if (filepath==''):
        return
    filewrite=open(filepath,"w")
    filewrite.write("EVENT NAME,EVENT DESCRIPTION,START DATE,START TIME,END DATE,END TIME,ALL DAY EVENT?,CATEGORIES\n")
    filewrite.close()

    filewrite=open(filepath,"a")
    for entry in range(entry_count):
        for i in range(0,8):
            filewrite.write('\"' + entry_list[entry][i] + '\"')
            if i < 7:
                filewrite.write(",")
        filewrite.write("\n")
    filewrite.close()

 
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
    print(str_categories)
    return str_eventname, str_eventdescription, str_startdate, str_starttime, str_enddate, str_endtime, bool_alldayevent, str_categories


def save_new_event(event_name: str, event_description: str, start_date: str, start_time: str, end_date: str, end_time: str, alldayevent: bool, categories):
    if (event_name=='' or event_description=='' or start_date==''):
        return
    print(event_name + " , " + event_description + " , " + start_date + " , " + start_time + " , " + end_date + " , " + end_time + " , " + str(alldayevent) + " , " + categories)

