import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Home from './pages/Home/Home';
import Module from './pages/Module/Module';
import Course from './pages/Course/Course';
import CourseList from './pages/CourseList/CourseList';
import { isAuthenticated } from './services/auth'; 

function App() {
  const [authStatus, setAuthStatus] = useState(null); 

  useEffect(() => {
    // Check if the user is authenticated
    const checkAuth = async () => {
      const authenticated = await isAuthenticated();
      setAuthStatus(authenticated);
    };

    checkAuth();
  }, []);

  if (authStatus === null) {
    return <div>Loading...</div>; // Show a loading state while checking authentication
  }

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes */}
        {authStatus ? (
          <>
            <Route path="/" element={<Home />} />
            <Route path="/courses" element={<CourseList />} />
            <Route path="/course/:courseId" element={<Course />} />
            <Route path="/course/:courseId/module/:moduleId" element={<Module />} />
            {/* ... other protected routes ... */}
          </>
        ) : (
          <Route path="*" element={<Login />} />
        )}
      </Routes>
    </Router>
  );
}

export default App;
