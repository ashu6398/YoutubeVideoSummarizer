let abortController;

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("summaryForm");
  const loader = document.getElementById("loader");
  const stopBtn = document.getElementById("stopButton");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    loader.classList.remove("hidden");
    stopBtn.classList.remove("hidden");
    showToast("⏳ Processing video...");

    if (abortController) {
      abortController.abort();
    }
    abortController = new AbortController();

    const formData = new FormData(form);

    fetch("/summarize", {
      method: "POST",
      body: formData,
      signal: abortController.signal
    })
    .then(response => {
      if (!response.ok) throw new Error("Request failed");
      return response.text();
    })
    .then(html => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, "text/html");
      const summary = doc.querySelector(".summary-box");

      if (summary) {
        const container = document.querySelector(".container");
        const oldSummary = container.querySelector(".summary-box");
        if (oldSummary) oldSummary.remove();
        container.appendChild(summary);
        showToast("✅ Summary loaded successfully!");
      }

      loader.classList.add("hidden");
      stopBtn.classList.add("hidden");
    })
    .catch(err => {
      if (err.name === "AbortError") {
        showToast("❌ Request aborted.");
      } else {
        showToast("⚠️ Something went wrong.");
      }
      loader.classList.add("hidden");
      stopBtn.classList.add("hidden");
    });
  });

  stopBtn.addEventListener("click", () => {
    if (abortController) abortController.abort();
    loader.classList.add("hidden");
    stopBtn.classList.add("hidden");
  });
});

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.innerText = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3000);
}
