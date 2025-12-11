document.addEventListener('DOMContentLoaded',function() { //check utility

//timestamp
 const now = new Date();
  document.getElementById("timestamp").textContent =
    "Current time: " + now.toLocaleString();
});