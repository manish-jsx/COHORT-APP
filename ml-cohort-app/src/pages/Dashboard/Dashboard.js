import React, { useEffect } from 'react'; // Removed unused useState
import { Link, useNavigate } from 'react-router-dom';
import { logout, isAuthenticated } from '../../services/auth';
import { Button, Container, Navbar, Nav, Offcanvas } from 'react-bootstrap';
import './Dashboard.css';

function Dashboard() {
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) { // Check if NOT authenticated to redirect
      navigate('/login');
    }
  }, [navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="home-container">
      {/* Navbar */}
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand as={Link} to="/">ML Cohort</Navbar.Brand>
          <Navbar.Toggle aria-controls={`offcanvasNavbar-expand-lg`} />
          <Navbar.Offcanvas
            id={`offcanvasNavbar-expand-lg`}
            aria-labelledby={`offcanvasNavbarLabel-expand-lg`}
            placement="end"
          >
            <Offcanvas.Header closeButton>
              <Offcanvas.Title id={`offcanvasNavbarLabel-expand-lg`}>
                Menu
              </Offcanvas.Title>
            </Offcanvas.Header>
            <Offcanvas.Body>
              <Nav className="justify-content-end flex-grow-1 pe-3">
                <Nav.Link as={Link} to="/dashboard">Home</Nav.Link>
                <Nav.Link as={Link} to="/courses">Courses</Nav.Link>
                {/* Add more navigation links as needed */}
                <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
              </Nav>
            </Offcanvas.Body>
          </Navbar.Offcanvas>
        </Container>
      </Navbar>

      {/* Hero Section */}
      <div className="hero-section">
        <Container>
          <h1>Master Machine Learning in 30 Days</h1>
          <p>Join our comprehensive cohort and unlock the power of AI.</p>
          <Button variant="primary" as={Link} to="/courses">Get Started</Button>
        </Container>
      </div>

      {/* Features Section */}
      <div className="features-section">
        <Container>
          <h2 className="text-center">Key Features</h2>
          <div className="row">
            {/* Feature Cards */}
            <div className="col-md-4">
              {/* Feature card content */}
            </div>
            {/* Add more feature cards as needed */}
          </div>
        </Container>
      </div>

      {/* Testimonials Section */}
      <div className="testimonials-section">
        {/* Testimonials with carousel or other display */}
      </div>

      {/* About Us Section */}
      <div className="about-us-section">
        {/* Information about your company, mission, etc. */}
      </div>

      {/* FAQ Section */}
      <div className="faq-section">
        {/* Frequently asked questions */}
      </div>

      {/* Footer */}
      <footer className="footer">
        {/* ... footer content */}
      </footer>
    </div>
  );
}

export default Dashboard;
