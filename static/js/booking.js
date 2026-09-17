(function () {
    const API_BASE = '/api/bookings';
    const LOCALE = 'en-CA';
    const WEEKDAY_PLURALS = ['Mondays', 'Tuesdays', 'Wednesdays', 'Thursdays', 'Fridays', 'Saturdays', 'Sundays'];
    const WEEKDAY_HEADERS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const HEADER_PYTHON_DAYS = [6, 0, 1, 2, 3, 4, 5];
    const form = document.getElementById('bookingForm');
    const alertBox = document.getElementById('bookingAlert');
    const confirmationBox = document.getElementById('bookingConfirmation');
    const confirmationDetails = document.getElementById('confirmationDetails');
    const serviceSelect = document.getElementById('service_id');
    const durationSelect = document.getElementById('duration_minutes');
    const serviceGrid = document.getElementById('bookingServiceGrid');
    const dateInput = document.getElementById('date');
    const dateHint = document.getElementById('dateHint');
    const calendarEl = document.getElementById('bookingCalendar');
    const dateGroup = dateInput ? dateInput.closest('.booking-date-group') : null;
    const slotSelect = document.getElementById('slot');
    const slotHint = document.getElementById('slotHint');
    const slotsEl = document.getElementById('bookingSlots');
    const slotGroup = slotSelect ? slotSelect.closest('.booking-slot-group') : null;
    const submitBtn = document.getElementById('bookingSubmit');

    if (!form) {
        return;
    }

    let clinicWeekdays = [0, 1, 2, 3, 4, 5];
    let calendarCursor = startOfDay(new Date());
    calendarCursor.setDate(1);

    function showAlert(message, type) {
        const toastType = type === 'danger' || type === 'error' ? 'error' : (type || 'error');
        if (window.mpToast) {
            window.mpToast(message, toastType);
            return;
        }
        if (alertBox) {
            alertBox.textContent = message;
            alertBox.className = 'alert alert-' + (type || 'danger');
            alertBox.classList.remove('d-none');
            return;
        }
        window.alert(message);
    }

    function hideAlert() {
        if (alertBox) {
            alertBox.classList.add('d-none');
        }
    }

    function startOfDay(value) {
        return new Date(value.getFullYear(), value.getMonth(), value.getDate());
    }

    function toISODate(value) {
        const year = value.getFullYear();
        const month = String(value.getMonth() + 1).padStart(2, '0');
        const day = String(value.getDate()).padStart(2, '0');
        return year + '-' + month + '-' + day;
    }

    function parseISODate(value) {
        if (!value) {
            return null;
        }
        const parts = value.split('-');
        if (parts.length !== 3) {
            return null;
        }
        const year = parseInt(parts[0], 10);
        const month = parseInt(parts[1], 10) - 1;
        const day = parseInt(parts[2], 10);
        if (Number.isNaN(year) || Number.isNaN(month) || Number.isNaN(day)) {
            return null;
        }
        return new Date(year, month, day);
    }

    function pythonWeekday(value) {
        return (value.getDay() + 6) % 7;
    }

    function formatWeekdaysLabel(days) {
        const names = (days || []).map(function (day) {
            return WEEKDAY_PLURALS[day];
        });
        if (!names.length) {
            return '';
        }
        if (names.length === 1) {
            return names[0];
        }
        if (names.length === 2) {
            return names[0] + ' and ' + names[1];
        }
        return names.slice(0, -1).join(', ') + ', and ' + names[names.length - 1];
    }

    function parseWeekdays(value) {
        if (!value) {
            return [];
        }
        return String(value).split(',').map(function (item) {
            return parseInt(item, 10);
        }).filter(function (day) {
            return day >= 0 && day <= 6;
        });
    }

    function getSelectedWeekdays() {
        const card = serviceGrid && serviceGrid.querySelector('.booking-service-card.is-selected');
        if (card && card.dataset.availableWeekdays !== undefined) {
            return parseWeekdays(card.dataset.availableWeekdays);
        }
        return clinicWeekdays.slice();
    }

    function hasSelectedService() {
        return Boolean(serviceSelect.value);
    }

    function isLimitedSchedule(weekdays) {
        return Boolean(weekdays && clinicWeekdays.length && weekdays.length < clinicWeekdays.length);
    }

    function getCsrfToken() {
        const input = form.querySelector('[name="csrfmiddlewaretoken"]');
        if (input && input.value) {
            return input.value;
        }
        const match = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    let turnstileWidgetId = null;

    function whenTurnstileReady(callback) {
        function invoke() {
            if (window.turnstile && typeof window.turnstile.render === 'function') {
                callback();
                return true;
            }
            return false;
        }
        if (invoke()) {
            return;
        }
        if (window.turnstile && typeof window.turnstile.ready === 'function') {
            window.turnstile.ready(function () {
                invoke();
            });
        }
        let attempts = 0;
        const timer = window.setInterval(function () {
            attempts += 1;
            if (invoke() || attempts > 150) {
                window.clearInterval(timer);
            }
        }, 100);
    }

    function renderTurnstile() {
        const mount = document.getElementById('cf-turnstile-booking');
        if (!mount || !mount.dataset.sitekey) {
            return;
        }
        whenTurnstileReady(function () {
            if (turnstileWidgetId !== null || typeof window.turnstile.render !== 'function') {
                return;
            }
            if (mount.querySelector('iframe, input[name="cf-turnstile-response"]')) {
                return;
            }
            turnstileWidgetId = window.turnstile.render(mount, {
                sitekey: mount.dataset.sitekey,
                action: mount.dataset.action || 'booking',
                theme: 'light',
            });
        });
    }

    function getTurnstileToken() {
        if (window.turnstile && turnstileWidgetId !== null && typeof window.turnstile.getResponse === 'function') {
            const token = window.turnstile.getResponse(turnstileWidgetId);
            if (token) {
                return token;
            }
        }
        if (window.turnstile && typeof window.turnstile.getResponse === 'function') {
            const token = window.turnstile.getResponse();
            if (token) {
                return token;
            }
        }
        const input = form.querySelector('[name="cf-turnstile-response"]');
        return input ? input.value : '';
    }

    function resetTurnstile() {
        if (window.turnstile && typeof window.turnstile.reset === 'function') {
            if (turnstileWidgetId !== null) {
                window.turnstile.reset(turnstileWidgetId);
            } else {
                window.turnstile.reset();
            }
        }
    }

    function turnstileIsRequired() {
        return Boolean(form.querySelector('.cf-turnstile, .mp-turnstile'));
    }

    async function fetchJson(url) {
        const response = await fetch(url);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        return data;
    }

    function setMinDate() {
        if (!dateInput) {
            return;
        }
        dateInput.min = toISODate(startOfDay(new Date()));
    }

    function updateDateHint(weekdays) {
        if (!dateHint) {
            return;
        }
        if (!hasSelectedService()) {
            dateHint.textContent = 'Highlighted days are open at the clinic. Choose a service to see its schedule.';
            return;
        }
        if (!weekdays.length) {
            dateHint.textContent = 'This service is not currently offered for online booking. Please call the clinic.';
            return;
        }
        if (isLimitedSchedule(weekdays)) {
            dateHint.textContent = 'This service is offered on ' + formatWeekdaysLabel(weekdays)
                + '. Highlighted dates are available to book.';
            return;
        }
        dateHint.textContent = 'Pick a highlighted day, then choose an open time.';
    }

    function formatSlotLabel(iso) {
        return new Date(iso).toLocaleTimeString(LOCALE, {
            hour: 'numeric',
            minute: '2-digit',
        });
    }

    function slotPeriod(iso) {
        const hour = new Date(iso).getHours();
        if (hour < 12) {
            return 'Morning';
        }
        if (hour < 17) {
            return 'Afternoon';
        }
        return 'Evening';
    }

    function selectedDateLabel() {
        const selected = parseISODate(dateInput.value);
        if (!selected) {
            return '';
        }
        return selected.toLocaleDateString(LOCALE, {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
        });
    }

    function enhanceSlots() {
        if (!slotsEl || slotsEl.dataset.ready === 'true') {
            return;
        }
        slotsEl.hidden = false;
        slotsEl.setAttribute('role', 'listbox');
        slotsEl.setAttribute('aria-label', 'Available times');
        if (slotGroup) {
            slotGroup.classList.add('is-enhanced');
        }
        slotsEl.addEventListener('click', function (event) {
            const btn = event.target.closest('[data-slot-value]');
            if (!btn || btn.disabled) {
                return;
            }
            slotSelect.value = btn.getAttribute('data-slot-value');
            slotSelect.disabled = false;
            slotSelect.dispatchEvent(new Event('change'));
        });
        slotsEl.dataset.ready = 'true';
    }

    function setSlotMessage(message) {
        enhanceSlots();
        if (!slotsEl) {
            return;
        }
        slotsEl.innerHTML = '<p class="booking-slots__empty">' + message + '</p>';
    }

    function syncSlotSelection() {
        if (!slotsEl) {
            return;
        }
        const selected = slotSelect.value;
        slotsEl.querySelectorAll('[data-slot-value]').forEach(function (el) {
            const isSelected = el.getAttribute('data-slot-value') === selected;
            el.classList.toggle('is-selected', isSelected);
            el.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
        });
    }

    function renderSlotButtons(slots) {
        enhanceSlots();
        if (!slotsEl) {
            return;
        }

        const groups = { Morning: [], Afternoon: [], Evening: [] };
        const order = ['Morning', 'Afternoon', 'Evening'];
        slots.forEach(function (slot) {
            groups[slotPeriod(slot.start_datetime)].push(slot);
        });
        const activeGroups = order.filter(function (period) {
            return groups[period].length;
        });
        const showHeadings = activeGroups.length > 1;
        const dateLabel = selectedDateLabel();

        let html = dateLabel ? '<p class="booking-slots__date">' + dateLabelEscape(dateLabel) + '</p>' : '';
        activeGroups.forEach(function (period) {
            if (showHeadings) {
                html += '<p class="booking-slots__period">' + period + '</p>';
            }
            html += '<div class="booking-slots__grid">';
            groups[period].forEach(function (slot) {
                const label = formatSlotLabel(slot.start_datetime);
                html += '<button type="button" class="booking-slot" data-slot-value="'
                    + slot.start_datetime + '" aria-pressed="false">'
                    + label + '</button>';
            });
            html += '</div>';
        });
        slotsEl.innerHTML = html;
        syncSlotSelection();
    }

    function dateLabelEscape(value) {
        return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function updateSubmitState() {
        if (!submitBtn) {
            return;
        }
        const hasService = Boolean(serviceSelect.value) && Boolean(durationSelect && durationSelect.value);
        const hasSchedule = hasService && Boolean(dateInput.value) && Boolean(slotSelect.value);
        const firstName = document.getElementById('first_name');
        const lastName = document.getElementById('last_name');
        const email = document.getElementById('email');
        const phone = document.getElementById('phone');
        const hasContact = Boolean(
            firstName && firstName.value.trim()
            && lastName && lastName.value.trim()
            && email && email.value.trim()
            && phone && phone.value.trim()
        );
        submitBtn.disabled = !(hasSchedule && hasContact);
    }

    function ensureCalendar() {
        if (!calendarEl || calendarEl.dataset.ready === 'true') {
            return;
        }

        calendarEl.innerHTML = ''
            + '<div class="booking-calendar__header">'
            + '<button type="button" class="booking-calendar__nav" data-cal-nav="-1" aria-label="Previous month">'
            + '<i class="fa-solid fa-chevron-left" aria-hidden="true"></i></button>'
            + '<p class="booking-calendar__month" data-cal-month></p>'
            + '<button type="button" class="booking-calendar__nav" data-cal-nav="1" aria-label="Next month">'
            + '<i class="fa-solid fa-chevron-right" aria-hidden="true"></i></button>'
            + '</div>'
            + '<div class="booking-calendar__weekdays" data-cal-weekdays></div>'
            + '<div class="booking-calendar__grid" data-cal-days role="listbox" aria-label="Appointment dates"></div>';

        calendarEl.addEventListener('click', function (event) {
            const nav = event.target.closest('[data-cal-nav]');
            if (nav && !nav.disabled) {
                const offset = parseInt(nav.getAttribute('data-cal-nav'), 10);
                calendarCursor = new Date(calendarCursor.getFullYear(), calendarCursor.getMonth() + offset, 1);
                renderCalendar();
                return;
            }
            const dayBtn = event.target.closest('[data-cal-date]');
            if (!dayBtn || dayBtn.disabled) {
                return;
            }
            dateInput.value = dayBtn.getAttribute('data-cal-date');
            dateInput.dispatchEvent(new Event('change'));
            renderCalendar();
        });

        calendarEl.hidden = false;
        if (dateGroup) {
            dateGroup.classList.add('is-enhanced');
        }
        calendarEl.dataset.ready = 'true';
    }

    function renderCalendar() {
        if (!calendarEl) {
            return;
        }
        ensureCalendar();

        const weekdays = getSelectedWeekdays();
        const today = startOfDay(new Date());
        const selected = parseISODate(dateInput.value);
        const year = calendarCursor.getFullYear();
        const month = calendarCursor.getMonth();
        const first = new Date(year, month, 1);
        const startOffset = first.getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const monthLabel = calendarEl.querySelector('[data-cal-month]');
        const weekdayWrap = calendarEl.querySelector('[data-cal-weekdays]');
        const dayWrap = calendarEl.querySelector('[data-cal-days]');
        const prevBtn = calendarEl.querySelector('[data-cal-nav="-1"]');
        const currentMonthStart = new Date(today.getFullYear(), today.getMonth(), 1);

        calendarEl.classList.toggle('is-limited', isLimitedSchedule(weekdays));
        if (monthLabel) {
            monthLabel.textContent = first.toLocaleDateString(LOCALE, { month: 'long', year: 'numeric' });
        }
        if (prevBtn) {
            prevBtn.disabled = calendarCursor <= currentMonthStart;
        }

        if (weekdayWrap) {
            weekdayWrap.innerHTML = HEADER_PYTHON_DAYS.map(function (day, index) {
                const available = weekdays.indexOf(day) !== -1;
                return '<span class="booking-calendar__weekday' + (available ? ' is-available' : '') + '">'
                    + WEEKDAY_HEADERS[index] + '</span>';
            }).join('');
        }

        if (!dayWrap) {
            updateDateHint(weekdays);
            return;
        }

        const cells = [];
        for (let i = 0; i < startOffset; i += 1) {
            cells.push('<button type="button" class="booking-calendar__day is-outside" tabindex="-1" disabled></button>');
        }
        for (let day = 1; day <= daysInMonth; day += 1) {
            const current = new Date(year, month, day);
            const iso = toISODate(current);
            const pyDay = pythonWeekday(current);
            const isPast = current < today;
            const isAvailable = weekdays.indexOf(pyDay) !== -1;
            const disabled = isPast || !isAvailable;
            const classes = ['booking-calendar__day'];
            if (isAvailable && !isPast) {
                classes.push('is-available');
            }
            if (iso === toISODate(today)) {
                classes.push('is-today');
            }
            if (selected && iso === toISODate(selected)) {
                classes.push('is-selected');
            }
            if (disabled) {
                classes.push('is-disabled');
            }
            cells.push(
                '<button type="button" class="' + classes.join(' ') + '"'
                + ' data-cal-date="' + iso + '"'
                + (disabled ? ' disabled' : '')
                + ' aria-label="' + current.toLocaleDateString(LOCALE, { weekday: 'long', month: 'long', day: 'numeric' }) + '"'
                + (selected && iso === toISODate(selected) ? ' aria-selected="true"' : '')
                + '>' + day + '</button>'
            );
        }
        dayWrap.innerHTML = cells.join('');
        updateDateHint(weekdays);
    }

    function syncDateWithService() {
        const weekdays = getSelectedWeekdays();
        const selected = parseISODate(dateInput.value);
        if (selected && (!hasSelectedService() || weekdays.indexOf(pythonWeekday(selected)) === -1)) {
            dateInput.value = '';
        }
        renderCalendar();
    }

    function selectServiceCard(card, shouldLoadSlots) {
        if (!card || !serviceSelect || !durationSelect) {
            return;
        }
        serviceGrid.querySelectorAll('.booking-service-card').forEach(function (el) {
            el.classList.remove('is-selected');
            el.setAttribute('aria-pressed', 'false');
        });
        card.classList.add('is-selected');
        card.setAttribute('aria-pressed', 'true');
        serviceSelect.value = card.dataset.serviceId || '';
        durationSelect.value = card.dataset.duration || '';
        syncDateWithService();
        updateSubmitState();
        if (shouldLoadSlots !== false) {
            loadSlots().catch(function (err) {
                showAlert(err.message, 'danger');
            });
        }
    }

    function restoreSelectedCard() {
        const serviceId = serviceSelect.value;
        const duration = durationSelect.value;
        if (!serviceGrid || !serviceId || !duration) {
            return;
        }
        const card = serviceGrid.querySelector(
            '.booking-service-card[data-service-id="' + serviceId + '"][data-duration="' + duration + '"]'
        );
        if (card) {
            selectServiceCard(card, false);
        }
    }

    function renderServiceCards(services) {
        if (!serviceGrid) {
            return;
        }
        serviceGrid.innerHTML = '';
        services.forEach(function (service) {
            const durations = (service.durations && service.durations.length)
                ? service.durations
                : [service.duration_minutes];
            durations.forEach(function (minutes) {
                const card = document.createElement('button');
                card.type = 'button';
                card.className = 'booking-service-card';
                card.dataset.serviceId = String(service.id);
                card.dataset.duration = String(minutes);
                card.dataset.availableWeekdays = (service.available_weekdays || []).join(',');
                card.setAttribute('aria-pressed', 'false');

                const name = document.createElement('span');
                name.className = 'booking-service-card__name';
                name.textContent = service.name;

                const time = document.createElement('span');
                time.className = 'booking-service-card__time';
                time.textContent = minutes + ' Minutes';

                card.appendChild(name);
                card.appendChild(time);
                serviceGrid.appendChild(card);
            });
        });
        restoreSelectedCard();
        renderCalendar();
    }

    async function loadServices() {
        const data = await fetchJson(API_BASE + '/services/');
        if (Array.isArray(data.clinic_weekdays) && data.clinic_weekdays.length) {
            clinicWeekdays = data.clinic_weekdays;
        }
        renderServiceCards(data.services || []);
    }

    async function loadSlots() {
        enhanceSlots();
        slotSelect.innerHTML = '<option value="" disabled selected>Loading times...</option>';
        slotSelect.disabled = true;
        setSlotMessage('Checking availability...');
        if (slotHint) {
            slotHint.textContent = 'Checking availability...';
        }

        if (!serviceSelect.value || (durationSelect && !durationSelect.value)) {
            slotSelect.innerHTML = '<option value="" disabled selected>Select a service first</option>';
            setSlotMessage(dateInput.value
                ? 'Choose a service to see open times for this date.'
                : 'Pick a highlighted date to see open times.');
            if (slotHint) {
                slotHint.textContent = 'Times update after you choose a service, length, and date.';
            }
            updateSubmitState();
            return;
        }

        if (!dateInput.value) {
            slotSelect.innerHTML = '<option value="" disabled selected>Select a date first</option>';
            setSlotMessage('Pick a highlighted date to see open times.');
            if (slotHint) {
                slotHint.textContent = 'Times update after you choose a service, length, and date.';
            }
            updateSubmitState();
            return;
        }

        const url = API_BASE + '/slots/?service_id=' + encodeURIComponent(serviceSelect.value)
            + '&date=' + encodeURIComponent(dateInput.value)
            + (durationSelect && durationSelect.value
                ? '&duration_minutes=' + encodeURIComponent(durationSelect.value)
                : '');

        const data = await fetchJson(url);
        slotSelect.innerHTML = '';

        if (!data.slots.length) {
            slotSelect.innerHTML = '<option value="" disabled selected>No times available</option>';
            setSlotMessage('No times on this date. Try another highlighted day.');
            if (slotHint) {
                slotHint.textContent = 'Try another highlighted date, or call the clinic for help.';
            }
            updateSubmitState();
            return;
        }

        slotSelect.appendChild(new Option('Select a time', '', true, true));
        data.slots.forEach(function (slot) {
            slotSelect.appendChild(new Option(formatSlotLabel(slot.start_datetime), slot.start_datetime));
        });
        slotSelect.disabled = false;
        renderSlotButtons(data.slots);
        if (slotHint) {
            slotHint.textContent = data.slots.length + ' time' + (data.slots.length === 1 ? '' : 's')
                + ' available on this date.';
        }
        updateSubmitState();
    }

    if (serviceGrid) {
        serviceGrid.addEventListener('click', function (event) {
            const card = event.target.closest('.booking-service-card');
            if (!card) {
                return;
            }
            selectServiceCard(card);
        });
    }

    if (dateInput) {
        dateInput.addEventListener('change', function () {
            loadSlots().catch(function (err) {
                showAlert(err.message, 'danger');
            });
            updateSubmitState();
            renderCalendar();
        });
    }

    if (slotSelect) {
        slotSelect.addEventListener('change', function () {
            syncSlotSelection();
            updateSubmitState();
        });
    }

    ['first_name', 'last_name', 'email', 'phone'].forEach(function (fieldId) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', updateSubmitState);
        }
    });

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        hideAlert();
        if (turnstileIsRequired() && !getTurnstileToken()) {
            showAlert('Please complete the verification checkbox, then try again.', 'danger');
            return;
        }
        submitBtn.disabled = true;
        const submitLabel = submitBtn.querySelector('span');
        if (submitLabel) {
            submitLabel.textContent = 'Sending request...';
        }

        const payload = {
            service_id: parseInt(serviceSelect.value, 10),
            duration_minutes: durationSelect ? parseInt(durationSelect.value, 10) : undefined,
            start_datetime: slotSelect.value,
            first_name: document.getElementById('first_name').value.trim(),
            last_name: document.getElementById('last_name').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            customer_notes: document.getElementById('customer_notes').value.trim(),
            company_website: (form.querySelector('[name="company_website"]') || {}).value || '',
            form_token: (form.querySelector('[name="form_token"]') || {}).value || '',
            turnstile_token: getTurnstileToken(),
        };

        try {
            const response = await fetch(API_BASE + '/appointments/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify(payload),
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Booking failed');
            }

            form.classList.add('d-none');
            confirmationBox.classList.remove('d-none');

            const appt = data.appointment;
            const when = new Date(appt.start_datetime).toLocaleString(LOCALE, {
                weekday: 'long',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: '2-digit',
            });
            const lengthLabel = appt.duration_minutes ? ' (' + appt.duration_minutes + ' Minutes)' : '';
            confirmationDetails.textContent =
                appt.service + lengthLabel + ' on ' + when
                + '. We will email you once the clinic approves or cannot take this time. Your reference is '
                + appt.confirmation_token + '.';
        } catch (err) {
            showAlert(err.message, 'danger');
            submitBtn.disabled = false;
            if (submitLabel) {
                submitLabel.textContent = 'Request Booking';
            }
            updateSubmitState();
            resetTurnstile();
        }
    });

    const fromMarkup = parseWeekdays(calendarEl && calendarEl.dataset.clinicWeekdays);
    if (fromMarkup.length) {
        clinicWeekdays = fromMarkup;
    }
    enhanceSlots();
    renderCalendar();
    setMinDate();
    updateSubmitState();
    renderTurnstile();
    setSlotMessage('Pick a highlighted date to see open times.');
    loadServices().catch(function (err) {
        showAlert(err.message, 'danger');
        renderCalendar();
    });
})();
