(function () {
  var debounce = function debounce(func, wait, immediate) {
    var timeout;
    return function () {
      var context = this,
        args = arguments;

      var later = function later() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };

      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
    };
  };

  var d = document,
    load = function () {
      [].forEach.call(
        d.querySelectorAll(".animated[data-animate]"),
        function (el) {
          if (isInViewport(el)) {
            // set image to nothing to clear, then load new
            el.classList.add(el.getAttribute("data-animate"));
            el.removeAttribute("data-animate");
          }
        },
      );
    };

  var isInViewport = function isInViewport(elem) {
    var bounding = elem.getBoundingClientRect(),
      padding = 0;
    return (
      bounding.top >= 0 &&
      bounding.left >= 0 &&
      bounding.bottom - elem.clientHeight - padding <=
        (document.documentElement.clientHeight ||
          d.documentElement.clientHeight) &&
      bounding.right - padding - elem.clientWidth <=
        (document.documentElement.clientWidth || d.documentElement.clientWidth)
    );
  };

  load();
  d.addEventListener("lazy", function () {
    setTimeout(function () {
      load();
    }, 0);
  });

  var resetHash = function () {
    if (window.location.hash != "") {
      history.pushState(
        "",
        document.title,
        window.location.pathname + window.location.search,
      );
    }
  };
  d.addEventListener("scroll", function () {
    debounce(load(), 200);

    debounce(resetHash(), 500);
  });
})();
