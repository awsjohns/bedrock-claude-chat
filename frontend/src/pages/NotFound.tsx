import React from 'react';
import { PiSmileyXEyesFill } from 'react-icons/pi';

const NotFound: React.FC = () => {
  return (
    <div className="flex h-screen flex-col items-center justify-center">
      <div className="flex text-5xl font-bold">
        <PiSmileyXEyesFill />
        404 ERROR
      </div>
      <div className="mt-4 text-lg">The page you are looking for could not be found</div>
    </div>
  );
};

export default NotFound;
