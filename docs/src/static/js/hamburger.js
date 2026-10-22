var $navbarBurgers = Array.prototype.slice.call(
  document.querySelectorAll(".navbar-burger"),
  0,
);

if ($navbarBurgers.length > 0) {
  $navbarBurgers.forEach(function (el) {
    el.addEventListener("click", function () {
      var target = el.dataset.target;
      var $target = document.getElementById(target);

      var open = el.classList.toggle("is-active");
      $target.classList.toggle("is-active", open);
      el.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
}
