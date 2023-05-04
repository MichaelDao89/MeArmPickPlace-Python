
setInterval(update, 100);

count = 1;

function update() {
    /*console.log('update');*/
    const date = new Date();
    document.getElementById("demo")
        .innerHTML = date.toLocaleTimeString();
    /*console.log(window.location.hostname)*/

    //flaskRoute = 'http://' + window.location.hostname + '/update';
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

    //fetch(flaskRoute)
    //    .then(response => response.json())
    //    .then(data => {
    //        document.getElementById('output').textContent = data;
    //        console.log(data);
    //    })
    //    .catch(error => console.log(error));

    //fetch(flaskRoute)
    //    .then(response => response.blob())
    //    .then(blob => {
    //        const url = URL.createObjectURL(blob);
    //        document.getElementById('myImage').src = url;
    //    })
}
