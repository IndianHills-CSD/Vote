// The array of months
var mons = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
];
mons.forEach(printMons);

/**
 * Creates an option tag for each month in the array
 *
 * @param mon represents each month in the array of months
 */
function printMons(mon) {
    var opt = document.createElement("option");
    var text = document.createTextNode(mon);
    var select = document.getElementById("expm");
    opt.appendChild(text);
    opt.setAttribute("value", String(mon));
    select.appendChild(opt);
}

/**
 * Formats the numeric values in the amount input field to two decimal places
 */
function decimals() {
    const amt = document.querySelector("input[name=amt]");

    // Checks if there is any numeric values in the "amt" field
    if (amt.value != "") {
        amt.value = parseFloat(amt.value).toFixed(2);
    }
}