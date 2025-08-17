const gridContainer = document.getElementById('grid-container');
const cellSize = 50;
let objectsOnGrid = [];
const gridDataInput = document.getElementById('mapObjects');
let curGrid = [];

let selectableObjectsOnGrid = [];
let nextSelectableObjectId = 0;
// Changed to an array to hold multiple selected objects
let currentlySelectedObjects = []; // Keeps track of all currently selected objects

/**
 * Clears all existing highlight cells and applies new highlighting based on a shape.
 * @param {HTMLElement} startObjectID - The map object around which to draw the shape.
 * @param {Array<Array<number>>} shape - The list of [row, col] offsets to highlight.
 * @param {string} type - AOE or targeting highlight
 */
function applyHighlightToGrid(startObjectID, shape, type) {
    let startRow = 0;
    let startCol = 0;

    // get coords for selected object
    for (let row = 0; row < curGrid.length; row++) {
        for (let col = 0; col < curGrid[row].length; col++) {
            if (curGrid[row][col].objects.includes(startObjectID)) {
                startRow = row;
                startCol = col;
            }
            // console.log(curGrid[row]);
        }
    }

    // activity shape is 9x9 centered at 4,4
    for (let row = startRow - 4; row < startRow + 5; row++) {
        for (let col = startCol - 4; col < startCol + 5; col++) {
            // console.log(row - startRow + 4);
            // console.log(col - startCol + 4);
            if (JSON.stringify(shape[row - startRow + 4][col - startCol + 4]) == 1) {
                const targetCell = gridContainer.querySelector(`.grid-row:nth-child(${row + 1}) .grid-cell:nth-child(${col + 1})`);
                if (targetCell && type == "AOE") {
                    targetCell.classList.add('AOE-cell');
                } if (targetCell && type == "targeting") {
                    targetCell.classList.add('targeting-cell');
                }
            }
        }
    }
}

/**
 * Evaluates a list of activities and highlights the grid accordingly.
 * @param {Array<Object>} activitiesList - The list of activity JSON objects.
 * @param {HTMLElement|null} selectedMapObject - The currently selected map object (null if none).
 */
function highlightActivities(activitiesList, selectedMapObject) {
    // clear any previous highlights
    const allAOECells = gridContainer.querySelectorAll(`.AOE-cell`);
    allAOECells.forEach(cell => {
        cell.classList.remove('AOE-cell');
    });
    const allTargetingCells = gridContainer.querySelectorAll(`.targeting-cell`);
    allTargetingCells.forEach(cell => {
        cell.classList.remove('targeting-cell');
    });
    console.log("removed highlights");
    // reapply highlights
    for (let i = 0; i < activitiesList.length; i++) {
        if (activitiesList[i].activityType === 'singleTarget' && (selectedMapObject == null)) {
            console.log("single target found!");
            applyHighlightToGrid(executorID, activitiesList[i].shape, "targeting");
        } else if (activitiesList[i].activityType === 'AOE' && selectedMapObject) {
            applyHighlightToGrid(selectedMapObject.id, activitiesList[i].shape, "AOE");
        }
    }
}

function createSelectableObject(objectType, objectIndex, objectIDNum, x, y) {
    const gridRect = gridContainer.getBoundingClientRect();
    let gridX = x - gridRect.left;
    let gridY = y - gridRect.top;

    let col = Math.floor(gridX / cellSize);
    let row = Math.floor(gridY / cellSize);

    col = Math.max(0, Math.min(9, col));
    row = Math.max(0, Math.min(9, row));

    const obj = document.createElement('div');
    obj.id = `${objectType}-${objectIndex}-${objectIDNum}`; // each object is the type, type asset index, then an arbitrary id value to differentiate
    obj.classList.add('selectable-object', objectType);
    obj.style.backgroundImage = `url(${mapObjects[objectIndex].mapIconImgFile})`
    obj.style.backgroundRepeat = 'no-repeat'; // Ensure image doesn't repeat
    obj.style.backgroundSize = 'cover'; // Resize image to fit object size
    obj.draggable = true;
    obj.style.position = 'absolute'; // Ensure absolute positioning
    const objRect = obj.getBoundingClientRect();
    gridContainer.appendChild(obj);
    const snappedX = col * cellSize;
    const snappedY = row * cellSize;
    // need to use translate3d rather than the style.left/top attributes so that it can be moved again with no jumps
    obj.style.transform = `translate3d(${snappedX}px, ${snappedY}px, 0)`;
    objectsOnGrid.push(obj);
    makeSelectable(obj, x, y);
}

function updateGridData() {
    // (This function remains the same)
    const grid = [];
    const curGridRows = encounter.footingMapIndexes.length;
    const curGridCols = encounter.footingMapIndexes[0].length;
    for (let row = 0; row < curGridRows; row++) {
        grid.push([]);
        for (let col = 0; col < curGridCols; col++) {
            grid[row].push({ objects: [] });
        }
    }

    // console.log(currentlySelectedObject);

    objectsOnGrid.forEach(obj => {
        const objRect = obj.getBoundingClientRect();
        const gridRect = gridContainer.getBoundingClientRect();
        const objLeft = objRect.left - gridRect.left;
        const objTop = objRect.top - gridRect.top;
        const objRight = objLeft + objRect.width;
        const objBottom = objTop + objRect.height;
        const objName = obj.id;

        for (let row = 0; row < curGridRows; row++) {
            for (let col = 0; col < curGridCols; col++) {
                const cellLeft = col * cellSize;
                const cellTop = row * cellSize;
                const cellRight = cellLeft + cellSize;
                const cellBottom = cellTop + cellSize;

                if ((objRight <= cellRight) && (objLeft >= cellLeft) && (objBottom <= cellBottom) && (objTop >= cellTop)) {
                    // console.log("pushed!");
                    grid[row][col].objects.push(objName);
                }
            }
        }
    });
    // console.log(grid);
    // console.log(JSON.stringify(grid));
    gridDataInput.value = JSON.stringify(grid);
    curGrid = grid;
}

