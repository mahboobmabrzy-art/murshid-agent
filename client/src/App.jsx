import React, { useState } from "react";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "https://api.example.com";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [resp, setResp] = useState(null);
  const [projectId, setProjectId] = useState("");
  const [token, setToken] = useState(localStorage.getItem("murshid_token") || "dev-token");

  async function send() {
    try {
      const r = await axios.post(
        `${API_BASE}/ask`,
        { project_id: projectId || null, prompt, context: {} },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResp(r.data);
    } catch (e) {
      setResp({ error: e.response?.data || e.message });
    }
  }

  return (
    <div className="container">
      <h1>مُرشد</h1>
      <div className="card">
        <label>معرّف المشروع (اختياري)</label>
        <input value={projectId} onChange={(e) => setProjectId(e.target.value)} />
        <label>أدخل طلبك</label>
        <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={4} />
        <div style={{display:"flex", gap:8}}>
          <button onClick={send}>أرسل</button>
          <input placeholder="Token (dev-token)" value={token} onChange={(e)=>{setToken(e.target.value); localStorage.setItem("murshid_token", e.target.value)}} />
        </div>
      </div>

      <div className="card">
        <h3>النتيجة</h3>
        <pre>{resp ? JSON.stringify(resp, null, 2) : "لا توجد نتيجة بعد"}</pre>
      </div>
    </div>
  );
}
