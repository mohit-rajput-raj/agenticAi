import { create } from "zustand";

interface OcrState {
  selectedFile: File | null;
  previewUrl: string | null;
  setSelectedFile: (file: File | null) => void;
}

export const useOcrStore = create<OcrState>((set) => ({
  selectedFile: null,
  previewUrl: null,
  setSelectedFile: (file) => set((state) => {
    // Revoke old object URL to prevent memory leaks
    if (state.previewUrl) {
      URL.revokeObjectURL(state.previewUrl);
    }
    return {
      selectedFile: file,
      previewUrl: file ? URL.createObjectURL(file) : null
    };
  }),
}));
