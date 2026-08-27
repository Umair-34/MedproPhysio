(function () {
  const calendarEl = document.getElementById('panelCalendar');
  const detailEl = document.getElementById('appointmentDetail');
  const liveBadge = document.getElementById('liveBadge');
  if (!calendarEl || !window.FullCalendar) {
    return;
  }

  const apiUrl = '/panel/api/appointments/';
  const csrfToken = window.PANEL_CSRF || '';
  const defaultReject = window.PANEL_DEFAULT_REJECT
    || 'This slot is already booked. Kindly book another slot.';
  const rejectModal = document.getElementById('rejectConfirmModal');
  const rejectConfirmBtn = document.getElementById('rejectConfirmBtn');
  const rejectConfirmPatient = document.getElementById('rejectConfirmPatient');
  const detailsModal = document.getElementById('appointmentDetailModal');
  if (rejectModal) rejectModal.hidden = true;
  if (detailsModal) detailsModal.hidden = true;
  const statusLabels = {
    pending: 'Pending',
    confirmed: 'Confirmed',
    cancelled: 'Cancelled',
    rejected: 'Rejected',
    completed: 'Completed',
    no_show: 'No show',
  };
  let calendar;
  let pollTimer;
  let lastServerTime = null;
  let selectedEvent = null;

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function patientName(event) {
    const props = event.extendedProps || {};
    return props.patient_name || event.title || '—';
  }

  function renderDetail(event) {
    if (!detailEl || !event) return;
    selectedEvent = event;
    const props = event.extendedProps || {};
    const status = props.status || '';
    const canReview = status === 'pending';
    const rejectMessage = props.default_reject_message || defaultReject;
    const serviceLabel = props.service
      ? (
        props.duration_minutes
          ? props.service + ' (' + props.duration_minutes + ' Minutes)'
          : props.service
      )
      : '—';
    const timeOpts = { hour: 'numeric', minute: '2-digit' };
    const when = event.start
      ? event.start.toLocaleString(undefined, {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: 'numeric',
          minute: '2-digit',
        }) + (event.end ? ' – ' + event.end.toLocaleTimeString(undefined, timeOpts) : '')
      : '—';

    let actions = '';
    if (canReview) {
      actions = `
        <div class="panel-review-actions" id="reviewActions">
          <button type="button" class="panel-btn panel-btn-primary" data-review="approve">Approve</button>
        </div>
        <form class="panel-reject-form" id="rejectForm">
          <label for="rejectReason">Message to the client</label>
          <textarea id="rejectReason" name="reason" rows="4" placeholder="${escapeHtml(defaultReject)}">${escapeHtml(rejectMessage)}</textarea>
          <div class="panel-review-actions">
            <button type="button" class="panel-btn panel-btn-danger" data-review="reject">Send rejection</button>
          </div>
        </form>
      `;
    }

    detailEl.innerHTML = `
      <p class="panel-review-status" id="reviewStatus" hidden></p>
      <dl class="panel-detail-list">
        <div><dt>Patient</dt><dd>${escapeHtml(patientName(event))}</dd></div>
        <div><dt>Service</dt><dd>${escapeHtml(serviceLabel)}</dd></div>
        <div><dt>Appointment time</dt><dd>${escapeHtml(when)}</dd></div>
        <div><dt>Status</dt><dd><span class="panel-status panel-status-${escapeHtml(status)}">${escapeHtml(statusLabels[status] || status || '—')}</span></dd></div>
        <div><dt>Phone</dt><dd>${props.phone ? `<a href="tel:${escapeHtml(props.phone)}">${escapeHtml(props.phone)}</a>` : '—'}</dd></div>
        <div><dt>Email</dt><dd>${props.email ? `<a href="mailto:${escapeHtml(props.email)}">${escapeHtml(props.email)}</a>` : '—'}</dd></div>
        <div><dt>Notes</dt><dd>${escapeHtml(props.notes || '—')}</dd></div>
      </dl>
      ${actions}
    `;
    openDetailsModal();
  }

  function syncBodyScroll() {
    const detailsOpen = detailsModal && !detailsModal.hidden;
    const rejectOpen = rejectModal && !rejectModal.hidden;
    document.body.style.overflow = (detailsOpen || rejectOpen) ? 'hidden' : '';
  }

  function openDetailsModal() {
    if (!detailsModal) return;
    detailsModal.hidden = false;
    syncBodyScroll();
  }

  function closeDetailsModal() {
    closeRejectModal();
    if (!detailsModal) return;
    detailsModal.hidden = true;
    syncBodyScroll();
  }

  function setReviewStatus(message, isError) {
    const el = document.getElementById('reviewStatus');
    if (!el) return;
    el.hidden = false;
    el.textContent = message;
    el.classList.toggle('is-error', Boolean(isError));
  }

  function postReview(url, body) {
    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: body ? JSON.stringify(body) : '{}',
    }).then(function (response) {
      return response.json().then(function (data) {
        if (!response.ok) {
          throw new Error(data.error || 'Could not update this appointment.');
        }
        return data;
      });
    });
  }

  function afterReview(message, nextStatus) {
    closeRejectModal();
    setReviewStatus(message, false);
    const actions = document.getElementById('reviewActions');
    const form = document.getElementById('rejectForm');
    if (actions) actions.remove();
    if (form) form.remove();
    if (nextStatus) {
      const statusEl = detailEl.querySelector('.panel-status');
      if (statusEl) {
        statusEl.className = 'panel-status panel-status-' + nextStatus;
        statusEl.textContent = statusLabels[nextStatus] || nextStatus;
      }
    }
    if (calendar) calendar.refetchEvents();
  }

  function openRejectModal() {
    if (!rejectModal || !selectedEvent) return;
    if (rejectConfirmPatient) {
      rejectConfirmPatient.textContent = patientName(selectedEvent);
    }
    rejectModal.hidden = false;
    syncBodyScroll();
    const keepBtn = rejectModal.querySelector('.panel-modal__actions [data-modal-dismiss]');
    if (keepBtn) {
      keepBtn.focus();
    }
  }

  function closeRejectModal() {
    if (!rejectModal) return;
    rejectModal.hidden = true;
    if (rejectConfirmBtn) rejectConfirmBtn.disabled = false;
    syncBodyScroll();
  }

  function submitRejection() {
    if (!selectedEvent) return;
    const textarea = document.getElementById('rejectReason');
    const reason = textarea ? textarea.value.trim() : defaultReject;
    if (rejectConfirmBtn) rejectConfirmBtn.disabled = true;
    setReviewStatus('Sending rejection email…', false);
    postReview(apiUrl + selectedEvent.id + '/reject/', { reason: reason || defaultReject })
      .then(function () {
        afterReview('Rejected. The client has been emailed.', 'rejected');
      })
      .catch(function (err) {
        if (rejectConfirmBtn) rejectConfirmBtn.disabled = false;
        closeRejectModal();
        setReviewStatus(err.message, true);
      });
  }

  if (detailEl) {
    detailEl.addEventListener('click', function (event) {
      const button = event.target.closest('[data-review]');
      if (!button || !selectedEvent) return;
      const action = button.getAttribute('data-review');

      if (action === 'reject') {
        openRejectModal();
        return;
      }
      if (action === 'approve') {
        button.disabled = true;
        setReviewStatus('Sending confirmation email…', false);
        postReview(apiUrl + selectedEvent.id + '/approve/')
          .then(function () {
            afterReview('Approved. Confirmation email sent to the client.', 'confirmed');
          })
          .catch(function (err) {
            button.disabled = false;
            setReviewStatus(err.message, true);
          });
      }
    });

    detailEl.addEventListener('submit', function (event) {
      if (event.target.id !== 'rejectForm') return;
      event.preventDefault();
      openRejectModal();
    });
  }

  if (detailsModal) {
    detailsModal.addEventListener('click', function (event) {
      if (event.target.closest('[data-detail-dismiss]')) {
        closeDetailsModal();
      }
    });
  }
  if (rejectModal) {
    rejectModal.addEventListener('click', function (event) {
      if (event.target.closest('[data-modal-dismiss]')) {
        closeRejectModal();
      }
    });
  }
  if (rejectConfirmBtn) {
    rejectConfirmBtn.addEventListener('click', submitRejection);
  }
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    if (rejectModal && !rejectModal.hidden) {
      closeRejectModal();
      return;
    }
    if (detailsModal && !detailsModal.hidden) {
      closeDetailsModal();
    }
  });

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

  let stackTimer = null;

  function restackTimegridEvents() {
    document.querySelectorAll('.fc-timegrid-col-events').forEach(function (col) {
      const items = Array.from(col.querySelectorAll(':scope > .fc-timegrid-event-harness')).map(function (el) {
        return {
          el: el,
          top: el.offsetTop,
          height: el.offsetHeight,
          bottom: el.offsetTop + el.offsetHeight,
        };
      }).sort(function (a, b) {
        return a.top - b.top;
      });
      if (!items.length) {
        return;
      }

      const clusters = [];
      items.forEach(function (item) {
        const last = clusters[clusters.length - 1];
        if (last && item.top < last.bottom - 2) {
          last.items.push(item);
          last.bottom = Math.max(last.bottom, item.bottom);
        } else {
          clusters.push({ items: [item], top: item.top, bottom: item.bottom });
        }
      });

      clusters.forEach(function (cluster) {
        const count = cluster.items.length;
        const gap = 3;
        const minHeight = 48;
        const available = Math.max(minHeight, cluster.bottom - cluster.top);
        const height = Math.max(minHeight, Math.floor((available - gap * (count - 1)) / count));
        cluster.items.forEach(function (item, index) {
          const top = cluster.top + index * (height + gap);
          item.el.style.inset = 'auto';
          item.el.style.left = '0';
          item.el.style.right = '0';
          item.el.style.width = '100%';
          item.el.style.top = top + 'px';
          item.el.style.height = height + 'px';
          item.el.style.zIndex = String(5 + index);
        });
      });
    });
  }

  function scheduleRestack() {
    window.clearTimeout(stackTimer);
    stackTimer = window.setTimeout(restackTimegridEvents, 0);
  }

  function eventTimeLabel(date) {
    if (!date) return '';
    const opts = date.getMinutes()
      ? { hour: 'numeric', minute: '2-digit' }
      : { hour: 'numeric' };
    return date.toLocaleTimeString(undefined, opts);
  }

  function eventServiceLabel(event) {
    const props = event.extendedProps || {};
    if (!props.service) return event.title || 'Appointment';
    if (props.duration_minutes) {
      return props.service + ' · ' + props.duration_minutes + ' min';
    }
    return props.service;
  }

  function calendarIsMobile() {
    return window.matchMedia('(max-width: 767px)').matches;
  }

  function calendarToolbar() {
    if (calendarIsMobile()) {
      return {
        left: 'prev,next',
        center: 'title',
        right: 'listWeek,timeGridDay',
      };
    }
    return {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek',
    };
  }

  var lastMobile = calendarIsMobile();

  function syncCalendarLayout() {
    if (!calendar) return;
    var mobile = calendarIsMobile();
    if (mobile === lastMobile) return;
    lastMobile = mobile;
    calendar.setOption('headerToolbar', calendarToolbar());
    calendar.changeView(mobile ? 'listWeek' : 'timeGridWeek');
  }

  calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: calendarIsMobile() ? 'listWeek' : 'timeGridWeek',
    firstDay: 1,
    headerToolbar: calendarToolbar(),
    height: 'auto',
    nowIndicator: true,
    displayEventTime: false,
    allDaySlot: false,
    slotMinTime: '08:00:00',
    slotMaxTime: '20:00:00',
    scrollTime: '08:00:00',
    slotDuration: '00:15:00',
    slotLabelInterval: '01:00:00',
    businessHours: [
      { daysOfWeek: [1, 2, 3, 4, 5], startTime: '08:00', endTime: '20:00' },
      { daysOfWeek: [6], startTime: '08:00', endTime: '16:00' },
      { daysOfWeek: [0], startTime: '09:00', endTime: '14:00' },
    ],
    views: {
      dayGridMonth: {
        eventDisplay: 'block',
        dayMaxEvents: false,
        dayMaxEventRows: false,
      },
      listWeek: {
        type: 'list',
        duration: { days: 7 },
        validRange: function () {
          const start = new Date();
          start.setHours(0, 0, 0, 0);
          return { start: start };
        },
        visibleRange: function (currentDate) {
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          const start = new Date(currentDate.valueOf());
          start.setHours(0, 0, 0, 0);
          const rangeStart = start < today ? today : start;
          const rangeEnd = new Date(rangeStart);
          rangeEnd.setDate(rangeEnd.getDate() + 7);
          return { start: rangeStart, end: rangeEnd };
        },
      },
    },
    events: fetchEvents,
    eventMinHeight: 52,
    slotEventOverlap: false,
    eventContent: function (arg) {
      const props = arg.event.extendedProps || {};
      const service = eventServiceLabel(arg.event);
      const name = props.patient_name || '';
      const wrap = document.createElement('div');

      if (arg.view.type.indexOf('timeGrid') === 0) {
        wrap.className = 'panel-cal-event';
        const serviceEl = document.createElement('strong');
        serviceEl.textContent = service;
        wrap.appendChild(serviceEl);
        if (name) {
          const nameEl = document.createElement('span');
          nameEl.textContent = name;
          wrap.appendChild(nameEl);
        }
        return { domNodes: [wrap] };
      }

      wrap.className = 'panel-cal-event panel-cal-event--inline';
      const label = document.createElement('span');
      label.className = 'panel-cal-event__label';
      label.textContent = [eventTimeLabel(arg.event.start), service, name]
        .filter(Boolean)
        .join(' · ');
      wrap.appendChild(label);
      wrap.title = [statusLabels[props.status] || '', label.textContent]
        .filter(Boolean)
        .join(': ');
      return { domNodes: [wrap] };
    },
    eventDidMount: function (info) {
      const status = (info.event.extendedProps || {}).status;
      if (status) {
        info.el.classList.add('panel-cal-status-' + status);
      }
      scheduleRestack();
    },
    datesSet: function () {
      scheduleRestack();
    },
    eventsSet: function () {
      scheduleRestack();
    },
    eventClick: function (info) {
      info.jsEvent.preventDefault();
      renderDetail(info.event);
    },
    windowResize: function () {
      syncCalendarLayout();
    },
  });

  calendar.render();

  document.querySelectorAll('[data-appointment-id]').forEach(function (item) {
    function openFromList() {
      const id = item.getAttribute('data-appointment-id');
      const event = calendar.getEventById(id);
      if (event) {
        renderDetail(event);
        return;
      }
      const start = new Date();
      start.setHours(0, 0, 0, 0);
      const end = new Date(start);
      end.setDate(end.getDate() + 1);
      fetch(
        apiUrl + '?start=' + encodeURIComponent(start.toISOString()) + '&end=' + encodeURIComponent(end.toISOString()),
        { credentials: 'same-origin' }
      )
        .then(function (response) { return response.json(); })
        .then(function (data) {
          const match = (data.events || []).find(function (ev) {
            return String(ev.id) === String(id);
          });
          if (!match) return;
          renderDetail({
            id: match.id,
            title: match.title,
            start: match.start ? new Date(match.start) : null,
            end: match.end ? new Date(match.end) : null,
            extendedProps: match.extendedProps || {},
          });
        })
        .catch(function () {});
    }
    item.addEventListener('click', openFromList);
    item.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openFromList();
      }
    });
  });

  window.addEventListener('resize', scheduleRestack);

  pollTimer = window.setInterval(pollUpdates, 60000);
})();
