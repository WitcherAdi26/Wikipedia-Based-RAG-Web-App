import React, { useState, useEffect } from 'react';
import './TypeWriterEffect.css'; // Ensure you import the CSS file

const TypewriterEffect = ({ text }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < text.length) {
      const timeout = setTimeout(() => {
        setDisplayedText((prev) => prev + text.charAt(index));
        setIndex(index + 1);
      }, 10); // Adjust typing speed here

      return () => clearTimeout(timeout);
    }
  }, [index, text]);

  return (
    <div className="answer-box">
      <span>{displayedText}</span><span className="cursor"></span>
    </div>
  );
};

export default TypewriterEffect;
