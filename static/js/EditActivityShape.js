let selectedRegionIndex = 0; // Default region

function createMap() {
    const rows = 9;
    const cols = 9;
    const mapContainer = document.getElementById('map');
    mapContainer.innerHTML = '';

    let mapData = [];
    // save form into browser JSON

    for (let i = 0; i < rows; i++) {
        const row = document.createElement('div');
        row.classList.add('map-row');
        mapData[i] = [];

        for (let j = 0; j < cols; j++) {
            const cell = document.createElement('button');
            cell.type = 'button' // Important: Prevent form submission
            cell.classList.add('map-cell');
            
            // initialize map with object values
            mapData[i][j] = activity.shape[i][j];
            
            if (mapData[i][j] == 1) {
                cell.style.backgroundColor = 'rgb(119,45,45)'; // red
            } else {
                cell.style.backgroundColor = 'rgb(220,220,220)'; // grey
            }

            // highlight origin square
            if ((i == 4) && (j == 4)) {
                cell.style.border = '6px solid black';
            }
            
            cell.addEventListener('click', () => {
                // toggle value
                if (mapData[i][j] == 1) {
                    mapData[i][j] = 0;
                    cell.style.backgroundColor = 'rgb(220,220,220)'; // grey
                } else {
                    mapData[i][j] = 1;
                    cell.style.backgroundColor = 'rgb(119,45,45)'; // red
                }
                document.getElementById("shapeData").value = JSON.stringify(mapData);
            });
            row.appendChild(cell);
        }
        mapContainer.appendChild(row);
    }
    document.getElementById("shapeData").value = JSON.stringify(mapData);
}