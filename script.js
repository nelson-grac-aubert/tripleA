document.addEventListener('DOMContentLoaded',function() {

//gauge ram
// Options de la jauge //not used
var options = {
    angle: 0.15,
    lineWidth: 0.44,
    radiusScale: 1,
    pointer: {
        length: 0.6,
        strokeWidth: 0.035,
        color: '#000000'
    },
    staticLabels: {
        font: "12px sans-serif",
        labels: [0, 20, 40, 60, 80, 100],
        fractionDigits: 0,
        color:'#fbfefe'
    },
    staticZones: [
        {strokeStyle: "#30B32D", min: 0, max: 50},
        {strokeStyle: "#FFDD00", min: 50, max: 80},
        {strokeStyle: "#F03E3E", min: 80, max: 100}
    ],
    highDpiSupport: true
};

// Initialisation de la jauge
var target = document.getElementById('gauge_ram');
var gauge = new Gauge(target).setOptions(options);


// Configuration des limites
gauge.maxValue = 100;
gauge.setMinValue(0);

// Valeur initiale
gauge.set(80);



//gauge cpu //not used 
var opts = {
  angle: 0.35, // The span of the gauge arc
  lineWidth: 0.1, // The line thickness
  radiusScale: 1, // Relative radius
  pointer: {
    length: 0.6, // Relative to gauge radius
    strokeWidth: 0.035, // The thickness
    color: '#000000' // Fill color
    
  },
  limitMax: false,     // If false, max value increases automatically if value > maxValue
  limitMin: false,     // If true, the min value of the gauge will be fixed
  colorStart: '#6F6EA0',   // Colors
  colorStop: '#2a2d41',    // just experiment with them
  strokeColor: '#EEEEEE',  // to see which ones work best for you
  generateGradient: true,
  highDpiSupport: true,     // High resolution support
  
};

var target = document.getElementById('gauge_percent'); // your canvas element
var gauge = new Donut(target).setOptions(opts); // create sexy gauge!

gauge.maxValue = 100; // set max gauge value
gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
gauge.animationSpeed = 32; // set animation speed (32 is default value)
gauge.set(50); // set actual value

//barchart not used in script.js
  const ctx = document.getElementById('bar_chart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });







//timestamp
 const now = new Date();
  document.getElementById("timestamp").textContent =
    "Current time: " + now.toLocaleString();
});