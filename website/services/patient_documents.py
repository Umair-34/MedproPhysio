from django.templatetags.static import static

from website.models import PatientDocument


def get_published_documents(category=None):
    queryset = PatientDocument.objects.filter(is_published=True)
    if category:
        queryset = queryset.filter(category=category)
    return queryset


def get_documents_grouped():
    groups = []
    number = 1
    for value, label in PatientDocument.DocumentCategory.choices:
        documents = list(get_published_documents(category=value))
        if documents:
            numbered_documents = []
            for document in documents:
                numbered_documents.append({'document': document, 'number': number})
                number += 1
            groups.append({
                'category': value,
                'label': label,
                'documents': numbered_documents,
            })
    return groups


def document_download_url(document):
    if document.file:
        return document.file.url
    if document.static_file:
        return static(document.static_file)
    return None
