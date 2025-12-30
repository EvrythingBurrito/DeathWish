const gridContainer = document.getElementById('grid-container');
const cellSize = 50;
let objectsOnGrid = [];
let curGrid = [];
let movementsTaken = 0;
let movement_path = [[]];
let prev_movement_coords = [];
let selectableObjectsOnGrid = [];
let nextSelectableObjectId = 0;
// Changed to an array to hold multiple selected objects
let currentlySelectedObjects = []; // Keeps track of all currently selected objects

document.getElementById('submit_action_form').addEventListener('submit', function(e) {
    // For each activity, fill in the corresponding hidden input
    actionActivities.forEach((activity, i) => {
        let data = {};
        if (activity.type === 'move') {
            // Find executor object
            const obj = objectsOnGrid.find(o => o.id === executorID);
            if (obj) {
                data.row = obj.dataset.row;
                data.col = obj.dataset.col;
                data.path = movement_path;
            }
            console.log("submitting move activity");
            console.log(data);
        } else if (activity.type === 'AOE') {
            // Collect all grid cells with the AOE-cell class
            const aoeCells = Array.from(document.querySelectorAll('.AOE-cell, .AOE-and-targeting-cell'));
            console.log(aoeCells);
            data.locations = aoeCells.map(cell => ({
                row: cell.getAttribute('data-row'),
                col: cell.getAttribute('data-col')
            }));
            console.log(data.locations);
        } else if (activity.type === 'singleTarget') {
            // Collect all selected map objects
            data.selectedObjects = currentlySelectedObjects.map(obj => ({
                id: obj.id,
                row: obj.dataset.row,
                col: obj.dataset.col
            }));
            console.log(data.selectedObjects);
        }
        // Set the value as a JSON string
        console.log(JSON.stringify(data));
        document.getElementById(`activity_${i}_data`).value = JSON.stringify(data);
    });
});

/**
 * Clears all existing highlight cells and applies new highlighting based on a shape.
 * @param {HTMLElement} startObjectID - The map object around which to draw the shape.
 * @param {Array<Array<number>>} shape - The list of [row, col] offsets to highlight.
 * @param {string} type - AOE or targeting highlight
 */
function applyHighlightToGrid(highlightIndexes, type) {
    highlightIndexes.forEach(([row, col]) => {
        const targetCell = gridContainer.querySelector(`#gridCell-${row}-${col}`);
        if (targetCell && type == "AOE") {
            // add dual highlight class
            if (targetCell.classList.contains('targeting-cell')) {
                targetCell.classList.add('AOE-and-targeting-cell');
            } else {
                targetCell.classList.add('AOE-cell');
            }
        }
        if (targetCell && type == "targeting") {
            // add dual highlight class
            if (targetCell.classList.contains('AOE-cell')) {
                targetCell.classList.add('AOE-and-targeting-cell');
            } else {
                targetCell.classList.add('targeting-cell');
            }
        }
        if (targetCell && type == "move") {
            targetCell.classList.add('move-cell');
        }
        if (targetCell && type == "path") {
            console.log("adding path highlight to cell:")
            console.log(targetCell.dataset.row)
            console.log(targetCell.dataset.col)
            targetCell.classList.add('path-cell');
        }
    });
    console.log(Array.from(document.querySelectorAll('.AOE-cell')));
}

/**
 * Evaluates a list of activities and highlights the grid accordingly.
 * @param {Array<Object>} activitiesList - The list of activity JSON objects.
 * @param {HTMLElement|null} selectedMapObject - The currently selected map object (null if none).
 */
function updateMapActivities(activitiesList, selectedMapObject) {
    // clear any previous non-path highlights
    const allHighlightedCells = gridContainer.querySelectorAll('.AOE-cell, .targeting-cell, .AOE-and-targeting-cell, .move-cell');
    allHighlightedCells.forEach(cell => {
        cell.classList.remove('AOE-cell', 'targeting-cell', 'AOE-and-targeting-cell', 'move-cell');
    });
    // remove selectable state from all cells
    disableCellSelectionMode();
    // apply highlights, enable cell selection for movement
    for (let i = 0; i < activitiesList.length; i++) {
        if (activitiesList[i].type === 'singleTarget') {
            applyHighlightToGrid(getActionIndexes(executorID, activitiesList[i].shape), "targeting");
        } 
        if (activitiesList[i].type === 'AOE' && selectedMapObject) {
            applyHighlightToGrid(getActionIndexes(selectedMapObject.id, activitiesList[i].shape), "AOE");
        }
        if (activitiesList[i].type === 'move') {
            if (movementsTaken < actionActivities[i].movementsGiven) {
                applyHighlightToGrid(getActionIndexes(executorID, activitiesList[i].shape), "move");
                enableCellSelectionMode(getActionIndexes(executorID, activitiesList[i].shape));
            } else {
                enableCellSelectionMode([prev_movement_coords]);
            }
        }
    }
}

