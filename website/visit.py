"""Visit page helpers for hours status and local SEO."""

from datetime import datetime, time
from django.conf import settings
from zoneinfo import ZoneInfo

from website import content

CLINIC_TZ = ZoneInfo(settings.TIME_ZONE)

CLOSE_LABELS = {
  (20, 0): '8:00 PM',
  (16, 0): '4:00 PM',
  (14, 0): '2:00 PM',
}

OPEN_LABELS = {
  (8, 0): '8:00 AM',
  (9, 0): '9:00 AM',
}


def _schedule_for_weekday(weekday):
  for row in content.CLINIC_HOURS:
    if row['weekday'] == weekday:
      return row
  return None


def _time_from_tuple(value):
  return time(value[0], value[1])


def _next_open_day(from_weekday):
  for offset in range(1, 8):
    weekday = (from_weekday + offset) % 7
    row = _schedule_for_weekday(weekday)
    if row:
      return row
  return None


def clinic_hours_bounds(weekday):
  """Return (opens, closes) for a weekday, or None if the clinic is closed that day."""
  row = _schedule_for_weekday(weekday)
  if not row:
    return None, None
  return _time_from_tuple(row['opens']), _time_from_tuple(row['closes'])


def clinic_hours_label(weekday):
  row = _schedule_for_weekday(weekday)
  if not row:
    return 'Closed'
  return row['hours']


def clinic_hours_with_today(now=None):
  if now is None:
    now = datetime.now(CLINIC_TZ)
  today = now.weekday()
  rows = []
  for row in content.CLINIC_HOURS:
    item = dict(row)
    item['is_today'] = row['weekday'] == today
    rows.append(item)
  return rows


def clinic_open_status(now=None):
  if now is None:
    now = datetime.now(CLINIC_TZ)

  today = _schedule_for_weekday(now.weekday())
  if not today:
    return 'closed', 'Closed today'

  opens = _time_from_tuple(today['opens'])
  closes = _time_from_tuple(today['closes'])
  current = now.time()
  close_label = CLOSE_LABELS.get(today['closes'], today['hours'].split(' to ')[-1].strip())
  open_label = OPEN_LABELS.get(today['opens'], today['hours'].split(' to ')[0].strip())

  if opens <= current < closes:
    return 'open', f'Open now. Closes at {close_label}'

  if current < opens:
    return 'closed', f'Opens today at {open_label}'

  next_day = _next_open_day(now.weekday())
  if next_day:
    next_open = OPEN_LABELS.get(next_day['opens'], next_day['label'])
    return 'closed', f'Closed for today. Opens {next_day["label"]} at {next_open}'
  return 'closed', 'Closed for today'
