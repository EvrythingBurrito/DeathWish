let selectedRegionIndex = 0; // Default region
const JSRegionURLS = {{regionURLs|tojson}}; // ignore these errors, not sure what the issue is

function updateSelectedRegionIndex() {
    selectedRegionIndex = document.getElementById('regionSelect').value;
}

function createMap() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    const mapContainer = document.getElementById('map');
    mapContainer.innerHTML = '';

    // save form into browser JSON
    mapData = Array(rows).fill(null).map(() => Array(cols).fill(selectedRegionIndex)); // Initialize map data

    for (let i = 0; i < rows; i++) {
        const row = document.createElement('div');
        row.classList.add('map-row');

        for (let j = 0; j < cols; j++) {
            const cell = document.createElement('button');
            cell.type = 'button' // Important: Prevent form submission
            cell.classList.add('map-cell');
            // cell.textContent = mapData[i][j];
            cell.style.backgroundImage = `url(${JSRegionURLS[mapData[i][j]]})`;

            cell.addEventListener('click', () => {
                // cell.textContent = selectedRegionIndex;
                cell.style.backgroundImage = `url(${JSRegionURLS[selectedRegionIndex]})`
                mapData[i][j] = selectedRegionIndex;
                document.getElementById("map_data").value = JSON.stringify(mapData);
            });
            row.appendChild(cell);
        }

        mapContainer.appendChild(row);
    }
}

createMap();