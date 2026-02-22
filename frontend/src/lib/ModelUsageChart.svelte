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
            backgroundColor: "rgba(14, 165, 233, 0.75)",
            borderColor: "rgba(56, 189, 248, 1)",
            borderWidth: 1,
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
            backgroundColor: "rgba(15, 23, 42, 0.98)",
            borderColor: "rgba(51, 65, 85, 0.9)",
            borderWidth: 1,
            titleColor: "rgb(248, 250, 252)",
            bodyColor: "rgb(226, 232, 240)",
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0,
              color: "rgb(148, 163, 184)",
            },
            grid: {
              color: "rgba(71, 85, 105, 0.3)",
            },
          },
          x: {
            ticks: {
              color: "rgb(148, 163, 184)",
            },
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

<section class="rounded-2xl border border-slate-700/70 bg-slate-900/70 p-5 shadow-lg shadow-slate-950/30">
  <h2 class="text-lg font-semibold text-slate-100">model usage</h2>
  <div class="mt-4 h-72">
    {#if sortedEntries.length > 0}
      <canvas bind:this={canvas}></canvas>
    {:else}
      <p class="text-sm text-slate-400">no model usage found in this export.</p>
    {/if}
  </div>
</section>
