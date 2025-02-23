'use client';
import React, { useState } from 'react';
import api from '../api';

export default function ParsePdf({}) {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post(
        '/parse-pdf', {
        method: 'POST',
        /*body: formData,*/
      });

      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      console.error("Error adding parsing pdf", error);
    }    
  };

  return (
    <div>
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <input type="file" onChange={handleFileChange} />
        <button
          className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:min-w-44"
          onClick={handleFileUpload}
        >
          Parse bank statement PDF
        </button>
        {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
      </main>
    </div>
  );
}