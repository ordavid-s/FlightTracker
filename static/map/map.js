let map = L.map('map').setView([51.505, -0.09], 13);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: 'Esri'
}).addTo(map);

let netMarkers = [];
let constantMarkers = [];

function heatMapColorValue(value){
    let h = (1.0 - value) * 240
    return "hsl(" + h + ", 100%, 50%)";
}

function addRssiCircle(data, markerGroup, border=false, color="", radius=300, opacity=0.5) {
    if(color === ""){
        color = heatMapColorValue(Math.min(30/Math.abs(data['rssi']), 1));
    }
    let circle = L.circle(data['location'], {
        stroke: border,
        color: 'black',
        fillColor: color,
        fillOpacity: opacity,
        radius: radius
    });
    circle.bindPopup(`${data['ssid']}  ||  ${data['bssid']}  ||  ${data['rssi']}dbm`);
    markerGroup.push(circle);
    circle.addTo(map);
}

function drawPath(pathData, markerGroup){
    let line = L.polyline(pathData, {
        color: 'blue'
    })
    markerGroup.push(line);
    line.addTo(map);
}

function handleConstantsKeyValue(key, value){
    if(key === "flightPath"){
        drawPath(value, constantMarkers);
    } else if(key === "problem"){
        value.forEach((singlePointInfo)=>{
            addRssiCircle(singlePointInfo, constantMarkers, true);
        })

    } else if(key === "dvr"){
        value.forEach((singlePointInfo)=>{
            addRssiCircle(singlePointInfo, constantMarkers, true);
        })
    } else if(key === "targets"){
        value.forEach((singlePointInfo)=>{
            addRssiCircle(singlePointInfo, constantMarkers, true, 'red', 100, 1.0);
        })
    }
}

function updateNetworks() {
    const formData = new FormData(document.getElementById('networks-form'));
    fetch('/update_networks',
        {
            method: 'POST',
            body: formData
        }
    ).then(async (res) => {
        let ans = await res.json();
        netMarkers.forEach((circ)=>{
            map.removeLayer(circ);
        })
        for(const netInfo of Object.values(ans)){
            netInfo.forEach((singlePointInfo)=>{
                addRssiCircle(singlePointInfo, netMarkers);
            })
        }
    }).catch((res) => {
        console.log(res);
    })
}


function updateConstants() {
    const formData = new FormData(document.getElementById('constants-form'));
    fetch('/update_constants',
        {
            method: 'POST',
            body: formData
        }
    ).then(async (res) => {
        let ans = await res.json();
        // remove constant markers
        constantMarkers.forEach((circ)=>{
            map.removeLayer(circ);
        })
        // add all marked constants
        for(const [key, value] of Object.entries(ans)){
            handleConstantsKeyValue(key, value);
        }
    }).catch((res) => {
        console.log(res);
    })
}