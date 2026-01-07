(function () {
  const dimsSelect = document.getElementById("dimsSelect");
  const zRow = document.getElementById("zRow");
  const btnReset = document.getElementById("btnReset");

  function syncUI() {
    const dims = dimsSelect?.value || "2";
    if (zRow) zRow.style.display = (dims === "3") ? "grid" : "none";
  }

  dimsSelect?.addEventListener("change", syncUI);

  btnReset?.addEventListener("click", () => {
    window.location.href = "/";
  });

  syncUI();
})();
