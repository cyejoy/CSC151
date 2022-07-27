from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import csv
import os

#Defines the dimensions and position of the main window
root = Tk()
root.config(bg="maroon")
root.title("Hogwarts Students Information System")
root.resizable(0,0)
root.geometry("500x625")
positionRight = int((root.winfo_screenwidth()/2 - 250))
positionDown = int((root.winfo_screenheight()/2 - 315))
root.geometry("+{}+{}".format(positionRight, positionDown))

#Creates a new 'data.csv' if that file is not present
if not os.path.exists('data.csv'):
        with open('data.csv','w') as csv_file:
                fieldnames=["id number","name","course","year level","gender"]
                write = csv.DictWriter(csv_file,fieldnames=fieldnames)
                write.writeheader()
                
#Declares a global image to be used as buttons and as a display picture
global image
pic = PhotoImage(file="image.png")
global logo 
hogwarts_logo = PhotoImage (file="logo.png")
global button_update
button_update = PhotoImage(file="button_update.png")
global button_delete
button_delete = PhotoImage(file="button_delete.png")
global button_addstudent
button_addstudent = PhotoImage(file="button_addstudent.png")
global button_cancel
button_cancel = PhotoImage(file="button_cancel.png")
global add
button_add = PhotoImage(file="button_add.png")
global save
button_save = PhotoImage(file="button_save.png")

#Function for deleting a student. Accepts a parameter pertaining to the id# of the student to be deleted
#Reads the csv file, finds the student with the id# and rewrites the file without the student 
def deleteStudent(number):
        with open('data.csv','r') as csv_file:
                read = csv.DictReader(csv_file)
                listStudents=[]
                for line in read:
                        if line['id#'] != number:
                                listStudents.append(line)
        with open('data.csv','w',newline='') as csv_file:
                fieldnames=["id#","name","course","year","gender"]
                write = csv.DictWriter(csv_file,fieldnames=fieldnames)
                write.writeheader()
                for i in listStudents:
                        write.writerow(i)
        showList()

#Function for displaying the list of students. Trace method, by default, sends in 3 parameters but none of those will be used
def showList(*args):
        #Destroys the current widgets in the frame
        for frame in myFrame.winfo_children():
                frame.destroy()
        #Stores the changes made in the search bar
        searchword = entryvar.get()
        
        with open('data.csv','r') as csv_file:
                read = csv.DictReader(csv_file)
                i=0
                for line in read:
                        #If seachbar is used, filters the list according to the string in the searchbar
                        if(line['id#'].startswith(searchword) or (line['name'].lower()).startswith(searchword.lower())):
                                #Widgets for displaying list of students
                                currFrame = Frame(myFrame, bg="black", highlightbackground="#B8860B", highlightthickness=3, height=100, width=470)
                                currFrame.grid(row=i, column=0, padx=5, pady=5)
                                currFrame.propagate(0)

                                picFrame = Label(currFrame, image=pic, height=90, width=90, bg="tan")
                                picFrame.pack(side=LEFT, padx=(7,0), pady=7)
                                picFrame.image=pic
                                    
                                textFrame = Frame(currFrame, height=90, width=360, bg="tan")
                                textFrame.pack(side=LEFT, padx=7, pady=7)
                                textFrame.propagate(0)
                                    
                                info = Label(textFrame, text=" ID no.\t: "+line['id#']+
                                                "\nName\t: "+line['name']+
                                                "\nCourse\t: "+line['course']+
                                                "\nYear\t: "+line['year']+
                                                "\nGender\t: "+line['gender'],justify=LEFT, bg="tan",anchor="w")
                                info.pack(side=LEFT)
                                
                                thisFrame = Frame(textFrame,bg="tan")
                                thisFrame.pack(side=RIGHT)
                                #Creates an instance of the line['id#'] variable so that each button will have different values
                                delete = Button(thisFrame, image=button_delete, borderwidth=0,bg='tan', command=lambda x=line['id#']:deleteStudent(x))
                                #Keeps a reference of the image to avoid garbage collection
                                delete.image=button_delete
                                delete.pack(side=BOTTOM, padx=5,pady=2)
                                edit = Button(thisFrame, image=button_update, borderwidth=0,bg='tan', command=lambda x=line:info_window("edit",x))
                                edit.image=button_update
                                edit.pack(side=TOP, padx=5,pady=2)
                        i+=1
        #Frame used to fix scrollbar not activating
        fixFrame = Frame(myFrame, height=1000, width=470)
        fixFrame.grid(row=i,column=0)
        fixFrame.propagate(0)

