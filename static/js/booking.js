(function () {
    const API_BASE = '/api/bookings';
    const LOCALE = 'en-CA';
    const form = document.getElementById('bookingForm');
    const alertBox = document.getElementById('bookingAlert');
    const confirmationBox = document.getElementById('bookingConfirmation');
    const confirmationDetails = document.getElementById('confirmationDetails');
    const serviceSelect = document.getElementById('service_id');
    const durationSelect = document.getElementById('duration_minutes');
    const serviceGrid = document.getElementById('bookingServiceGrid');
    const dateInput = document.getElementById('date');
    const slotSelect = document.getElementById('slot');
    const slotHint = document.getElementById('slotHint');
    const submitBtn = document.getElementById('bookingSubmit');

    if (!form) {
        return;
    }

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
        if (window.turnstile && typeof window.turnstile.ready === 'function') {
            window.turnstile.ready(callback);
            return;
        }
        let attempts = 0;
        const timer = window.setInterval(function () {
            attempts += 1;
            if (window.turnstile && typeof window.turnstile.ready === 'function') {
                window.clearInterval(timer);
                window.turnstile.ready(callback);
            } else if (attempts > 50) {
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
        const today = new Date();
        dateInput.min = today.toISOString().split('T')[0];
    }

    function updateSubmitState() {
        const hasService = Boolean(serviceSelect.value) && Boolean(durationSelect && durationSelect.value);
        const hasSchedule = hasService && Boolean(dateInput.value) && Boolean(slotSelect.value);
        const hasContact = Boolean(
            document.getElementById('first_name').value.trim()
            && document.getElementById('last_name').value.trim()
            && document.getElementById('email').value.trim()
            && document.getElementById('phone').value.trim()
        );
        submitBtn.disabled = !(hasSchedule && hasContact);
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
    }

    async function loadServices() {
        const data = await fetchJson(API_BASE + '/services/');
        renderServiceCards(data.services || []);
    }

    async function loadSlots() {
        slotSelect.innerHTML = '<option value="" disabled selected>Loading times...</option>';
        slotSelect.disabled = true;
        if (slotHint) {
            slotHint.textContent = 'Checking availability...';
        }

        if (!serviceSelect.value || !dateInput.value || (durationSelect && !durationSelect.value)) {
            slotSelect.innerHTML = '<option value="" disabled selected>Select a date first</option>';
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
            if (slotHint) {
                slotHint.textContent = 'Try another date, or call the clinic for help.';
            }
            updateSubmitState();
            return;
        }

        slotSelect.appendChild(new Option('Select a time', '', true, true));
        data.slots.forEach(function (slot) {
            const start = new Date(slot.start_datetime);
            const label = start.toLocaleString(LOCALE, {
                weekday: 'short',
                hour: 'numeric',
                minute: '2-digit',
            });
            slotSelect.appendChild(new Option(label, slot.start_datetime));
        });
        slotSelect.disabled = false;
        if (slotHint) {
            slotHint.textContent = data.slots.length + ' time' + (data.slots.length === 1 ? '' : 's') + ' available on this date.';
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

    dateInput.addEventListener('change', function () {
        loadSlots().catch(function (err) {
            showAlert(err.message, 'danger');
        });
        updateSubmitState();
    });

    slotSelect.addEventListener('change', updateSubmitState);

    ['first_name', 'last_name', 'email', 'phone'].forEach(function (fieldId) {
        document.getElementById(fieldId).addEventListener('input', updateSubmitState);
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

    setMinDate();
    updateSubmitState();
    renderTurnstile();
    loadServices().catch(function (err) {
        showAlert(err.message, 'danger');
    });
})();
