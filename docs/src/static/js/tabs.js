document.addEventListener('click', function (e) {
  if (
    e.target.closest('.tabs li a') &&
    e.target.closest('.tabs li a').hasAttribute('tab')
  ) {
    console.log('tab click');

    // change active tab button
    var tabLinks = e.target.closest('.tabs').querySelectorAll('li.is-active');

    for (var i = 0; i < tabLinks.length; i++) {
      tabLinks[i].classList.remove('is-active');
    }

    e.target.closest('li').classList.add('is-active');

    // change active tab

    // find container with tab
    var tabContainer = document
      .querySelector('.tab-container .tab#' + e.target.getAttribute('tab'))
      .closest('.tab-container');

    var tabs = tabContainer.querySelectorAll('.tab.is-active');

    for (var i = 0; i < tabs.length; i++) {
      tabs[i].classList.remove('is-active');
    }

    tabContainer
      .querySelector('.tab#' + e.target.getAttribute('tab'))
      .classList.add('is-active');
  }
});
