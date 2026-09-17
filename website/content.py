"""Site wide content and navigation configuration."""

SITE_NAME = 'Medpro Physiotherapy Massage and Wellness Centre'
SITE_TAGLINE = 'Calgary physiotherapy, massage, and wellness care'
SITE_META_DESCRIPTION = (
  'Medpro Physiotherapy Massage and Wellness Centre is a Calgary clinic offering '
  'physiotherapy, massage therapy, chiropractic, acupuncture, and kinesiology.'
)

HOME_META_TITLE = 'Calgary Physiotherapy & Massage Clinic'
HOME_META_DESCRIPTION = (
  'Medpro Physiotherapy Massage and Wellness Centre offers physiotherapy, massage therapy, '
  'chiropractic, acupuncture, and kinesiology in Calgary. Book online today.'
)

HOME_HERO = {
  'image': 'images/home/hero-physio-portrait.jpg',
  'eyebrow': 'Physiotherapy, Massage & Wellness Care',
  'title_before': 'Find lasting relief and move through life',
  'title_accent': 'with confidence.',
  'title_after': '',
  'intro': (
    'Modern, patient-centred physiotherapy, massage, chiropractic, and wellness care in '
    'northwest Calgary, designed to help you recover, move better, and feel stronger.'
  ),
  'primary_cta': 'Book an Appointment',
  'secondary_cta': 'Explore Our Services',
  'badge': 'Same-week appointments',
  'experience_value': '6+',
  'experience_label': 'Years of combined clinical experience',
  'rating_value': '5.0',
  'rating_label': 'patient rating',
  'rating_detail': 'Based on Google reviews from Calgary patients',
  'avatars': [
    {'initial': 'U', 'color': '#ef6c00'},
    {'initial': 'J', 'color': '#8e6c88'},
    {'initial': 'L', 'color': '#558b2f'},
    {'initial': 'A', 'color': '#e91e63'},
  ],
  'features': [
    {
      'icon': 'fa-solid fa-user-doctor',
      'title': 'Care you can trust',
      'text': 'Licensed, experienced clinicians',
    },
    {
      'icon': 'fa-solid fa-chart-line',
      'title': 'Measurable progress',
      'text': 'Clear goals and regular reviews',
    },
    {
      'icon': 'fa-solid fa-hand-holding-heart',
      'title': 'Personal treatment',
      'text': 'Built around your body and goals',
    },
    {
      'icon': 'fa-solid fa-calendar-check',
      'title': 'Direct booking',
      'text': 'Book online in minutes',
    },
  ],
}

# Legacy alias kept for any external references to slide images.
HOME_HERO_SLIDES = [
  {'image': 'images/home/slide-1.jpg', 'kicker': '', 'title': '', 'subtitle': ''},
]

HOME_FIRST_VISIT_IMAGE = 'images/home/first-visit.jpg'

HOME_SERVICE_PROMOS = [
  {'slug': 'physiotherapy', 'title': 'Physiotherapy', 'image': 'images/services/physiotherapy.jpg'},
  {'slug': 'kinesiology', 'title': 'Exercise Therapy', 'image': 'images/services/exercise-therapy.jpg'},
  {'slug': 'sports-performance', 'title': 'Sports Injury', 'image': 'images/services/sports-injury.jpg'},
  {'slug': 'manual-therapy', 'title': 'Manual Therapy', 'image': 'images/services/manual-therapy.jpg'},
  {'slug': 'chiropractic', 'title': 'Chiropractic', 'image': 'images/services/chiropractic.jpg'},
  {'slug': 'massage-therapy', 'title': 'Massage Therapy', 'image': 'images/services/massage-therapy.jpg'},
  {'slug': 'acupuncture', 'title': 'Acupuncture', 'image': 'images/services/acupuncture.jpg'},
  {'slug': 'psychology-counselling', 'title': 'Psychology Counselling', 'image': 'images/services/psychology-counselling.jpg'},
  {'slug': 'physiotherapy', 'title': 'MVA Injury', 'image': 'images/services/mva-injury.jpg'},
  {'slug': 'concussion-management', 'title': 'Concussion Management', 'image': 'images/services/concussion-management.jpg'},
  {'slug': 'myofascial-release', 'title': 'Chronic Pain', 'image': 'images/services/chronic-pain.jpg'},
  {'slug': 'physiotherapy', 'title': 'Pregnancy Physio', 'image': 'images/services/pregnancy-physio.jpg'},
  {'slug': 'exercise-rehab', 'title': 'Post Surgery Rehab', 'image': 'images/services/post-surgery-rehab.jpg'},
]

HOME_COUNTER_VALUE = 95
HOME_COUNTER_LABEL = 'Excellent Results'

HOME_WHY_TITLE = 'Why Choose Medpro Physiotherapy And Wellness?'
HOME_WHY_PARAGRAPHS = [
  (
    'Over 6 years of combined expertise in outpatient orthopedic, neurological and sports medicine, '
    'we are an independently owned group of veteran physical therapists.'
  ),
  (
    'We are dedicated to restoring mobility, relieving pain, and enhancing well being. With our expert '
    'physiotherapists and personalized care, you will experience a journey towards optimal health and vitality.'
  ),
]

