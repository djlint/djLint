// Buttons with data-copy put that text on the clipboard and show a check.
document.addEventListener("click", function (e) {
  var button = e.target.closest("[data-copy]");
  if (!button || !navigator.clipboard) return;
  navigator.clipboard
    .writeText(button.getAttribute("data-copy"))
    .then(function () {
      var icon = button.querySelector("i");
      button.classList.add("is-copied");
      icon.className = "fas fa-check";
      setTimeout(function () {
        button.classList.remove("is-copied");
        icon.className = "fa-regular fa-copy";
      }, 1500);
    });
});