#Function for displaying the add and edit window
def info_window(command,student):
        #Function for both adding and editing a student
        #For editing student, saves the current changes to the info, delete the current info and rewrites the file with the new info
        def addStudent():
                #Guarantees that the input fields are not empty
                if ID.get()=="" or name.get()=="" or course.get()=="" or year.get()=="" or gender.get()=="":
                        messagebox.showinfo("Student Information System","Fill in all the fields.",parent=infoWindow)
                else:
                        #Checks ID format
                        if len(ID.get().split("-")) != 2:
                                messagebox.showinfo("Student Information System","Invalid ID format(yyyy-nnnn).",parent=infoWindow)
                                return
                        if len(ID.get().split("-")[0])!=4 or len(ID.get().split("-")[1])!=4:
                                messagebox.showinfo("Student Information System","Invalid ID format(yyyy-nnnn).",parent=infoWindow)
                                return
                        if ID.get().split("-")[0].isdigit()==False or ID.get().split("-")[1].isdigit()==False:
                                messagebox.showinfo("Student Information System","Invalid ID format(yyyy-nnnn).",parent=infoWindow)
                                return
                        #Checks if an existing record already exist
                        with open('data.csv','r') as csv_file:
                                read = csv.DictReader(csv_file)
                                listStudents=[]
                                for line in read:
                                        if line['id#'] == ID.get() or line['name'] == name.get():
                                                if command == "edit" and line['id#'] == ID.get():
                                                        continue
                                                messagebox.showinfo("Student Information System","Record already exists.",parent=infoWindow)
                                                return
                                        
                        student = [ID.get(),name.get(),course.get(),year.get(),gender.get()]
                        if command == "edit":
                                deleteStudent(student[0])
                        with open('data.csv','a',newline='') as csv_file:
                                write = csv.writer(csv_file)
                                write.writerow(student)
                        infoWindow.destroy()
                        showList()
                
        #Creates a new window
        infoWindow = Toplevel()
        infoWindow.configure(bg="#B8860B")
        infoWindow.title("Add Student" if command == "add" else "Edit Student")
        infoWindow.resizable(0,0)
        infoWindow.geometry("500x270")
        infoWindow.geometry("+{}+{}".format(positionRight, positionDown))

        #Widgets for displaying the entry fields
        thisFrame = LabelFrame(infoWindow,bg="black")
        thisFrame.pack(fill="both", expand=True, padx=10, pady=10) 

        headFrame = Label(thisFrame, text="Add Student", font=30,bg="maroon", fg="white" )
        headFrame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=W+E)

        Label(thisFrame, text="ID #\t:", anchor=W,fg="white", bg="black").grid(row=1,column=0, padx=5, pady=5)
        Label(thisFrame, text="Name\t:", anchor=W,fg="white", bg="black").grid(row=2,column=0, padx=5,pady=5)
        Label(thisFrame, text="Course\t:", anchor=W,fg="white", bg="black").grid(row=3,column=0, padx=5, pady=5)
        ID = Entry(thisFrame, width=66)
        ID.grid(row=1, column=1, pady=5) 
        name = Entry(thisFrame, width=66)
        name.grid(row=2, column=1, pady=7)
        course = Entry(thisFrame, width=66)
        course.grid(row=3, column=1, pady=5)

        thisframe = Frame(thisFrame,bg="black")
        thisframe.grid(row=4, column=0, columnspan=2,pady=5, sticky=W)
        Label(thisframe, text="Year\t:",fg="white", bg="black").grid(row=0,column=0, padx=5, pady=5)
        Label(thisframe, text="Gender\t:", anchor=E,fg="white", bg="black").grid(row=0,column=2, padx=5, pady=5)
        year = StringVar()
        year.set("1st year")
        drop = OptionMenu(thisframe, year, "1st","2nd","3rd","4th")
        drop.grid(row=0, column=1, padx=5,pady=5)
        drop.config(width=18)
        gender = StringVar()
        gender.set("Male")
        Radiobutton(thisframe, text="Male",variable=gender, value="Male",fg="white", bg="black").grid(row=0, column=4, padx=10,pady=5)
        Radiobutton(thisframe, text="Female",variable=gender, value="Female",fg="white", bg="black").grid(row=0, column=5, padx=10,pady=5)
        
        #Sets the entry fields with the current student info
        if (command == "edit"):
                ID.insert(0,student['id#'])
                ID.config(state=DISABLED)
                name.insert(0,student['name'])
                course.insert(0,student['course'])
                year.set(student['year'])
                gender.set(student['gender'])
                    
        tempFrame = Frame(thisFrame,bg="black")
        tempFrame.grid(row=5, column=0, columnspan=2)
        cancel = Button(tempFrame, image=button_cancel, borderwidth=0,bg='black', command=infoWindow.destroy)
        cancel.image=button_cancel
        cancel.grid(row=0,column=0, padx=5, pady=5)
        add = Button(tempFrame, image=button_add if command=="add" else button_save, borderwidth=0,bg='black', command=addStudent)
        add.image=button_add if command=="add" else button_save
        add.grid(row=0,column=1, padx=5, pady=5)

