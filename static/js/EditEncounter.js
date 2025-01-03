const gridContainer = document.getElementById('grid-container');
const objectPalette = document.getElementById('object-palette');
const gridDataInput = document.getElementById('grid_data');
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
    obj.id = `draggable-object-${nextObjectId++}`;
    obj.classList.add('draggable-object', objectType);
    console.log(objectPicURLs[objectIndex])
    console.log(objectIndex)
    console.log(objectType)
    obj.style.backgroundImage = `url(${objectPicURLs[objectIndex]})`
    obj.style.backgroundRepeat = 'no-repeat'; // Ensure image doesn't repeat
    obj.style.backgroundSize = 'cover'; // Resize image to fit object size
    obj.draggable = true;
    obj.style.position = 'absolute'; // Ensure absolute positioning
    obj.style.left = (col * cellSize) + 'px';
    obj.style.top = (row * cellSize) + 'px';
    gridContainer.appendChild(obj);
    objectsOnGrid.push(obj);
    makeDraggable(obj);
}

function makeDraggable(obj) {
    let isDragging = false;
    let dragOffsetX = 0;
    let dragOffsetY = 0;
    obj.addEventListener('mousedown', dragStart);
    obj.addEventListener('touchstart', dragStart, { passive: false });

    function dragStart(e) {
        e.preventDefault();
        isDragging = true;
        currentObject = obj;
        const gridRect = gridContainer.getBoundingClientRect();
        let touch = e.touches ? e.touches[0] : e;
        let x = touch.clientX - gridRect.left;
        let y = touch.clientY - gridRect.top;
    
        const objRect = obj.getBoundingClientRect();
        dragOffsetX = x - objRect.left; //Simplified offset calculation
        dragOffsetY = y - objRect.top;
    
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
            let touch = e.changedTouches && e.changedTouches.length > 0 ? e.changedTouches[0] : e; // Corrected touch handling
            let x = touch.clientX - gridRect.left;
            let y = touch.clientY - gridRect.top;
    
            x = Math.max(0, Math.min(gridRect.width - currentObject.offsetWidth, x));
            y = Math.max(0, Math.min(gridRect.height - currentObject.offsetHeight, y));
    
            let col = Math.round(x / cellSize);
            let row = Math.round(y / cellSize);
    
            const snappedX = col * cellSize;
            const snappedY = row * cellSize;
    
            currentObject.style.transform = `translate3d(${snappedX}px, ${snappedY}px, 0)`;
            currentObject.style.left = '';
            currentObject.style.top = '';
            currentObject = null;
            updateGridData();
        }
    }
    
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
        const objName = obj.classList[1];

        for (let row = 0; row < 10; row++) {
            for (let col = 0; col < 10; col++) {
                const cellLeft = col * cellSize;
                const cellTop = row * cellSize;
                const cellRight = cellLeft + cellSize;
                const cellBottom = cellTop + cellSize;

                if (!(objRight < cellLeft || objLeft > cellRight || objBottom < cellTop || objTop > cellBottom)) {
                    grid[row][col].objects.push(objName);
                }
            }
        }
    });

    gridDataInput.value = JSON.stringify(grid);
}