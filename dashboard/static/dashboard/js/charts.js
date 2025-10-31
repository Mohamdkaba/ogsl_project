document.addEventListener("DOMContentLoaded", function () {
  // === 1️⃣ Graphique "Jeux de données par source" ===
  const ctxSource = document.getElementById("datasetsChart");

  fetch("/dashboard/data/datasets_by_source/")
    .then((response) => response.json())
    .then((data) => {
      const chartData = {
        labels: data.labels,
        datasets: [
          {
            label: "Nombre de jeux de données par source",
            data: data.counts,
            backgroundColor: [
              "#007bff",
              "#ffc107",
              "#28a745",
              "#dc3545",
              "#6f42c1",
            ],
          },
        ],
      };

      new Chart(ctxSource, {
        type: "bar",
        data: chartData,
        options: {
          responsive: true,
          plugins: { legend: { display: true } },
          scales: { y: { beginAtZero: true } },
        },
      });
    })
    .catch((error) =>
      console.error("Erreur lors du chargement des données :", error)
    );

  // === 2️⃣ Graphique "Jeux de données par thème" ===
  const ctxTheme = document.getElementById("datasetsByThemeChart");
  let datasetsByThemeChart = null; // 👈 Important : variable globale

  async function loadThemeChart(url = "/dashboard/datasets-by-theme/") {
    try {
      const response = await fetch(url);
      const data = await response.json();

      const labels = data.map((item) => item.theme);
      const counts = data.map((item) => item.count);

      // 💥 Si un graphique existe déjà, on le détruit avant de recréer
      if (
        datasetsByThemeChart &&
        typeof datasetsByThemeChart.destroy === "function"
      ) {
        datasetsByThemeChart.destroy();
        datasetsByThemeChart = null; // On le vide explicitement
      }

      // 🎨 Création du graphique à partir du canvas existant
      datasetsByThemeChart = new Chart(ctxTheme.getContext("2d"), {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Nombre de jeux de données par thème",
              data: counts,
              backgroundColor: [
                "#17a2b8",
                "#20c997",
                "#6610f2",
                "#e83e8c",
                "#fd7e14",
              ],
            },
          ],
        },
        options: {
          responsive: true,
          animation: {
            duration: 600, // petite animation douce
          },
          plugins: {
            legend: { display: true },
          },
          scales: {
            y: { beginAtZero: true },
          },
        },
      });
    } catch (error) {
      console.error("Erreur lors du chargement des données par thème :", error);
    }
  }

  // Chargement initial du graphique "par thème"
  loadThemeChart();

  // === 3️⃣ Filtre dynamique par source ===
  const sourceFilter = document.getElementById("sourceFilter");

  if (sourceFilter) {
    sourceFilter.addEventListener("change", function () {
      const sourceId = this.value;
      const url = sourceId
        ? `/dashboard/data/datasets_by_theme_filtered/${sourceId}/`
        : `/dashboard/datasets-by-theme/`;
      loadThemeChart(url);
    });
  }
});
