import { useState } from "react";

const API = "http://127.0.0.1:9000";

export default function App() {
  const [registerData, setRegisterData] = useState(null);
  const [sendResult, setSendResult] = useState(null);
  const [receiveResult, setReceiveResult] = useState(null);

  const [senderId, setSenderId] = useState("");
  const [receiverId, setReceiverId] = useState("");
  const [message, setMessage] = useState("");

  const [receiveUserId, setReceiveUserId] = useState("");
  const [messageId, setMessageId] = useState("");

  const registerUser = async () => {
    const res = await fetch(`${API}/register-user`, {
      method: "POST"
    });
    const data = await res.json();
    setRegisterData(data);
  };

  const sendMessage = async () => {
    const res = await fetch(`${API}/send-message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sender_id: senderId,
        receiver_id: receiverId,
        message: message
      })
    });
    const data = await res.json();
    setSendResult(data);
  };

  const receiveMessage = async () => {
    const res = await fetch(`${API}/receive-message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: receiveUserId,
        message_id: messageId
      })
    });
    const data = await res.json();
    setReceiveResult(data);
  };

  return (
    <div style={styles.container}>
      <h1>Secure Messaging with Blockchain Integrity</h1>

      <section style={styles.section}>
        <h2>Register User</h2>
        <button onClick={registerUser}>Register</button>
        {registerData && (
          <pre>{JSON.stringify(registerData, null, 2)}</pre>
        )}
      </section>

      <section style={styles.section}>
        <h2>Send Message</h2>
        <input placeholder="Sender ID" value={senderId} onChange={e => setSenderId(e.target.value)} />
        <input placeholder="Receiver ID" value={receiverId} onChange={e => setReceiverId(e.target.value)} />
        <input placeholder="Message" value={message} onChange={e => setMessage(e.target.value)} />
        <button onClick={sendMessage}>Send</button>
        {sendResult && (
          <pre>{JSON.stringify(sendResult, null, 2)}</pre>
        )}
      </section>

      <section style={styles.section}>
        <h2>Receive Message</h2>
        <input placeholder="User ID" value={receiveUserId} onChange={e => setReceiveUserId(e.target.value)} />
        <input placeholder="Message ID" value={messageId} onChange={e => setMessageId(e.target.value)} />
        <button onClick={receiveMessage}>Receive</button>
        {receiveResult && (
          <pre>{JSON.stringify(receiveResult, null, 2)}</pre>
        )}
      </section>
    </div>
  );
}

const styles = {
  container: {
    fontFamily: "Arial",
    maxWidth: "800px",
    margin: "40px auto",
    padding: "20px"
  },
  section: {
    marginBottom: "40px",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "8px"
  }
};
