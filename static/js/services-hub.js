(function () {
  'use strict';

  var searchInput = document.getElementById('serviceSearch');
  var gridItems = document.querySelectorAll('.mp-services-grid-item');
  var resultsEl = document.getElementById('serviceResults');
  var emptyEl = document.getElementById('servicesEmpty');
  var resetBtn = document.getElementById('serviceReset');

  if (!gridItems.length) {
    return;
  }

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
      var title = normalize(item.getAttribute('data-title'));
      var summary = normalize(item.getAttribute('data-summary'));
      var visible = !query || title.indexOf(query) !== -1 || summary.indexOf(query) !== -1;

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

  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      if (searchInput) {
        searchInput.value = '';
      }
      applyFilters();
      if (searchInput) {
        searchInput.focus();
      }
    });
  }

  applyFilters();
})();
