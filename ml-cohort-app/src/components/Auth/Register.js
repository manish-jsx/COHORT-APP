import React, { useState } from 'react';
import { register } from '../../services/auth';
import { useNavigate , Link} from 'react-router-dom';
import { Form, Button, Container, Row, Col, Alert, Spinner } from 'react-bootstrap';

function Register() {
  const [username, setUsername] = useState('');
  const [firstName, setFirstName] = useState('');  // Add for first name
  const [lastName, setLastName] = useState('');  // Add for last name
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  //   useEffect(() => {
  //   // Check if authenticated on initial load
  //   if (isAuthenticated) {
  //     navigate('/login');
  //   }
  // }, [ navigate]); // Add isAuthenticated as a dependency


  const handleSubmit = async (event) => {
    event.preventDefault();
    const newErrors = {};

    // Validation for each field
    if (username.trim() === '') {
      newErrors.username = 'Username is required';
    }
    if (!validateEmail(email)) { // Check for valid email format
      newErrors.email = 'Valid email is required';
    }
    if (password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }
    if (password !== password2) {
      newErrors.password2 = 'Passwords do not match';
    }

    // If any errors, update the errors state
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsLoading(true);
  
    try {
      const success = await register(username, email, password, firstName, lastName);
      if (success) {
        navigate('/login');
      }
    } catch (error) {
      // Handle network errors
      if (!error.response) {
        setErrors({ general: 'Network error. Please try again later.' });
      } else if(error.response.status === 500) { // Handle 500 internal server errors
        setErrors({ general: 'Internal Server Error, please try again later!' })
      } else {
        const errorData = await error.response.json();
        console.log("Error response:", errorData);
        setErrors(errorData);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function for basic email validation
  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }


  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={6}>
          <h2>Register</h2>
          {/* General Error Message */}
          {errors.general && (
            <Alert variant="danger">{errors.general}</Alert>
          )}

          {/* Non-Field Errors Message (usually for server-side errors) */}
          {errors.non_field_errors && (
            <Alert variant="danger">{errors.non_field_errors.join(", ")}</Alert>
          )}

          {/* Display specific errors for other fields */}
          {errors.username && (
            <Alert variant="danger">{errors.username[0]}</Alert>
          )}
          {errors.email && (
            <Alert variant="danger">{errors.email[0]}</Alert>
          )}
          {errors.password1 && (
            <Alert variant="danger">{errors.password1[0]}</Alert>
          )}
          {errors.password2 && (
            <Alert variant="danger">{errors.password2[0]}</Alert>
          )}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="username">
              {/* ... username field ... */}
              <Form.Label>Username</Form.Label>
              <Form.Control 
                type="text" 
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)} 
                required 
              />

            </Form.Group>

 {/* First Name field */}
 <Form.Group className="mb-3" controlId="firstName">
              <Form.Label>First Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter first name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                isInvalid={!!errors.first_name} // Handle error for first_name (if any)
              />
              <Form.Control.Feedback type="invalid">
                {errors.first_name}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Last Name field */}
            <Form.Group className="mb-3" controlId="lastName">
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter last name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                isInvalid={!!errors.last_name} // Handle error for last_name (if any)
              />
              <Form.Control.Feedback type="invalid">
                {errors.last_name}
              </Form.Control.Feedback>
            </Form.Group>
            
            {/* Email field */}
            <Form.Group className="mb-3" controlId="email">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                isInvalid={!!errors.email}
              />
              <Form.Control.Feedback type="invalid">
                {errors.email}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Password field */}
            <Form.Group className="mb-3" controlId="password1"> 
              <Form.Label>Password</Form.Label>
              <Form.Control 
                type="password" 
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                isInvalid={!!errors.password} 
              />
              <Form.Control.Feedback type="invalid">
                {errors.password}
              </Form.Control.Feedback>
            </Form.Group>

            {/* Confirm Password field */}
            <Form.Group className="mb-3" controlId="password2"> 
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control 
                type="password" 
                placeholder="Confirm password"
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                isInvalid={!!errors.password2} 
              />
              <Form.Control.Feedback type="invalid">
                {errors.password2}
              </Form.Control.Feedback>
            </Form.Group>

            <Button variant="primary" type="submit" disabled={isLoading}>
              {isLoading ? <Spinner animation="border" size="sm" /> : "Register"}
            </Button>

            <div className="text-center mt-3">
              <p>Already a member?</p> 
              <Link to="/login">Login Here</Link> 
            </div>

          </Form>
        </Col>
      </Row>
    </Container>
  );
}


export default Register;
