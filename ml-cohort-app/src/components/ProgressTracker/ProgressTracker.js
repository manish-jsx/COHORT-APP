import React, { useState, useEffect } from 'react';
import { getUserProgress } from '../../services/progress'; // Fetch user progress

function ProgressTracker() {
  const [progress, setProgress] = useState({});

  useEffect(() => {
    getUserProgress().then(setProgress);
  }, []);

  return (
    <div>
      <h2>My Progress</h2>
      {/* Display progress data (completed modules, quiz scores, etc.) */}
    </div>
  );
}

export default ProgressTracker;
