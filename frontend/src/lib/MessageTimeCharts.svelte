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

  export let timeStats = {};

  let hourCanvas = null;
  let dayCanvas = null;
  let monthCanvas = null;
  let yearCanvas = null;

  let charts = [];

  $: hourEntries = Object.entries(timeStats?.msgs_sent_by_hour ?? {});
  $: dayEntries = Object.entries(timeStats?.msgs_sent_by_day ?? {});
  $: monthEntries = Object.entries(timeStats?.msgs_sent_by_month ?? {});
  $: yearEntries = Object.entries(timeStats?.msgs_sent_by_year ?? {}).sort(
    (first, second) => Number(first[0]) - Number(second[0])
  );

  $: if (hourCanvas && dayCanvas && monthCanvas && yearCanvas) {
    renderCharts();
  }

  function renderCharts() {
    destroyCharts();

    charts.push(
      makeChart(hourCanvas, "messages by hour", hourEntries, "rgba(14, 165, 233, 0.78)")
    );
    charts.push(
      makeChart(dayCanvas, "messages by day", dayEntries, "rgba(45, 212, 191, 0.78)")
    );
    charts.push(
      makeChart(monthCanvas, "messages by month", monthEntries, "rgba(96, 165, 250, 0.78)")
    );
    charts.push(
      makeChart(yearCanvas, "messages by year", yearEntries, "rgba(52, 211, 153, 0.78)")
    );
  }

  function makeChart(canvas, label, entries, color) {
    if (!canvas) {
      return null;
    }

    return new Chart(canvas, {
      type: "bar",
      data: {
        labels: entries.map(([key]) => key),
        datasets: [
          {
            label: "messages",
            data: entries.map(([, value]) => value),
            backgroundColor: color,
            borderColor: "rgba(148, 163, 184, 0.35)",
            borderWidth: 1,
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: label,
            color: "rgb(226, 232, 240)",
            align: "start",
            font: {
              size: 14,
              weight: "600",
            },
          },
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
              maxRotation: 45,
              minRotation: 0,
            },
            grid: {
              display: false,
            },
          },
        },
      },
    });
  }

  function destroyCharts() {
    for (const chart of charts) {
      if (chart) {
        chart.destroy();
      }
    }
    charts = [];
  }

  onDestroy(() => {
    destroyCharts();
  });
</script>

<section class="rounded-2xl border border-slate-700/70 bg-slate-900/70 p-5 shadow-lg shadow-slate-950/30">
  <h2 class="text-lg font-semibold text-slate-100">message timing</h2>
  <div class="mt-4 grid gap-4 lg:grid-cols-2">
    <div class="rounded-xl border border-slate-800 bg-slate-950/70 p-3">
      <div class="h-60"><canvas bind:this={hourCanvas}></canvas></div>
    </div>
    <div class="rounded-xl border border-slate-800 bg-slate-950/70 p-3">
      <div class="h-60"><canvas bind:this={dayCanvas}></canvas></div>
    </div>
    <div class="rounded-xl border border-slate-800 bg-slate-950/70 p-3">
      <div class="h-60"><canvas bind:this={monthCanvas}></canvas></div>
    </div>
    <div class="rounded-xl border border-slate-800 bg-slate-950/70 p-3">
      <div class="h-60"><canvas bind:this={yearCanvas}></canvas></div>
    </div>
  </div>
</section>
