import React, { useRef, useState } from "react";
import aditya from "./assets/team/aditya.jpg";
import anubhav from "./assets/team/anubhav.jpg";
import ashish from "./assets/team/ashish.jpg";
import ayush from "./assets/team/ayush.jpg";
import priyanshu from "./assets/team/priyanshu.jpg";
import srishti from "./assets/team/srishti.jpg";

const API = process.env.REACT_APP_API_URL || "";
const accept = { image: "image/jpeg,image/png,image/webp", video: "video/mp4,video/quicktime,video/webm,video/x-msvideo", audio: "audio/mpeg,audio/wav,audio/flac,audio/ogg" };
const team = [
  ["Ayush", ayush], ["Aditya", aditya], ["Anubhav", anubhav],
  ["Ashish", ashish], ["Priyanshu", priyanshu], ["Srishti", srishti],
];

function UploadWorkspace() {
  const [kind, setKind] = useState("image"); const [file, setFile] = useState();
  const [result, setResult] = useState(); const [error, setError] = useState("");
  const [busy, setBusy] = useState(false); const [feedback, setFeedback] = useState(""); const input = useRef();
  async function analyze(event) {
    event.preventDefault(); if (!file) return setError("Select a file before starting analysis.");
    setBusy(true); setError(""); setResult(); const body = new FormData(); body.append("file", file);
    try {
      const response = await fetch(`${API}/api/analyze/${kind}`, { method: "POST", body }); const job = await response.json();
      if (!response.ok) throw new Error(job.error?.message || "Analysis failed.");
      let current;
      for (let attempt = 0; attempt < 120; attempt += 1) {
        await new Promise(resolve => setTimeout(resolve, 1000)); const status = await fetch(`${API}${job.status_url}`); current = await status.json();
        if (!status.ok) throw new Error(current.error?.message || "Analysis failed."); if (["completed", "failed"].includes(current.status)) break;
      }
      if (!current || current.status !== "completed") throw new Error(current?.error_code ? "Analysis could not be completed." : "Analysis is still queued. Please check back shortly.");
      setResult(current);
    } catch (err) { setError(err.message); } finally { setBusy(false); }
  }
  async function sendFeedback(claim) {
    const response = await fetch(`${API}/api/analysis/${result.id}/feedback`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ claim }) });
    setFeedback(response.ok ? "Thanks — your feedback is submitted for review, not treated as a verified label." : "We could not submit feedback. Please try again.");
  }
  return <section className="workspace" id="analyze"><div className="section-wrap"><div className="eyebrow">Analysis workspace</div><h2>Start with the evidence.</h2><p>Uploads are validated before forensic checks. A detector result appears only when a validated model is configured.</p><form onSubmit={analyze} className="upload-card"><div className="tabs" role="tablist">{["image", "video", "audio"].map(type => <button type="button" role="tab" aria-selected={kind === type} className={kind === type ? "selected" : ""} onClick={() => { setKind(type); setFile(); setResult(); }} key={type}>{type}</button>)}</div><label className="dropzone" onDragOver={event => event.preventDefault()} onDrop={event => { event.preventDefault(); setFile(event.dataTransfer.files[0]); }}><input ref={input} type="file" accept={accept[kind]} onChange={event => setFile(event.target.files[0])}/><span>{file ? file.name : `Drop a ${kind} here or choose a file`}</span><small>{kind === "image" ? "JPEG, PNG, or WebP · up to 25 MB" : "Validated locally by the API · up to 250 MB"}</small></label>{error && <p className="error" role="alert">{error}</p>}<button className="primary" disabled={busy}>{busy ? "Queued / processing…" : "Analyze media"}</button></form>{result && <article className="report" aria-live="polite"><div><div className="eyebrow">Assessment</div><h3>{result.assessment === "inconclusive" ? "Inconclusive" : result.assessment}</h3><p>No calibrated detection model is available on this deployment, so no synthetic-media probability has been reported.</p></div><dl><div><dt>Media hash</dt><dd className="hash">{result.sha256}</dd></div><div><dt>Analysis ID</dt><dd>{result.id}</dd></div><div><dt>Evidence</dt><dd>{result.report.forensic_signals.dimensions ? `${result.report.forensic_signals.format}, ${result.report.forensic_signals.dimensions.width} × ${result.report.forensic_signals.dimensions.height}` : "Container validation passed"}</dd></div></dl><p className="notice">{result.report.recommendation}</p><div className="feedback"><span>Does this need correction?</span><button type="button" onClick={() => sendFeedback("result_incorrect")}>Report an issue</button><button type="button" onClick={() => sendFeedback("unsure")}>I’m not sure</button></div>{feedback && <p className="feedback-message">{feedback}</p>}</article>}</div></section>;
}

function Team() { return <section id="about" className="team-section"><div className="section-wrap"><div className="team-copy"><div className="eyebrow">The people behind the work</div><h2>About The DeepBusters.</h2><p>We are building a calmer, more transparent way to investigate synthetic media—where a model output is only one part of the evidence.</p></div><div className="team-grid">{team.map(([name, photo]) => <article className="member" key={name}><img src={photo} alt={`Portrait of ${name}`} loading="lazy"/><h3>{name}</h3><p>DeepBusters team</p></article>)}</div></div></section>; }

export default function App() { return <><header><a className="brand" href="#top">MAAYABREAKER <span>/ THE DEEPBUSTERS</span></a><nav><a href="#how">How it works</a><a href="#about">About</a><a href="#learn">Learn</a><a href="#analyze" className="nav-cta">Analyze media</a></nav></header><main id="top"><section className="hero"><div><div className="eyebrow">Digital media forensics</div><h1>See beyond the pixels.</h1><p>MaayaBreaker helps people inspect digital media for signs of manipulation—while being transparent about evidence, uncertainty, and limits.</p><div className="actions"><a className="primary" href="#analyze">Analyze media</a><a className="text-link" href="#how">How analysis works →</a></div></div><aside><div className="signal">FORENSIC REVIEW</div><div className="scan"><i/><i/><i/><i/></div><p>Evidence before conclusions.</p></aside></section><section className="facts"><div><strong>Images</strong><span>Metadata & file forensics</span></div><div><strong>Video</strong><span>Secure intake foundation</span></div><div><strong>Audio</strong><span>Secure intake foundation</span></div></section><UploadWorkspace/><section className="split" id="how"><div><div className="eyebrow">Methodology</div><h2>Results should be explainable.</h2><p>We separate model predictions from forensic signals and user-provided context. This prevents technical artifacts from being presented as proof.</p></div><ol><li><b>1</b><span>Validate the upload and identify its real media type.</span></li><li><b>2</b><span>Extract contextual file and image evidence.</span></li><li><b>3</b><span>Use registered, calibrated models only when available.</span></li><li><b>4</b><span>Invite correction into a human-review queue.</span></li></ol></section><Team/><section id="learn" className="learn"><div className="section-wrap"><div className="eyebrow">Verification toolkit</div><h2>Before you share suspicious media</h2><div className="checklist"><span>Check the original source</span><span>Compare independent reporting</span><span>Inspect the surrounding context</span><span>Preserve the original file</span></div></div></section></main><footer><span>MaayaBreaker is an evidence-assistance tool, not a final authority.</span><span>Privacy-first by design · Unverified feedback is never training data</span></footer></>; }
