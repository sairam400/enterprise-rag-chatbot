import { useRef, useState } from "react";
import { sendMessage } from "../api";
import MessageBubble from "./MessageBubble";
import styles from "./ChatWindow.module.css";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const conversationId = useRef(null);

  async function handleSubmit(event) {
    event.preventDefault();
    const question = input.trim();
    if (!question || busy) return;

    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setInput("");
    setBusy(true);
    setError(null);

    try {
      const result = await sendMessage(question, conversationId.current);
      conversationId.current = result.conversation_id;
      setMessages((prev) => [...prev, { role: "assistant", text: result.answer, sources: result.sources }]);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className={styles.chat}>
      <div className={styles.messages}>
        {messages.length === 0 && (
          <p className={styles.emptyState}>Upload a document, then ask a question about it.</p>
        )}
        {messages.map((message, i) => (
          <MessageBubble key={i} role={message.role} text={message.text} sources={message.sources} />
        ))}
      </div>

      {error && <p className={styles.error}>{error}</p>}

      <form className={styles.form} onSubmit={handleSubmit}>
        <input
          className={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about your documents..."
          disabled={busy}
        />
        <button className={styles.sendButton} type="submit" disabled={busy || !input.trim()}>
          Send
        </button>
      </form>
    </section>
  );
}
