import React, {useState} from "react";
import {createRoot} from "react-dom/client";
import "./style.css";

function App() {
  const [policy, setPolicy] = useState("ALLOW role=analyst\nDENY access_key_age>90\nREQUIRE mfa=true");
  const [report, setReport] = useState(null);
  async function run() {
    const r = await fetch("http://127.0.0.1:8000/reports", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({policy})
    });
    setReport(await r.json());
  }
  return <main>
    <h1>Data Protection Reporting</h1>
    <p>Evaluate identity controls against a reusable policy.</p>
    <textarea value={policy} onChange={e=>setPolicy(e.target.value)} />
    <button onClick={run}>Run report</button>
    {report && <section><h2>{report.passed}/{report.total} identities passed</h2>
      {report.results.map(x=><article key={x.username}>
        <strong>{x.username}</strong>: {x.passed ? "PASS" : "FAIL"}
      </article>)}
    </section>}
  </main>
}
createRoot(document.getElementById("root")).render(<App/>);
