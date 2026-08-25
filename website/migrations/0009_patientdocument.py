from django.db import migrations, models


def seed_patient_documents(apps, schema_editor):
    PatientDocument = apps.get_model('website', 'PatientDocument')
    documents = [
        {
            'slug': 'new-patient-intake-form',
            'title': 'New Patient Intake Form',
            'description': 'Complete our intake form before your first visit to save time at reception.',
            'category': 'intake',
            'static_file': 'documents/new-patient-intake-form.pdf',
            'sort_order': 1,
        },
        {
            'slug': 'health-history-form',
            'title': 'Health History Form',
            'description': 'Share your medical background so we can tailor physiotherapy or massage care to your needs.',
            'category': 'intake',
            'static_file': 'documents/health-history-form.pdf',
            'sort_order': 2,
        },
        {
            'slug': 'wcb-consent-form',
            'title': 'WCB Consent Form',
            'description': 'Required for WCB Alberta workplace injury claims treated at our Calgary clinic.',
            'category': 'wcb',
            'static_file': 'documents/wcb-consent-form.pdf',
            'sort_order': 3,
        },
        {
            'slug': 'direct-billing-authorization',
            'title': 'Direct Billing Authorization',
            'description': 'Authorize direct billing to your extended health insurer when eligible.',
            'category': 'insurance',
            'static_file': 'documents/direct-billing-authorization.pdf',
            'sort_order': 4,
        },
    ]
    for data in documents:
        PatientDocument.objects.update_or_create(slug=data['slug'], defaults=data)


def remove_patient_documents(apps, schema_editor):
    PatientDocument = apps.get_model('website', 'PatientDocument')
    PatientDocument.objects.filter(
        slug__in=[
            'new-patient-intake-form',
            'health-history-form',
            'wcb-consent-form',
            'direct-billing-authorization',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_add_concussion_management_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('intake', 'Intake forms'), ('wcb', 'WCB and workplace'), ('insurance', 'Insurance'), ('general', 'General')], db_index=True, default='intake', max_length=32)),
                ('file', models.FileField(blank=True, help_text='Upload a PDF or document file. Optional if a bundled static file is set.', upload_to='patient_documents/%Y/%m/')),
                ('static_file', models.CharField(blank=True, help_text='Path under static/, e.g. documents/new-patient-intake-form.pdf', max_length=255)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_published', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Patient document',
                'verbose_name_plural': 'Patient documents',
                'ordering': ['sort_order', 'title'],
            },
        ),
        migrations.RunPython(seed_patient_documents, remove_patient_documents),
    ]
