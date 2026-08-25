#!/usr/bin/env python3
"""Remove em dashes, en dashes, and prose hyphens from user-facing site content."""

from __future__ import annotations

import io
import os
import re
import sys
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TECHNICAL_PATTERNS = (
    '/',
    '\\',
    '.svg',
    '.jpg',
    '.jpeg',
    '.png',
    '.webp',
    '.pdf',
    'http',
    'fa-',
    'mp-',
    'bg-',
    'swiper',
    'col-',
    'django.',
    'website:',
    'images/',
    'static/',
    'content_pages/',
)


def clean_dashes(text: str) -> str:
    """Remove prose em dashes. Keep hyphens in compounds, phones, emails, days, and times."""
    if not text:
        return text
    text = text.replace('&mdash;', '—').replace('&#8212;', '—')
    text = text.replace(' — ', ', ')
    text = text.replace('—', ', ')
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r' ,', ',', text)
    return text


def is_technical_string(value: str) -> bool:
    if not value:
        return True
    if any(pattern in value for pattern in TECHNICAL_PATTERNS):
        return True
    if re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value):
        return True
    if re.fullmatch(r'[a-z0-9_]+(?:-[a-z0-9_]+)*', value):
        return True
    return False


def clean_html(html: str) -> str:
    parts = re.split(r'(<[^>]+>)', html)
    return ''.join(part if part.startswith('<') else clean_dashes(part) for part in parts)


def rewrite_python_strings(source: str) -> tuple[str, int]:
    out: list[tokenize.TokenInfo] = []
    changed = 0

    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type != tokenize.STRING:
            out.append(tok)
            continue

        prefix = ''
        literal = tok.string
        if literal.startswith(('"""', "'''")):
            quote = literal[:3]
            body = literal[3:-3]
            suffix = literal[-3:]
        elif literal.startswith(("'", '"')):
            quote = literal[0]
            body = literal[1:-1]
            suffix = quote
        else:
            out.append(tok)
            continue

        if is_technical_string(body):
            out.append(tok)
            continue

        cleaned = clean_dashes(body)
        if cleaned == body:
            out.append(tok)
            continue

        changed += 1
        new_literal = f'{prefix}{quote}{cleaned}{suffix}'
        out.append(tokenize.TokenInfo(tok.type, new_literal, tok.start, tok.end, tok.line))

    return tokenize.untokenize(out), changed


def rewrite_template_text(source: str) -> tuple[str, int]:
    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        text = match.group(1)
        if not text.strip() or '{{' in text or '{%' in text:
            return match.group(0)
        cleaned = clean_dashes(text)
        if cleaned != text:
            changed += 1
        return f'>{cleaned}<'

    updated = re.sub(r'>([^<>{}]+)<', repl, source)
    return updated, changed


def rewrite_json_strings(source: str) -> tuple[str, int]:
    changed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        raw = match.group(0)
        try:
            import json

            value = json.loads(raw)
        except json.JSONDecodeError:
            return raw
        if not isinstance(value, str) or is_technical_string(value):
            return raw
        if '<' in value and '>' in value:
            cleaned = clean_html(value)
        else:
            cleaned = clean_dashes(value)
        if cleaned == value:
            return raw
        changed += 1
        return json.dumps(cleaned, ensure_ascii=False)

    updated = re.sub(r'"(?:\\.|[^"\\])*"', repl, source)
    return updated, changed


CONTENT_FILES = [
    ROOT / 'website/content.py',
    ROOT / 'website/blog_content.py',
    ROOT / 'website/page_content.py',
    ROOT / 'website/treatment_content.py',
    ROOT / 'fixtures/02_bookings.json',
    ROOT / 'fixtures/03_website.json',
]

