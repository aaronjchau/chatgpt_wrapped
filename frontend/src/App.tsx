import { DragEvent, FormEvent, useMemo, useState } from "react";

type UploadResult = {
  global_stats: Record<string, number>;
  conversation_stats: Record<string, Record<string, number>>;
  model_stats: Record<string, number>;
  meta?: Record<string, number>;
};

const apiBase = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);

  const canUpload = useMemo(() => Boolean(file) && !isLoading, [file, isLoading]);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!file) {
      setError("Please choose conversations.json first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiBase}/api/v1/upload/conversations`, {
        method: "POST",
        body: formData,
      });
      const payload = (await response.json()) as UploadResult | { detail?: string };

      if (!response.ok) {
        const detail = "detail" in payload ? payload.detail : undefined;
        throw new Error(detail ?? "Upload failed.");
      }

      setResult(payload as UploadResult);
    } catch (uploadError) {
      setResult(null);
      setError(uploadError instanceof Error ? uploadError.message : "Upload failed.");
    } finally {
      setIsLoading(false);
    }
  };

  const onDropFile = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files?.[0] ?? null;
    setFile(droppedFile);
  };

  const selectedFileName = file?.name ?? "No file selected";

  return (
    <main className="app-shell">
      <section className="panel">
        <h1>ChatGPT Wrapped</h1>
        <p>Upload your local conversations export and analyze it on localhost.</p>

        <form onSubmit={onSubmit} className="upload-form">
          <label
            htmlFor="file"
            className="drop-zone"
            onDragOver={(event) => event.preventDefault()}
            onDrop={onDropFile}
          >
            <span className="label">Drag + drop conversations.json here</span>
            <span className="sub-label">or click to choose file</span>
          </label>
          <input
            id="file"
            type="file"
            accept=".json,application/json"
            className="hidden-file-input"
            onChange={(event) => {
              const selected = event.target.files?.[0] ?? null;
              setFile(selected);
            }}
          />
          <p className="selected-file">{selectedFileName}</p>

          <button type="submit" disabled={!canUpload}>
            {isLoading ? "Analyzing..." : "Upload + Analyze"}
          </button>
        </form>

        {error ? <p className="error">{error}</p> : null}
        {result ? <p className="ok">Upload complete. Results loaded.</p> : null}

        {result ? <ResultsPanel result={result} /> : null}
      </section>
    </main>
  );
}

function ResultsPanel({ result }: { result: UploadResult }) {
  const modelRows = Object.entries(result.model_stats);
  const conversationRows = Object.entries(result.conversation_stats);
  const maxModelValue = Math.max(...modelRows.map(([, count]) => count), 1);

  return (
    <section className="results">
      <h2>Global Stats</h2>
      <div className="global-grid">
        {Object.entries(result.global_stats).map(([key, value]) => (
          <article key={key} className="stat-card">
            <p className="stat-key">{key}</p>
            <p className="stat-value">{value.toLocaleString()}</p>
          </article>
        ))}
      </div>

      <h2>Model Usage</h2>
      <div className="model-list">
        {modelRows.length === 0 ? <p>No model stats found.</p> : null}
        {modelRows.map(([modelId, count]) => {
          const widthPercent = Math.max(8, Math.round((count / maxModelValue) * 100));
          return (
            <div key={modelId} className="model-row">
              <span>{modelId}</span>
              <div className="bar-wrap">
                <div className="bar-fill" style={{ width: `${widthPercent}%` }} />
              </div>
              <strong>{count}</strong>
            </div>
          );
        })}
      </div>

      <h2>Conversation Stats</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Conversation ID</th>
              <th>Msgs Sent</th>
              <th>Words Sent</th>
              <th>Msgs Recd</th>
              <th>Words Recd</th>
            </tr>
          </thead>
          <tbody>
            {conversationRows.slice(0, 25).map(([conversationId, stats]) => (
              <tr key={conversationId}>
                <td>{conversationId}</td>
                <td>{stats.convo_msgs_sent ?? 0}</td>
                <td>{stats.convo_words_sent ?? 0}</td>
                <td>{stats.convo_msgs_recd ?? 0}</td>
                <td>{stats.convo_words_recd ?? 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {conversationRows.length > 25 ? (
        <p className="sub-label">Showing first 25 conversations.</p>
      ) : null}
    </section>
  );
}
