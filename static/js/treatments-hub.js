(function () {
  'use strict';

  var searchInput = document.getElementById('treatmentSearch');
  var filterButtons = document.querySelectorAll('.treatments-filter-btn');
  var gridItems = document.querySelectorAll('.treatments-grid-item');
  var resultsEl = document.getElementById('treatmentResults');
  var emptyEl = document.getElementById('treatmentsEmpty');
  var resetBtn = document.getElementById('treatmentReset');
  var pillars = document.querySelectorAll('.treatments-hub-pillar');

  if (!gridItems.length) {
    return;
  }

  var activeFilter = 'all';

  function normalize(value) {
    return (value || '').toLowerCase().trim();
  }

  function applyFilters() {
    var query = normalize(searchInput ? searchInput.value : '');
    var visibleCount = 0;
    var resultsLabel = resultsEl ? (resultsEl.getAttribute('data-results-label') || 'item') : 'item';
    var resultsLabelPlural = resultsEl
      ? (resultsEl.getAttribute('data-results-label-plural') || resultsLabel + 's')
      : 'items';

    gridItems.forEach(function (item) {
      var hubGroup = item.getAttribute('data-hub-group') || '';
      var matchesFilter = activeFilter === 'all'
        || hubGroup === activeFilter
        || (activeFilter === 'core' && item.classList.contains('is-core'))
        || (activeFilter === 'specialty' && item.classList.contains('is-specialty'));
      var title = normalize(item.getAttribute('data-title'));
      var summary = normalize(item.getAttribute('data-summary'));
      var matchesSearch = !query || title.indexOf(query) !== -1 || summary.indexOf(query) !== -1;
      var visible = matchesFilter && matchesSearch;

      item.hidden = !visible;
      item.classList.toggle('is-hidden', !visible);
      if (visible) {
        visibleCount += 1;
      }
    });

    if (resultsEl) {
      resultsEl.textContent = visibleCount === 1
        ? 'Showing 1 ' + resultsLabel
        : 'Showing ' + visibleCount + ' ' + resultsLabelPlural;
    }

    if (emptyEl) {
      emptyEl.hidden = visibleCount !== 0;
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }

  filterButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      activeFilter = button.getAttribute('data-filter') || 'all';
      filterButtons.forEach(function (btn) {
        var isActive = btn === button;
        btn.classList.toggle('is-active', isActive);
        btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
      });
      applyFilters();
    });
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      activeFilter = 'all';
      if (searchInput) {
        searchInput.value = '';
      }
      filterButtons.forEach(function (btn) {
        var isAll = btn.getAttribute('data-filter') === 'all';
        btn.classList.toggle('is-active', isAll);
        btn.setAttribute('aria-pressed', isAll ? 'true' : 'false');
      });
      applyFilters();
      if (searchInput) {
        searchInput.focus();
      }
    });
  }

  pillars.forEach(function (pillar) {
    pillar.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        pillar.classList.add('is-pressed');
        window.setTimeout(function () {
          pillar.classList.remove('is-pressed');
        }, 180);
      }
    });
  });

  applyFilters();
})();
