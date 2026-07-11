"use client";

import { useOcrStore } from "@/store/useOcrStore";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { useRef } from "react";
import Image from "next/image";

export default function OcrPage() {
  const { selectedFile, previewUrl, setSelectedFile } = useOcrStore();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const mutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      
      const response = await axios.post("http://127.0.0.1:8000/ocr", formData);
      return response.data;
    },
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
      mutation.reset(); // clear previous results
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      mutation.mutate(selectedFile);
    }
  };

  const triggerFileSelect = () => {
    fileInputRef.current?.click();
  };

  const clearSelection = () => {
    setSelectedFile(null);
    mutation.reset();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center py-16 px-4 font-sans">
      <div className="max-w-5xl w-full">
        <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 mb-4 tracking-tight">
          AI Receipt & Table Extractor
        </h1>
        <p className="text-slate-400 text-lg mb-12">
          Upload an image of a receipt or table, and let our vision model accurately extract the underlying data into a structured JSON format.
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Upload & Preview Section */}
          <div className="flex flex-col gap-6">
            <div 
              className={`border-2 border-dashed rounded-3xl p-8 flex flex-col items-center justify-center min-h-[400px] transition-all duration-300 ${previewUrl ? 'border-emerald-500/50 bg-emerald-500/5' : 'border-slate-800 bg-slate-900/50 hover:bg-slate-800/50 hover:border-slate-600'}`}
            >
              <input 
                type="file" 
                ref={fileInputRef}
                onChange={handleFileChange}
                accept="image/*"
                className="hidden"
              />
              
              {previewUrl ? (
                <div className="relative w-full h-full min-h-[300px] flex flex-col items-center justify-center group">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img 
                    src={previewUrl} 
                    alt="Selected" 
                    className="max-h-[350px] object-contain rounded-xl shadow-2xl transition-transform duration-300 group-hover:scale-[1.02]"
                  />
                  <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-slate-950/60 rounded-xl">
                    <button 
                      onClick={clearSelection}
                      className="px-6 py-2 bg-red-500/80 hover:bg-red-500 text-white font-medium rounded-full backdrop-blur-sm transition-colors"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center text-center cursor-pointer" onClick={triggerFileSelect}>
                  <div className="w-20 h-20 mb-6 rounded-full bg-slate-800 flex items-center justify-center text-emerald-400 shadow-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-10 h-10">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold mb-2">Click to select an image</h3>
                  <p className="text-slate-500 text-sm">PNG, JPG, JPEG up to 10MB</p>
                </div>
              )}
            </div>

            <button
              onClick={previewUrl ? handleUpload : triggerFileSelect}
              disabled={mutation.isPending}
              className={`w-full py-4 rounded-2xl font-bold text-lg shadow-xl transition-all duration-300 flex items-center justify-center gap-2 ${
                !previewUrl 
                  ? 'bg-slate-800 text-slate-400 hover:bg-slate-700' 
                  : mutation.isPending
                    ? 'bg-emerald-600/50 text-emerald-100 cursor-wait'
                    : 'bg-emerald-500 hover:bg-emerald-400 text-slate-950 hover:shadow-emerald-500/25 hover:-translate-y-1'
              }`}
            >
              {mutation.isPending ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing Image...
                </>
              ) : previewUrl ? (
                'Extract Data'
              ) : (
                'Choose File'
              )}
            </button>
          </div>

          {/* Result Section */}
          <div className="flex flex-col h-full min-h-[400px]">
            <div className="flex-1 bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden flex flex-col shadow-2xl relative">
              <div className="px-6 py-4 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 flex items-center justify-between z-10">
                <h3 className="font-semibold text-slate-200">Extracted JSON</h3>
                {mutation.isSuccess && (
                  <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-bold rounded-full border border-emerald-500/20">
                    Success
                  </span>
                )}
                {mutation.isError && (
                  <span className="px-3 py-1 bg-red-500/10 text-red-400 text-xs font-bold rounded-full border border-red-500/20">
                    Error
                  </span>
                )}
              </div>
              
              <div className="p-6 overflow-auto flex-1 h-full custom-scrollbar">
                {mutation.isPending ? (
                  <div className="h-full flex flex-col items-center justify-center text-slate-500 space-y-4">
                    <div className="w-16 h-16 border-4 border-slate-800 border-t-emerald-500 rounded-full animate-spin"></div>
                    <p className="animate-pulse">Analyzing image and generating JSON...</p>
                  </div>
                ) : mutation.isError ? (
                  <div className="text-red-400 bg-red-400/10 p-4 rounded-xl border border-red-400/20">
                    <p className="font-semibold mb-1">Failed to extract data</p>
                    <p className="text-sm opacity-80">{mutation.error instanceof Error ? mutation.error.message : 'Unknown error'}</p>
                  </div>
                ) : mutation.isSuccess && mutation.data ? (
                  <pre className="text-sm text-emerald-300 font-mono leading-relaxed whitespace-pre-wrap">
                    {JSON.stringify(mutation.data, null, 2)}
                  </pre>
                ) : (
                  <div className="h-full flex items-center justify-center text-slate-600 italic">
                    Upload an image and click extract to view the JSON output here.
                  </div>
                )}
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
