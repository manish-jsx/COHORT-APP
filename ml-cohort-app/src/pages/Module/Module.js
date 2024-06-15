import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import NotebookViewer from '../../components/NotebookViewer/NotebookViewer';
import VideoPlayer from '../../components/VideoPlayer/VideoPlayer';
import { getModuleDetails } from '../../services/course';
import Markdown from 'react-markdown'; // Assuming you're using this library

function Module() {
  const { moduleId } = useParams();
  const [module, setModule] = useState(null);

  useEffect(() => {
    getModuleDetails(moduleId).then(setModule);
  }, [moduleId]);

  if (!module) return <div>Loading...</div>;

  return (
    <div>
      <h1>Module</h1>
      <h2>{module.title}</h2>
      <Markdown>{module.content}</Markdown> 
      {module.notebook && <NotebookViewer notebookUrl={module.notebook} />}
      {module.videos && <VideoPlayer videos={module.videos} />}
    </div>
  );
}

export default Module;
