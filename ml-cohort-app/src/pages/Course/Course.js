import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getCourseDetails } from '../../services/course';

function Course() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);

  useEffect(() => {
    getCourseDetails(courseId).then(setCourse);
  }, [courseId]);

  if (!course) return <div>Loading...</div>;

  return (
    <div>
      <h2>{course.title}</h2>
      <p>{course.description}</p>

      <h3>Modules:</h3>
      <ul>
        {course.modules.map((module) => (
          <li key={module.id}>
            <Link to={`/course/${courseId}/module/${module.id}`}>{module.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Course;
