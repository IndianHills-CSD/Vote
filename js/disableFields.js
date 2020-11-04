/**
 * Disables the credit card fields
 */
function disableCredFields() {
    var sender = document.querySelector("input[name=sender]");
    var ccnum = document.querySelector("input[name=ccnum]");
    var cvv = document.querySelector("input[name=cvv]");
    var expm = document.querySelector("select[name=expm]");
    var expy = document.querySelector("input[name=expy]");

    if (sender.value != "") {
        ccnum.disabled = true;
        cvv.disabled = true;
        expm.disabled = true;
        expy.disabled = true;
    } else {
        ccnum.disabled = false;
        cvv.disabled = false;
        expm.disabled = false;
        expy.disabled = false;
    }
}