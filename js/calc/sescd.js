
function httpGetAsync(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            document.getElementById("result").innerHTML = xmlHttp.responseText;
    }
    xmlHttp.open("GET", theUrl, true);
    xmlHttp.send(null);
}

function send_v1_request() {
    ti_length = parseFloat(document.getElementById('TI_length').value)
    total_length = parseFloat(document.getElementById('total_length').value)
    crp_level = parseFloat(document.getElementById('CRP').value)
    fc_level = parseFloat(document.getElementById('FC').value)

    input_data = {'ti_length': ti_length, 'total_length': total_length, 'crp_level': crp_level, 'fc_level': fc_level};

    fetch("https://tcml-scales-website.herokuapp.com/v1/calculate", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input_data)
    })
        .then(response => response.text())
        .then(res => {
            console.log(res);
            document.getElementById("result_output").innerHTML = res;
        });

}
