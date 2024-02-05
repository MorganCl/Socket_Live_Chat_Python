
# Python program to implement client side of chat room. 
import socket, select, sys, json
from _thread import start_new_thread
import tkinter as tk
from tkinter import filedialog, messagebox

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port))


class App:
    def __init__(self):
        self.client = tk.Tk()
        self.client.geometry("500x500")
        self.client.title("Chat")

        self.menu = tk.Menu(self.client)
        self.client.config(menu=self.menu)

        self.options = tk.Menu(self.menu)
        self.options.add_command(label="Save chat", command=lambda : self.user_commands("save_chat"))
        self.options.add_command(label="Clear chat", command=lambda : self.user_commands("clear_chat"))
        self.options.add_separator()
        self.options.add_command(label="Exit", command=lambda : self.user_commands("exit"))
        self.menu.add_cascade(label="Options", menu=self.options)

        self.preferences = tk.Menu(self.menu)
        self.preferences.add_command(label="Change name", command=self.prompt)
        self.preferences.add_command(label="View profile", command=self.prompt)
        self.menu.add_cascade(label="Preferences", menu=self.preferences)

        self.message = tk.Entry(self.client, font=("Verdana", 10))
        self.message.insert(0, "Type your message here...")
        self.message.bind("<FocusIn>", self.on_focus)
        self.message.bind("<FocusOut>", self.on_focusout)
        self.message.bind("<Return>", self.send_message)
        self.message.pack(side="bottom", fill="x")

        self.message_scroll = tk.Scrollbar(self.client)
        self.messages = tk.Text(self.client, height=4, )
        self.message_scroll.pack(side="right", fill="y")
        self.messages.pack(side="left", fill="both")
        self.message_scroll.config(command=self.messages.yview)
        self.messages.config(yscrollcommand=self.message_scroll.set)

        start_new_thread(self.update, ())

        self.client.grid_rowconfigure(0, weight=1)
        self.client.grid_columnconfigure(0, weight=1)

        self.client.mainloop()

    def prompt(self):
        self.get_name = tk.Toplevel(self.client)
        self.get_name.geometry("290x40")
        
        self.name = tk.Entry(self.get_name, font=("Verdana", 12))
        self.name.pack(side="left", fill="y")
        submit = tk.Button(self.get_name, text="Continue", command=self.submit_name)
        submit.pack(side="right", fill="both")

        self.get_name.mainloop()

    def submit_name(self):
        name = self.name.get()
        if len(name) < 15:
            clean = json.dumps({"text" : name, "action" : "name"})
            server.send(clean.encode())
            self.get_name.destroy()
        else:
            tkMessageBox.showinfo("Error", "Chat name must be less than 15 chars")

    def user_commands(self, command):
        if command == "exit":
            server.close()
            quit()
        elif command == "save_chat":
            all_chat = self.messages.get("1.0", "end")
            filename = tkFileDialog.asksaveasfilename(filetypes=(("Text files", "*.txt"), ("Log files", "*.log"), ("All files", "*.*")))
            f = open(filename, "w")
            f.write(all_chat)
            f.close()
        elif command == "clear_chat":
            self.messages.delete('1.0', 'end')

    def on_focus(self, event):
        if self.message.get() == "Type your message here...":
            self.message.delete(0, "end") # delete all the text in the entry
            self.message.insert(0, "") #Insert blank for user input
            self.message.config(fg = "black")

    def on_focusout(self, event):
        if self.message.get() == "":
            self.message.insert(0, "Type your message here...")
            self.message.config(fg = "grey")

    def send_message(self, event):
        clean = json.dumps({"text" : self.message.get(), "action" : "message"})
        server.send(clean.encode())
        self.message.delete(0, "end")

    def update(self):
        while True:
            sockets_list = [server]
            read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
            for socks in read_sockets:
                if socks == server: 
                    message = socks.recv(2048)
                    self.messages.insert("end", message)
                    self.messages.see("end")

app = App()
