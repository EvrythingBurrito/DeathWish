const gridContainer = document.getElementById('grid-container');
const objectPalette = document.getElementById('object-palette');
const gridDataInput = document.getElementById('mapData');
const cellSize = 50;
let objectsOnGrid = [];
let nextObjectId = 0;
let isDraggingPalette = false; // Flag for palette dragging
let currentPaletteObject = null; // Currently dragged palette object
let paletteOffsetX = 0;
let paletteOffsetY = 0;

function handlePaletteStart(e) {
    e.preventDefault();
    isDraggingPalette = true;
    currentPaletteObject = e.target;
    const rect = currentPaletteObject.getBoundingClientRect();
    if (e.type === 'mousedown') {
        paletteOffsetX = e.clientX - rect.left;
        paletteOffsetY = e.clientY - rect.top;
        window.addEventListener('mouseup', handlePaletteEnd); // Attach to window!
        window.addEventListener('mousemove', handlePaletteMove);
    } else if (e.type === 'touchstart') {
        paletteOffsetX = e.touches[0].clientX - rect.left;
        paletteOffsetY = e.touches[0].clientY - rect.top;
        window.addEventListener('touchend', handlePaletteEnd);
        window.addEventListener('touchmove', handlePaletteMove);
    }
}

function handlePaletteMove(e) {
    if (isDraggingPalette && currentPaletteObject) {
        e.preventDefault();
    }
}

function handlePaletteEnd(e) {
    if (isDraggingPalette && currentPaletteObject) {
        isDraggingPalette = false;
        window.removeEventListener('mouseup', handlePaletteEnd); // Remove listener
        window.removeEventListener('mousemove', handlePaletteMove);
        window.removeEventListener('touchend', handlePaletteEnd);
        window.removeEventListener('touchmove', handlePaletteMove);
        const rect = currentPaletteObject.getBoundingClientRect();
        const data = {
            type: currentPaletteObject.dataset.type,
            index: currentPaletteObject.dataset.index
        };
        const gridRect = gridContainer.getBoundingClientRect();
        let x, y;
        if (e.type === 'mouseup') {
            x = e.clientX;
            y = e.clientY;
        } else if (e.type === 'touchend') {
            if(e.changedTouches.length > 0){
                x = e.changedTouches[0].clientX;
                y = e.changedTouches[0].clientY;
            } else {
                return;
            }
        }
        if (x > gridRect.left && x < gridRect.right && y > gridRect.top && y < gridRect.bottom) {
            createDraggableObject(data.type, data.index, x, y);
            updateGridData();
        }
        currentPaletteObject = null;
    }
}

const paletteObjects = document.querySelectorAll('.palette-object');
paletteObjects.forEach(obj => {
    obj.addEventListener('mousedown', handlePaletteStart);
    obj.addEventListener('touchstart', handlePaletteStart, { passive: false });
});

function createDraggableObject(objectType, objectIndex, x, y) {
    const gridRect = gridContainer.getBoundingClientRect();
    let gridX = x - gridRect.left;
    let gridY = y - gridRect.top;

    let col = Math.floor(gridX / cellSize);
    let row = Math.floor(gridY / cellSize);

    col = Math.max(0, Math.min(9, col));
    row = Math.max(0, Math.min(9, row));

    const obj = document.createElement('div');
    obj.id = `${objectType}-${objectIndex}-${nextObjectId++}`; // each object is the type, type asset index, then an arbitrary id value to differentiate
    obj.classList.add('draggable-object', objectType);
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
    makeDraggable(obj, x, y);
}