HOME_ABOUT_IMAGE = 'images/home/about-clinic.jpg'
HOME_ABOUT_INTRO = (
  'Our Calgary clinic brings experienced therapists, modern treatment methods, and genuine one on one '
  'attention together, so you leave each visit understanding your plan and feeling confident in your recovery.'
)

HOME_ABOUT_STORY = {
  'eyebrow': 'Care that lasts',
  'title_before': 'Commitment To',
  'title_accent': 'Expert Care',
  'title_after': 'And Lasting Recovery',
  'intro': (
    'Compassion fuels our expertise, and your progress drives our purpose. '
    'By working together, we lay the groundwork for long-term recovery in northwest Calgary.'
  ),
  'cta': 'Know More',
  'image': 'images/home/about-clinic.jpg',
  'panel_image': 'images/home/first-visit.jpg',
  'tabs': [
    {
      'id': 'vision',
      'label': 'Our Vision',
      'icon': 'fa-solid fa-eye',
      'summary': (
        'We help clients resume their lifelong pursuit of health, fitness, and well-being '
        'at work, at home, and in the activities they love most.'
      ),
      'points': [
        'Confident Healing',
        'Easy Motion',
        'Therapeutic Relief',
        'Strength Rebuilding',
      ],
    },
    {
      'id': 'mission',
      'label': 'Our Mission',
      'icon': 'fa-solid fa-shield-heart',
      'summary': (
        'Physiotherapists empower recovery by restoring movement and strength with expert, '
        'patient-centred care under one roof.'
      ),
      'points': [
        'Accessible Care',
        'Evidence Based Plans',
        'One-on-One Attention',
        'Lasting Progress',
      ],
    },
    {
      'id': 'values',
      'label': 'Our Values',
      'icon': 'fa-solid fa-bullseye',
      'summary': (
        'High-quality treatment, genuine patient care, and professional service guide every '
        'visit at Medpro Physiotherapy.'
      ),
      'points': [
        'High Quality',
        'Patient Care',
        'Professional Service',
        'Community Focus',
      ],
    },
  ],
}

HOME_ABOUT_HIGHLIGHTS = [
  {
    'icon': 'fa-solid fa-user-doctor',
    'title': 'Expert therapists',
    'text': 'Licensed physiotherapists and massage therapists focused on clear assessment and hands on care.',
  },
  {
    'icon': 'fa-solid fa-bolt',
    'title': 'Advanced techniques',
    'text': 'Evidence based treatment for injury recovery, chronic pain, and return to sport goals.',
  },
  {
    'icon': 'fa-solid fa-hand-holding-heart',
    'title': 'Personalized care',
    'text': 'Plans shaped around your work, activity level, and what matters most to you in Calgary.',
  },
]

HOME_ABOUT_STATS = [
  {'value': '6+', 'label': 'Years of experience'},
  {'value': '95%', 'label': 'Patient satisfaction'},
  {'value': '6+', 'label': 'Treatment disciplines'},
]

HOME_FIRST_VISIT_TITLE = 'Getting ready for your first appointment'
HOME_FIRST_VISIT_LEAD = 'Ready to take the first step? Here is how to prepare for a comfortable, productive visit.'
HOME_FIRST_VISIT_INTRO = (
  'A few simple steps before you arrive can help your appointment run smoothly '
  'and make treatment easier from the start.'
)

HOME_FIRST_VISIT_TIPS = [
  'Eat lightly beforehand. Arriving on an empty stomach can leave you feeling faint or unsteady during assessment or treatment.',
  'Wear comfortable, easy to move in clothing. Shorts, loose pants, or a t shirt make it simpler for your therapist to examine and treat the areas that need attention.',
  'Most care plans include more than one session. Lasting improvement usually builds over time, even when you notice relief after your first visit.',
]

HOME_BENEFITS = [
  {
    'title': 'Expert Calgary Practitioners',
    'summary': 'Licensed physiotherapists, massage therapists, and chiropractors under one roof.',
    'icon': 'images/icon-benefits-1.svg',
    'icon_alt': 'Expert practitioners icon',
    'delay': '',
  },
  {
    'title': 'WCB and Insurance Billing',
    'summary': 'Workplace injury support, WCB Alberta claims, and extended health receipts.',
    'icon': 'images/icon-benefits-2.svg',
    'icon_alt': 'Insurance and WCB billing icon',
    'delay': '0.25s',
  },
  {
    'title': 'Book Online in Minutes',
    'summary': 'Schedule physiotherapy or massage at our Calgary clinic anytime.',
    'icon': 'images/icon-benefits-3.svg',
    'icon_alt': 'Online booking icon',
    'delay': '0.5s',
  },
]

HOME_ABOUT_POINTS = [
  ('Expert therapists', 'images/icon-about-list-1.svg', 'Expert therapist icon'),
  ('Advanced techniques', 'images/icon-about-list-2.svg', 'Advanced treatment techniques icon'),
  ('Personalized Calgary care', 'images/icon-about-list-3.svg', 'Personalized care icon'),
]

ABOUT_META_DESCRIPTION = (
  'Learn about Medpro Physio, a Calgary physiotherapy and wellness clinic in '
  'northwest Calgary. Our mission, values, and patient centred approach to recovery.'
)

