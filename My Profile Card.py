from tkinter import *

window = Tk()
window.title('My Profile Card')
window.geometry('1000x1000')

title = Label(window, text='My Profile Card', fg='white', bg='purple', width=100)
title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

name_label = Label(window, text='Name:', fg='black', bg='white')
name_label.grid(row=1, column=1, padx=10, pady=5)

name_entry = Entry(window, fg='blue', bg='lightyellow', width=100)
name_entry.grid(row=1, column=1, padx=10, pady=5)

hobby_label = Label(window, text='Hobby:', fg='black', bg='white')
hobby_label.grid(row=2, column=0, padx=10, pady=5)

hobby_entry = Entry(window, fg='blue', bg='lightyellow', width=100)
hobby_entry.grid(row=2, column=0, padx=10, pady=5)

about_frame = Frame(window, relief=RAISED, borderwidth=3)
about_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

about_label = Label(about_frame, text='About Me:')
about_label.pack()

about_text = Text(about_frame, fg='green', bg='lightyellow', width=40, height=4)
about_text.pack()

submit = Button(window, text='Show My Card', bg='purple', fg='white', width=50)
submit.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()