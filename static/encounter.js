const gridContainer = document.getElementById('grid-container');
const objectPalette = document.getElementById('object-palette');
const gridDataInput = document.getElementById('grid_data');
const cellSize = 50;
let objectsOnGrid = [];
let nextObjectId = 0;

objectPalette.addEventListener('dragstart', (e) => {
    e.dataTransfer.setData('text/plain', e.target.dataset.type);
});

gridContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
});

gridContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    const objectType = e.dataTransfer.getData('text/plain');
    createDraggableObject(objectType, e.clientX, e.clientY);
});

function createDraggableObject(objectType, x, y) {
    const gridRect = gridContainer.getBoundingClientRect();
    const obj = document.createElement('div');
    obj.id = `draggable-object-${nextObjectId++}`;
    obj.classList.add('draggable-object', objectType);
    obj.draggable = true;
    obj.style.left = (x - gridRect.left -50) + 'px';
    obj.style.top = (y - gridRect.top - 50) + 'px';
    gridContainer.appendChild(obj);
    objectsOnGrid.push(obj);
    makeDraggable(obj);
}

function makeDraggable(obj) {
    let initialX;
    let initialY;
    let xOffset = parseInt(obj.style.left) || 0;
    let yOffset = parseInt(obj.style.top) || 0;

    obj.addEventListener('dragstart', (e) => {
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;
    });

    obj.addEventListener('drag', (e) => {
        if (e.clientX && e.clientY) {
            xOffset = e.clientX - initialX;
            yOffset = e.clientY - initialY;
            obj.style.left = xOffset + 'px';
            obj.style.top = yOffset + 'px';
        }
    });
    obj.addEventListener('dragend', updateGridData);
}

function updateGridData() {
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
        const objName = obj.classList[1]; // Get the object type

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

gridContainer.addEventListener('drop', updateGridData);