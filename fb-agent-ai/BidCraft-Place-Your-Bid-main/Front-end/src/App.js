import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css"; // Import CSS

function App() {
  const [accessToken, setAccessToken] = useState("");
  const [postId, setPostId] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!accessToken || !postId) {
      setMessage("Both fields are required!");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        `http://localhost:8000/update-credentials?access_token=${encodeURIComponent(
          accessToken
        )}&post_id=${encodeURIComponent(postId)}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        }
      );

      const data = await response.json();
      if (data.status === "success") {
        setMessage("Credentials updated successfully!");
        setAccessToken("");
        setPostId("");
      } else {
        setMessage("Failed to update credentials!");
      }
    } catch (error) {
      console.error("Error:", error);
      setMessage("An error occurred! Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="next-container">
      <h2 className="next-title">Update Credentials</h2>

      <form onSubmit={handleSubmit} className="input-container">
        <div className="input-group">
          <label>Access Token:</label>
          <input
            type="text"
            value={accessToken}
            onChange={(e) => setAccessToken(e.target.value)}
            className="input-field"
            required
          />
        </div>
        <div className="input-group">
          <label>Post ID:</label>
          <input
            type="text"
            value={postId}
            onChange={(e) => setPostId(e.target.value)}
            className="input-field"
            required
          />
        </div>
        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>

      {message && <p className="response-message">{message}</p>}

      <button className="back-button" onClick={() => navigate("/next")}>
        Go to Next Page
      </button>
    </div>
  );
}

export default App;
