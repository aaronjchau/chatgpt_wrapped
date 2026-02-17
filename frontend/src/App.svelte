<script>
  import ModelUsageChart from './lib/ModelUsageChart.svelte'

  const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

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
              <ModelUsageChart rows={modelRows} />
            </div>
          {/if}
        </div>
      </section>
    {/if}
  </section>
</main>
