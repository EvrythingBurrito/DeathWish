let selectedFootingIndex = 0; // Default footing

function updateSelectedFootingIndex() {
    selectedFootingIndex = document.getElementById('footingSelect').value;
    console.log(selectedFootingIndex);
}

function createMap() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    const mapContainer = document.getElementById('map');
    mapContainer.innerHTML = '';

    // console.log(encounter.footingMapIndexes);
    let mapData = [];
    // save form into browser JSON
    prevRows = encounter.footingMapIndexes.length;

    for (let i = 0; i < rows; i++) {
        const row = document.createElement('div');
        row.classList.add('map-row');
        if (i < prevRows) {
            prevCols = encounter.footingMapIndexes[i].length;
        } else {
            // doesn't matter since row is new anyway
            prevCols = encounter.footingMapIndexes[0].length;
        }
        // console.log(prevCols);
        mapData[i] = [];

        for (let j = 0; j < cols; j++) {
            const cell = document.createElement('button');
            cell.type = 'button' // Important: Prevent form submission
            cell.classList.add('map-cell');
            
            // fill new cells with selected footing if none existed before
            if (i >= prevRows || j >= prevCols) {
                mapData[i].push(selectedFootingIndex);
            } else {
                // console.log(encounter.footingMapIndexes[i][j]);
                mapData[i].push(encounter.footingMapIndexes[i][j]);
            }
            cell.style.backgroundImage = `url(${footings[mapData[i][j]].mapIconFile})`;

            cell.addEventListener('click', () => {
                mapData[i][j] = selectedFootingIndex;
                cell.style.backgroundImage = `url(${footings[mapData[i][j]].mapIconFile})`;
                document.getElementById("footingData").value = JSON.stringify(mapData);
            });
            row.appendChild(cell);
        }

        mapContainer.appendChild(row);
    }
    // console.log(mapData);
    document.getElementById("footingData").value = JSON.stringify(mapData);
}