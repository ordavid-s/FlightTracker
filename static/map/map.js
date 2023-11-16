let map = L.map('map').setView([51.505, -0.09], 13);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: 'Esri'
}).addTo(map);

let markers = [];

function addRssiCircle(data) {
    let circle = L.circle(data['location'], {
        color: 'blue',
        fillColor: 'blue',
        fillOpacity: Math.min(30/Math.abs(data['rssi']), 1),
        radius: 300
    });
    circle.bindPopup(`${data['ssid']}  ||  ${data['bssid']}  ||  ${data['rssi']}dbm`);
    markers.push(circle);
    circle.addTo(map);
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
        markers.forEach((circ)=>{
            map.removeLayer(circ);
        })
        for(const netInfo of Object.values(ans)){
            netInfo.forEach((singlePointInfo)=>{
                addRssiCircle(singlePointInfo);
            })
        }
    }).catch((res) => {
        console.log(res);
    })

}