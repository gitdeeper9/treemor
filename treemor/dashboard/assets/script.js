/* TREEMOR Dashboard JavaScript */
console.log("🌲 TREEMOR Dashboard loaded");

// Update status periodically
function updateStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('network-status').innerHTML = 
                `<span class="status-indicator status-${data.status}"></span> ${data.status.toUpperCase()}`;
            document.getElementById('sensor-count').innerText = data.active_sensors;
            document.getElementById('avg-tssi').innerText = data.average_tssi;
            document.getElementById('events-today').innerText = data.events_today;
        })
        .catch(error => console.error('Error:', error));
}

// Refresh every 10 seconds if status elements exist
if (document.getElementById('network-status')) {
    updateStatus();
    setInterval(updateStatus, 10000);
}

// Event handler for detection test
function testDetection() {
    fetch('/api/test-detection', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(`Test detection: ${data.message}`);
        });
}