ABOUT_PAGE_IMAGE = 'images/home/about-clinic.jpg'
ABOUT_PAGE_TITLE = 'Calgary physiotherapy with a patient first approach'
ABOUT_PAGE_LEAD = (
  'At Medpro Physiotherapy Massage and Wellness Centre, we combine hands on treatment, '
  'clear education, and a welcoming clinic experience so you always know what comes next in your recovery.'
)

ABOUT_INTRO = (
  'Medpro Physiotherapy has been helping Calgary patients recover from injury, manage '
  'pain, and stay active. Our licensed physiotherapists, massage therapists, and wellness '
  'practitioners work together under one roof at our Nolanridge Court clinic.',
  'Every visit starts with a thorough assessment and a plan built around your goals, whether '
  'that is returning to work, sport, or everyday movement without pain. We explain your '
  'treatment in plain language and support you long after you leave the clinic.',
)

ABOUT_MISSION = {
  'title': 'Our Mission',
  'summary': (
    'To deliver accessible, expert physiotherapy and wellness care to northwest Calgary '
    'communities. We invest in skilled practitioners, evidence based treatment, and a clinic '
    'environment where every patient feels heard, supported, and confident in their recovery.'
  ),
  'icon': 'fa-solid fa-bullseye',
}

ABOUT_VISION = {
  'title': 'Our Vision',
  'summary': (
    'We are committed as primary healthcare professionals to help our clients resume their '
    'lifelong pursuit of health, fitness, and well being, at work, at home, and in the '
    'activities they love most.'
  ),
  'icon': 'fa-solid fa-eye',
}

ABOUT_VALUES = [
  {
    'title': 'High Quality',
    'summary': (
      'We take a goal oriented approach to healing. Whatever your goals might be, we want to '
      'help you achieve them with clear plans and measurable progress.'
    ),
    'icon': 'fa-solid fa-award',
    'delay': '',
  },
  {
    'title': 'Patient Care',
    'summary': (
      'We provide hands on treatment in the clinic and education you can take home, so you '
      'become an active partner in your recovery and long term physical health.'
    ),
    'icon': 'fa-solid fa-hand-holding-heart',
    'delay': '0.2s',
  },
  {
    'title': 'Professional Service',
    'summary': (
      'Our multidisciplinary team brings years of clinical experience and a shared passion for '
      'helping Nolan Hill, Kincora, and greater Calgary stay active.'
    ),
    'icon': 'fa-solid fa-user-doctor',
    'delay': '0.4s',
  },
]

ABOUT_CLOSING = (
  'Our team of highly trained professionals uses proven manual therapy, exercise rehab, and '
  'integrated wellness services to restore you to pain free health. We evaluate and treat the '
  'root factors behind your issue, including posture, daily habits, work demands, and the '
  'movement patterns that contribute to your pain, so recovery lasts.'
)

HOME_QUALITY_POINTS = [
  'Same week appointments for acute pain and sports injuries',
  'Direct billing and receipts for Alberta extended health plans',
  'One clinic for physiotherapy, massage, chiropractic, and more',
]

HOME_REHAB_BENEFITS = [
  ('Experienced team', 'images/icon-rehab-benefits-1.svg', 'Experienced rehabilitation team icon'),
  ('Modern equipment', 'images/icon-rehab-benefits-2.svg', 'Modern clinic equipment icon'),
  ('Personalized plans', 'images/icon-rehab-benefits-3.svg', 'Personalized treatment plan icon'),
  ('Easy northeast access', 'images/icon-rehab-benefits-4.svg', 'Convenient Calgary location icon'),
  ('Insurance friendly', 'images/icon-rehab-benefits-5.svg', 'Insurance billing icon'),
  ('Community focused', 'images/icon-rehab-benefits-6.svg', 'Community wellness icon'),
]

HOME_HOW_IT_WORKS = [
  {
    'title': 'Book your Calgary appointment',
    'summary': (
      'Choose your service online or call our Calgary clinic. Tell us about your injury, '
      'pain, or wellness goals so we can match you with the right practitioner.'
    ),
    'icon': 'images/icon-how-it-work-1.svg',
    'icon_alt': 'Book appointment icon',
    'delay': '',
  },
  {
    'title': 'Assessment and treatment plan',
    'summary': (
      'Your therapist completes a thorough assessment, explains findings in plain language, '
      'and builds a plan tailored to your work, sport, and daily activities in Calgary.'
    ),
    'icon': 'images/icon-how-it-work-2.svg',
    'icon_alt': 'Assessment icon',
    'delay': '0.25s',
  },
  {
    'title': 'Hands on care and rehab',
    'summary': (
      'Receive physiotherapy, massage, chiropractic, acupuncture, or exercise rehab based on '
      'your needs, with progress tracked at every visit.'
    ),
    'icon': 'images/icon-how-it-work-3.svg',
    'icon_alt': 'Treatment icon',
    'delay': '0.5s',
  },
  {
    'title': 'Recover and stay active',
    'summary': (
      'Follow your home program, return to work or sport safely, and book follow up care at '
      'our northwest Calgary clinic as needed.'
    ),
    'icon': 'images/icon-how-it-work-4.svg',
    'icon_alt': 'Recovery icon',
    'delay': '0.75s',
  },
]

