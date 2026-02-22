<script>
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

  let selectedFile = null;
  let isImporting = false;
  let errorMessage = "";
  let successMessage = "";
  let importData = null;
  let globalStatsEntries = [];

  const GLOBAL_STAT_LABELS = {
    total_convos: "total conversations",
    total_msgs_sent: "messages sent",
    total_msgs_recd: "messages received",
    total_words_sent: "words sent",
    total_words_recd: "words received",
  };

  function onFileSelected(event) {
    const files = event.currentTarget.files;
    selectedFile = files && files.length > 0 ? files[0] : null;
    errorMessage = "";
    successMessage = "";
    importData = null;
  }

  async function runImport() {
    if (!selectedFile) {
      return;
    }

    isImporting = true;
    errorMessage = "";
    successMessage = "";

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_BASE_URL}/api/v1/import/conversations`, {
        method: "POST",
        body: formData,
      });

      const body = await response.json();

      if (!response.ok) {
        throw new Error(body.detail ?? "Import failed.");
      }

      importData = body;
      successMessage = "Import complete.";
    } catch (error) {
      errorMessage = error?.message ?? "Import failed.";
      importData = null;
    } finally {
      isImporting = false;
    }
  }

  $: globalStatsEntries = importData?.global_stats
    ? Object.entries(importData.global_stats)
    : [];
</script>

<main class="mx-auto min-h-screen max-w-5xl p-6">
  <h1 class="text-3xl font-semibold">chatgpt wrapped</h1>
  <p class="mt-2 text-slate-300">import your conversations.json to load your stats.</p>

  <section class="mt-8 rounded-xl border border-slate-800 bg-slate-900/60 p-4">
    <label class="mb-2 block text-sm font-medium text-slate-200" for="import-file">
      conversations file
    </label>
    <input
      id="import-file"
      class="block w-full cursor-pointer rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100"
      type="file"
      accept=".json,application/json"
      on:change={onFileSelected}
    />

    <button
      class="mt-4 rounded-md bg-sky-500 px-4 py-2 text-sm font-semibold text-slate-950 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-300"
      type="button"
      on:click={runImport}
      disabled={!selectedFile || isImporting}
    >
      {isImporting ? "Importing..." : "Import conversations"}
    </button>

    {#if errorMessage}
      <p class="mt-3 text-sm font-medium text-rose-300">{errorMessage}</p>
    {/if}

    {#if successMessage}
      <p class="mt-3 text-sm font-medium text-emerald-300">{successMessage}</p>
    {/if}

    {#if importData}
      <p class="mt-2 text-xs text-slate-400">
        parsed {importData.meta.messages_parsed} messages from {importData.meta.conversations_received}
        conversations
      </p>
    {/if}
  </section>

  {#if globalStatsEntries.length > 0}
    <section class="mt-6 rounded-xl border border-slate-800 bg-slate-900/60 p-4">
      <h2 class="text-lg font-semibold text-slate-100">global stats</h2>
      <div class="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {#each globalStatsEntries as [key, value]}
          <article class="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
            <p class="text-xs uppercase tracking-wide text-slate-400">{GLOBAL_STAT_LABELS[key] ?? key}</p>
            <p class="mt-1 text-2xl font-semibold text-slate-100">{value}</p>
          </article>
        {/each}
      </div>
    </section>
  {/if}
</main>
