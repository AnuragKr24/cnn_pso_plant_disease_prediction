// Attach the event only when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('predictBtn').addEventListener('click', sendImage);
});

async function sendImage(event) {
  // Prevent page refresh
  if (event) event.preventDefault();

  const fileInput = document.getElementById('imageInput');
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload an image first!");
    return;
  }

  // Preview the image
  const reader = new FileReader();
  reader.onload = function (e) {
    document.getElementById('previewImage').src = e.target.result;
  };
  reader.readAsDataURL(file);

  // Show loading text
  document.getElementById('baseline').innerText = "⏳ Predicting...";
  document.getElementById('pso').innerText = "⏳ Predicting...";

  // Prepare form data for backend
  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await fetch('http://127.0.0.1:5000/', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) throw new Error("Backend error");

    const result = await response.json();

    // FIX: Display correct fields returned by backend
    document.getElementById("baseline").innerText =
      `${result.baseline_prediction} (${(result.baseline_confidence * 100).toFixed(2)}%)`;

    document.getElementById("pso").innerText =
      `${result.pso_prediction} (${(result.pso_confidence * 100).toFixed(2)}%)`;

  } catch (error) {
    console.error(error);
    alert("Error connecting to backend!");
    document.getElementById('baseline').innerText = "";
    document.getElementById('pso').innerText = "";
  }
}
