import smtplib
import tkinter as tk

from tkinter import messagebox
import time

WIDTH = 750
HEIGHT = 470
sender = ""
receiver = ""
password = ""
subject = ""
body = ""

class LoginGUI:
    def __init__(self,master):
        self.master = master
        self.frame = tk.Frame(self.master, bg = 'light yellow', padx = 200)
        # Label Logic
        tk.Label(self.frame, text="Login", font=("Bradley Hand", 30, 'bold'), bg='light yellow').grid(row = 0, column = 0, pady = 5, columnspan = 3)
        #user name entry
        tk.Label(self.frame, text = 'Username: ',
                               bg = 'light yellow').grid(row = 1, column = 0)
        self.nameEntry = tk.Entry(self.frame,
                      font =("Ink Free",15),
                      bg = '#cfc85d')
        self.nameEntry.grid( row = 1, column =1)
        #password entry
        tk.Label(self.frame, text = 'Password: ',
                               bg = 'light yellow').grid(row = 2, column = 0)
        self.passwordEntry = tk.Entry(self.frame,
                      font =("Ink Free",15),
                      bg = '#cfc85d', show ='*')
        self.passwordEntry.grid(row =2, column =1)
        self.frame.rowconfigure(3, weight = 1)
        self.mess = tk.Label(self.frame, bg= 'light yellow')
        self.mess.grid(row= 3, column= 0, columnspan= 3)
        tk.Button(self.frame, text='Sign In', bg='light yellow', command = self.login).grid(row= 4, column = 0, columnspan= 3)
        self.server = self.serverConnect()
        self.master.bind("<Return>", self.login)
        self.frame.grid(row = 1, column = 0, sticky ='')

    def serverConnect(self):
        # start transport layer security
        print('connect')
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        return server


    def login(self, event = None):
        # global sender
        # global password
        print('log in')
        sender = self.nameEntry.get()
        print(sender)
        password = self.passwordEntry.get()
        time.sleep(0.5)

        try:
            self.server.login(sender, password)
            print("Logged in...")
            self.newWindow = tk.Tk()
            self.newWindow.title("Email Compose")
            self.newWindow.geometry(str(WIDTH) + 'x' + str(HEIGHT))
            self.compose = composeGUI(self.newWindow, self.server)
            self.master.destroy()

        except smtplib.SMTPAuthenticationError:
            print("wrong")
            self.mess.config(text = 'Invalid username or password, try again', fg ='red')


#Upper window
class composeGUI():
    def __init__(self, master, server):
        self.server = server
        self.master = master
        self.frame = tk.Frame(master, bg='light yellow')
        self.canvas = tk.Canvas(self.frame, width=WIDTH, height=HEIGHT, bg = 'light yellow')

        # Recipient
        self.toText = tk.Text(self.canvas, font=('Arial', 12), bg='light yellow',
                      width=99, height=0, highlightthickness=0)
        self.toText.place(x=51, y=33)


        tk.Label(self.canvas, text='To:', bg='systemTransparent', font=('Arial', 12, 'bold')).place(x=20, y=31)
        self.canvas.create_line(20, 50, WIDTH - 10, 50, fill='light gray', width=2)

        # Subject
        self.subjectText = tk.Text(self.canvas, font=('Arial', 12), bg='light yellow',
                           width=95, height=0, highlightthickness=0)
        self.subjectText.place(x=80, y=68)


        tk.Label(self.canvas, text='Subject:', bg='systemTransparent', font=('Arial', 12, 'bold')).place(x=20, y=66)
        self.canvas.create_line(20, 85, WIDTH - 10, 85, fill='light gray', width=2)

        #body
        self.bodyText = tk.Text(self.canvas, bg='lightyellow', font=('Ink Free', 12), height=22,
                    width=82, padx=5, pady=5, highlightthickness=0)
        self.bodyText.place(x=20, y=93)


        #send button
        self.sendButton = tk.Button(self.canvas, text ='Send', bg='light blue',
                                    command=self.send)
        self.sendButton.place(x=WIDTH - 40, y=HEIGHT - 32)

        #pack
        self.canvas.pack()
        self.frame.pack()

    def send(self):
        # global receiver, subject, body
        # global toText, subjectText, bodyText
        receiver = self.toText.get("1.0", tk.END).strip()
        print(receiver)
        subject = self.subjectText.get("1.0", tk.END).strip()
        print(subject)
        body = self.bodyText.get("1.0", tk.END).strip()
        # print("Sent!")
        message = 'Subject: {}\n\n{}'.format(subject,body)

        try:
            self.server.sendmail(sender, receiver, message)
            messagebox.showinfo(message = "Email sent!")
        except Exception as err:
            print(f"General exception: {err}")
        except:
            messagebox.showerror(title='ERROR!', message='Some thing went wrong :(')
        self.server.quit()
        self.master.destroy()

def main():
    root = tk.Tk()
    root['bg'] = 'light yellow'
    root.title("Email Compose")
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    root.grid_rowconfigure(0, weight=2)
    root.grid_rowconfigure(1, weight=3)
    root.grid_rowconfigure(2, weight=3)
    root.grid_columnconfigure(0, weight=1)
    app = LoginGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
