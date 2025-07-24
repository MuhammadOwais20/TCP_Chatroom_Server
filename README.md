# TCP-Based Chatroom Server (Python)

This is a group-based project developed using Python that implements a **TCP-based Chatroom Server**. It allows multiple clients to connect and communicate with each other in real-time over the **same local network (LAN)**.

The server uses:
- **Socket programming** for TCP communication
- **Threading** for handling multiple clients
- **Singly linked list** for dynamic client management
- **File logging** to maintain chat history

---

## Problem Statement

Traditional array-based systems are inefficient in managing dynamic client connections. This project tackles:
- Real-time message broadcasting
- Efficient connection/disconnection handling
- Chat session logging
- Dynamic memory management using a linked list

---

## Features

- Multiple clients can join simultaneously
- Real-time message broadcasting
- Linked list used for managing client details
- Maintains chat history in a log file
- Clean shutdown with `exit` command

---

## How It Works

### Server Side
- Binds to a port and listens for incoming connections
- Adds each client to a linked list with their socket, nickname, and IP
- Handles incoming messages and broadcasts them to others
- Removes disconnected clients from the list

### Client Side
- Connects to the server and sets a nickname
- Sends and receives messages using two threads:
  - One for sending
  - One for receiving

---
