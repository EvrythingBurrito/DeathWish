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

def encounter_screen(encounter, canvas):
    # mapGridJSON is stored as a json string
    mapGridJSON = json.loads(encounter.mapGridJSON)
    numRows = len(mapGridJSON)
    numCols = len(mapGridJSON[0])
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    cellWidth = canvas_width / numCols
    cellHeight = canvas_height / numRows

    # Store image references to prevent garbage collection
    canvas.image_refs = []  

    mapIconImgFile = None
    for row in range(numRows):
        for col in range(numCols):
            x1 = col * cellWidth
            y1 = row * cellHeight
            x2 = (col + 1) * cellWidth
            y2 = (row + 1) * cellHeight
            image = Image.open(Game.assets.footingDict[encounter.footingMap[row][col]].mapIconFile[1:])
            # Resize the image to fit the cell
            image = image.resize((int(cellWidth), int(cellHeight)), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Create the image on the canvas
            image_id = canvas.create_image(x1, y1, anchor=tk.NW, image=photo)
            canvas.image_refs.append(photo)

            # Optionally create the rectangle outline on top of the image
            canvas.create_rectangle(x1, y1, x2, y2, outline="gray", width=1) #Width added to make outlines thinner

            for object in mapGridJSON[row][col]["objects"]:
                mapObjectID = object.split("-")
                print(mapObjectID)
                if mapObjectID[1]: # object found on cell location
                    assetIndex = int(mapObjectID[1])
                    mapIconImgFile = Game.assets.allMapObjects[assetIndex].mapIconImgFile
                    # get rid of starting "/"
                    mapIconImgFile = mapIconImgFile[1:]
                    img = Image.open(mapIconImgFile)
                    # Resize image to fit the cell
                    img = img.resize((int(cellWidth), int(cellHeight)), Image.LANCZOS) # Use LANCZOS for best quality
                    photo = ImageTk.PhotoImage(img)
                
                    # Add image to canvas and store a reference
                    image_id = canvas.create_image(col * cellWidth, row * cellHeight, anchor=tk.NW, image=photo)
                    canvas.image_refs.append(photo) # Keep a reference!

def campaign_screen(campaign, canvas):
    # mapGridJSON is stored as a json string
    mapGridJSON = json.loads(campaign.mapGridJSON)
    # regionMapIndexes is a 2D list
    regionMapIndexes = campaign.regionMapIndexes
    numRows = len(mapGridJSON)
    numCols = len(mapGridJSON[0])
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    cellWidth = canvas_width / numCols
    cellHeight = canvas_height / numRows

    # Store image references to prevent garbage collection
    canvas.image_refs = []  

    mapIconImgFile = None
    for row in range(numRows):
        for col in range(numCols):
            x1 = col * cellWidth
            y1 = row * cellHeight
            x2 = (col + 1) * cellWidth
            y2 = (row + 1) * cellHeight
            image = Image.open(Game.assets.regionList[int(campaign.regionMapIndexes[row][col])].worldMapIconFile[1:])
            # Resize the image to fit the cell
            image = image.resize((int(cellWidth), int(cellHeight)), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Create the image on the canvas
            image_id = canvas.create_image(x1, y1, anchor=tk.NW, image=photo)
            canvas.image_refs.append(photo)

            # Optionally create the rectangle outline on top of the image
            canvas.create_rectangle(x1, y1, x2, y2, outline="gray", width=1) #Width added to make outlines thinner
            for object in mapGridJSON[row][col]["objects"]:
                mapObjectID = object.split("-")
                # print(mapObjectID)
                if mapObjectID[1]: # object found on cell location
                    assetIndex = int(mapObjectID[1])
                    if mapObjectID[0] == "stationary" or mapObjectID[0] == "party":
                        mapIconImgFile = Game.assets.landmarkList[assetIndex].mapIconImgFile
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
        # initialize game screens
        curEncounter = Game.assets.encounterList[0]
        curCampaign = Game.assets.campaignList[0]
        refresh = 0

        def update_tkinter():
            nonlocal refresh, gameState, curState, curEncounter, curCampaign
            # pop state changes off queue
            if processQueue.qsize() > 0:
                message = processQueue.get_nowait()
                print(message)
                refresh = 1
                if isinstance(message, tuple) and message[0] == "gameState":
                    gameState = message[1]
                elif isinstance(message, tuple) and message[0] == "refreshEncounter":
                    curEncounter = message[1]
                elif isinstance(message, tuple) and message[0] == "refreshCampaign":
                    curCampaign = message[1]
            # update game screen based on state changes
            else:
                if (refresh == 1):
                    refresh = 0
                    if gameState == "title":
                        title_screen(canvas)
                        canvas.update()
                    elif gameState == "encounter":
                        encounter_screen(curEncounter, canvas)
                        canvas.update()
                    elif gameState == "campaign":
                        campaign_screen(curCampaign, canvas)
                        canvas.update()

            root.after(100, update_tkinter)

        def on_resize(event):
            root.after(100, update_tkinter)

        root.bind("<Configure>", on_resize) #Bind resize event to the new function
        root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False)) #Bind escape to exit fullscreen
        root.after(100, update_tkinter)
        root.mainloop()
    
    return tkinter_thread