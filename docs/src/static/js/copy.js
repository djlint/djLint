// Buttons with data-copy put that text on the clipboard, then show a check,
// or a cross when the browser refused, for a moment. A polite live region
// says the same to screen readers.
var status;

function announce(message) {
  if (!status) {
    status = document.createElement("span");
    status.className = "is-sr-only";
    status.setAttribute("role", "status");
    document.body.appendChild(status);
  }
  status.textContent = message || "";
}

function flash(button, state, iconClass, message) {
  var icon = button.querySelector("i");
  button.classList.add(state);
  icon.className = iconClass;
  announce(message);
  setTimeout(function () {
    button.classList.remove(state);
    icon.className = "fa-regular fa-copy";
    announce("");
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
