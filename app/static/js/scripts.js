
function toolShow(id, data) {
    var tooltip = document.getElementById('tooltip'); 
    tooltip.style.display = 'block';
    tooltip.innerHTML = `<h5>${data["name"]}</h5>${data["num_available"]} of ${data["num_machines"]} machines available<br><i>Click for more</i>`;

}

function toolHide() {
    var tooltip = document.getElementById('tooltip');
    tooltip.style.display = 'none';
    tooltip.innerHTML = '';
}

async function getLocationData(locationId) {

    const url = `/location/${locationId}/location_data`;
    try {
        const response = await fetch(url, { credentials: 'same-origin' });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data);
        toolShow(locationId, data);
    } 
    catch (error) {
        console.log("ERROR");
        console.error(error.message);
    }
}

document.addEventListener('mousemove', function(e){
    document.getElementById('tooltip').style.left = (e.pageX+5)+"px";
    document.getElementById('tooltip').style.top = (e.pageY+5)+"px";
    
});