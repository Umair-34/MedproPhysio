(function () {
  'use strict';

  var tabList = document.querySelector('.treatment-tabs');
  var tabs = document.querySelectorAll('.treatment-tab');
  var panels = document.querySelectorAll('.treatment-panel');

  if (!tabs.length || !tabList) {
    return;
  }

  function activateTab(tabName, focusTab) {
    var activeTab = null;

    tabs.forEach(function (tab) {
      var isActive = tab.getAttribute('data-tab') === tabName;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
      tab.setAttribute('tabindex', isActive ? '0' : '-1');
      if (isActive) {
        activeTab = tab;
      }
    });

    panels.forEach(function (panel) {
      var isActive = panel.getAttribute('data-panel') === tabName;
      panel.classList.toggle('active', isActive);
      if (isActive) {
        panel.removeAttribute('hidden');
      } else {
        panel.setAttribute('hidden', 'hidden');
      }
    });

    if (focusTab && activeTab) {
      activeTab.focus();
    }
  }

  tabList.setAttribute('role', 'tablist');

  tabs.forEach(function (tab, index) {
    tab.setAttribute('role', 'tab');
    tab.setAttribute('id', 'treatment-tab-' + tab.getAttribute('data-tab'));
    tab.setAttribute('tabindex', tab.classList.contains('active') ? '0' : '-1');

    var panelName = tab.getAttribute('data-tab');
    var panel = document.querySelector('[data-panel="' + panelName + '"]');
    if (panel) {
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
    }

    tab.addEventListener('click', function () {
      activateTab(tab.getAttribute('data-tab'), false);
    });

    tab.addEventListener('keydown', function (event) {
      var nextIndex = null;

      if (event.key === 'ArrowRight') {
        nextIndex = (index + 1) % tabs.length;
      } else if (event.key === 'ArrowLeft') {
        nextIndex = (index - 1 + tabs.length) % tabs.length;
      } else if (event.key === 'Home') {
        nextIndex = 0;
      } else if (event.key === 'End') {
        nextIndex = tabs.length - 1;
      }

      if (nextIndex !== null) {
        event.preventDefault();
        activateTab(tabs[nextIndex].getAttribute('data-tab'), true);
      }
    });
  });
})();
