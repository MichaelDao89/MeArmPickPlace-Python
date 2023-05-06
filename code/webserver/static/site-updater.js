
setInterval(update, 50);
count = 1;

function update() {
    /*console.log('update');*/
    const date = new Date();
    document.getElementById("demo")
        .innerHTML = date.toLocaleTimeString();

    fetch('http://' + window.location.hostname + '/update')
        .then(response => response.text())
        .then(data => {
            //console.log(data);
            const urls = JSON.parse(data);
            document.getElementById('main').src = urls[0];
            document.getElementById('sub1').src = urls[1];
            document.getElementById('sub2').src = urls[2];
            document.getElementById('sub3').src = urls[3];
        });
}
