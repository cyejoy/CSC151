from tkinter import *
import re
from tkinter import messagebox
import tkinter.font as font
import os
import sqlite3
#Imports a class from the py file taken from the internet
#Class is for implementy a autocomplete entry for guided inputs
from autofill import AutocompleteEntry

#Defines the dimensions and position of the main window
root = Tk()
root.config(bg="black")
root.title("Hogwarts Students Information System")
root.resizable(0,0)
root.geometry("1000x800")
positionRight = int(root.winfo_screenwidth()/2)
positionDown = int(root.winfo_screenheight()/2)
root.geometry("+{}+{}".format(positionRight-500, positionDown-400))

#Creates the connection to the database
dbase = sqlite3.connect('SIS_data.db')
cursor = dbase.cursor()
dbase.execute("PRAGMA foreign_keys = ON;"); 
#Creates the tables for the data
cursor.execute("""CREATE TABLE IF NOT EXISTS course_list(
        course_number integer PRIMARY KEY,
        course_code text varchar(10),
        course_name text
        )""")
cursor.execute("""CREATE TABLE IF NOT EXISTS student_list(
        id_number integer UNIQUE,
        student_name text,
        course_number integer,
        year_level text,
        student_gender text,
        FOREIGN KEY (course_number)
            REFERENCES course_list(course_number)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        )""")
dbase.commit()

#Declares images to be used
pic = PhotoImage(file="image.png")
hogwarts_logo = PhotoImage (file="logo.png")
button_update = PhotoImage(file="button_update.png")
button_delete = PhotoImage(file="button_delete.png")
button_addstudent = PhotoImage(file="button_addstudent.png")
button_cancel = PhotoImage(file="button_cancel.png")
button_add = PhotoImage(file="button_add.png")
button_save = PhotoImage(file="button_save.png")
button_courses = PhotoImage(file="button_courses.png")
button_students = PhotoImage(file="button_students.png")
button_addcourse = PhotoImage(file="button_add-course.png")
button_addstudent = PhotoImage(file="button_add-student.png")
button_viewstudents = PhotoImage(file="button_view-students.png")
button_update1 = PhotoImage(file="button_update1.png")
button_delete1 = PhotoImage(file="button_delete1.png")

#Function for creating and updating the list of courses and students
def update_list():
    global studentList
    cursor.execute("SELECT * FROM student_list")
    studentList = cursor.fetchall()
    global courseList
    cursor.execute("SELECT * FROM course_list")
    courseList = cursor.fetchall()

#Function for determining which list to show on the display
def diverge(command,strain):
    update_list()
    if command == 0:
        global thisEntry
        thisEntry = StringVar()
        myEntry = Entry(searchFrame, textvariable=thisEntry, width = 90)
        myEntry.grid(row=0, column=1,ipady=3)
        #Traces the changes made in the search bar
        thisEntry.trace('w',show_course)
        show_course()
    else:
        global thatEntry
        thatEntry = StringVar()
        global strainer
        strainer = strain
        theirEntry = Entry(searchFrame, textvariable=thatEntry, width = 90)
        theirEntry.grid(row=0, column=1,ipady=3)
        #Traces the changes made in the search bar
        thatEntry.trace('w',show_student)
        show_student()
        
#Function for deleting a course        
def delete_course(course):
    reponse = messagebox.askyesno("Hogwarts Student Information System","Delete this course?")
    if reponse == 0:
        return
    cursor.execute("DELETE from course_list WHERE course_number=?",(course[0],))
    dbase.commit()
    show_course()

