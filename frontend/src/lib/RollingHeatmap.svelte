<script>
  let { days = [] } = $props()
  let hoverText = $state('')
  let hoverVisible = $state(false)
  let hoverX = $state(0)
  let hoverY = $state(0)
  let wrapper = $state(null)

  function parseDate(dateString) {
    const [year, month, day] = dateString.split('-').map(Number)
    return new Date(Date.UTC(year, month - 1, day))
  }

  function mondayIndex(date) {
    const weekday = date.getUTCDay()
    if (weekday === 0) {
      return 6
    }
    return weekday - 1
  }

  function buildWeeks(daySeries) {
    if (!daySeries.length) {
      return []
    }

    const firstDate = parseDate(daySeries[0].date)
    const leadingBlanks = mondayIndex(firstDate)
    const paddedDays = Array(leadingBlanks).fill(null)

    for (const day of daySeries) {
      paddedDays.push({
        date: day.date,
        count: Number(day.count) || 0,
      })
    }

    while (paddedDays.length % 7 !== 0) {
      paddedDays.push(null)
    }

    const weekColumns = []
    for (let index = 0; index < paddedDays.length; index += 7) {
      weekColumns.push(paddedDays.slice(index, index + 7))
    }

    return weekColumns
  }

  function cellColor(count, maxCount) {
    if (count === null) {
      return 'transparent'
    }

    if (count === 0) {
      return '#1e293b'
    }

    if (maxCount <= 1) {
      return '#14b8a6'
    }

    const ratio = count / maxCount
    if (ratio <= 0.25) {
      return '#134e4a'
    }
    if (ratio <= 0.5) {
      return '#0f766e'
    }
    if (ratio <= 0.75) {
      return '#14b8a6'
    }

    return '#5eead4'
  }

  function tooltip(day) {
    if (!day) {
      return ''
    }

    const noun = day.count === 1 ? 'message' : 'messages'
    return `${day.date}: ${day.count} ${noun}`
  }

  function setTooltipPosition(event) {
    if (!wrapper) {
      return
    }

    const rect = wrapper.getBoundingClientRect()
    hoverX = event.clientX - rect.left + 14
    hoverY = event.clientY - rect.top - 12
  }

  function showTooltip(event, day) {
    hoverText = tooltip(day)
    hoverVisible = Boolean(hoverText)
    setTooltipPosition(event)
  }

  function moveTooltip(event) {
    if (!hoverVisible) {
      return
    }

    setTooltipPosition(event)
  }

  function hideTooltip() {
    hoverVisible = false
    hoverText = ''
  }

  const weeks = $derived(buildWeeks(days))
  const maxCount = $derived(
    days.reduce((maxValue, day) => Math.max(maxValue, Number(day.count) || 0), 0)
  )
</script>

{#if weeks.length === 0}
  <p class="text-sm text-slate-400">No rolling heatmap data found.</p>
{:else}
  <div class="relative overflow-x-auto" bind:this={wrapper}>
    {#if hoverVisible}
      <div
        class="pointer-events-none absolute z-10 rounded-md border border-slate-600 bg-slate-800 px-2 py-1 text-xs text-slate-100 shadow-lg"
        style={`left:${hoverX}px; top:${hoverY}px; transform: translate(-50%, -100%);`}
      >
        {hoverText}
      </div>
    {/if}

    <div class="inline-flex gap-1 py-1">
      {#each weeks as week}
        <div class="flex flex-col gap-1">
          {#each week as day}
            {#if day}
              <button
                type="button"
                aria-label={tooltip(day)}
                class="h-3 w-3 rounded-sm border-0 p-0 transition-transform hover:scale-125 cursor-pointer"
                style={`background-color: ${cellColor(day.count, maxCount)}`}
                title={tooltip(day)}
                onmouseenter={(event) => showTooltip(event, day)}
                onmousemove={moveTooltip}
                onmouseleave={hideTooltip}
              ></button>
            {:else}
              <div class="h-3 w-3 rounded-sm bg-transparent"></div>
            {/if}
          {/each}
        </div>
      {/each}
    </div>
  </div>

  <div class="mt-3 flex items-center gap-1 text-xs text-slate-400">
    <span class="mr-1">Less</span>
    <span class="h-3 w-3 rounded-sm bg-slate-800"></span>
    <span class="h-3 w-3 rounded-sm bg-teal-900"></span>
    <span class="h-3 w-3 rounded-sm bg-teal-700"></span>
    <span class="h-3 w-3 rounded-sm bg-teal-500"></span>
    <span class="h-3 w-3 rounded-sm bg-teal-300"></span>
    <span class="ml-1">More</span>
  </div>
{/if}
