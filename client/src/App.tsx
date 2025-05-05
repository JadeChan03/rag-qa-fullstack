import React, { useState } from 'react';
import {
  TextField,
  Button,
  Typography,
  Container,
  CircularProgress,
  Box,
  Paper,
  createTheme,
  ThemeProvider,
} from '@mui/material';

// define the structure for the response
interface AnswerResponse {
  answer: string;
  source: string[];
  confidence: number;
}

// create a custom theme with teal colors
const theme = createTheme({
  palette: {
    primary: {
      main: '#008080',
    },
    secondary: {
      main: '#005757',
    },
  },
});

const App: React.FC = () => {
  const [question, setQuestion] = useState<string>(''); // user's question
  const [answer, setAnswer] = useState<string | null>(null); // retrieved answer
  const [sources, setSources] = useState<string[] | null>(null); // source documents
  const [confidence, setConfidence] = useState<number | null>(null); // confidence score
  const [loading, setLoading] = useState<boolean>(false); // loading state
  const [error, setError] = useState<string | null>(null); // error state

  // function to handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      // make a post request to the backend
      const response = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: question }),
      });

      if (!response.ok) {
        throw new Error('failed to fetch answer from the server.');
      }

      const data: AnswerResponse = await response.json();
      setAnswer(data.answer); // set the answer
      setSources(data.source); // set the sources
      setConfidence(data.confidence); // set the confidence score
    } catch (err) {
      setError((err as Error).message); // set error message
    } finally {
      setLoading(false); // reset loading state
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh', // full height of the viewport

          overflow: 'hidden',
        }}
      >
        <Container maxWidth="md">
          <Paper elevation={3} style={{ padding: '2rem', borderRadius: '8px' }}>
            <Typography variant="h4" gutterBottom style={{ fontWeight: 600 }}>
              Internal Q&A System
            </Typography>
            <Typography
              variant="body1"
              color="textSecondary"
              style={{ marginBottom: '2rem' }}
            >
              Please ask only enterprise-related questions. Provide specific
              details for optimal accuracy. Response times may be longer due to
              this being a demo version.
            </Typography>

            <form onSubmit={handleSubmit}>
              <TextField
                label="Ask a Question"
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
                style={{
                  marginTop: '1rem',
                  padding: '0.75rem',
                  fontSize: '1rem',
                  fontWeight: 600,
                }}
              >
                {loading ? (
                  <CircularProgress size={24} color="inherit" />
                ) : (
                  'Submit'
                )}
              </Button>
            </form>

            {error && (
              <Typography
                color="error"
                variant="body2"
                style={{ marginTop: '1.5rem', fontWeight: 500 }}
              >
                Error: {error}
              </Typography>
            )}

            {answer && (
              <Box
                marginTop="2rem"
                padding="1.5rem"
                border="1px solid #ddd"
                borderRadius="8px"
                bgcolor="#f9f9f9"
              >
                <Typography
                  variant="h6"
                  gutterBottom
                  style={{ fontWeight: 600, marginBottom: '1rem' }}
                >
                  Answer
                </Typography>
                <Typography variant="body1" style={{ marginBottom: '1rem' }}>
                  {answer}
                </Typography>

                {confidence !== null && (
                  <Typography
                    variant="body2"
                    color="textSecondary"
                    style={{ marginBottom: '0.5rem' }}
                  >
                    Confidence: {Math.round(confidence * 100)}%
                  </Typography>
                )}

                {sources && (
                  <Typography
                    variant="body2"
                    color="textSecondary"
                    style={{ marginTop: '0.5rem' }}
                  >
                    Source: {sources.join(', ')}
                  </Typography>
                )}
              </Box>
            )}
          </Paper>
        </Container>
      </div>
    </ThemeProvider>
  );
};

export default App;
