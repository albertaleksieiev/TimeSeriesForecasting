
function submitForm() {
    const asset = document.getElementById('asset').value;
    const from_period = document.getElementById('from_period').value;
    const to_period = document.getElementById('to_period').value;
    const interval = document.getElementById('interval').value; // Get the selected interval
    const lenprediction = document.getElementById('lenprediction').value;

    const data = { asset, from_period, to_period, interval, lenprediction };

    fetch('/generate-plot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        const plotImage = document.getElementById('plotImage');
        plotImage.src = 'data:image/png;base64,' + data.image;
        plotImage.style.display = 'block';
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


document.addEventListener('DOMContentLoaded', function () {
    // Get today's date

    document.getElementById("interval").value = "15m";

    // Or, select the option by index (zero-based)
    document.getElementById("interval").selectedIndex = 4;

    document.getElementById('from_period').value = '2024-03-17';
     document.getElementById('to_period').value = '2024-03-19';
    //
    // // Set the values of the inputs
    // document.getElementById('from_period').value = formatDate(twentyDaysBefore);
    // document.getElementById('to_period').value = formatDate(nextDay);
});