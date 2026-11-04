/**
 * KrishiMitra - Charts Component (Chart.js)
 * Visual analytics for farmer dashboard and mandi price movements.
 */

function initDashboardCharts(healthCounts, cropAcres) {
  // 1. Crop Health Doughnut Chart
  const healthCtx = document.getElementById('cropHealthChart');
  if (healthCtx && window.Chart) {
    new Chart(healthCtx, {
      type: 'doughnut',
      data: {
        labels: ['Healthy', 'At Risk', 'Diseased'],
        datasets: [{
          data: [
            healthCounts.healthy || 0,
            healthCounts.at_risk || 0,
            healthCounts.diseased || 0
          ],
          backgroundColor: [
            '#22c55e', // Green
            '#eab308', // Amber
            '#ef4444'  // Red
          ],
          borderWidth: 2,
          borderColor: '#ffffff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              padding: 14,
              font: { size: 12 }
            }
          }
        },
        cutout: '70%'
      }
    });
  }

  // 2. Crop Cultivation Area Bar Chart
  const acresCtx = document.getElementById('cropAcresChart');
  if (acresCtx && window.Chart && cropAcres) {
    const labels = Object.keys(cropAcres);
    const data = Object.values(cropAcres);

    new Chart(acresCtx, {
      type: 'bar',
      data: {
        labels: labels.length ? labels : ['No Crops Added'],
        datasets: [{
          label: 'Acres Cultivated',
          data: data.length ? data : [0],
          backgroundColor: '#2e7d32',
          borderRadius: 6,
          maxBarThickness: 36
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Acres',
              font: { size: 11 }
            },
            grid: { color: '#f1f5f9' }
          },
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }
}


function initMandiTrendsChart(trendsData) {
  const trendCtx = document.getElementById('mandiTrendChart');
  if (!trendCtx || !window.Chart || !trendsData) return;

  new Chart(trendCtx, {
    type: 'line',
    data: {
      labels: trendsData.months,
      datasets: [
        {
          label: 'Cotton (Kapas) Rs/Qtl',
          data: trendsData.cotton,
          borderColor: '#2e7d32',
          backgroundColor: 'rgba(46, 125, 50, 0.08)',
          borderWidth: 2.5,
          tension: 0.35,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6
        },
        {
          label: 'Paddy (Dhan) Rs/Qtl',
          data: trendsData.paddy,
          borderColor: '#0284c7',
          backgroundColor: 'transparent',
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 4
        },
        {
          label: 'Maize Rs/Qtl',
          data: trendsData.maize,
          borderColor: '#f59e0b',
          backgroundColor: 'transparent',
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.35,
          pointRadius: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            boxWidth: 14,
            usePointStyle: true,
            font: { size: 12 }
          }
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              return `${context.dataset.label}: ₹${context.parsed.y.toLocaleString('en-IN')}`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: '#f1f5f9' },
          ticks: {
            callback: function (val) {
              return '₹' + val;
            }
          }
        },
        x: {
          grid: { display: false }
        }
      }
    }
  });
}
