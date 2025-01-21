function rentVehicle(locationId) {
    window.location.href = `/customer/rent_vehicle?locationId=${locationId}`;
}

function openPopupReturn(vehicleId) {
    const popup_move = document.getElementById('popup_return');
    const overlay = document.getElementById('overlay');

    fetch(`/customer/return_vehicle?vehicleId=${vehicleId}`)
        .then(response => response.json())
        .then(data => {
            const locationId = data.locationId;
            const locationList = data.locationList;
            const locationName = data.locationName
            document.getElementById('vehicleId').value = vehicleId;

            const moveToSelect = document.getElementById('move_to');
            moveToSelect.innerHTML = '';
            locationList.forEach(location => {
                const option = document.createElement('option');
                option.value = location.id;
                option.textContent = `${location.id} - ${location.locationName}`;
                moveToSelect.appendChild(option);
            });

            popup_move.style.display = 'block';
            overlay.style.display = 'block';
        })
        .catch(error => console.error('Error fetching move move data:', error));
}

function openPopupReport(vehicleId) {
    const popup_report = document.getElementById('popup_report');
    const overlay = document.getElementById('overlay');
    const vehicle = document.getElementById('vehicle');
    vehicle.value = vehicleId;

    popup_report.style.display = 'block';
    overlay.style.display = 'block';
}

function Closebtn() {
    const popup_report = document.getElementById('popup_report');
    const popup_return = document.getElementById('popup_return');
    const overlay = document.getElementById('overlay');
    popup_report.style.display = 'none';
    popup_return.style.display = 'none';
    overlay.style.display = 'none';
}
