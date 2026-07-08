import { useRef, useState } from "react";
import { uploadDocument } from "../api";
import styles from "./UploadPanel.module.css";

export default function UploadPanel({ documents, onUploaded }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  async function handleFileChange(event) {
    const file = event.target.files[0];
    if (!file) return;

    setBusy(true);
    setError(null);
    try {
      const info = await uploadDocument(file);
      onUploaded(info);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
      inputRef.current.value = "";
    }
  }

  return (
    <aside className={styles.panel}>
      <h2 className={styles.heading}>Documents</h2>

      <label className={styles.uploadButton}>
        {busy ? "Uploading..." : "Upload document"}
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt,.md"
          onChange={handleFileChange}
          disabled={busy}
          hidden
        />
      </label>

      {error && <p className={styles.error}>{error}</p>}

      <ul className={styles.list}>
        {documents.map((doc) => (
          <li key={doc.filename} className={styles.item}>
            <span className={styles.filename}>{doc.filename}</span>
            <span className={styles.chunkCount}>{doc.chunks} chunks</span>
          </li>
        ))}
        {documents.length === 0 && <li className={styles.empty}>No documents uploaded yet.</li>}
      </ul>
    </aside>
  );
}
