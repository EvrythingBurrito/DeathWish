const gridContainer = document.getElementById('grid-container');
const objectPalette = document.getElementById('object-palette');
const cellSize = 50;
let objectsOnGrid = [];
let nextObjectId = 0;
let isDraggingPalette = false; // Flag for palette dragging
let currentPaletteObject = null; // Currently dragged palette object
let paletteOffsetX = 0;
let paletteOffsetY = 0;
let isDragging = false;
let currentObject = null;
let dragOffsetX = 0;
let dragOffsetY = 0;

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
            type: mapObjects[currentPaletteObject.dataset.index].type,
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
            console.log(data.type);
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

// Get reference to the trash area
const trashArea = document.getElementById('trash-area');

// Example objectTypes (ensure this global is defined, often from Jinja)
// For testing purposes, you might define it globally here if not from Jinja:
// const objectTypes = ['red_block', 'blue_circle', 'green_triangle'];

// Event listeners for the trash area
trashArea.addEventListener('dragover', (e) => {
    e.preventDefault(); // Allow drop
    trashArea.classList.add('drag-over'); // Visual feedback
});

trashArea.addEventListener('dragleave', () => {
    trashArea.classList.remove('drag-over'); // Remove visual feedback
});

trashArea.addEventListener('drop', (e) => {
    e.preventDefault();
    trashArea.classList.remove('drag-over');

    // This part handles drops from the palette *onto the trash*.
    // If you only want to delete existing objects, you might remove this.
    // However, it's good practice to handle it.
    try {
        const data = JSON.parse(e.dataTransfer.getData('application/json'));
        console.log(`Palette object '${data.type}' dropped into trash. Not adding to grid.`);
        // No action needed, object from palette is simply not added to grid.
    } catch (error) {
        // This catch block would handle existing objects being dropped,
        // but we'll manage that through the makeDraggable dragEnd below for simplicity.
        console.warn("Attempted to drop non-palette data or existing object onto trash via standard drop event.");
    }
});

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
        // Corrected offset calculation to be relative to the object's top-left within its current visual position
        dragOffsetX = touch.clientX - objRect.left;
        dragOffsetY = touch.clientY - objRect.top;

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
            // Calculate new position relative to grid based on mouse/touch and initial click offset
            let x = touch.clientX - gridRect.left - dragOffsetX;
            let y = touch.clientY - gridRect.top - dragOffsetY;

            // Keep object within grid bounds during drag (optional if dragging to trash)
            // If you want to allow it to go slightly outside before dropping in trash,
            // you could comment this out or adjust the boundary.
            // x = Math.max(0, Math.min(gridRect.width - currentObject.offsetWidth, x));
            // y = Math.max(0, Math.min(gridRect.height - currentObject.offsetHeight, y));

            currentObject.style.transform = `translate3d(${x}px, ${y}px, 0)`;
        }
    }

    function dragEnd(e) {
        if (!isDragging || !currentObject) return; // Ensure we're actually dragging an object

        isDragging = false;
        // Remove event listeners from window
        window.removeEventListener('mousemove', drag);
        window.removeEventListener('mouseup', dragEnd);
        window.removeEventListener('touchmove', drag);
        window.removeEventListener('touchend', dragEnd);

        const gridRect = gridContainer.getBoundingClientRect();
        const trashRect = trashArea.getBoundingClientRect(); // Get trash area bounds

        let dropX, dropY;
        if (e.type === 'mouseup') {
            dropX = e.clientX;
            dropY = e.clientY;
        } else if (e.type === 'touchend') {
            if (e.changedTouches.length === 0) return; // No touch points, exit
            dropX = e.changedTouches[0].clientX;
            dropY = e.changedTouches[0].clientY;
        } else {
            return; // Unknown event type
        }

        // Check if dropped into trash area
        if (dropX > trashRect.left && dropX < trashRect.right &&
            dropY > trashRect.top && dropY < trashRect.bottom) {
            // REMOVE OBJECT LOGIC
            gridContainer.removeChild(currentObject); // Remove from DOM
            objectsOnGrid = objectsOnGrid.filter(obj => obj.id !== currentObject.id); // Remove from array
            updateGridData(); // Update hidden input
            console.log(`Object ${currentObject.id} deleted.`);
        } else {
            // Snap to grid (existing logic)
            let x = dropX - gridRect.left;
            let y = dropY - gridRect.top;

            x = Math.max(0, Math.min(gridRect.width - currentObject.offsetWidth, x));
            y = Math.max(0, Math.min(gridRect.height - currentObject.offsetHeight, y));

            let col = Math.round(x / cellSize);
            let row = Math.round(y / cellSize);

            const snappedX = col * cellSize;
            const snappedY = row * cellSize;

            currentObject.style.transform = `translate3d(${snappedX}px, ${snappedY}px, 0)`;
            currentObject.style.left = ''; // Reset left and top
            currentObject.style.top = '';
            updateGridData(); // Update hidden input
        }

        currentObject = null; // Reset current dragged object
    }

    // Attach initial mousedown/touchstart listeners to the object itself
    obj.addEventListener('mousedown', dragStart);
    obj.addEventListener('touchstart', dragStart, { passive: false });
}