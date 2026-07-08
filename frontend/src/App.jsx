import { useEffect, useState } from "react";
import { listDocuments } from "./api";
import ChatWindow from "./components/ChatWindow";
import UploadPanel from "./components/UploadPanel";
import styles from "./App.module.css";

export default function App() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    listDocuments()
      .then(setDocuments)
      .catch(() => setDocuments([]));
  }, []);

  function handleUploaded(info) {
    setDocuments((prev) => [...prev, info]);
  }

  return (
    <div className={styles.app}>
      <UploadPanel documents={documents} onUploaded={handleUploaded} />
      <ChatWindow />
    </div>
  );
}
