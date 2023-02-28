import tkinter
from tkinter import ttk
from tkinter import messagebox




TITLE = "PV Module"



def send_data():
    if accept_var.get()=="Accepted":

        firstname = first_name_entry.get()
        lastname = last_name_entry.get()

        title = title_combobox.get()
        age = age_spinbox.get()
        nationality = nationality_combobox.get()

        registered_status = registered_status_var.get()
        from pvmodule.location import Location
        Location = Location()
        location = Location.set_location('Oeiras')
        print(Location.get_info(location))

    else:
        tkinter.messagebox.showwarning(title="Error", message="You have not accepted the terms & conditions.")


    







window = tkinter.Tk()
window.title(TITLE)

######Widget
frame = tkinter.Frame(window)
frame.pack()

######Saving user info
user_info_frame = tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row = 0 , column = 0, padx = 10, pady = 10)

######Widget inside LabelFrame
#titles
first_name_label= tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row = 0 , column = 0)
#titles
last_name_label= tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row = 0 , column = 1)

######Entries
#Text Entry
first_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row = 1 , column = 0)

last_name_entry = tkinter.Entry(user_info_frame)
last_name_entry.grid(row = 1 , column = 1)

#List Entry
title_label = tkinter.Label(user_info_frame, text="Title")
title_combobox = ttk.Combobox(user_info_frame, values= ["", "Mr.", "Ms.", "Dr."])
title_label.grid(row = 0, column = 2)
title_combobox.grid(row = 1, column = 2)

age_label = tkinter.Label(user_info_frame, text="Age")
age_spinbox = tkinter.Spinbox(user_info_frame, from_= 18, to = 110)
age_label.grid(row = 2, column = 0)
age_spinbox.grid(row = 3, column = 0)

nationality_label = tkinter.Label(user_info_frame, text="Nationality")
nationality_combobox = ttk.Combobox(user_info_frame, values= ["EN", "PT", "DE", "BR"])
nationality_label.grid(row = 2, column = 1)
nationality_combobox.grid(row = 3, column = 1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)



######Saving course info
courses_frame = tkinter.LabelFrame(frame, text="Registration")
courses_frame.grid(row=1, column=0, sticky="news", padx=10, pady=10)

registered_label = tkinter.Label(courses_frame, text = "Registration Status")
registered_status_var = tkinter.StringVar(value="Not Registered")
registered_label.grid(row = 0, column = 0)

registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered", variable=registered_status_var, onvalue="Registered" , offvalue="Not Registered")
registered_check.grid(row = 1, column = 0)


######Terms and Condition info
terms_and_conditions_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
terms_and_conditions_frame.grid(row=2, column=0, sticky="news", padx=10, pady=10)
accept_var = tkinter.StringVar(value = "Not Accepted")
terms_check = tkinter.Checkbutton(terms_and_conditions_frame, text="I accept the terms and conditions.", variable=accept_var, onvalue= "Accepted", offvalue="Not Accepted")
terms_check.grid(row = 0, column = 0)


######Button

button = tkinter.Button(frame, text = "Send Data", command= send_data )
button.grid(row=3, column=0, sticky="news", padx=10, pady=10 )














window.mainloop()