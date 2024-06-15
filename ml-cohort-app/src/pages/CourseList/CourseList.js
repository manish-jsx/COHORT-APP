import React, { useState, useEffect } from 'react';
import { getAllCourses } from '../../services/course';
import { Link } from 'react-router-dom';

function CourseList() {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    getAllCourses()
      .then(setCourses)
      .catch(error => console.error("Error fetching courses:", error)); // Error handling
  }, []);

  return (
    <div>
      <h2>Available Courses</h2>
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

export default CourseList;
