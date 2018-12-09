var totalRowCount = 0;
var rowCount = 0;
var table = document.getElementById("allBookings");
var rows = table.getElementsByTagName("tr");
var wholeString = "";
var partString;

for (var i = 0; i < rows.length; i++) {
	totalRowCount++;
	if (rows[i].getElementsByTagName("td").length > 0) {
		rowCount++
	}
	var message = "Total Row Count: " + totalRowCount;
    message += "\nRow Count: " + rowCount;
}

for (var i = 1; i < totalRowCount; i++){
	partString = i + '<input type="radio" name="choice" value="' + i + '">'
	wholeString = wholeString + partString;
}
document.getElementById('dynamicRadio').innerHTML = wholeString;