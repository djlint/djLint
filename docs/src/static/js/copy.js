// Buttons with data-copy put that text on the clipboard, then show a check,
// or a cross when the browser refused, for a moment. A polite live region
// says the same to screen readers; it is mounted empty up front because
// screen readers ignore a region that appears together with its message.
var status = document.createElement("span");
status.className = "is-sr-only";
status.setAttribute("role", "status");

function mountStatus() {
  document.body.appendChild(status);
}
if (document.body) mountStatus();
else document.addEventListener("DOMContentLoaded", mountStatus);

var statusTimer;

function flash(button, state, iconClass, message) {
  var icon = button.querySelector("i");
  // A new click replaces the previous result instead of being cut short
  // by its timer.
  clearTimeout(button.copyTimer);
  clearTimeout(statusTimer);
  button.classList.remove("is-copied", "is-failed");
  button.classList.add(state);
  icon.className = iconClass;
  status.textContent = message || "";
  button.copyTimer = setTimeout(function () {
    button.classList.remove(state);
    icon.className = "fa-regular fa-copy";
  }, 1500);
  statusTimer = setTimeout(function () {
    status.textContent = "";
  }, 1500);
}

document.addEventListener("click", function (e) {
  var button = e.target.closest("[data-copy]");
  if (!button) return;
  var failed = function () {
    flash(
      button,
      "is-failed",
      "fas fa-xmark",
      button.getAttribute("data-copy-failed"),
    );
  };
  if (!navigator.clipboard) return failed();
  navigator.clipboard
    .writeText(button.getAttribute("data-copy"))
    .then(function () {
      flash(
        button,
        "is-copied",
        "fas fa-check",
        button.getAttribute("data-copied"),
      );
    }, failed);
});
