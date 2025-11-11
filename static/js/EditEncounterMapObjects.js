const gridDataInput = document.getElementById('mapObjects');

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
    console.log(obj)
    console.log(objectsOnGrid)
    makeDraggable(obj, x, y);
}

function updateGridData() {
    // (This function remains the same)
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
}

function updateGridFromData(gridData) {
    // Clear existing objects on the grid
    const gridRect = gridContainer.getBoundingClientRect();
    objectsOnGrid.forEach(obj => gridContainer.removeChild(obj));
    objectsOnGrid = [];
    nextObjectId = 0;

    for (let row = 0; row < gridData.length; row++) {
        for (let col = 0; col < gridData[row].length; col++) {
            const cellData = gridData[row][col];
            if (cellData.objects && cellData.objects.length > 0) {
                cellData.objects.forEach(obj => {
                    // Find the index of the object type. The data transferred and the data contained within the grid expects an index, not the name of the object.
                    const objectNameArray = obj.split("-");
                    const objectType = objectNameArray[0];
                    const objectIndex = objectNameArray[1];
                    const x = col * cellSize + gridRect.left;
                    const y = row * cellSize + gridRect.top;
                    createDraggableObject(objectType, objectIndex, x, y);
                });
            }
        }
    }
    updateGridData();
}