#Function for creating the interface of the course details window    
def course_window(comm,course):
    #Function for adding or updating the info of a course
    def command():
        #Checks if an existing record already exist
        if comm == "add":
            for thiscourse in courseList:
                if thiscourse[1] == code.get('1.0',"end-1c") or thiscourse[2] == cname.get('1.0',"end-1c"):
                    messagebox.showinfo("Hogwarts Student Information System","Record already exists.",parent=cWindow)
                    return
        #Guarantees that the input fields are not empty
        if code.get("1.0",END)=="\n" or cname.get("1.0",END)=="\n":
            messagebox.showinfo("Hogwarts Student Information System","Fill in all the fields.",parent=cWindow)
        else:
            if comm == "edit":
                cursor.execute("UPDATE course_list SET course_name=? WHERE course_number=?",
                               (cname.get('1.0',"end-1c"),course[0]))
            else:
                cursor.execute("INSERT INTO course_list(course_code,course_name)VALUES(?,?)",
                                   (code.get('1.0',"end-1c"),cname.get('1.0',"end-1c")))
            dbase.commit()
            cWindow.destroy()
            show_course()
        
    cWindow = Toplevel()
    cWindow.geometry("500x170")
    cWindow.resizable(0,0)
    cWindow.geometry("+{}+{}".format(positionRight-250, positionDown-85))
    
    this = LabelFrame(cWindow,text="Add Course Details",font='Helvitica 12 bold')
    this.pack(padx=5,pady=5,fill='both',expand='yes')

    Label(this,text="Course Code\t:").grid(row=0,column=0,padx=5,pady=(10,5))
    Label(this,text="Course Name\t:").grid(row=1,column=0,padx=5,pady=5)
    code = Text(this, width=44,height=1)
    code.grid(row=0,column=1,padx=5,pady=(10,5))
    cname = Text(this, width=44, height=2)
    cname.grid(row=1,column=1,padx=5,pady=5)

    if comm == "edit":
        code.insert(END,course[1])
        code.config(state=DISABLED)
        cname.insert(END, course[2])
        
    buttonFrame = Frame(this)
    buttonFrame.grid(row=2,column=0,columnspan=2)
    commandButton = Button(buttonFrame,text="ADD COURSE" if comm=="add" else "EDIT COURSE",height=2,width=30,command=command)
    commandButton.pack(side=LEFT,padx=5,pady=5)
    cancelButton = Button(buttonFrame,text="CANCEL",height=2,width=30)
    cancelButton.pack(side=RIGHT,padx=5,pady=5)

#Function for displaying the list of course in the database
def show_course(*args):
    update_list()
    mycanvas.yview_moveto(0)
    for frame in listFrame.winfo_children():
        frame.destroy()
    searchword = thisEntry.get()
    
    this.config(text="AVAILABLE COURSES")
    addButton.config(text="Add Course", command=lambda:course_window("add",[]))
    addButton.config(image=button_addcourse)
    
    row,column=0,0
    #Loops through the list of courses
    for course in courseList:
        #Only displays course with names containing the search string
        if searchword.lower() in course[2].lower():
            if column==3:
                row += 1
                column = 0
            currFrame=Frame(listFrame, highlightbackground="maroon", highlightthickness=3,bg="chocolate",height=250, width=306)
            currFrame.grid(row=row,column=column,padx=(15,0),pady=(15,0))
            currFrame.grid_propagate(0)
            Label(currFrame,text=course[1],bg="black",font='Helvitica 30 bold',fg="white").grid(row=0,column=0,columnspan=2,padx=(20,0),pady=(30,0),sticky=W+E)
            Label(currFrame,text=course[2],bg="black",font='Helvitica 12 italic',fg="white").grid(row=1,column=0,columnspan=2,padx=(20,0),pady=(5,30),sticky=W+E)
            viewButton = Button(currFrame,image=button_viewstudents, borderwidth=0,bg='maroon',command=lambda x=course[0]:diverge(1,x))
            viewButton.image=button_viewstudents
            viewButton.grid(row=2,column=0,columnspan=2,padx=(20,0),pady=1)
            editButton = Button(currFrame,image=button_update1, borderwidth=0,bg='maroon',command=lambda x=course:course_window("edit",x))
            editButton.image=button_update1
            editButton.grid(row=3,column=0,padx=(20,0),pady=1)
            deleteButton = Button(currFrame,image=button_delete1, borderwidth=0,bg='maroon',command=lambda x=course:delete_course(x))
            deleteButton.image=button_delete1
            deleteButton.grid(row=3,column=1,padx=(3,0),pady=1)
            column += 1
    fixFrame = Frame(listFrame, height=2000, width=470, bg="black")
    fixFrame.grid(row=row+1,column=0,columnspan=3)
    fixFrame.grid_propagate(0)

