import React, { useRef, useEffect, useState } from 'react';

const Canvas = () => {
  const canvasRef = useRef(null);
  const [positions, setPositions] = useState([]);

  useEffect(() => {
    const fetchMousePositions = async () => {
      while (true) {
        try {
          const response = await fetch('http://127.0.0.1:8000/mouse_position');
          const data = await response.json();
          setPositions(prev => [...prev.slice(-100), data]); // Limit the number of positions stored
        } catch (error) {
          console.error('Failed to fetch mouse positions:', error);
        }
        await new Promise(resolve => setTimeout(resolve, 100)); // Fetch every 0.1 seconds
      }
    };

    fetchMousePositions();
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    if (positions.length > 1) {
      const prevPos = positions[positions.length - 2];
      const currentPos = positions[positions.length - 1];

      context.strokeStyle = 'black';
      context.lineWidth = 2;
      context.beginPath();
      context.moveTo(prevPos.x, prevPos.y);
      context.lineTo(currentPos.x, currentPos.y);
      context.stroke();
    }
  }, [positions]);

  return <canvas ref={canvasRef} width={1920} height={1080} style={{ border: '1px solid black' }} />;
};

export default Canvas;
