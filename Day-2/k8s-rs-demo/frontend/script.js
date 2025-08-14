fetch("http://10.100.119.143:8000/api/hello")
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").innerText = data.message;
    })
    .catch(() => {
        document.getElementById("message").innerText = "Error connecting to backend";
    });