function makeDraggable(obj) {
    let isDragging = false;
    let dragOffsetX = 0;
    let dragOffsetY = 0;
    let initialX = 0;
    let initialY = 0;

    function dragStart(e) {
        e.preventDefault();
        isDragging = true;
        currentObject = obj;

        const gridRect = gridContainer.getBoundingClientRect();
        let touch = e.touches ? e.touches[0] : e;
        initialX = touch.clientX - gridRect.left;
        initialY = touch.clientY - gridRect.top;

        const objRect = obj.getBoundingClientRect();
        dragOffsetX = initialX - objRect.left;
        dragOffsetY = initialY - objRect.top;

        // Set initial transform based on the object's initial position
        obj.style.transform = `translate3d(${objRect.left - gridRect.left}px, ${objRect.top - gridRect.top}px, 0)`;

        if (e.type === 'mousedown') {
            window.addEventListener('mousemove', drag);
            window.addEventListener('mouseup', dragEnd);
        } else if (e.type === 'touchstart') {
            window.addEventListener('touchmove', drag, { passive: false });
            window.addEventListener('touchend', dragEnd);
        }
    }

    function drag(e) {
        if (isDragging && currentObject) {
            e.preventDefault();
            const gridRect = gridContainer.getBoundingClientRect();
            let touch = e.touches ? e.touches[0] : e;
            let x = touch.clientX - (2*gridRect.left) - dragOffsetX;
            let y = touch.clientY - (2*gridRect.top) - dragOffsetY;
            x = Math.max(0, Math.min(gridRect.width - currentObject.offsetWidth, x));
            y = Math.max(0, Math.min(gridRect.height - currentObject.offsetHeight, y));
            currentObject.style.transform = `translate3d(${x}px, ${y}px, 0)`;
        }
    }

    function dragEnd(e) {
        if (isDragging && currentObject) {
            isDragging = false;
            window.removeEventListener('mousemove', drag);
            window.removeEventListener('mouseup', dragEnd);
            window.removeEventListener('touchmove', drag);
            window.removeEventListener('touchend', dragEnd);

            const gridRect = gridContainer.getBoundingClientRect();
            let touch = e.changedTouches && e.changedTouches.length > 0 ? e.changedTouches[0] : e;
            let x = touch.clientX - gridRect.left;
            let y = touch.clientY - gridRect.top;

            x = Math.max(0, Math.min(gridRect.width - currentObject.offsetWidth, x));
            y = Math.max(0, Math.min(gridRect.height - currentObject.offsetHeight, y));

            let col = Math.round(x / cellSize);
            let row = Math.round(y / cellSize);

            const snappedX = col * cellSize;
            const snappedY = row * cellSize;

            currentObject.style.transform = `translate3d(${snappedX}px, ${snappedY}px, 0)`;
            currentObject.style.left = ''; // Crucial: Reset left and top
            currentObject.style.top = '';
            currentObject = null;
            updateGridData();
        }
    }

    obj.addEventListener('mousedown', dragStart);
    obj.addEventListener('touchstart', dragStart, { passive: false });
}

function updateGridData() {
    // (This function remains the same)
    const grid = [];
    for (let row = 0; row < 10; row++) {
        grid.push([]);
        for (let col = 0; col < 10; col++) {
            grid[row].push({ objects: [] });
        }
    }

    objectsOnGrid.forEach(obj => {
        const objRect = obj.getBoundingClientRect();
        const gridRect = gridContainer.getBoundingClientRect();
        const objLeft = objRect.left - gridRect.left;
        const objTop = objRect.top - gridRect.top;
        const objRight = objLeft + objRect.width;
        const objBottom = objTop + objRect.height;
        const objName = obj.id;

        for (let row = 0; row < 10; row++) {
            for (let col = 0; col < 10; col++) {
                const cellLeft = col * cellSize;
                const cellTop = row * cellSize;
                const cellRight = cellLeft + cellSize;
                const cellBottom = cellTop + cellSize;

                if ((objRight <= cellRight) && (objLeft >= cellLeft) && (objBottom <= cellBottom) && (objTop >= cellTop)) {
                    grid[row][col].objects.push(objName);
                }
            }
        }
    });
    // console.log(objectsOnGrid.length);
    // console.log(JSON.stringify(grid));
    gridDataInput.value = JSON.stringify(grid);
}

// note: grid cells will also have a dict key called "conditions", which points to a list of active conditions on that cell

function updateGridFromData(gridData) {
    // Clear existing objects on the grid
    const gridRect = gridContainer.getBoundingClientRect();
    objectsOnGrid.forEach(obj => gridContainer.removeChild(obj));
    objectsOnGrid = [];
    nextObjectId = 0;

    for (let row = 0; row < gridData.length; row++) {
        for (let col = 0; col < gridData[row].length; col++) {
            const cellData = gridData[row][col];
            // console.log(cellData);
            if (cellData.objects && cellData.objects.length > 0) {
                cellData.objects.forEach(obj => {
                    // Find the index of the object type. The data transferred and the data contained within the grid expects an index, not the name of the object.
                    const objectNameArray = obj.split("-");
                    const objectType = objectNameArray[0];
                    const objectIndex = objectNameArray[1];
                    const x = col * cellSize + gridRect.left;
                    const y = row * cellSize + gridRect.top;
                    // console.log(objectNameArray);
                    createDraggableObject(objectType, objectIndex, x, y);
                });
            }
        }
    }
    updateGridData();
}