HOME_FAQS = [
  {
    'question': 'Where is your Calgary physiotherapy clinic located?',
    'answer': (
      'Medpro Physiotherapy is at 1130-367 Nolanridge Cr NW, Calgary, AB T3R 1W9 '
      'in northwest Calgary. We serve Nolan Hill, Kincora, Sage Hill, and nearby communities.'
    ),
    'icon': 'fa-solid fa-location-dot',
  },
  {
    'question': 'What services do you offer in Calgary?',
    'answer': (
      'We provide physiotherapy, massage therapy, chiropractic care, acupuncture, kinesiology, '
      'manual therapy, dry needling, vestibular therapy, and concussion management.'
    ),
    'icon': 'fa-solid fa-hand-holding-medical',
  },
  {
    'question': 'Do you accept WCB and insurance?',
    'answer': (
      'Yes. We support WCB Alberta workplace injury claims and provide receipts for extended '
      'health insurance plans. Ask our front desk about direct billing options.'
    ),
    'icon': 'fa-solid fa-file-invoice-dollar',
  },
  {
    'question': 'How do I book an appointment?',
    'answer': (
      'Book online through our website or call the clinic during opening hours. Same week '
      'appointments are often available for acute pain and injuries.'
    ),
    'icon': 'fa-solid fa-calendar-check',
  },
]

SITE_TESTIMONIALS = [
  {
    'quote': (
      'taking physio sessions, staff is professional and friendly, providing excellent services'
    ),
    'name': 'Umar Qayyum',
    'role': 'Google Local Guide',
    'initial': 'U',
    'avatar_color': '#ef6c00',
    'image_alt': 'Google review by Umar Qayyum at Medpro Physio Calgary',
  },
  {
    'quote': (
      'I came in with pain that had been bothering me for a while, and they really helped me alot. '
      'Feeling better now and would definitely recommend this clinic.'
    ),
    'name': 'Jeff Mark',
    'role': 'Google review',
    'initial': 'J',
    'avatar_color': '#8e6c88',
    'image_alt': 'Google review by Jeff Mark at Medpro Physio Calgary',
  },
  {
    'quote': 'Professional and friendly staff with excellent service!',
    'name': 'Lawrabe Naeem',
    'role': 'Google review',
    'initial': 'L',
    'avatar_color': '#558b2f',
    'image_alt': 'Google review by Lawrabe Naeem at Medpro Physio Calgary',
  },
  {
    'quote': 'Nice folks',
    'name': 'Aman Gupta',
    'role': 'Google Local Guide',
    'initial': 'A',
    'avatar_color': '#e91e63',
    'image_alt': 'Google review by Aman Gupta at Medpro Physio Calgary',
  },
]

HOME_TESTIMONIALS = SITE_TESTIMONIALS

SERVICES_HUB_META_TITLE = 'Calgary Physiotherapy, Massage & Wellness Services'
SERVICES_HUB_META_DESCRIPTION = (
  'Explore physiotherapy, massage therapy, chiropractic, acupuncture, kinesiology, and specialty '
  'services at Medpro Physiotherapy in northwest Calgary. Book online today.'
)
SERVICES_HUB_INTRO = (
  'From physiotherapy and massage to chiropractic, acupuncture, and advanced rehab techniques, '
  'our Calgary team builds a clear plan for every patient. Each service page explains assessment, '
  'care approach, typical timelines, and real recovery examples.'
)
SERVICES_HUB_FAQS = [
  (
    'What services do you offer in Calgary?',
    'We offer physiotherapy, massage therapy, chiropractic care, acupuncture, kinesiology, psychology counselling, '
    'manual therapy, dry needling, vestibular therapy, concussion management, and more at our northwest Calgary clinic.',
  ),
  (
    'How do I choose the right service?',
    'Book online or call our clinic. We match you with the right practitioner based on your injury, pain, '
    'or wellness goals. Many patients start with physiotherapy or massage and add complementary care as needed.',
  ),
  (
    'Do you accept insurance and WCB?',
    'Yes. We support WCB Alberta workplace injury claims and provide receipts for extended health insurance. '
    'Ask our front desk about direct billing for eligible Alberta plans.',
  ),
  (
    'Can I book multiple services at one clinic?',
    'Yes. Medpro Physiotherapy brings multiple disciplines under one roof in Calgary, '
    'so your care team can coordinate physiotherapy, massage, chiropractic, and more in one location.',
  ),
]

SITE_PHONE = '(587) 317-6906'
SITE_PHONE_LINK = 'tel:+15873176906'