TEMPLATE_FILES = [
    ROOT / 'templates/website/home.html',
    ROOT / 'templates/website/blog.html',
    ROOT / 'templates/website/blog_detail.html',
    ROOT / 'templates/website/appointment.html',
    ROOT / 'templates/includes/site_footer.html',
    ROOT / 'templates/includes/booking_sidebar.html',
    ROOT / 'templates/website/services.html',
    ROOT / 'templates/website/visit_us.html',
    ROOT / 'templates/includes/patient_hub_sidebar.html',
]


def update_files() -> int:
    total = 0
    for path in CONTENT_FILES:
        if not path.exists():
            continue
        source = path.read_text()
        if path.suffix == '.py':
            updated, count = rewrite_python_strings(source)
        else:
            updated, count = rewrite_json_strings(source)
        if count:
            path.write_text(updated)
            print(f'Updated {path.relative_to(ROOT)} ({count} strings)')
            total += count

    for path in TEMPLATE_FILES:
        if not path.exists():
            continue
        source = path.read_text()
        updated, count = rewrite_template_text(source)
        if count:
            path.write_text(updated)
            print(f'Updated {path.relative_to(ROOT)} ({count} text nodes)')
            total += count

    return total


def update_database() -> int:
    sys.path.insert(0, str(ROOT))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    import django

    django.setup()

    from bookings.models import Service
    from website.models import (
        BlogPost,
        ContentPage,
        PageAssessmentStep,
        PageCaseStudy,
        PageContentBenefit,
        PageContentFAQ,
        PageContentSection,
        PageRecoveryPhase,
        PageTreatmentMethod,
        PatientDocument,
    )

    def clean_value(value):
        if isinstance(value, str):
            if '<' in value and '>' in value:
                return clean_html(value)
            if is_technical_string(value):
                return value
            return clean_dashes(value)
        if isinstance(value, list):
            return [clean_value(item) for item in value]
        if isinstance(value, dict):
            return {key: clean_value(item) for key, item in value.items()}
        return value

    text_fields = [
        (ContentPage, ('title', 'summary', 'meta_description', 'description', 'faq_intro', 'benefits_heading', 'typical_sessions', 'first_improvement', 'recovery_timeline')),
        (PageContentSection, ('heading', 'body')),
        (PageContentBenefit, ('text',)),
        (PageContentFAQ, ('question', 'answer')),
        (PageAssessmentStep, ('title', 'body')),
        (PageTreatmentMethod, ('title', 'body')),
        (PageRecoveryPhase, ('phase', 'timeframe', 'body')),
        (PageCaseStudy, ('patient_label', 'issue', 'approach', 'outcome', 'timeline')),
        (PatientDocument, ('title', 'description')),
        (Service, ('name', 'description')),
        (BlogPost, ('title', 'summary', 'meta_title', 'meta_description', 'content')),
    ]

    json_fields = [
        (BlogPost, ('key_takeaways', 'sections', 'faqs', 'related_services')),
    ]

    changed = 0
    for model, fields in text_fields:
        for obj in model.objects.all():
            updates = {}
            for field in fields:
                value = getattr(obj, field, None)
                if not value or not isinstance(value, str):
                    continue
                if '<' in value and '>' in value:
                    cleaned = clean_html(value)
                elif is_technical_string(value):
                    continue
                else:
                    cleaned = clean_dashes(value)
                if cleaned != value:
                    updates[field] = cleaned
            if updates:
                for field, value in updates.items():
                    setattr(obj, field, value)
                obj.save(update_fields=list(updates.keys()))
                changed += len(updates)

    for model, fields in json_fields:
        for obj in model.objects.all():
            updates = {}
            for field in fields:
                value = getattr(obj, field, None)
                cleaned = clean_value(value)
                if cleaned != value:
                    updates[field] = cleaned
            if updates:
                for field, value in updates.items():
                    setattr(obj, field, value)
                obj.save(update_fields=list(updates.keys()))
                changed += len(updates)
    return changed


def main() -> int:
    file_changes = update_files()
    db_changes = update_database()
    print(f'Done. Updated {file_changes} file strings and {db_changes} database fields.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
