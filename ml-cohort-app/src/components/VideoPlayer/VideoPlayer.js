import React from 'react';
import ReactPlayer from 'react-player'; // Assuming you're using react-player

function VideoPlayer({ videos }) {
  return (
    <div>
      {videos.map((video, index) => (
        <ReactPlayer key={index} url={video.url} controls={true} />
      ))}
    </div>
  );
}

export default VideoPlayer;
