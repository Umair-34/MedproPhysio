(function () {
    const API_BASE = '/api/bookings';
    const LOCALE = 'en-CA';
    const form = document.getElementById('bookingForm');
    const alertBox = document.getElementById('bookingAlert');
    const confirmationBox = document.getElementById('bookingConfirmation');
    const confirmationDetails = document.getElementById('confirmationDetails');
    const serviceSelect = document.getElementById('service_id');
    const dateInput = document.getElementById('date');
    const slotSelect = document.getElementById('slot');
    const slotHint = document.getElementById('slotHint');
    const submitBtn = document.getElementById('bookingSubmit');
    const stepperItems = document.querySelectorAll('.booking-stepper-item');

    if (!form) {
        return;
    }

    function showAlert(message, type) {
        alertBox.textContent = message;
        alertBox.className = 'alert alert-' + type;
        alertBox.classList.remove('d-none');
    }

    function hideAlert() {
        alertBox.classList.add('d-none');
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
            return window.turnstile.getResponse(turnstileWidgetId) || '';
        }
        const input = form.querySelector('[name="cf-turnstile-response"]');
        return input ? input.value : '';
    }

    function resetTurnstile() {
        if (window.turnstile && turnstileWidgetId !== null && typeof window.turnstile.reset === 'function') {
            window.turnstile.reset(turnstileWidgetId);
        }
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

    function updateStepper() {
        const hasService = Boolean(serviceSelect.value);
        const hasSchedule = hasService && Boolean(dateInput.value) && Boolean(slotSelect.value);
        const hasContact = Boolean(
            document.getElementById('first_name').value.trim()
            && document.getElementById('last_name').value.trim()
            && document.getElementById('email').value.trim()
            && document.getElementById('phone').value.trim()
        );

        const activeStep = hasSchedule && hasContact ? 4 : hasSchedule ? 3 : hasService ? 2 : 1;

        stepperItems.forEach(function (item) {
            const step = parseInt(item.dataset.step, 10);
            item.classList.toggle('is-active', step === activeStep);
            item.classList.toggle('is-complete', step < activeStep);
        });

        submitBtn.disabled = !(hasSchedule && hasContact);
    }

    async function loadServices() {
        const data = await fetchJson(API_BASE + '/services/');
        serviceSelect.innerHTML = '<option value="" disabled selected>Select a service</option>';
        data.services.forEach(function (service) {
            const option = document.createElement('option');
            option.value = service.id;
            option.textContent = service.name + ' (' + service.duration_minutes + ' min)';
            serviceSelect.appendChild(option);
        });
    }

    async function loadSlots() {
        slotSelect.innerHTML = '<option value="" disabled selected>Loading times...</option>';
        slotSelect.disabled = true;
        if (slotHint) {
            slotHint.textContent = 'Checking availability...';
        }

        if (!serviceSelect.value || !dateInput.value) {
            slotSelect.innerHTML = '<option value="" disabled selected>Select a date first</option>';
            if (slotHint) {
                slotHint.textContent = 'Times update after you choose a service and date.';
            }
            updateStepper();
            return;
        }

        const url = API_BASE + '/slots/?service_id=' + encodeURIComponent(serviceSelect.value)
            + '&date=' + encodeURIComponent(dateInput.value);

        const data = await fetchJson(url);
        slotSelect.innerHTML = '';

        if (!data.slots.length) {
            slotSelect.innerHTML = '<option value="" disabled selected>No times available</option>';
            if (slotHint) {
                slotHint.textContent = 'Try another date, or call the clinic for help.';
            }
            updateStepper();
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
        updateStepper();
    }

    serviceSelect.addEventListener('change', function () {
        loadSlots().catch(function (err) {
            showAlert(err.message, 'danger');
        });
        updateStepper();
    });

    dateInput.addEventListener('change', function () {
        loadSlots().catch(function (err) {
            showAlert(err.message, 'danger');
        });
        updateStepper();
    });

    slotSelect.addEventListener('change', updateStepper);

    ['first_name', 'last_name', 'email', 'phone'].forEach(function (fieldId) {
        document.getElementById(fieldId).addEventListener('input', updateStepper);
    });

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        hideAlert();
        submitBtn.disabled = true;
        submitBtn.querySelector('span').textContent = 'Confirming...';

        const payload = {
            service_id: parseInt(serviceSelect.value, 10),
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
            document.querySelector('.booking-stepper').classList.add('d-none');
            confirmationBox.classList.remove('d-none');

            const appt = data.appointment;
            const when = new Date(appt.start_datetime).toLocaleString(LOCALE, {
                weekday: 'long',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: '2-digit',
            });
            confirmationDetails.textContent =
                appt.service + ' on ' + when
                + '. Your reference is ' + appt.confirmation_token + '.';
        } catch (err) {
            showAlert(err.message, 'danger');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = 'Confirm Booking';
            updateStepper();
            resetTurnstile();
        }
    });

    setMinDate();
    updateStepper();
    renderTurnstile();
    loadServices().catch(function (err) {
        showAlert(err.message, 'danger');
    });
})();