#Function for deleting a student   
def delete_student(number):
    reponse = messagebox.askyesno("Hogwarts Student Information System","Delete this student?")
    if reponse == 0:
        return
    cursor.execute("DELETE from student_list WHERE id_number=?",(number,))
    dbase.commit()
    show_student()

#Function for creating the interface of the student details window    
def student_window(comm,student,strainer):
    #Function for both adding and editing a student
    def command():
        #Guarantees that the input fields are not empty
        if ID.get()=="" or name.get()=="" or thiscourse.get()=="" or year.get()=="" or gender.get()=="":
            messagebox.showinfo("Hogwarts Student Information System","Fill in all the fields.",parent=sWindow)
        else:
            #Checks ID format
            if len(ID.get().split("-")) != 2:
                messagebox.showinfo("Hogwarts Student Information System","Invalid ID format(yyyy-nnnn).",parent=sWindow)
                return
            if len(ID.get().split("-")[0])!=4 or len(ID.get().split("-")[1])!=4:
                messagebox.showinfo("Hogwarts Student Information System","Invalid ID format(yyyy-nnnn).",parent=sWindow)
                return
            if ID.get().split("-")[0].isdigit()==False or ID.get().split("-")[1].isdigit()==False:
                messagebox.showinfo("Hogwarts Student Information System","Invalid ID format(yyyy-nnnn).",parent=sWindow)
                return
            if thiscourse.get() not in nameList:
                messagebox.showinfo("Hogwarts Student Information System","Course not found.",parent=sWindow)
                return
            #Checks if an existing record already exist
            for student in studentList:
                if student[0] == ID.get() or student[1] == name.get():
                    if comm == "edit" and student[0] == ID.get():
                        continue
                    messagebox.showinfo("Hogwarts Student Information System","Record already exists.",parent=sWindow)
                    return

            for course in courseList:
                if thiscourse.get()==course[2]:
                    courseNumber=course[0]
                    break
                
            if comm == "edit":
                cursor.execute("UPDATE student_list SET student_name=?,course_number=?,year_level=?,student_gender=? WHERE id_number=?",
                               (name.get(),courseNumber,year.get(),gender.get(),ID.get()))
            else:
                cursor.execute("INSERT INTO student_list(id_number,student_name,course_number,year_level,student_gender)VALUES(?,?,?,?,?)",
                               (ID.get(),name.get(),courseNumber,year.get(),gender.get()))
            dbase.commit()
            sWindow.destroy()
            show_student()
   
    #Creates a new window
    sWindow = Toplevel()
    sWindow.configure(bg="black")
    sWindow.title("Add Student" if command == "add" else "Edit Student")
    sWindow.resizable(0,0)
    sWindow.geometry("500x270")
    sWindow.geometry("+{}+{}".format(positionRight-250, positionDown-135))

    #Widgets for displaying the entry fields
    thisFrame = LabelFrame(sWindow,bg="maroon")
    thisFrame.pack(fill="both", expand=True, padx=10, pady=10)

    headFrame = Label(thisFrame, text="Add Student", font=30,fg="white",bg="black")
    headFrame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=W+E)

    Label(thisFrame, text="ID #\t:", anchor=W,fg="white",bg="maroon").grid(row=1,column=0, padx=5, pady=5)
    Label(thisFrame, text="Name\t:", anchor=W,fg="white",bg="maroon").grid(row=2,column=0, padx=5,pady=5)
    Label(thisFrame, text="Course\t:", anchor=W,fg="white", bg="maroon").grid(row=3,column=0, padx=5, pady=5)
    ID = Entry(thisFrame, width=66)
    ID.grid(row=1, column=1, pady=5)
    name = Entry(thisFrame, width=66)
    name.grid(row=2, column=1, pady=7)

    thiscourse = Entry(thisFrame,width=66)
    thiscourse.grid(row=3, column=1, pady=5)
       
    def matches(fieldValue, acListEntry):
        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
        return re.match(pattern, acListEntry)
    nameList = []
    for course in courseList:
        nameList.append(course[2])
    #Uses the referenced py file for making an autocomplete entry
    thiscourse = AutocompleteEntry(nameList,thisFrame,width=66,matchesFunction=matches)
    thiscourse.grid(row=3, column=1, pady=5)

    if comm=="add" and strainer!="":
        for course in courseList:
            if course[0]==strainer:
                thiscourse.insert(0,course[2])

    thisframe = Frame(thisFrame,bg="maroon")
    thisframe.grid(row=4, column=0, columnspan=2,pady=5, sticky=W)
    Label(thisframe, text="Year\t:",fg="white", bg="maroon").grid(row=0,column=0, padx=5, pady=5)
    Label(thisframe, text="Gender\t:", anchor=E,fg="white", bg="maroon").grid(row=0,column=2, padx=5, pady=5)
    year = StringVar()
    year.set("1st year")
    drop = OptionMenu(thisframe, year, "1st year","2nd year","3rd year","4th year")
    drop.grid(row=0, column=1, padx=5,pady=5)
    drop.config(width=18)
    gender = StringVar()
    gender.set("Male")
    Radiobutton(thisframe, text="Male",variable=gender, value="Male",fg="white", bg="maroon").grid(row=0, column=4, padx=10,pady=5)
    Radiobutton(thisframe, text="Female",variable=gender, value="Female",fg="white", bg="maroon").grid(row=0, column=5, padx=10,pady=5)
    
    #Sets the entry fields with the current student info
    if (comm == "edit"):
        ID.insert(0,student[0])
        ID.config(state=DISABLED)
        name.insert(0,student[1])
        for course in courseList:
            if course[0]==student[2]:
                thiscourse.insert(0,course[2])
        year.set(student[3])
        gender.set(student[4])
    thiscourse.deleteListbox()
    tempFrame = Frame(thisFrame,bg="maroon")
    tempFrame.grid(row=5, column=0, columnspan=2)
    cancel = Button(tempFrame, image=button_cancel, borderwidth=0,bg='maroon', command=sWindow.destroy)
    cancel.image=button_cancel
    cancel.grid(row=0,column=0, padx=5, pady=5)
    add = Button(tempFrame, image=button_add if command=="add" else button_save, borderwidth=0,bg='maroon', command=command)
    add.image=button_add if command=="add" else button_save
    add.grid(row=0,column=1, padx=5, pady=5)

