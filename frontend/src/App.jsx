import { useState } from "react";

function App() {
  const [notes, setNotes] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateSummary = async () => {
    if (!notes.trim()) {
      setError("Please enter meeting notes.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/generate-summary",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: notes,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to connect to backend.");
    }

    setLoading(false);
  };

  const handleCopy = () => {
    if (result?.follow_up_email) {
      navigator.clipboard.writeText(result.follow_up_email);
      alert("Email copied to clipboard!");
    }
  };

  const handleClear = () => {
    setNotes("");
    setResult(null);
    setError("");
  };

  const handleRegenerate = () => {
    generateSummary();
  };

  const handleExportTXT = () => {
    if (!result) return;

    const content = `
Short Summary:
${result.short_summary}

Detailed Summary:
${result.detailed_summary}

Key Decisions:
${result.key_decisions?.join("\n")}

Action Items:
${result.action_items
  ?.map(
    (item) =>
      `Task: ${item.task || item}
Owner: ${item.owner || "Not specified"}
Deadline: ${item.deadline || "Not specified"}
Priority: ${item.priority || "Not specified"}`
  )
  .join("\n\n")}

Follow-up Email:
${result.follow_up_email}
`;

    const blob = new Blob([content], {
      type: "text/plain",
    });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "meeting_summary.txt";
    a.click();

    URL.revokeObjectURL(url);
  };

  const handleExportJSON = () => {
    if (!result) return;

    const blob = new Blob(
      [JSON.stringify(result, null, 2)],
      {
        type: "application/json",
      }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "meeting_summary.json";
    a.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div
      style={{
        maxWidth: "900px",
        margin: "0 auto",
        padding: "30px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>Meeting Notes Processor</h1>

      <p>
        Enter meeting notes below and generate a structured summary using AI.
      </p>

      <textarea
        rows="12"
        style={{
          width: "100%",
          padding: "10px",
          fontSize: "14px",
        }}
        placeholder="Paste meeting notes here..."
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
      />

      <br />
      <br />

      <button
        onClick={generateSummary}
        disabled={loading}
        style={{
          padding: "10px 20px",
          cursor: "pointer",
        }}
      >
        {loading ? "Generating..." : "Generate Summary"}
      </button>

      {error && (
        <div
          style={{
            marginTop: "20px",
            padding: "10px",
            border: "1px solid red",
          }}
        >
          {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>Short Summary</h2>
          <p>{result.short_summary}</p>

          <h2>Detailed Summary</h2>
          <p>{result.detailed_summary}</p>

          <h2>Key Decisions</h2>
          <ul>
            {result.key_decisions?.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h2>Action Items</h2>

          {result.action_items?.length > 0 ? (
            <table
              border="1"
              cellPadding="10"
              style={{
                width: "100%",
                borderCollapse: "collapse",
              }}
            >
              <thead>
                <tr>
                  <th>Task</th>
                  <th>Owner</th>
                  <th>Deadline</th>
                  <th>Priority</th>
                </tr>
              </thead>

              <tbody>
                {result.action_items.map((item, index) => (
                  <tr key={index}>
                    <td>{item.task || item}</td>
                    <td>{item.owner || "Not specified"}</td>
                    <td>{item.deadline || "Not specified"}</td>
                    <td>{item.priority || "Not specified"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No action items found.</p>
          )}

          <h2>Follow-up Email</h2>

          <textarea
            value={result.follow_up_email}
            readOnly
            rows={12}
            style={{
              width: "100%",
              padding: "10px",
            }}
          />

          <br />
          <br />

          <button
            onClick={handleCopy}
            style={{
              marginRight: "10px",
              padding: "8px 16px",
            }}
          >
            Copy
          </button>

          <button
            onClick={handleClear}
            style={{
              marginRight: "10px",
              padding: "8px 16px",
            }}
          >
            Clear
          </button>

          <button
            onClick={handleRegenerate}
            style={{
              marginRight: "10px",
              padding: "8px 16px",
            }}
          >
            Regenerate
          </button>

          <button
            onClick={handleExportTXT}
            style={{
              marginRight: "10px",
              padding: "8px 16px",
            }}
          >
            Export TXT
          </button>

          <button
            onClick={handleExportJSON}
            style={{
              padding: "8px 16px",
            }}
          >
            Export JSON
          </button>
        </div>
      )}
    </div>
  );
}

export default App;