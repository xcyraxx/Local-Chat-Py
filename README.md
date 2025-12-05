# Python LAN Chat App

A simple Python chat application with GUI, supporting multiple clients on a LAN. Built using **Tkinter** for the interface and **sockets** for networking.

---

## Features

- GUI-based chat client  
- Supports multiple clients simultaneously  
- Real-time messaging  
- Username identification  
- Automatic scrolling chat window  
- Threaded client for asynchronous receiving  

---

## Requirements

- Python 3.7+  
- Standard Python libraries:
  - `tkinter`
  - `socket`
  - `threading`
  - `select`
- (No external packages required)

---

## Files

| File | Description |
|------|-------------|
| `server.py` | Runs the chat server |
| `client.py` | Handles client networking |
| `app.py` | Tkinter GUI for connecting and chatting |

---

## Usage

### 1. Start the server

```bash
python3 server.py
```
- When prompted, enter your LAN IP (e.g., `192.45.2.1`) or use `0.0.0.0` to accept connections on all interfaces.  
- The server will listen on port `4747`.

### 2. Start the client (on any device in the LAN)

```bash
python3 app.py
```
- Enter the server IP and your username
- Click **Connect**
- Start chatting!


---

## Notes

- Make sure all devices are on the **same LAN**.
- The server must be started before clients connect.
- If a client disconnects, others are notified automatically.
- Currently, the app **does not encrypt messages**. Only use on trusted networks.

---
