
function openPopupCharge(charge,id) {
    const popup_charge = document.getElementById('popup_charge');
    const overlay = document.getElementById('overlay');
    const chargeRangeInput = document.getElementById('ChargeRange');
    const vehicleIdInput = document.getElementById('vehicleID');
    chargeRangeInput.value = charge;
    vehicleIdInput.value = id;
    popup_charge.style.display = 'block';
    overlay.style.display = 'block';
}

function openPopupRepair(vehicleId) {
    const popup_repair = document.getElementById('popup_repair');
    const overlay = document.getElementById('overlay');

    fetch(`/operater/vehicle/repair?vehicleId=${vehicleId}`)
       .then(response => response.json())
       .then(data => {
            // 将返回的信息存储到变量中
           if (data.error) {
                console.error(data.error);
                alert(data.error);
                return;
            }
            const malfunctionType = data.malfunctionType;
            const reportDate = data.reportDate;
            const customerId = data.customerId;
            const vehicleId = data.vehicleId
            const description = data.description;
            const operator = data.operator;
            const fixed = data.Fixed;
            const repairDate = data.repairDate;
            document.getElementById('reportedDate').value = new Date(reportDate).toISOString().slice(0, -8);
            document.getElementById('malfunctionType').value = malfunctionType;
            document.getElementById('customer').value = customerId;
            document.getElementById('vehicle').value = vehicleId;
            document.getElementById('description').value = description;
            document.getElementById('operator').value = operator;
            document.getElementById('Fixed').checked = fixed;
            if (repairDate) {
                document.getElementById('repairDate').value = new Date(repairDate).toISOString().slice(0, -8);
            }
            popup_repair.style.display = 'block';
            overlay.style.display = 'block';
        })
       .catch(error => {
            console.error('Error fetching repair data:', error);
            alert('Error fetching repair data:', error);
        });


}

function openPopupMove(vehicleId) {
    const popup_move = document.getElementById('popup_move');
    const overlay = document.getElementById('overlay');

    fetch(`/operater/vehicle/move?vehicleId=${vehicleId}`)
       .then(response => response.json())
       .then(data => {
            const locationId = data.locationId;
            const locationList = data.locationList;
            const locationName = data.locationName
            document.getElementById('currentLocationId').value = locationId;
            document.getElementById('currentLocationName').value = locationName;
            document.getElementById('vehicleId').value = vehicleId;

            const moveToSelect = document.getElementById('move_to');
            moveToSelect.innerHTML = '';
            locationList.forEach(location => {
                const option = document.createElement('option');
                option.value = location.id;
                option.textContent = location.locationName;
                moveToSelect.appendChild(option);
            });

            popup_move.style.display = 'block';
            overlay.style.display = 'block';
        })
       .catch(error => console.error('Error fetching move move data:', error));

}



function Closebtn() {
    const popup_charge = document.getElementById('popup_charge');
    const popup_repair = document.getElementById('popup_repair');
    const popup_move = document.getElementById('popup_move');
    const overlay = document.getElementById('overlay');
    popup_charge.style.display = 'none';
    popup_repair.style.display = 'none';
    popup_move.style.display = 'none';
    overlay.style.display = 'none';
}
