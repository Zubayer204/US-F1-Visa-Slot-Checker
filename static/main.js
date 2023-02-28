// Get the dialog element
var dialog = document.getElementById("dialog");

// Get the OK button element
var ok = document.getElementById("ok");

// Get the Cancel button element
var cancel = document.getElementById("cancel");

// Hide the dialog when the OK button is clicked
ok.onclick = function() {
    dialog.style.display = "none";
};

// Hide the dialog when the Cancel button is clicked
cancel.onclick = function() {
    dialog.style.display = "none";
};