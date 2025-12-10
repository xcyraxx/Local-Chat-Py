import tkinter as tk
from tkinter import ttk, scrolledtext
import client

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Client")
        self.geometry("480x500")

        # Container for frames IPScreen and ChatScreen
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        # Frame creation
        self.frames = {}
        for F in (IPScreen, ChatScreen):
            frame = F(container, self)
            self.frames[F] = frame

        # IPScreen
        self.current = None
        self.show_frame(IPScreen)

    def show_frame(self, page):
        # hide current
        if self.current is not None:
            self.current.pack_forget()

        # show new
        frame = self.frames[page]
        frame.pack(fill="both", expand=True)
        self.current = frame


class IPScreen(ttk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)
		
		# Grid config
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)
		self.grid_rowconfigure(8, weight=1)  # push content to middle

		# IP_entry widget
		ttk.Label(self, text="Enter Server IP:").grid(row=1, column=0, pady=5)
		self.ip_entry = ttk.Entry(self)
		self.ip_entry.grid(row=2, column=0, pady=5, ipady=3, ipadx=10)
		
		# Username entry widget
		ttk.Label(self, text="Enter your name:").grid(row=3, column=0, pady=5)
		self.user_entry = ttk.Entry(self)
		self.user_entry.grid(row=4, column=0, pady=5, ipady=3, ipadx=10)

		# Secret Key entry widget
		ttk.Label(self, text="Enter Secret Key:").grid(row=5, column=0, pady=5)
		self.key_entry = ttk.Entry(self, show="*")
		self.key_entry.grid(row=6, column=0, pady=5, ipady=3, ipadx=10)
		
		# Connect button
		ttk.Button(self, text="Connect", command=self.connect_to_server
		).grid(row=7, column=0, pady=5, ipady=3, ipadx=5)

	def connect_to_server(self):
		ip = self.ip_entry.get().strip()
		username = self.user_entry.get().strip()
		password = self.key_entry.get().strip()
		
		controller = self.master.master
		chat_screen = controller.frames[ChatScreen]
		
		client.connect(ip, 4747, username, password, chat_screen.handle_incoming)
		
		controller.show_frame(ChatScreen)

class ChatScreen(ttk.Frame):
	def __init__(self, parent, controller):
		super().__init__(parent)

		# Internal layout of chat screen
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)
		
		# Message area
		self.chat_area = scrolledtext.ScrolledText(self, state='disabled', width=100, height=20)
		self.chat_area.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
		
		# Frame for text area and send button
		frame_msg = ttk.Frame(self)
		frame_msg.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
		
		frame_msg.grid_columnconfigure(0, weight=1)
		
		# text area
		self.msg_entry = ttk.Entry(frame_msg)
		self.msg_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
		
		# send button
		self.send_btn = ttk.Button(frame_msg, text="Send", command=self.send_message)
		self.send_btn.grid(row=0, column=1,padx=5, pady=5)
		
		self.msg_entry.bind("<Return>", self.on_enter_pressed)
		
	def on_enter_pressed(self, event):
		self.send_message()
	
	def send_message(self):
		message = self.msg_entry.get().strip()
		if message:
			client.send_msg(message)
			self.add_msg(f"You:{message}\n")
			self.msg_entry.delete(0, 'end')
			
	def handle_incoming(self, username, message):
		self.after(0, self.add_msg, f"{username}:{message}\n")
		
	def add_msg(self, text):
		self.chat_area.config(state='normal')
		self.chat_area.insert('end', text)
		self.chat_area.config(state='disabled')
		self.chat_area.yview('end')
			
	
			
if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
