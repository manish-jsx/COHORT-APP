import React, { useState, useEffect } from 'react';
import { getForumThreads, createForumThread } from '../../services/forum';

function Forum() {
  const [threads, setThreads] = useState([]);
  const [newThreadTitle, setNewThreadTitle] = useState('');

  useEffect(() => {
    getForumThreads().then(setThreads);
  }, []);

  const handleCreateThread = async () => {
    try {
      const newThread = await createForumThread(newThreadTitle);
      setThreads([...threads, newThread]);
      setNewThreadTitle(''); // Clear input field
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div>
      <h2>Discussion Forum</h2>
      {/* Display Existing Threads */}
      <ul>
        {threads.map(thread => (
          <li key={thread.id}>
            {/* ... thread details (title, link to thread page) */}
          </li>
        ))}
      </ul>

      {/* Create New Thread Form */}
      <form onSubmit={handleCreateThread}>
        <input 
          type="text" 
          placeholder="New thread title..."
          value={newThreadTitle}
          onChange={(e) => setNewThreadTitle(e.target.value)} 
        />
        <button type="submit">Create Thread</button>
      </form>
    </div>
  );
}

export default Forum;
