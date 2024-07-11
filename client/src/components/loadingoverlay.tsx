import * as React from "react"

const LoadingOverlay = () => (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 cursor-progress">
      <div className="bg-white p-6 rounded shadow-lg">
        <p className="text-center">Loading...</p>
      </div>
    </div>
  );
  
  export default LoadingOverlay;