SITE_CTA = {
  'eyebrow': 'Ready when you are',
  'title': 'Take the first step toward easier, stronger movement.',
  'text': (
    'Book your assessment and get a clear plan built around your pain, your routine, '
    'and the activities that matter to you.'
  ),
  'primary_cta': 'Book an Appointment',
  'image': 'images/home/first-visit.jpg',
  'image_alt': 'Physiotherapist helping a patient with movement at Medpro Physio',
}
SITE_EMAIL = 'Medprophysio@outlook.com'
SITE_ADDRESS = '1130-367 Nolanridge Cr NW, Calgary, AB T3R 1W9, Canada'
SITE_ADDRESS_SHORT = '367 Nolanridge Cr NW, Calgary'
SITE_STREET_ADDRESS = '1130-367 Nolanridge Cr NW'
SITE_POSTAL_CODE = 'T3R 1W9'
SITE_CITY = 'Calgary'
SITE_REGION = 'Alberta'
SITE_COUNTRY = 'CA'
SITE_LATITUDE = 51.1702219
SITE_LONGITUDE = -114.1662636
SITE_GOOGLE_PLACE_ID = 'ChIJcUBVbQdpcVMR-u84x5J6QaU'
SITE_GOOGLE_BUSINESS_URL = (
  f'https://www.google.com/maps/place/?q=place_id:{SITE_GOOGLE_PLACE_ID}'
)
SITE_GOOGLE_DIRECTIONS_URL = (
  f'https://www.google.com/maps/dir/?api=1&destination_place_id={SITE_GOOGLE_PLACE_ID}'
  '&travelmode=driving'
)
SITE_MAP_EMBED_URL = (
  f'https://maps.google.com/maps?q=place_id:{SITE_GOOGLE_PLACE_ID}&z=16&output=embed'
)
SITE_MAP_URL = SITE_GOOGLE_DIRECTIONS_URL

CLINIC_HOURS_SUMMARY = (
  'Monday to Thursday 9:00 AM to 7:00 PM. Friday 10:00 AM to 6:00 PM. '
  'Saturday 9:00 AM to 2:00 PM. Closed Sunday.'
)

WORKING_HOURS = [
  'Mon to Thu: 9:00 AM to 7:00 PM',
  'Fri: 10:00 AM to 6:00 PM',
  'Sat: 9:00 AM to 2:00 PM',
  'Sun: Closed',
]

CLINIC_HOURS = [
  {'label': 'Monday', 'hours': '9:00 AM to 7:00 PM', 'weekday': 0, 'opens': (9, 0), 'closes': (19, 0)},
  {'label': 'Tuesday', 'hours': '9:00 AM to 7:00 PM', 'weekday': 1, 'opens': (9, 0), 'closes': (19, 0)},
  {'label': 'Wednesday', 'hours': '9:00 AM to 7:00 PM', 'weekday': 2, 'opens': (9, 0), 'closes': (19, 0)},
  {'label': 'Thursday', 'hours': '9:00 AM to 7:00 PM', 'weekday': 3, 'opens': (9, 0), 'closes': (19, 0)},
  {'label': 'Friday', 'hours': '10:00 AM to 6:00 PM', 'weekday': 4, 'opens': (10, 0), 'closes': (18, 0)},
  {'label': 'Saturday', 'hours': '9:00 AM to 2:00 PM', 'weekday': 5, 'opens': (9, 0), 'closes': (14, 0)},
  {'label': 'Sunday', 'hours': 'Closed', 'weekday': 6, 'opens': None, 'closes': None},
]

OPENING_HOURS_SCHEMA = [
  {
    'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
    'opens': '09:00',
    'closes': '19:00',
  },
  {
    'days': ['Friday'],
    'opens': '10:00',
    'closes': '18:00',
  },
  {
    'days': ['Saturday'],
    'opens': '09:00',
    'closes': '14:00',
  },
]

VISIT_PARKING = 'Free parking available at our Nolanridge Court clinic in northwest Calgary.'

BOOKING_STEPS = [
  {
    'number': '01',
    'icon': 'images/icon-booking-process-1.svg',
    'title': 'Choose your service',
    'text': 'Select physiotherapy, massage therapy, chiropractic, or another treatment at our Calgary clinic.',
  },
  {
    'number': '02',
    'icon': 'images/icon-booking-process-2.svg',
    'title': 'Pick date and time',
    'text': 'View live availability and choose a practitioner or any available team member.',
  },
  {
    'number': '03',
    'icon': 'images/icon-booking-process-3.svg',
    'title': 'Enter your details',
    'text': 'No account needed. Add your contact information in under two minutes.',
  },
  {
    'number': '04',
    'icon': 'images/icon-booking-process-4.svg',
    'title': 'We confirm by email',
    'text': 'Staff review your request, then you receive a confirmation or a note if that time is not available.',
  },
]

BOOKING_TRUST_POINTS = [
  'Same week appointments often available',
  'Free parking at our Nolanridge Court clinic',
  'WCB and extended health receipts provided',
  'Friendly team ready to help by phone',
]

VISIT_TRANSIT = 'Calgary Transit serves Nolan Hill, Kincora, Sage Hill, and northwest Calgary with nearby bus connections.'
VISIT_LANDMARKS = (
  'We are located at 1130-367 Nolanridge Cr NW in northwest Calgary, convenient for '
  'Nolan Hill, Kincora, Sage Hill, Citadel, and Evanston.'
)
VISIT_SERVICE_AREAS = [
  'Calgary', 'Nolan Hill', 'Kincora', 'Sage Hill', 'Citadel',
  'Evanston', 'Symons Gate', 'Hidden Valley', 'Hamptons', 'Royal Oak',
]
VISIT_FAQS = [
  (
    'Where is Medpro Physiotherapy located?',
    'We are at 1130-367 Nolanridge Cr NW, Calgary, AB T3R 1W9. Use the map on this '
    'page or open directions in Google Maps for turn by turn navigation from your location.',
  ),
  (
    'Is there parking at the clinic?',
    VISIT_PARKING,
  ),
  (
    'What are your clinic hours?',
    CLINIC_HOURS_SUMMARY,
  ),
  (
    'How do I find the clinic on Google Maps?',
    'Search for Medpro Physio on Google Maps or tap View on Google to open our '
    'Google Business Profile listing with directions, hours, and reviews.',
  ),
]


