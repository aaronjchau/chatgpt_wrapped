<script>
  export let points = [];

  let gridContainer = null;
  let tooltip = null;

  $: maxCount = points.reduce((max, point) => Math.max(max, point.count), 0);
  $: tiles = points.map((point, index) => {
    const date = new Date(`${point.date}T00:00:00Z`);
    const weekday = date.getUTCDay();
    const week = Math.floor(index / 7);
    return {
      ...point,
      weekday,
      week,
    };
  });

  function formatDate(dateLabel) {
    return new Date(`${dateLabel}T00:00:00Z`).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      timeZone: "UTC",
    });
  }

  function tileColor(count) {
    if (count === 0 || maxCount === 0) {
      return "bg-slate-800";
    }

    const intensity = count / maxCount;
    if (intensity < 0.25) {
      return "bg-emerald-900";
    }
    if (intensity < 0.5) {
      return "bg-emerald-700";
    }
    if (intensity < 0.75) {
      return "bg-emerald-500";
    }
    return "bg-emerald-300";
  }

  function showTooltip(event, tile) {
    if (!gridContainer) {
      return;
    }

    const rect = gridContainer.getBoundingClientRect();
    tooltip = {
      x: event.clientX - rect.left + 12,
      y: event.clientY - rect.top - 18,
      text: `${tile.count} messages on ${formatDate(tile.date)}`,
    };
  }

  function hideTooltip() {
    tooltip = null;
  }
</script>

<section class="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
  <h2 class="text-lg font-semibold text-slate-100">rolling 12-month activity</h2>

  {#if tiles.length > 0}
    <div class="mt-4 overflow-x-auto">
      <div class="relative" bind:this={gridContainer}>
        <div
          class="grid min-w-[780px] grid-rows-7 gap-1"
          style="grid-template-columns: repeat(53, minmax(0, 1fr));"
        >
        {#each tiles as tile}
          <button
            type="button"
            aria-label={`${tile.count} messages on ${formatDate(tile.date)}`}
            class={`h-3 w-3 rounded-[3px] transition-transform hover:scale-125 ${tileColor(tile.count)}`}
            style={`grid-column: ${tile.week + 1}; grid-row: ${tile.weekday + 1};`}
            on:mouseenter={(event) => showTooltip(event, tile)}
            on:mousemove={(event) => showTooltip(event, tile)}
            on:mouseleave={hideTooltip}
            on:focus={(event) => showTooltip(event, tile)}
            on:blur={hideTooltip}
          ></button>
        {/each}
        </div>

        {#if tooltip}
          <div
            class="pointer-events-none absolute z-10 rounded-md border border-slate-700 bg-slate-950/95 px-2 py-1 text-xs text-slate-100 shadow-lg"
            style={`left: ${tooltip.x}px; top: ${tooltip.y}px;`}
          >
            {tooltip.text}
          </div>
        {/if}
      </div>
    </div>
    <div class="mt-3 flex items-center gap-2 text-xs text-slate-400">
      <span>less</span>
      <span class="h-3 w-3 rounded-[3px] bg-slate-800"></span>
      <span class="h-3 w-3 rounded-[3px] bg-emerald-900"></span>
      <span class="h-3 w-3 rounded-[3px] bg-emerald-700"></span>
      <span class="h-3 w-3 rounded-[3px] bg-emerald-500"></span>
      <span class="h-3 w-3 rounded-[3px] bg-emerald-300"></span>
      <span>more</span>
    </div>
  {:else}
    <p class="mt-3 text-sm text-slate-400">no daily activity data found.</p>
  {/if}
</section>
