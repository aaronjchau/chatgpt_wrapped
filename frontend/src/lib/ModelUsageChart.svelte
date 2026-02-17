<script>
  import { onMount } from 'svelte'
  import {
    BarController,
    BarElement,
    CategoryScale,
    Chart,
    Legend,
    LinearScale,
    Tooltip,
  } from 'chart.js'

  Chart.register(BarController, BarElement, CategoryScale, LinearScale, Legend, Tooltip)

  let {
    rows = [],
    datasetLabel = 'Messages',
    barColor = '#2dd4bf',
    heightClass = 'h-72',
    axisTickColor = '#cbd5e1',
    gridColor = 'rgba(148, 163, 184, 0.2)',
  } = $props()

  let chart
  let canvas

  function syncChart() {
    if (!chart) {
      return
    }

    chart.data.labels = rows.map(([modelId]) => modelId)
    chart.data.datasets[0].data = rows.map(([, count]) => count)
    chart.data.datasets[0].label = datasetLabel
    chart.data.datasets[0].backgroundColor = barColor
    chart.update()
  }

  onMount(() => {
    chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: [],
        datasets: [
          {
            label: datasetLabel,
            data: [],
            backgroundColor: barColor,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: {
              maxRotation: 45,
              minRotation: 0,
              color: axisTickColor,
            },
            grid: {
              color: gridColor,
            },
          },
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0,
              color: axisTickColor,
            },
            grid: {
              color: gridColor,
            },
          },
        },
      },
    })

    syncChart()

    return () => {
      chart.destroy()
    }
  })

  $effect(() => {
    syncChart()
  })
</script>

<div class={heightClass}>
  <canvas bind:this={canvas}></canvas>
</div>
