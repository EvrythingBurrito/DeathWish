from multiprocessing import Process
import multiprocessing
import time
# Flask
from flask import Flask, render_template, url_for, request
import FlaskAppTop
# TKinter
import tkinter as tk
from TKAppTop import create_tkinter_thread
# threading
import threading
# DeathWish Custom
import Game
from Region import Region

def run_flask_app(host, port, processQueue): #This function is what will be run in the process
    app = FlaskAppTop.create_flask_app(processQueue)
    app.run(host=host, port=port, debug=False, use_reloader=False)

def main():
    processQueue = multiprocessing.Queue()

    # Create and start the Tkinter thread using the factory function
    tkinter_thread_function = create_tkinter_thread(processQueue)
    tkinter_thread_handle = threading.Thread(target=tkinter_thread_function, daemon=True)
    tkinter_thread_handle.start()

    # Start Flask in a separate process
    host_name = "127.0.0.1"
    # host_name = "0.0.0.0" # listen on all public IPs
    port = "5000"
    flask_process = Process(target=run_flask_app, args=(host_name, port, processQueue), daemon=True)
    flask_process.start()
    print("Flask started")

    try:
        while True:
            time.sleep(1)  # Check every second (adjust as needed)
    except KeyboardInterrupt:
        print("Exiting...")
        # Add cleanup code here if needed (e.g., stopping subprocesses more gracefully)
        flask_process.terminate() #Terminate the flask process
        flask_process.join() #Wait for the flask process to properly close
        print("Flask process closed")

# app main
if __name__ == "__main__":
    main()