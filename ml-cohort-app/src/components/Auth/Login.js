import React, { useState, useEffect } from 'react';
import { login, isAuthenticated } from '../../services/auth';
import { useNavigate, Link } from 'react-router-dom';
import { Form, Button, Container, Row, Col, Alert } from 'react-bootstrap';

function Login() {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); // State to handle login errors
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null); // Clear any previous errors

    try {
      const loginSuccessful = await login(usernameOrEmail, password);
      if (loginSuccessful) {
        navigate('/');
      } else {
        setError('Incorrect username or password'); // Or get error from backend
      }
    } catch (err) {
      setError(err.message); // Ensure the error message from the backend is set here
    }
  };

  useEffect(() => {
    // Check if authenticated on initial load
    if (isAuthenticated()) {
      navigate('/');
    }
  }, [navigate]); // Add isAuthenticated as a dependency

  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={6}>
          <h2>Login</h2>
          {error && <Alert variant="danger">{error}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="usernameOrEmail">
              <Form.Label>Username or Email</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username or email"
                value={usernameOrEmail}
                onChange={(e) => setUsernameOrEmail(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="password">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>

            <Button variant="primary" type="submit">
              Login
            </Button>

            <div className="text-center mt-3">
              <Link to="/register">Don't have an account? Register</Link>
            </div>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default Login;
