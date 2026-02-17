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

  let { rows = [] } = $props()

  let chart
  let canvas

  function syncChart() {
    if (!chart) {
      return
    }

    chart.data.labels = rows.map(([modelId]) => modelId)
    chart.data.datasets[0].data = rows.map(([, count]) => count)
    chart.update()
  }

  onMount(() => {
    chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: [],
        datasets: [
          {
            label: 'Messages',
            data: [],
            backgroundColor: '#0f172a',
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
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0,
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

<div class="h-72">
  <canvas bind:this={canvas}></canvas>
</div>
