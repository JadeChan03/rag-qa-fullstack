import React, { useState } from "react";
import { TextField, Button, Typography, Container, CircularProgress, Box } from "@mui/material";

// Define the structure for the response
interface AnswerResponse {
  answer: string;
}

const App: React.FC = () => {
  const [question, setQuestion] = useState<string>(""); // User's question
  const [answer, setAnswer] = useState<string | null>(null); // Retrieved answer
  const [loading, setLoading] = useState<boolean>(false); // Loading state
  const [error, setError] = useState<string | null>(null); // Error state

  // Function to handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent page reload
    setLoading(true); // Set loading state
    setError(null); // Reset error state

    try {
      // Make a POST request to the backend
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: question }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch answer from the server.");
      }

      const data: AnswerResponse = await response.json();
      setAnswer(data.answer); // Set the answer
    } catch (err) {
      setError((err as Error).message); // Set error message
    } finally {
      setLoading(false); // Reset loading state
    }
  };

  return (
    <Container maxWidth="sm" style={{ marginTop: "2rem", textAlign: "center" }}>
      <Typography variant="h4" gutterBottom>
        RAG QA Frontend
      </Typography>

      <form onSubmit={handleSubmit}>
        <TextField
          label="Ask a question"
          variant="outlined"
          fullWidth
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          margin="normal"
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          disabled={loading}
          style={{ marginTop: "1rem" }}
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : "Submit"}
        </Button>
      </form>

      {error && (
        <Typography color="error" variant="body1" style={{ marginTop: "1rem" }}>
          Error: {error}
        </Typography>
      )}

      {answer && (
        <Box marginTop="2rem" padding="1rem" border="1px solid #ddd" borderRadius="4px">
          <Typography variant="h6" gutterBottom>
            Answer:
          </Typography>
          <Typography variant="body1" color="textSecondary">
            {answer}
          </Typography>
        </Box>
      )}
    </Container>
  );
};

export default App;