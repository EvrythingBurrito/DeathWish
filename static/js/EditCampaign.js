let selectedRegionIndex = 0; // Default region

function updateSelectedRegionIndex() {
    selectedRegionIndex = document.getElementById('regionSelect').value;
}

function createMap() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    const mapContainer = document.getElementById('map');
    mapContainer.innerHTML = '';

    // save form into browser JSON
    mapData = mapDataOriginal

    for (let i = 0; i < rows; i++) {
        const row = document.createElement('div');
        row.classList.add('map-row');

        for (let j = 0; j < cols; j++) {
            const cell = document.createElement('button');
            cell.type = 'button' // Important: Prevent form submission
            cell.classList.add('map-cell');
            // cell.textContent = mapData[i][j];
            cell.style.backgroundImage = `url(${regions[mapData[i][j]].worldMapIconFile})`;

            cell.addEventListener('click', () => {
                // cell.textContent = selectedRegionIndex;
                mapData[i][j] = selectedRegionIndex;
                cell.style.backgroundImage = `url(${regions[mapData[i][j]].worldMapIconFile})`;
                document.getElementById("map_data").value = JSON.stringify(mapData);
            });
            row.appendChild(cell);
        }

        mapContainer.appendChild(row);
    }
}