(function () {
  const body = document.body;
  const toggle = document.getElementById('panelMenuToggle');
  const overlay = document.getElementById('panelNavOverlay');
  const sidebar = document.getElementById('panelSidebar');
  if (!toggle || !sidebar) return;

  const desktopQuery = window.matchMedia('(min-width: 992px)');

  function setOpen(open) {
    body.classList.toggle('is-nav-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }

  function close() {
    setOpen(false);
  }

  toggle.addEventListener('click', function () {
    setOpen(!body.classList.contains('is-nav-open'));
  });

  if (overlay) {
    overlay.addEventListener('click', close);
  }

  sidebar.querySelectorAll('[data-panel-nav-close]').forEach(function (el) {
    el.addEventListener('click', close);
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') close();
  });

  if (desktopQuery.addEventListener) {
    desktopQuery.addEventListener('change', function (event) {
      if (event.matches) close();
    });
  } else if (desktopQuery.addListener) {
    desktopQuery.addListener(function (event) {
      if (event.matches) close();
    });
  }
})();
