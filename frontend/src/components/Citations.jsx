import styles from "./Citations.module.css";

export default function Citations({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className={styles.citations}>
      <p className={styles.label}>Sources</p>
      <ul className={styles.list}>
        {sources.map((source) => (
          <li key={source.index} className={styles.item}>
            <span className={styles.index}>[{source.index}]</span> {source.source_file}
            {source.page_number ? ` (page ${source.page_number})` : ""}
          </li>
        ))}
      </ul>
    </div>
  );
}