#Widgets in the main window                    
header = Frame(root, height=100, width=500, bg="black")
header.propagate(0)
header.grid(row=0, column=0)
Label(header, text="STUDENT INFORMATION SYSTEM", font = 'Helvitica 15 bold', bg="black", fg="maroon").place(relx=.55, rely=.4, anchor='c')
Label(header, text="Hogwarts University", font = 'Impact 12', bg="black", fg="maroon").place(relx=.55, rely=.65, anchor='c')

logoFrame = Label(header, image=hogwarts_logo, height=90, width=90, bg="white")
logoFrame.pack(side=LEFT, padx=(7,0), pady=7)
logoFrame.image=hogwarts_logo

#Code for a dynamic searchbar
searchFrame = Frame(root)
searchFrame.grid(row=1,column=0,pady=3)
Label(searchFrame, bg="#fbc681", text="SEARCH:", anchor=W, font = 'Arial 9 bold', fg="white").grid(row=0, column=0)
#Declares a string variable to contain the current string in the search bar
entryvar = StringVar()      
myentry = Entry(searchFrame, textvariable=entryvar, width = 68)
myentry.grid(row=0, column=1)
#Traces the changes made in the search bar
entryvar.trace('w',showList)

#Code for making a frame with a scrollbar
wrapper = LabelFrame(root, height=350, width=800)
wrapper.grid(row=2, column=0)
mycanvas = Canvas(wrapper, width=475,height=440)
myFrame= Frame(mycanvas, bg="black")
yscrollbar = Scrollbar(wrapper, orient="vertical", command=mycanvas.yview)
yscrollbar.pack(side=RIGHT, fill="y")
mycanvas.pack(side=LEFT)
mycanvas.configure(yscrollcommand=yscrollbar.set)
mycanvas.bind('<Configure>',lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
mycanvas.create_window((0,0), window=myFrame, anchor="nw")

add = Button(root,image=button_addstudent, borderwidth=0,bg='black', command=lambda:info_window("add",1))
add.image=button_addstudent
add.grid(row=3, column=0, pady=5)

showList()

root.mainloop()
