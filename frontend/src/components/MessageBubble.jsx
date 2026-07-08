import Citations from "./Citations";
import styles from "./MessageBubble.module.css";

export default function MessageBubble({ role, text, sources }) {
  const isUser = role === "user";

  return (
    <div className={`${styles.row} ${isUser ? styles.rowUser : styles.rowAssistant}`}>
      <div className={`${styles.bubble} ${isUser ? styles.bubbleUser : styles.bubbleAssistant}`}>
        {text}
        {!isUser && <Citations sources={sources} />}
      </div>
    </div>
  );
}
