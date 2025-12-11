document.addEventListener('DOMContentLoaded',function() { 

//timestamp
 const now = new Date();
  document.getElementById("timestamp").textContent =
    "Current time: " + now.toLocaleString();
});
