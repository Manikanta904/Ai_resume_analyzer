const BASE_URL = "http://127.0.0.1:8000";

// ------------------- ANALYZE -------------------
export const analyzeResume = async (formData) => {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Analyze API failed");
  }

  return response.json();
};

// ------------------- REWRITE -------------------
export const rewriteResume = async (formData) => {
  const response = await fetch(`${BASE_URL}/rewrite-resume`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Rewrite API failed");
  }

  return response.json();
};

// ------------------- DOWNLOAD -------------------
export const downloadResume = async (data) => {
  const response = await fetch(`${BASE_URL}/download-resume`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Download API failed");
  }

  return response.blob();
};
