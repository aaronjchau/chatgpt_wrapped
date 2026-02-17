import { FormEvent, useMemo, useState } from "react";

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
      const payload = await response.json();

      if (!response.ok) {
        throw new Error(payload.detail ?? "Upload failed.");
      }

      setResult(payload);
    } catch (uploadError) {
      setResult(null);
      setError(uploadError instanceof Error ? uploadError.message : "Upload failed.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="app-shell">
      <section className="panel">
        <h1>ChatGPT Wrapped</h1>
        <p>Upload your local conversations export and analyze it on localhost.</p>

        <form onSubmit={onSubmit} className="upload-form">
          <label htmlFor="file" className="label">
            conversations.json
          </label>
          <input
            id="file"
            type="file"
            accept=".json,application/json"
            onChange={(event) => {
              const selected = event.target.files?.[0] ?? null;
              setFile(selected);
            }}
          />

          <button type="submit" disabled={!canUpload}>
            {isLoading ? "Analyzing..." : "Upload + Analyze"}
          </button>
        </form>

        {error ? <p className="error">{error}</p> : null}
        {result ? <p className="ok">Upload complete. Results loaded.</p> : null}
      </section>
    </main>
  );
}