FAQS_PAGE_META_DESCRIPTION = (
  'Answers about booking, insurance, WCB claims, services, parking, and what to expect '
  'at Medpro Physiotherapy in northwest Calgary.'
)
FAQS_PAGE_LEAD = (
  'Search or browse common questions about appointments, billing, services, and visiting '
  'our Calgary clinic.'
)

FAQS_PAGE_CATEGORIES = [
  {'id': 'all', 'label': 'All topics', 'icon': 'fa-solid fa-layer-group'},
  {'id': 'booking', 'label': 'Booking', 'icon': 'fa-solid fa-calendar-check'},
  {'id': 'insurance', 'label': 'Insurance & WCB', 'icon': 'fa-solid fa-file-invoice-dollar'},
  {'id': 'services', 'label': 'Services', 'icon': 'fa-solid fa-hand-holding-medical'},
  {'id': 'clinic', 'label': 'Clinic & visit', 'icon': 'fa-solid fa-location-dot'},
]

FAQS_PAGE_FAQS = [
  {
    'question': 'Do I need a referral to book?',
    'answer': (
      'No referral is required for most private appointments in Alberta. For WCB workplace '
      'injuries, please bring your claim details to your first visit.'
    ),
    'icon': 'fa-solid fa-file-medical',
    'category': 'booking',
  },
  {
    'question': 'Can I book online?',
    'answer': (
      'Yes. Use our online booking page to choose your service, practitioner, and time. '
      'No account is required, and same week appointments are often available.'
    ),
    'icon': 'fa-solid fa-calendar-check',
    'category': 'booking',
  },
  {
    'question': 'How do I book an appointment?',
    'answer': (
      'Book online through our website or call the clinic during opening hours. Tell us about '
      'your injury, pain, or wellness goals so we can match you with the right practitioner.'
    ),
    'icon': 'fa-solid fa-phone-volume',
    'category': 'booking',
  },
  {
    'question': 'What should I bring to my first appointment?',
    'answer': (
      'Bring your Alberta health card, insurance details, WCB claim number if applicable, '
      'any referral letters or imaging reports, and wear comfortable clothing.'
    ),
    'icon': 'fa-solid fa-briefcase-medical',
    'category': 'booking',
  },
  {
    'question': 'Do you accept WCB and insurance?',
    'answer': (
      'Yes. We support WCB Alberta workplace injury claims and provide receipts for extended '
      'health insurance plans. Ask our front desk about direct billing options.'
    ),
    'icon': 'fa-solid fa-file-invoice-dollar',
    'category': 'insurance',
  },
  {
    'question': 'Can I use extended health benefits?',
    'answer': (
      'Most extended health plans cover physiotherapy, massage, chiropractic, and acupuncture. '
      'We provide detailed receipts for reimbursement and direct billing where eligible.'
    ),
    'icon': 'fa-solid fa-shield-heart',
    'category': 'insurance',
  },
  {
    'question': 'Which services do you offer?',
    'answer': (
      'We offer physiotherapy, massage therapy, chiropractic care, acupuncture, kinesiology, '
      'manual therapy, dry needling, vestibular therapy, concussion management, and more.'
    ),
    'icon': 'fa-solid fa-hand-holding-medical',
    'category': 'services',
  },
  {
    'question': 'How do I choose the right service?',
    'answer': (
      'Book online or call our clinic. We match you with the right practitioner based on your '
      'injury, pain, or wellness goals. Many patients start with physiotherapy or massage.'
    ),
    'icon': 'fa-solid fa-user-doctor',
    'category': 'services',
  },
  {
    'question': 'Can I book multiple services at one clinic?',
    'answer': (
      'Yes. Medpro Physiotherapy brings multiple disciplines under one roof, so your care team '
      'can coordinate physiotherapy, massage, chiropractic, and more in one location.'
    ),
    'icon': 'fa-solid fa-people-group',
    'category': 'services',
  },
  {
    'question': 'Where is your Calgary clinic located?',
    'answer': (
      'We are at 1130-367 Nolanridge Cr NW, Calgary, AB T3R 1W9 in northwest Calgary. '
      'We serve Nolan Hill, Kincora, Sage Hill, and nearby communities.'
    ),
    'icon': 'fa-solid fa-location-dot',
    'category': 'clinic',
  },
  {
    'question': 'Is there parking at the clinic?',
    'answer': VISIT_PARKING,
    'icon': 'fa-solid fa-square-parking',
    'category': 'clinic',
  },
  {
    'question': 'What are your clinic hours?',
    'answer': CLINIC_HOURS_SUMMARY,
    'icon': 'fa-regular fa-clock',
    'category': 'clinic',
  },
  {
    'question': 'How do I find the clinic on Google Maps?',
    'answer': (
      'Search for Medpro Physio on Google Maps or use the directions link on our Visit Us page '
      'for turn by turn navigation from your location.'
    ),
    'icon': 'fa-solid fa-map-location-dot',
    'category': 'clinic',
  },
]


