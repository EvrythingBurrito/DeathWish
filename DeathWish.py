# Flask
from flask import Flask, render_template, url_for, request
import Pages
# TKinter
import tkinter as tk
# threading
import threading
# DeathWish Custom
import Game
from Region import Region

# flask page definition
# host_name = "127.0.0.1"
host_name = "0.0.0.0" # listen on all public IPs
port = "5000"
# flask main
def run_flask_app():
    Pages.app.run(host=host_name, port=port, debug=False, use_reloader=False)

# tkinter main
def run_tkinter_app():
    root = tk.Tk()
    root.title("DeathWish")

    def update_display():
        text_box.delete(1.0, tk.END)
        for region in Game.DMAssets.regionList:
            text_box.insert(tk.END, str(region) + '\n')
        root.after(1000, update_display)  # Update every second

    text_box = tk.Text(root)
    text_box.pack(fill=tk.BOTH, expand=True)
    update_display()

    root.mainloop()

# app main
if __name__ == "__main__":
    # flask_thread = threading.Thread(target=run_flask_app)
    # flask_thread.start()
    # run_tkinter_app()
    run_flask_app()