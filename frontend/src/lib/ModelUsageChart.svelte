<script>
  import { onDestroy } from "svelte";
  import {
    BarController,
    BarElement,
    CategoryScale,
    Chart,
    LinearScale,
    Tooltip,
  } from "chart.js";

  Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip);

  export let modelStats = {};

  let canvas = null;
  let chart = null;
  let sortedEntries = [];

  $: sortedEntries = Object.entries(modelStats ?? {}).sort((first, second) => second[1] - first[1]);

  $: if (canvas) {
    renderChart();
  }

  function renderChart() {
    if (chart) {
      chart.destroy();
      chart = null;
    }

    if (!sortedEntries.length) {
      return;
    }

    chart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: sortedEntries.map(([model]) => model),
        datasets: [
          {
            label: "messages",
            data: sortedEntries.map(([, count]) => count),
            backgroundColor: "rgba(56, 189, 248, 0.85)",
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            displayColors: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0,
            },
            grid: {
              color: "rgba(148, 163, 184, 0.15)",
            },
          },
          x: {
            grid: {
              display: false,
            },
          },
        },
      },
    });
  }

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<section class="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
  <h2 class="text-lg font-semibold text-slate-100">model usage</h2>
  <div class="mt-4 h-72">
    {#if sortedEntries.length > 0}
      <canvas bind:this={canvas}></canvas>
    {:else}
      <p class="text-sm text-slate-400">no model usage found in this export.</p>
    {/if}
  </div>
</section>