def google_review_url():
  if SITE_GOOGLE_PLACE_ID:
    return f'https://search.google.com/local/writereview?placeid={SITE_GOOGLE_PLACE_ID}'
  return SITE_GOOGLE_BUSINESS_URL

FOCUS_AREAS = [
  {'slug': 'sports-recovery', 'title': 'Sports Recovery', 'summary': 'Return to sport safely after injury with structured rehab in Calgary.'},
  {'slug': 'workplace-acc-injuries', 'title': 'Workplace & WCB Injuries', 'summary': 'Support for work related injuries and WCB Alberta claims.'},
  {'slug': 'motor-vehicle-accident', 'title': 'Motor Vehicle Accident (MVA)', 'summary': 'Physiotherapy and massage for MVA injuries, whiplash, and insurance claims in Calgary.'},
  {'slug': 'post-surgery-rehab', 'title': 'Post Surgery Rehabilitation', 'summary': 'Guided recovery before and after surgery at our Calgary clinic.'},
  {'slug': 'balance-vestibular', 'title': 'Balance & Vestibular Care', 'summary': 'Help for dizziness, vertigo, and balance concerns.'},
  {'slug': 'pregnancy-postnatal', 'title': 'Pregnancy & Postnatal Support', 'summary': 'Care for pregnancy related pain and postnatal recovery in Calgary.'},
  {'slug': 'chronic-pain', 'title': 'Chronic Pain Management', 'summary': 'Long term strategies to improve daily function.'},
  {'slug': 'pelvic-health', 'title': 'Pelvic Health', 'summary': 'Specialist support for pelvic floor concerns.'},
  {'slug': 'concussion-recovery', 'title': 'Concussion Recovery', 'summary': 'Graduated return to activity after concussion.'},
  {'slug': 'acupuncture-wellness', 'title': 'Acupuncture Wellness', 'summary': 'Holistic acupuncture for pain relief and wellbeing.'},
]

FOCUS_AREAS_INJURY_SLUGS = {
  'sports-recovery',
  'workplace-acc-injuries',
  'motor-vehicle-accident',
  'post-surgery-rehab',
  'concussion-recovery',
}

FOCUS_AREAS_HUB_META_TITLE = 'Calgary Physiotherapy Focus Areas & Specialty Programs'
FOCUS_AREAS_HUB_META_DESCRIPTION = (
  'Explore sports recovery, WCB and MVA injury rehab, post surgery care, chronic pain, '
  'pregnancy support, pelvic health, and more at Medpro Physio in northeast Calgary.'
)
FOCUS_AREAS_HUB_INTRO = (
  'Our Calgary clinic in Calgary offers specialized programs across physiotherapy, massage, '
  'chiropractic, acupuncture, and kinesiology. Each focus area page explains who it helps, '
  'what to expect, and how we build your recovery plan.'
)
FOCUS_AREAS_HUB_FAQS = [
  (
    'What are focus areas at your Calgary clinic?',
    'Focus areas are specialized programs for common patient needs such as sports injuries, '
    'workplace and MVA claims, post surgery rehab, chronic pain, pregnancy support, and balance care.',
  ),
  (
    'How do I know which focus area fits me?',
    'Choose the program closest to your situation, or book online and our team will match you '
    'with the right practitioner and treatment plan at our Calgary clinic.',
  ),
  (
    'Do you support WCB and motor vehicle accident claims?',
    'Yes. We help patients with WCB Alberta workplace injuries and MVA rehabilitation, including '
    'documentation and coordinated care with your treatment team.',
  ),
  (
    'Can I combine focus area care with other treatments?',
    'Yes. Many patients combine physiotherapy, massage, chiropractic, and acupuncture under one '
    'roof so your care team can coordinate recovery in northeast Calgary.',
  ),
]

TREATMENTS_COL1 = [
  {'slug': 'physiotherapy', 'title': 'Physiotherapy', 'primary': True},
  {'slug': 'massage-therapy', 'title': 'Massage Therapy', 'primary': True},
  {'slug': 'manual-therapy', 'title': 'Manual Therapy'},
  {'slug': 'exercise-rehab', 'title': 'Exercise Rehabilitation'},
  {'slug': 'kinesiology', 'title': 'Kinesiology', 'primary': True},
  {'slug': 'dry-needling', 'title': 'Dry Needling'},
  {'slug': 'balance-fall-prevention', 'title': 'Balance & Fall Prevention'},
  {'slug': 'joint-mobilisation', 'title': 'Joint Mobilisation'},
  {'slug': 'sports-performance', 'title': 'Sports Performance'},
  {'slug': 'psychology-counselling', 'title': 'Psychology Counselling', 'primary': True},
]

TREATMENTS_COL2 = [
  {'slug': 'chiropractic', 'title': 'Chiropractic Care', 'primary': True},
  {'slug': 'acupuncture', 'title': 'Acupuncture', 'primary': True},
  {'slug': 'myofascial-release', 'title': 'Myofascial Release'},
  {'slug': 'ultrasound-therapy', 'title': 'Ultrasound Therapy'},
  {'slug': 'kinesio-taping', 'title': 'Kinesio Taping'},
  {'slug': 'mckenzie-method', 'title': 'McKenzie Method'},
  {'slug': 'ergonomic-training', 'title': 'Ergonomic Training'},
  {'slug': 'vestibular-therapy', 'title': 'Vestibular Therapy'},
  {'slug': 'postural-restoration', 'title': 'Postural Restoration'},
  {'slug': 'electrical-stimulation', 'title': 'Electrical Stimulation'},
  {'slug': 'concussion-management', 'title': 'Concussion Management'},
]

