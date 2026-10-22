// Buttons with data-copy put that text on the clipboard, then show a check,
// or a cross when the browser refused, for a moment.
function flash(button, state, iconClass) {
  var icon = button.querySelector("i");
  button.classList.add(state);
  icon.className = iconClass;
  setTimeout(function () {
    button.classList.remove(state);
    icon.className = "fa-regular fa-copy";
  }, 1500);
}

document.addEventListener("click", function (e) {
  var button = e.target.closest("[data-copy]");
  if (!button) return;
  var failed = function () {
    flash(button, "is-failed", "fas fa-xmark");
  };
  if (!navigator.clipboard) return failed();
  navigator.clipboard
    .writeText(button.getAttribute("data-copy"))
    .then(function () {
      flash(button, "is-copied", "fas fa-check");
    }, failed);
});