#Function for displaying the list of students
def show_student(*args):
    update_list()
    mycanvas.yview_moveto(0)
    for frame in listFrame.winfo_children():
        frame.destroy()
    searchword = thatEntry.get()
    for course in courseList:
        if course[0]==strainer:
            courseTitle=course[2]
    this.config(text="STUDENT LIST | ALL COURSES" if strainer=="" else "STUDENT LIST | " + courseTitle)
    addButton.config(text="Add Student", command=lambda:student_window("add",[],strainer))
    addButton.config(image=button_addstudent)

    #Filters the student list according to course
    if strainer != "":
        filtered = [x for x in studentList if x[2]==strainer]
    else:
        filtered = studentList
    row,column=0,0
    for student in filtered:
        if (student[0].startswith(searchword) or (student[1].lower()).startswith(searchword.lower())):
            #Widgets for displaying list of students
            if column==2:
                row+=1
                column=0
            currFrame = Frame(listFrame, bg="maroon", highlightbackground="#484444", highlightthickness=3, height=100, width=470)
            currFrame.grid(row=row, column=column, padx=5, pady=(7,0))
            currFrame.propagate(0)

            picFrame = Label(currFrame, image=pic, height=90, width=90, bg="white")
            picFrame.pack(side=LEFT, padx=(7,0), pady=7)
            picFrame.image=pic
                
            textFrame = Frame(currFrame, height=90, width=360, bg="white")
            textFrame.pack(side=LEFT, padx=7, pady=7)
            textFrame.propagate(0)

            for course in courseList:
                if course[0]==student[2]:
                    studcourse = course[2]
                    break
                
            info = Label(textFrame, text=" ID#\t: "+student[0]+
                            "\nNAME\t: "+student[1]+
                            "\nCOURSE\t: "+studcourse+
                            "\nYEAR\t: "+student[3]+
                            "\nGENDER\t: "+student[4],justify=LEFT, bg="white",anchor="w")
            info.pack(side=LEFT)
            
            thisFrame = Frame(textFrame,bg="white")
            thisFrame.pack(side=RIGHT)
            #Creates an instance of the line['id#'] variable so that each button will have different values
            delete = Button(thisFrame, image=button_delete, borderwidth=0,bg='white', command=lambda x=student[0]:delete_student(x))
            #Keeps a reference of the image to avoid garbage collection
            delete.image=button_delete
            delete.pack(side=BOTTOM, padx=5,pady=2)
            edit = Button(thisFrame, image=button_update, borderwidth=0,bg='white', command=lambda x=student:student_window("edit",x,""))
            edit.image=button_update
            edit.pack(side=TOP, padx=5,pady=2)
            column += 1
    fixFrame = Frame(listFrame, height=1000, width=470, bg="maroon")
    fixFrame.grid(row=row+1,column=0,columnspan=2)
    fixFrame.propagate(0)
        
