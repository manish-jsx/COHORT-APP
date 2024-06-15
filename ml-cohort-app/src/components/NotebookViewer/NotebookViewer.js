import React from 'react';
import Iframe from 'react-iframe'; // If using nbviewer embedded

function NotebookViewer({ notebookUrl }) {
  return (
    <Iframe url={notebookUrl} width="100%" height="600px" />
  );
}

export default NotebookViewer;
