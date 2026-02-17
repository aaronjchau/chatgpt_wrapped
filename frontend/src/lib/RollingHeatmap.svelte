<script>
  let { days = [] } = $props()

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
      return '#e2e8f0'
    }

    if (maxCount <= 1) {
      return '#0f766e'
    }

    const ratio = count / maxCount
    if (ratio <= 0.25) {
      return '#99f6e4'
    }
    if (ratio <= 0.5) {
      return '#5eead4'
    }
    if (ratio <= 0.75) {
      return '#14b8a6'
    }

    return '#0f766e'
  }

  function tooltip(day) {
    if (!day) {
      return ''
    }

    const noun = day.count === 1 ? 'message' : 'messages'
    return `${day.date}: ${day.count} ${noun}`
  }

  const weeks = $derived(buildWeeks(days))
  const maxCount = $derived(
    days.reduce((maxValue, day) => Math.max(maxValue, Number(day.count) || 0), 0)
  )
</script>

{#if weeks.length === 0}
  <p class="text-sm text-slate-600">No rolling heatmap data found.</p>
{:else}
  <div class="overflow-x-auto">
    <div class="inline-flex gap-1">
      {#each weeks as week}
        <div class="flex flex-col gap-1">
          {#each week as day}
            {#if day}
              <div
                class="h-3 w-3 rounded-sm transition-transform hover:scale-125 cursor-pointer"
                style={`background-color: ${cellColor(day.count, maxCount)}`}
                title={tooltip(day)}
              ></div>
            {:else}
              <div class="h-3 w-3 rounded-sm bg-transparent"></div>
            {/if}
          {/each}
        </div>
      {/each}
    </div>
  </div>

  <div class="mt-3 flex items-center gap-1 text-xs text-slate-500">
    <span class="mr-1">Less</span>
    <span class="h-3 w-3 rounded-sm bg-slate-200"></span>
    <span class="h-3 w-3 rounded-sm bg-teal-200"></span>
    <span class="h-3 w-3 rounded-sm bg-teal-300"></span>
    <span class="h-3 w-3 rounded-sm bg-teal-500"></span>
    <span class="h-3 w-3 rounded-sm bg-teal-700"></span>
    <span class="ml-1">More</span>
  </div>
{/if}
