document.addEventListener('DOMContentLoaded',function() {


    //pie chart
  const xValues = [".txt", ".py", ".pdf", ".jpg"];
  const yValues = [{{percent_txt_placholder}},{{percent_py_placholder}},{{percent_pdf_placholder}},{{percent_jpg_placholder}}];  
  const barColors = [
  "#E3E3E3",
  "#456882",
  "#234C6A",
  "#1B3C53"
  ];

  const ctx = document.getElementById('pie_chart');

  new Chart(ctx, {
  type: "pie",
  data: {
      labels: xValues,
      datasets: [{
      backgroundColor: barColors,
      data: yValues
      }]
  },
  options: {
      plugins: {
      legend: {display:true},
      title: {
          display: true,
          text: "Pourcentage des fichiers dans le dossier",
          font: {size:16}
      }
      }
  }
  });

  //timestamp
  const now = new Date();
  document.getElementById("timestamp").textContent =
  "Dernière Mise a jour : " + now.toLocaleString();

});