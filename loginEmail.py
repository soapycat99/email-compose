import smtplib
from tkinter import *
from tkinter import messagebox
import time

sender =""
receiver =""
password = ""
subject = ""
body = ""
WIDTH = 750
HEIGHT = 470

window = Tk()
window['bg'] = 'light yellow'
window.title("Email Compose")
window.geometry(str(WIDTH) + 'x' + str(HEIGHT))

#Label Logic
Label(window, text ="Login", font = ("Bradley Hand", 30, 'bold'), bg ='light yellow').place(x= 300, y = 30)

#user name entry
usernameLabel = Label(window, text = 'Username: ',
                       bg = 'light yellow').place(x = 180, y= 100)
nameEntry = Entry(window,
              font =("Ink Free",15),
              bg = '#cfc85d')
nameEntry.place(x = 250, y = 100)
#password entry
passwordLabel = Label(window, text = 'Password: ',
                       bg = 'light yellow').place(x = 180, y = 140)
passwordEntry = Entry(window,
              font =("Ink Free",15),
              bg = '#cfc85d', show ='*')
passwordEntry.place( x = 250, y = 140)

#start transport layer security
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

def login(event = NONE):
    global sender
    global password
    sender = nameEntry.get()
    print(sender)
    password = passwordEntry.get()
    time.sleep(1)

    try:
        server.login(sender, password)
        print("Logged in...")
        for label in window.winfo_children():
            label.destroy()
        compose()
    except smtplib.SMTPAuthenticationError:
        print("wrong")
        Label(window, text = 'Invalid username or password, try again', fg ='red',
              bg = 'light yellow').place( x = 210, y = 175)

def compose():
    global receiver, subject, body
    canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg = 'light yellow')

    # Recipient
    toText = Text(canvas, font=('Arial', 12), bg='light yellow',
                  width=99, height=0, highlightthickness=0)
    toText.place(x=51, y=33)


    Label(canvas, text='To:', bg='systemTransparent', font=('Arial', 12, 'bold')).place(x=20, y=31)
    canvas.create_line(20, 50, WIDTH - 10, 50, fill='light gray', width=2)

    # Subject
    subjectText = Text(canvas, font=('Arial', 12), bg='light yellow',
                       width=95, height=0, highlightthickness=0)
    subjectText.place(x=80, y=68)


    Label(canvas, text='Subject:', bg='systemTransparent', font=('Arial', 12, 'bold')).place(x=20, y=66)
    canvas.create_line(20, 85, WIDTH - 10, 85, fill='light gray', width=2)

    #body
    bodyText = Text(canvas, bg='lightyellow', font=('Ink Free', 12), height=22,
                width=82, padx=5, pady=5, highlightthickness=0)
    bodyText.place(x=20, y=93)


    #send button
    sendButton = Button(canvas,text ='Send', state=ACTIVE, bg='light blue',
                        command= lambda : send(toText, subjectText, bodyText))
    sendButton.place(x=WIDTH - 40, y=HEIGHT - 32)

    #pack
    canvas.pack()

def send(toText, subjectText, bodyText):
    # global toText, subjectText, bodyText
    receiver = toText.get("1.0", END).strip()
    print(receiver)
    subject = subjectText.get("1.0", END).strip()
    print(subject)
    body = bodyText.get("1.0", END).strip()
    # print("Sent!")
    message = f''' From: Snoop Dogg {sender}
    To: Bao Tran {receiver}
    Subject: {subject} \n
    {str(body)} '''
    print(message)
    try:
        server.sendmail(sender, receiver, message)
        messagebox.showinfo(message = "Email sent!")
    except Exception as err:
        print(f"General exception: {err}")
    except:
        messagebox.showerror(title='ERROR!', message='Some thing went wrong :(')

    window.destroy()


window.bind("<Return>", login)
submit_button = Button(window, text= 'Sign In',
                      bg= 'light yellow', command= login)
submit_button.place(x= 320, y= 200)



window.mainloop()