function getActionIndexes(startObjectID, shape) {
    let startRow = 0;
    let startCol = 0;
    let actionIndexes = [];
// create list of indexes to be highlighted/selectable
        // get coords for selected object
    for (let row = 0; row < curGrid.length; row++) {
        for (let col = 0; col < curGrid[row].length; col++) {
            if (curGrid[row][col].objects.includes(startObjectID)) {
                startRow = row;
                startCol = col;
            }
        }
    }
    // activity shape is 9x9 centered at 4,4
    for (let row = startRow - 4; row < startRow + 5; row++) {
        for (let col = startCol - 4; col < startCol + 5; col++) {
            if (JSON.stringify(shape[row - startRow + 4][col - startCol + 4]) == 1) {
                actionIndexes.push([row, col]);
            }
        }
    }
    return actionIndexes;
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
    // update object's dataset for row and col
    obj.dataset.row = row;
    obj.dataset.col = col;
    objectsOnGrid.push(obj);
    makeSelectable(obj, x, y);
}

function updateGridData() {
    const grid = [];
    const curGridRows = encounter.footingMap.length;
    const curGridCols = encounter.footingMap[0].length;
    for (let row = 0; row < curGridRows; row++) {
        grid.push([]);
        for (let col = 0; col < curGridCols; col++) {
            grid[row].push({ objects: [] });
        }
    }

    objectsOnGrid.forEach(obj => {
        const objName = obj.id;
        const row = parseInt(obj.dataset.row);
        const col = parseInt(obj.dataset.col);
        if (!isNaN(row) && !isNaN(col) && grid[row] && grid[row][col]) {
            grid[row][col].objects.push(objName);
        }
    });
    
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
        updateMapActivities(actionActivities, null);
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

function enableCellSelectionMode(selectableIndexes = []) {
    // Remove previous selectable state from all cells
    const allCells = gridContainer.querySelectorAll('.grid-cell');
    allCells.forEach(cell => {
        cell.classList.remove('cell-selectable');
        cell.removeEventListener('click', cellSelectionHandler);
    });

    // Add selectable state only to specified cells
    selectableIndexes.forEach(([row, col]) => {
        const cell = gridContainer.querySelector(`#gridCell-${row}-${col}`);
        if (cell) {
            cell.classList.add('cell-selectable');
            cell.addEventListener('click', cellSelectionHandler);
        }
    });
}

function disableCellSelectionMode() {
    const cells = gridContainer.querySelectorAll('.grid-cell');
    cells.forEach(cell => {
        cell.classList.remove('cell-selectable');
        cell.removeEventListener('click', cellSelectionHandler);
    });
}

function cellSelectionHandler(e) {
    e.stopPropagation();
    const cell = e.currentTarget;
    // Find the object by executorID
    const obj = objectsOnGrid.find(o => o.id === executorID);
    // if clicked cell was a path, retrace step taken. Otherwise, continue path highlighting
    if (cell.classList.contains('path-cell')) {
        cell.classList.remove('path-cell');
        movement_path.pop();
        movementsTaken -= 1;
    } else {
        prev_movement_coords = [obj.dataset.row, obj.dataset.col];
        movement_path.push(prev_movement_coords);
        applyHighlightToGrid([prev_movement_coords], "path");
        enableCellSelectionMode([prev_movement_coords]);
        movementsTaken += 1;
    }
    if (obj) {
        // Get cell's row and col from data attributes
        const row = parseInt(cell.getAttribute('data-row'));
        const col = parseInt(cell.getAttribute('data-col'));
        // Calculate new position
        const snappedX = col * cellSize;
        const snappedY = row * cellSize;
        obj.style.transform = `translate3d(${snappedX}px, ${snappedY}px, 0)`;
        // update object's dataset for row and col
        obj.dataset.row = row;
        obj.dataset.col = col;
        // rerun map utilities
        updateGridData();
        // console.log(curGrid);
        updateMapActivities(actionActivities, null);
    }
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
        updateMapActivities(actionActivities, mostRecentlySelectedObject);
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
        // console.log(`Object ${obj.id} unselected. Total selected: ${currentlySelectedObjects.length}`);
    } else {
        // Object is not selected, select it
        obj.classList.add('selected');
        // Add to the array
        currentlySelectedObjects.push(obj);
        // console.log(`Object ${obj.id} selected. Total selected: ${currentlySelectedObjects.length}`);
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