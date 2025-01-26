let selectedRegionIndex = 0; // Default region

function updateSelectedRegionIndex() {
    selectedRegionIndex = document.getElementById('regionSelect').value;
    console.log(selectedRegionIndex);
}

function createMap() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    const mapContainer = document.getElementById('map');
    mapContainer.innerHTML = '';

    // console.log(campaign.regionMapIndexes);
    let mapData = [];
    // save form into browser JSON
    prevRows = campaign.regionMapIndexes.length;

    for (let i = 0; i < rows; i++) {
        const row = document.createElement('div');
        row.classList.add('map-row');
        if (i < prevRows) {
            prevCols = campaign.regionMapIndexes[i].length;
        } else {
            // doesn't matter since row is new anyway
            prevCols = campaign.regionMapIndexes[0].length;
        }
        // console.log(prevCols);
        mapData[i] = [];

        for (let j = 0; j < cols; j++) {
            
            const cell = document.createElement('button');
            cell.type = 'button' // Important: Prevent form submission
            cell.classList.add('map-cell');
            
            // fill new cells with selected region if none existed before
            if (i >= prevRows || j >= prevCols) {
                mapData[i].push(selectedRegionIndex);
            } else {
                // console.log(campaign.regionMapIndexes[i][j]);
                mapData[i].push(campaign.regionMapIndexes[i][j]);
            }
            cell.style.backgroundImage = `url(${regions[mapData[i][j]].worldMapIconFile})`;

            cell.addEventListener('click', () => {
                mapData[i][j] = selectedRegionIndex;
                cell.style.backgroundImage = `url(${regions[mapData[i][j]].worldMapIconFile})`;
                document.getElementById("regionData").value = JSON.stringify(mapData);
            });
            row.appendChild(cell);
        }

        mapContainer.appendChild(row);
    }
    // console.log(mapData);
    document.getElementById("regionData").value = JSON.stringify(mapData);
}