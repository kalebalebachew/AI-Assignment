function submitForm() {
    var notes = document.getElementById("notes").value;

    // Send the notes to the server using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/predict", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var result = JSON.parse(xhr.responseText);
            document.getElementById("result").innerHTML = "<p>Model Prediction: " + result.prediction + "</p>";
        }
    };
    xhr.send(JSON.stringify({ notes: notes }));
}
