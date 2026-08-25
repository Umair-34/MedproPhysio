(function () {
  const calendarEl = document.getElementById('panelCalendar');
  const detailEl = document.getElementById('appointmentDetail');
  const liveBadge = document.getElementById('liveBadge');
  if (!calendarEl || !window.FullCalendar) {
    return;
  }

  const apiUrl = '/panel/api/appointments/';
  let calendar;
  let pollTimer;
  let lastServerTime = null;

  function renderDetail(event) {
    if (!detailEl) return;
    const props = event.extendedProps || {};
    detailEl.innerHTML = `
      <h2>Appointment details</h2>
      <dl class="panel-detail-list">
        <div><dt>Patient</dt><dd>${event.title.split(' — ').slice(1).join(' — ') || event.title}</dd></div>
        <div><dt>Service</dt><dd>${props.service || '—'}</dd></div>
        <div><dt>When</dt><dd>${event.start.toLocaleString()} – ${event.end.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })}</dd></div>
        <div><dt>Status</dt><dd><span class="panel-status panel-status-${props.status}">${props.status || '—'}</span></dd></div>
        <div><dt>Phone</dt><dd>${props.phone ? `<a href="tel:${props.phone}">${props.phone}</a>` : '—'}</dd></div>
        <div><dt>Email</dt><dd>${props.email ? `<a href="mailto:${props.email}">${props.email}</a>` : '—'}</dd></div>
        <div><dt>Notes</dt><dd>${props.notes || '—'}</dd></div>
      </dl>
    `;
  }

  function flashLive() {
    if (!liveBadge) return;
    liveBadge.classList.add('is-pulse');
    window.setTimeout(function () {
      liveBadge.classList.remove('is-pulse');
    }, 800);
  }

  function fetchEvents(info, successCallback, failureCallback) {
    const params = new URLSearchParams({
      start: info.startStr,
      end: info.endStr,
    });
    fetch(`${apiUrl}?${params.toString()}`, { credentials: 'same-origin' })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        lastServerTime = data.server_time;
        successCallback(data.events);
      })
      .catch(failureCallback);
  }

  function pollUpdates() {
    if (!calendar) return;
    const params = new URLSearchParams();
    if (lastServerTime) {
      params.set('since', lastServerTime);
    }
    fetch(`${apiUrl}?${params.toString()}`, { credentials: 'same-origin' })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (data.events && data.events.length) {
          calendar.refetchEvents();
          flashLive();
        }
        lastServerTime = data.server_time;
      })
      .catch(function () {});
  }

  calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek',
    },
    height: 'auto',
    nowIndicator: true,
    events: fetchEvents,
    eventClick: function (info) {
      renderDetail(info.event);
    },
  });

  calendar.render();

  pollTimer = window.setInterval(pollUpdates, 60000);
})();
