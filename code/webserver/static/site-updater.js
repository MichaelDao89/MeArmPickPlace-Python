
setInterval(update, 50);
count = 1;

function update() {
    /*console.log('update');*/
    const date = new Date();
    document.getElementById("demo")
        .innerHTML = date.toLocaleTimeString();

    // Update images
    fetch('http://' + window.location.hostname + '/get-images-links')
        .then(response => response.text())
        .then(data => {
            //console.log(data);
            const urls = JSON.parse(data);
            document.getElementById('main').src = urls[0];
            document.getElementById('sub1').src = urls[1];
            document.getElementById('sub2').src = urls[2];
            document.getElementById('sub3').src = urls[3];
        });

    // Update log
    fetch('http://' + window.location.hostname + '/get-log')
        .then(response => response.text())
        .then(data => {
            const log = JSON.parse(data);
            document.getElementById('log').innerHTML = log;
        });
}