PATIENT_HUB = [
  {'slug': 'new-patient', 'title': 'New Patient Guide', 'url_name': 'website:patient-page'},
  {'slug': 'insurance', 'title': 'Insurance & WCB Info', 'url_name': 'website:patient-page'},
  {'title': 'Patient Stories', 'url_name': 'website:patient-stories'},
  {'title': 'Wellness Blog', 'url_name': 'website:blog'},
]

PATIENT_PAGES = {
  'new-patient': {
    'title': 'New Patient Guide',
    'page_type': 'guide',
    'meta_description': (
      'Prepare for your first visit to Medpro Physio in Calgary. Learn what to bring and what to '
      'expect at our northwest Calgary clinic.'
    ),
    'intro': (
      'Welcome to Medpro Physio. Whether you are visiting for physiotherapy, massage '
      'therapy, chiropractic care, or another service, this guide helps you feel prepared for your '
      'first appointment in northwest Calgary.'
    ),
    'highlights': [
      'No account required to book online',
      'Arrive 10 minutes early for your first visit',
      'Our team helps with intake details at reception',
    ],
    'expectations_title': 'What to expect at your first visit',
    'expectations_intro': (
      'Your first appointment usually takes 45 to 60 minutes. We want to understand your story, '
      'assess how you move, and build a plan that fits your goals.'
    ),
    'expectations': [
      'Our front desk team will welcome you, confirm your details, and help with insurance or WCB paperwork.',
      'Your practitioner will ask about your symptoms, history, daily activities, and treatment goals.',
      'We assess movement, strength, posture, and function in the area being treated.',
      'You receive a clear explanation of our findings and a recommended treatment plan.',
      'Many first visits include hands on treatment or starter exercises when appropriate.',
      'We schedule follow up visits and give you home guidance to support your recovery.',
    ],
    'preparation_title': 'How to prepare',
    'preparation': [
      'Bring your Alberta health card and photo ID.',
      'Bring insurance details, WCB claim number, or MVA information if applicable.',
      'Bring referral letters, imaging reports, or specialist notes you already have.',
      'Wear comfortable clothing that lets us assess the affected area.',
      'Arrive 10 to 15 minutes early so we can confirm your details at reception.',
    ],
    'bring_title': 'What to bring',
    'bring_items': [
      {'icon': 'fa-id-card', 'title': 'Health card & ID', 'text': 'Alberta health card and photo identification.'},
      {'icon': 'fa-file-medical', 'title': 'Insurance or WCB details', 'text': 'Policy information, claim numbers, or adjuster contact details.'},
      {'icon': 'fa-x-ray', 'title': 'Medical reports', 'text': 'Referrals, X rays, MRI reports, or specialist letters if you have them.'},
      {'icon': 'fa-shirt', 'title': 'Comfortable clothing', 'text': 'Shorts for knee treatment, tank top for shoulder care, or loose layers.'},
    ],
  },
  'insurance': {
    'title': 'Insurance & WCB Info',
    'page_type': 'info',
    'meta_description': (
      'WCB Alberta workplace injury coverage, extended health insurance, and payment options at '
      'Medpro Physio in northwest Calgary.'
    ),
    'intro': (
      'We support WCB Alberta claims and provide receipts for extended health insurance plans. '
      'If you are unsure what applies to your visit, call our clinic and we will help you prepare.'
    ),
    'info_cards': [
      {
        'icon': 'fa-hard-hat',
        'title': 'WCB workplace injuries',
        'text': (
          'If your injury is covered by WCB Alberta, bring your claim number and any paperwork from '
          'your employer or case manager. We coordinate treatment plans and progress reporting for '
          'approved claims.'
        ),
      },
      {
        'icon': 'fa-file-invoice-dollar',
        'title': 'Extended health insurance',
        'text': (
          'Most Alberta plans cover physiotherapy, chiropractic, massage therapy, and acupuncture. '
          'Coverage limits and referral requirements vary by provider, so check your policy before '
          'your visit.'
        ),
      },
      {
        'icon': 'fa-credit-card',
        'title': 'Payment options',
        'text': (
          'We accept debit and credit cards. Direct billing is available for eligible insurers. '
          'Payment is due at the time of your appointment unless your plan or WCB claim covers the visit.'
        ),
        'link_label': 'Book an appointment',
        'link_name': 'website:book',
      },
    ],
    'tips': [
      'Call your insurer to confirm remaining benefits and whether a doctor referral is required.',
      'Bring your policy number and plan member ID to your first appointment.',
      'Keep receipts we provide for reimbursement if direct billing is not available.',
    ],
  },
}


def all_treatments():
  return TREATMENTS_COL1 + TREATMENTS_COL2


def get_content_item(section, slug):
  sections = {
    'treatments': all_treatments(),
  }
  for item in sections.get(section, []):
    if item['slug'] == slug:
      return item
  return None
