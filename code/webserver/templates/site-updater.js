console.log('hello');
setInterval(update, 500);

function update() {
    console.log('update');
    const date = new Date();
    document.getElementById("demo")
        .innerHTML = date.toLocaleTimeString();

    document.get("/update", )

    fetch('http://172.19.49.52/update')
        .then(response => response.json())
        .then(data => {
            document.getElementById('output').textContent = data;
            console.log(data);
        })
        .catch(error => console.log(error));
}