function updateGridFromData(gridData) {
    // Clear existing objects on the grid
    const gridRect = gridContainer.getBoundingClientRect();
    objectsOnGrid.forEach(obj => gridContainer.removeChild(obj));
    objectsOnGrid = [];

    for (let row = 0; row < gridData.length; row++) {
        for (let col = 0; col < gridData[row].length; col++) {
            const cellData = gridData[row][col];
            if (cellData.objects && cellData.objects.length > 0) {
                cellData.objects.forEach(obj => {
                    // Find the index of the object type. The data transferred and the data contained within the grid expects an index, not the name of the object.
                    const objectNameArray = obj.split("-");
                    const objectType = objectNameArray[0];
                    const objectIndex = objectNameArray[1];
                    const objectIDNum = objectNameArray[2];
                    const x = col * cellSize + gridRect.left;
                    const y = row * cellSize + gridRect.top;
                    createSelectableObject(objectType, objectIndex, objectIDNum, x, y);
                });
            }
        }
    }
    updateGridData();
    // only do these for action menu
    if (actionActivities) {
        highlightActivities(actionActivities, null);
    }
}

///////////// 

/**
 * Makes an individual HTML element selectable.
 * When clicked, it will toggle its selection state.
 * If Ctrl/Cmd key is pressed, it will add/remove from multi-selection.
 * Otherwise, it will clear existing selections and select only itself.
 * @param {HTMLElement} obj - The DOM element to make selectable.
 */
function makeSelectable(obj) {
    if (!obj) {
        console.error("makeSelectable: obj is undefined.");
        return;
    }

    obj.addEventListener('click', (e) => handleSelectionClick(e, obj));
    obj.addEventListener('touchstart', (e) => handleSelectionClick(e, obj), { passive: true }); // Use passive for touch events if not preventing default
}

/**
 * Handles the click event for a selectable object, managing single and multi-selection.
 * @param {Event} e - The click/touch event.
 * @param {HTMLElement} clickedObject - The DOM element that was clicked.
 */
function handleSelectionClick(e, clickedObject) {
    e.stopPropagation(); // Prevent the click from bubbling up to the gridContainer

    const isCtrlOrCmdPressed = e.ctrlKey || e.metaKey; // Ctrl for Windows/Linux, Cmd for Mac

    if (isCtrlOrCmdPressed) {
        // Multi-select behavior (toggle selection)
        toggleObjectSelection(clickedObject);
    } else {
        // Single-select behavior (clear all, then select clicked)
        // Only clear if the clicked object is not already the ONLY selected object
        if (!(currentlySelectedObjects.length === 1 && currentlySelectedObjects.includes(clickedObject))) {
            clearSelection(false); // Clear all existing selections without affecting the clicked object's immediate state
        }
        toggleObjectSelection(clickedObject); // Toggle the clicked object's selection
    }

    // The logic for which object to pass depends on your multi-select behavior.
    // For AOE, it should be the most recently selected object. Let's assume
    // the last item in the array is the most recently selected one.
    const mostRecentlySelectedObject = currentlySelectedObjects.length > 0
        ? currentlySelectedObjects[currentlySelectedObjects.length - 1]
        : null;
    if (actionActivities) {
        highlightActivities(actionActivities, mostRecentlySelectedObject);
    }

    // Optional: Call a custom callback function if you need to do something else
    // after selection/deselection (e.g., update an info panel)
    // onObjectsSelectedOrUnselected(currentlySelectedObjects);
    updateGridData(); // Update data if selection state affects what you save
}

/**
 * Toggles the 'selected' class and updates the currentlySelectedObjects array.
 * @param {HTMLElement} obj - The object to toggle selection for.
 */
function toggleObjectSelection(obj) {
    if (obj.classList.contains('selected')) {
        // Object is currently selected, unselect it
        obj.classList.remove('selected');
        // Remove from the array
        currentlySelectedObjects = currentlySelectedObjects.filter(item => item !== obj);
        console.log(`Object ${obj.id} unselected. Total selected: ${currentlySelectedObjects.length}`);
    } else {
        // Object is not selected, select it
        obj.classList.add('selected');
        // Add to the array
        currentlySelectedObjects.push(obj);
        console.log(`Object ${obj.id} selected. Total selected: ${currentlySelectedObjects.length}`);
    }
}

/**
 * Clears the current selection, unhighlighting all selected objects.
 * @param {boolean} [shouldLog=true] - Optional. If true, logs a message.
 */
function clearSelection(shouldLog = true) {
    if (currentlySelectedObjects.length > 0) {
        currentlySelectedObjects.forEach(obj => {
            obj.classList.remove('selected');
        });
        if (shouldLog) {
            console.log(`Cleared ${currentlySelectedObjects.length} selected objects.`);
        }
        currentlySelectedObjects = []; // Clear the array
    }
}