<script>
  import ModelUsageChart from './lib/ModelUsageChart.svelte'
  import RollingHeatmap from './lib/RollingHeatmap.svelte'

  const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
  const dayOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const monthOrder = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ]

  let file = null
  let isLoading = false
  let error = ''
  let result = null

  $: selectedFileName = file?.name ?? 'No file selected'
  $: canImport = Boolean(file) && !isLoading
  $: globalRows = result ? Object.entries(result.global_stats) : []
  $: modelRows = result
    ? Object.entries(result.model_stats).sort(([, a], [, b]) => b - a)
    : []
  $: timeStats = result?.time_stats ?? null
  $: hourRows = timeStats
    ? Array.from({ length: 24 }, (_, hour) => [
        `${String(hour).padStart(2, '0')}:00`,
        timeStats.msgs_sent_by_hour?.[String(hour)] ?? 0,
      ])
    : []
  $: dayRows = timeStats
    ? dayOrder.map((dayName) => [dayName.slice(0, 3), timeStats.msgs_sent_by_day?.[dayName] ?? 0])
    : []
  $: monthRows = timeStats
    ? monthOrder.map((monthName) => [monthName.slice(0, 3), timeStats.msgs_sent_by_month?.[monthName] ?? 0])
    : []
  $: rolling12Months = timeStats?.rolling_12_months ?? null
  $: rollingDailyRows = rolling12Months?.daily_counts ?? []

  function onFileChange(event) {
    file = event.currentTarget.files?.[0] ?? null
  }

  async function onSubmit(event) {
    event.preventDefault()

    if (!file) {
      error = 'Please choose conversations.json first.'
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    isLoading = true
    error = ''

    try {
      const response = await fetch(`${apiBase}/api/v1/import/conversations`, {
        method: 'POST',
        body: formData,
      })
      const payload = await response.json()

      if (!response.ok) {
        throw new Error(payload?.detail ?? 'Import failed.')
      }

      result = payload
    } catch (importError) {
      result = null
      error = importError instanceof Error ? importError.message : 'Import failed.'
    } finally {
      isLoading = false
    }
  }
</script>

<main class="min-h-screen bg-slate-100 px-4 py-12 text-slate-900">
  <section class="mx-auto w-full max-w-5xl rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
    <h1 class="text-2xl font-semibold">ChatGPT Wrapped</h1>
    <p class="mt-2 text-sm text-slate-600">Import your local conversations export and analyze it on localhost.</p>

    <form on:submit={onSubmit} class="mt-6 space-y-3">
      <div class="space-y-2">
        <label for="file" class="text-sm font-medium text-slate-700">conversations.json</label>
        <input
          id="file"
          type="file"
          accept=".json,application/json"
          class="block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm"
          on:change={onFileChange}
        />
        <p class="text-sm text-slate-600">{selectedFileName}</p>
      </div>

      <button
        type="submit"
        disabled={!canImport}
        class="rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isLoading ? 'Analyzing...' : 'Import + Analyze'}
      </button>
    </form>

    {#if error}
      <p class="mt-4 text-sm font-semibold text-red-700">{error}</p>
    {/if}

    {#if result}
      <p class="mt-4 text-sm font-semibold text-emerald-700">Import complete. Results loaded.</p>

      <section class="mt-8 space-y-8">
        <div>
          <h2 class="text-lg font-semibold">Global Stats</h2>
          <div class="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {#each globalRows as [key, value]}
              <article class="rounded-lg border border-slate-200 bg-slate-50 p-3">
                <p class="text-xs uppercase tracking-wide text-slate-500">{key}</p>
                <p class="mt-1 text-xl font-semibold text-slate-900">{value.toLocaleString()}</p>
              </article>
            {/each}
          </div>
        </div>

        <div>
          <h2 class="text-lg font-semibold">Model Usage</h2>
          {#if modelRows.length === 0}
            <p class="mt-3 text-sm text-slate-600">No model stats found.</p>
          {:else}
            <div class="mt-3 rounded-lg border border-slate-200 bg-white p-3">
              <ModelUsageChart rows={modelRows} datasetLabel="Assistant messages" />
            </div>
          {/if}
        </div>

        <div>
          <h2 class="text-lg font-semibold">Message Timing (UTC)</h2>
          {#if !timeStats}
            <p class="mt-3 text-sm text-slate-600">No time stats found.</p>
          {:else}
            <div class="mt-3 grid gap-4 lg:grid-cols-3">
              <article class="rounded-lg border border-slate-200 bg-white p-3">
                <h3 class="text-sm font-semibold text-slate-700">By Hour of Day</h3>
                <div class="mt-2">
                  <ModelUsageChart
                    rows={hourRows}
                    datasetLabel="Messages sent"
                    barColor="#0f766e"
                    heightClass="h-56"
                  />
                </div>
              </article>

              <article class="rounded-lg border border-slate-200 bg-white p-3">
                <h3 class="text-sm font-semibold text-slate-700">By Day of Week</h3>
                <div class="mt-2">
                  <ModelUsageChart
                    rows={dayRows}
                    datasetLabel="Messages sent"
                    barColor="#0f766e"
                    heightClass="h-56"
                  />
                </div>
              </article>

              <article class="rounded-lg border border-slate-200 bg-white p-3">
                <h3 class="text-sm font-semibold text-slate-700">By Month of Year</h3>
                <div class="mt-2">
                  <ModelUsageChart
                    rows={monthRows}
                    datasetLabel="Messages sent"
                    barColor="#0f766e"
                    heightClass="h-56"
                  />
                </div>
              </article>
            </div>

            <article class="mt-4 rounded-lg border border-slate-200 bg-white p-3">
              <h3 class="text-sm font-semibold text-slate-700">Rolling 12-Month Heatmap (GitHub Style)</h3>
              {#if rolling12Months?.start_date && rolling12Months?.end_date}
                <p class="mt-1 text-xs text-slate-500">
                  {rolling12Months.start_date} to {rolling12Months.end_date}
                </p>
              {/if}
              <div class="mt-3">
                <RollingHeatmap days={rollingDailyRows} />
              </div>
            </article>
          {/if}
        </div>
      </section>
    {/if}
  </section>
</main>
