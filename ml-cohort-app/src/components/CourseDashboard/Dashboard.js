import React, { useState, useEffect } from 'react';
import { getEnrolledCourses } from '../../services/course'; // Fetch enrolled courses
import { Link } from 'react-router-dom';

function Dashboard() {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    getEnrolledCourses().then(setCourses);
  }, []);

  return (
    <div>
      <h2>My Courses</h2>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>
            <Link to={`/course/${course.id}`}>{course.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
