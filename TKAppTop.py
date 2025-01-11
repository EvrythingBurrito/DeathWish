import tkinter as tk
import time
import os
from PIL import Image, ImageTk
import multiprocessing
from multiprocessing import Queue
import DeathWish
import json
# DeathWish Custom
import Game
from MapObject import MapObject

def title_screen(canvas):
    """Displays the title screen with background image and centered text."""
    canvas.delete("all")  # Clear the canvas  
    # Load and resize background image
    bg_image = Image.open("static/css/parchment.jpg")
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    bg_image = bg_image.resize((canvas_width, canvas_height), Image.LANCZOS) # Resize to fit canvas
    bg_photo = ImageTk.PhotoImage(bg_image)
    # Display the background image
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)
    canvas.background_image = bg_photo  # Keep a reference
    # Display the title text (centered)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        text="DeathWish",
        font=("Poor Richard", 72),  # Increased font size for better visibility
        fill="black",  # Changed text color for contrast
        anchor=tk.CENTER #Ensure text is properly centered
    )

def encounter_screen(encounterIndex, canvas): #from previous responses
    encounter = Game.assets.encounterList[encounterIndex]
    print(encounter.name)
    # mapGrid is stored as a json string
    mapGrid = json.loads(encounter.mapGrid)
    numRows = len(mapGrid[0])
    numCols = len(mapGrid)
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    cellWidth = canvas_width / numCols
    cellHeight = canvas_height / numRows

    # Store image references to prevent garbage collection
    canvas.image_refs = []  

    mapIconImgFile = None
    for row in range(numRows):
        for col in range(numCols):
            canvas.create_rectangle(col * cellWidth, row * cellHeight, (col + 1) * cellWidth, (row + 1) * cellHeight, outline="gray")
            for object in mapGrid[row][col]["objects"]:
                mapObjectID = object.split("-")
                print(mapObjectID)
                if mapObjectID[1]: # object found on cell location
                    assetIndex = int(mapObjectID[1])
                    if mapObjectID[0] == "npc":
                        mapIconImgFile = Game.assets.NPCList[assetIndex].mapIconImgFile
                    # get rid of starting "/"
                    mapIconImgFile = mapIconImgFile[1:]
                    img = Image.open(mapIconImgFile)
                    # Resize image to fit the cell
                    img = img.resize((int(cellWidth), int(cellHeight)), Image.LANCZOS) # Use LANCZOS for best quality
                    photo = ImageTk.PhotoImage(img)
                
                    # Add image to canvas and store a reference
                    image_id = canvas.create_image(col * cellWidth, row * cellHeight, anchor=tk.NW, image=photo)
                    canvas.image_refs.append(photo) # Keep a reference!

def create_tkinter_thread(processQueue):
    def tkinter_thread():
        root = tk.Tk()
        root.title("Game")
        # root.attributes('-fullscreen', True)
        # root.geometry("3840x2160")
        # root.geometry("1280x720")
        root.geometry("640x480")
        canvas = tk.Canvas(root, bg="black")
        canvas.pack(fill=tk.BOTH, expand=True)
        gameState = "title"
        curState = "encounter"
        encounterIndex = 0
        curEncounterIndex = 0

        def update_tkinter():
            nonlocal gameState, curState, encounterIndex, curEncounterIndex
            # pop state changes off queue
            if processQueue.qsize() > 0:
                message = processQueue.get_nowait()
                if isinstance(message, tuple) and message[0] == "gameState":
                    gameState = message[1]
                elif isinstance(message, tuple) and message[0] == "encounterIndex":
                    encounterIndex = message[1]
            # update game screen based on state changes
            else:
                # update state screen
                if curState != gameState: 
                    curState = gameState
                    canvas.delete("all")
                    if gameState == "title":
                        title_screen(canvas)
                        canvas.update()
                    elif gameState == "encounter":
                        encounter_screen(curEncounterIndex, canvas)
                        canvas.update()
                # if encounter state has changed, update encounter screen
                elif (gameState == "encounter") & (curEncounterIndex != encounterIndex):
                    curEncounterIndex = encounterIndex
                    canvas.delete("all")
                    encounter_screen(curEncounterIndex, canvas)
                    canvas.update()

            root.after(100, update_tkinter)

        def on_resize(event):
            root.after(100, update_tkinter)

        root.bind("<Configure>", on_resize) #Bind resize event to the new function
        root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False)) #Bind escape to exit fullscreen
        root.after(100, update_tkinter)
        root.mainloop()
    
    return tkinter_thread