header = Frame(root, height=100, width=1000, bg="#971010")
header.propagate(0)
header.grid(row=0, column=0,columnspan=2)
Label(header, text="STUDENT INFORMATION SYSTEM", font = 'Helvitica 32 bold', bg="#971010", fg="white").place(relx=.47, rely=.40, anchor='c')
Label(header, text="Hogwarts University", font = 'Helvitica 18 bold', bg="#971010", fg="white").place(relx=.47, rely=.7, anchor='c')

logoFrame = Label(header, image=hogwarts_logo, height=90, width=90, bg="white")
logoFrame.pack(side=LEFT, padx=(7,0), pady=7)
logoFrame.image=hogwarts_logo

midFrame = LabelFrame(root,bg="black",highlightcolor="#484444")
midFrame.grid(row=1,column=0,columnspan=2)
this = Label(midFrame, text="AVAILABLE COURSES", font = 'Helvitica 25 bold', fg="white", anchor=CENTER,bg="#484444")
this.grid(row=0,column=0,sticky=W+E)
searchFrame = Frame(midFrame,bg="#484444")
searchFrame.grid(row=1,column=0,pady=10)
Label(searchFrame, text="SEARCH:", anchor=W, font = 'Arial 10', fg="white",bg="#484444").grid(row=0, column=0)
addButton = Button(searchFrame,image=button_addcourse, borderwidth=0,bg='#484444',command=lambda:course_window("add",[]))
addButton.image=button_addcourse
addButton.grid(row=0,column=2,padx=6)

wrapper = LabelFrame(root,bg="black")
wrapper.grid(row=2, column=0,columnspan=2)
mycanvas = Canvas(wrapper, width=975,height=540,bg="black")
listFrame= Frame(mycanvas,bg="black")
yscrollbar = Scrollbar(wrapper, orient="vertical", command=mycanvas.yview)
yscrollbar.pack(side=RIGHT, fill="y")
mycanvas.pack(side=LEFT)
mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
mycanvas.create_window((0,0), window=listFrame, anchor="nw")

courseButton = Button(root,image=button_courses, borderwidth=0,bg='black',command=lambda:diverge(0,""))
courseButton.image=button_courses
courseButton.grid(row=3,column=0,pady=6,padx=(5,0))
studentButton = Button(root,image=button_students, borderwidth=0,bg='black',command=lambda:diverge(1,""))
studentButton.image=button_students
studentButton.grid(row=3,column=1,padx=(0,5))

diverge(0,"")

root.mainloop()