import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import "./CSS/NextPage.css";

function NextPage() {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");
  const [comment, setComment] = useState("");
  const [answer, setAnswer] = useState("");
  const [logs, setLogs] = useState("");

  const handleProcessComments = async () => {
    try {
      const response = await fetch("http://localhost:8000/process-comments", {
        method: "GET",
        headers: { Accept: "application/json" },
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
      } else {
        setMessage("Failed to process comments.");
      }
    } catch (error) {
      setMessage("Error: Unable to reach the server.");
    }
  };

  const handleSubmit = async () => {
    if (!comment || !answer) {
      setMessage("Please enter both comment and answer.");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/update-user-answer?comment=${encodeURIComponent(
          comment
        )}&answer=${encodeURIComponent(answer)}`,
        {
          method: "POST",
          headers: { Accept: "application/json" },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
        setComment("");
        setAnswer("");
      } else {
        setMessage("Failed to update the answer.");
      }
    } catch (error) {
      setMessage("Error: Unable to reach the server.");
    }
  };

  const handleGetLogs = async () => {
    try {
      const response = await fetch("http://localhost:8000/get-logs", {
        method: "GET",
        headers: { Accept: "application/json" },
      });

      if (response.ok) {
        const data = await response.json();
        setLogs(data.logs);
        setMessage("Logs retrieved successfully.");
      } else {
        setMessage("Failed to fetch logs.");
      }
    } catch (error) {
      setMessage("Error: Unable to reach the server.");
    }
  };

  const handleComposeLogFile = () => {
    if (!logs) {
      setMessage("No logs available to compose.");
      return;
    }

    const doc = new jsPDF();
    doc.setFont("helvetica", "normal");

    const lines = logs.split("\n"); // Split logs by new line
    const tableData = lines.map((line, index) => {
      const wrappedText = doc.splitTextToSize(line, 180); // Ensure text fits within column width
      return [index + 1, wrappedText]; // Row number + wrapped text
    });

    autoTable(doc, {
      head: [["#", "Log Entry"]],
      body: tableData,
      startY: 20,
      styles: { fontSize: 10, cellPadding: 3 },
      columnStyles: {
        0: { cellWidth: 10 }, // Row number column
        1: { cellWidth: 180 }, // Wrapped log entry column
      },
    });

    doc.save("logs.pdf");
    setMessage("Log file composed and downloaded successfully.");
  };

  return (
    <div className="next-container">
      <h2 className="next-title">Welcome to the Next Page</h2>

      <button className="process-button" onClick={handleProcessComments}>
        Process Comments
      </button>

      <div className="input-container">
        <input
          type="text"
          placeholder="Enter Comment"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          className="input-field"
        />
        <input
          type="text"
          placeholder="Enter Answer"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          className="input-field"
        />
      </div>

      <button className="submit-button" onClick={handleSubmit}>
        Submit
      </button>

      <div className="button-group">
        <button className="log-button" onClick={handleGetLogs}>
          Get Logs
        </button>
        <button className="compose-button" onClick={handleComposeLogFile}>
          Compose Log File
        </button>
      </div>

      {message && <p className="response-message">{message}</p>}

      <div className="log-display">
        <h3>Logs:</h3>
        <pre>{logs || "No logs available."}</pre>
      </div>

      <button className="back-button" onClick={() => navigate("/")}>
        Go Back
      </button>
    </div>
  );
}

export default NextPage;
