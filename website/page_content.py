"""SEO page content for detail pages optimized for Calgary physiotherapy and massage."""

CITY = 'Calgary'
REGION = 'Alberta'
LOCATION_PHRASE = f'{CITY}, {REGION}'
CLINIC_SEO = f'physiotherapy and massage clinic in {CITY}'

DEFAULT_FAQ_INTRO = (
  f'Have questions about {CITY} physiotherapy, massage therapy, or booking at our Calgary clinic? '
  f'Find answers below or contact our team for personal guidance.'
)


def _meta(title, focus):
    return (
        f'{title} in {LOCATION_PHRASE}. {focus} '
        f'Visit our Calgary {CLINIC_SEO} for physiotherapy, massage therapy, and wellness care.'
    )


FOCUS_AREA_PAGES = {
    'sports-recovery': {
        'meta_description': _meta(
            'Sports Injury Physiotherapy and Massage',
            'Expert sports recovery with Calgary physiotherapy and massage therapy for all activity levels.',
        ),
        'intro': (
            f'Whether you run the Bow River pathway, play hockey in a Calgary league, or train at the gym, '
            f'sports injuries can sideline you quickly. Our sports recovery program at our Calgary '
            f'{CLINIC_SEO} combines physiotherapy, massage therapy, and exercise rehab so you can heal safely '
            f'and return to activity with confidence.'
        ),
        'sections': [
            (
                'Who we help in Calgary',
                'We treat runners, cyclists, skiers, gym goers, youth athletes, and weekend warriors across '
                'northeast Calgary and the wider city. Common issues include sprains, strains, tendonitis, '
                'overuse injuries, and post surgical sports rehab.',
            ),
            (
                'Our approach',
                'Your recovery starts with a thorough movement and strength assessment. We identify the root '
                'cause, not just the painful area, then build a staged plan covering pain relief, mobility, '
                'strength, and sport specific return to play progressions.',
            ),
            (
                'Physiotherapy and massage treatments',
                'Depending on your injury, your plan may include manual therapy, dry needling, exercise '
                'prescription, massage therapy, and chiropractic care. All services are available at our '
                f'Calgary physiotherapy and massage clinic in Calgary.',
            ),
        ],
        'benefits': [
            'Faster, safer return to training and competition',
            'Lower risk of repeat injury with structured progressions',
            'Clear home exercise programs between visits',
            'Direct billing available for many Alberta extended health plans',
        ],
        'faqs': [
            (
                'Do I need a doctor referral for physiotherapy or massage in Calgary?',
                'Most extended health plans in Alberta do not require a referral for physiotherapy or massage therapy, '
                'but check with your insurer. We provide receipts for reimbursement.',
            ),
            (
                'How soon after an injury should I book?',
                'Early assessment helps prevent compensations and chronic problems. Book as soon as you can '
                'after an acute injury and we will guide you on icing, loading, and next steps.',
            ),
        ],
    },
    'workplace-acc-injuries': {
        'meta_description': _meta(
            'Workplace and WCB Injury Physiotherapy',
            'Calgary physiotherapy and massage for work related injuries covered by WCB Alberta.',
        ),
        'intro': (
            f'Injured on the job in {CITY}? Our Calgary {CLINIC_SEO} supports workers recovering from '
            f'workplace injuries through physiotherapy, massage therapy, chiropractic care, and functional rehab. '
            f'We help you manage pain, restore movement, and prepare for a safe return to work.'
        ),
        'sections': [
            (
                'WCB and workplace injuries',
                'Workers Compensation Board Alberta covers many workplace injuries. If your claim is accepted, '
                'physiotherapy and massage therapy can play a central role in your recovery plan. Bring your WCB '
                'claim number and any paperwork to your first visit.',
            ),
            (
                'Common work injuries we treat',
                'Back and neck strain from lifting or desk work, repetitive strain injuries, falls, shoulder '
                'injuries, and post incident deconditioning are common in Calgary workplaces, from construction '
                'and trades to office and healthcare settings.',
            ),
            (
                'Return to work focus',
                'We align treatment with your job demands, whether that means sitting tolerance, lifting '
                'capacity, standing endurance, or driving. Progress is documented so you, your employer, and '
                'WCB have a clear picture of your recovery.',
            ),
        ],
        'benefits': [
            'Experienced in work related injury assessment and rehab',
            'Functional goals tied to your actual job tasks',
            'Coordination with WCB requirements and reporting',
            'Physiotherapy and massage under one Calgary roof',
        ],
        'faqs': [
            (
                'Can I book before my WCB claim is approved?',
                'Yes. Many patients begin with private pay or extended health coverage while a claim is processed. '
                'We will explain your options at booking.',
            ),
        ],
    },
    'motor-vehicle-accident': {
        'meta_description': _meta(
            'Motor Vehicle Accident (MVA) Physiotherapy Calgary',
            'Calgary MVA injury rehab for whiplash, back pain, and collision recovery with physiotherapy and massage.',
        ),
        'intro': (
            f'After a motor vehicle accident in {CITY}, pain and stiffness can linger long after the scene is '
            f'cleared. Our Calgary {CLINIC_SEO} helps patients recover from MVA injuries with physiotherapy, '
            f'massage therapy, chiropractic care, and guided exercise so you can move comfortably again and '
            f'return to work, driving, and daily life.'
        ),
        'sections': [
            (
                'MVA injuries we treat',
                'Whiplash and neck pain, headaches, mid back and low back pain, shoulder and rib injuries, '
                'jaw tension, dizziness, and soft tissue strains are common after rear end collisions, T bone '
                'impacts, and multi vehicle accidents on Calgary roads. Symptoms may appear immediately or '
                'develop over the days following a crash.',
            ),
            (
                'Alberta insurance and your claim',
                'Alberta has a regulated automobile insurance system for accident benefits. If you were injured '
                'in a collision, you may be eligible for coverage for approved treatment such as physiotherapy and '
                'massage therapy through your automobile insurance claim. Bring your claim details, policy '
                'information, and any forms from your insurer or adjuster to your first visit.',
            ),
            (
                'Your assessment and treatment plan',
                'We start with a thorough history of the accident, your symptoms, and how they affect sleep, '
                'work, and driving. Your assessment covers movement, strength, posture, and any red flags that '
                'need medical follow up. Treatment may include manual therapy, exercise rehab, massage therapy, '
                'acupuncture, and education on pacing and home recovery.',
            ),
            (
                'Whiplash and early treatment',
                'Early, appropriate care after whiplash often leads to better outcomes than prolonged rest alone. '
                'We guide you through gradual mobility, strengthening, and return to activity while monitoring '
                'symptoms such as headaches, arm pain, or dizziness that may need coordinated care.',
            ),
            (
                'Documentation and progress reporting',
                'For MVA claims, insurers often require treatment plans and progress updates. Our team documents '
                'your visits and communicates clearly so you understand next steps in your recovery and claim process.',
            ),
        ],
        'benefits': [
            'Experienced care for whiplash and collision related injuries',
            'Physiotherapy, massage, and chiropractic under one Calgary roof',
            'Treatment plans aligned with your symptoms and daily goals',
            'Convenient Calgary location with free parking',
            'Support navigating paperwork for your MVA claim',
        ],
        'faqs': [
            (
                'When should I start physiotherapy after a car accident in Calgary?',
                'If you have ongoing pain, stiffness, or difficulty with daily activities after a collision, '
                'book an assessment as soon as you can. Early treatment can reduce the risk of symptoms becoming '
                'long term, especially with whiplash and neck injuries.',
            ),
            (
                'Does Alberta automobile insurance cover physiotherapy after an MVA?',
                'Many MVA treatment costs are covered through your automobile insurance accident benefits when '
                'your claim is approved. Coverage details depend on your policy and insurer. Bring your claim '
                'number and any treatment approval forms to your appointment.',
            ),
            (
                'What should I bring to my first MVA appointment?',
                'Bring photo ID, your Alberta health card, insurance and claim information, details of the '
                'accident, any police or medical reports, and a list of medications. Wear comfortable clothing '
                'so we can assess your neck, back, or other injured areas.',
            ),
            (
                'Can massage therapy help after a motor vehicle accident?',
                'Yes. Massage therapy can reduce muscle tension, headaches, and stress related to collision '
                'injuries, especially when combined with physiotherapy and exercise rehab. Your therapist will '
                'recommend what is appropriate for your stage of recovery.',
            ),
        ],
    },
    'post-surgery-rehab': {
        'meta_description': _meta(
            'Post Surgery Physiotherapy Calgary',
            'Structured post surgical rehab with Calgary physiotherapy and massage after orthopedic surgery.',
        ),
        'intro': (
            f'Recovering from surgery in {CITY} requires more than rest. It requires guided rehabilitation. '
            f'Our Calgary {CLINIC_SEO} provides post surgical physiotherapy and massage therapy to restore '
            f'strength, mobility, and confidence after orthopedic and musculoskeletal procedures.'
        ),
        'sections': [
            (
                'Pre surgery and after surgery care',
                'Strengthening before surgery can improve outcomes. After your procedure, we follow surgeon '
                'protocols while adapting to your progress, managing swelling, scar tissue, range of motion, '
                'and gradual loading.',
            ),
            (
                'Surgeries we commonly rehab',
                'ACL and meniscus repair, rotator cuff surgery, hip and knee replacement, spinal surgery, '
                'fracture fixation, and arthroscopic procedures are familiar territory for our Calgary team.',
            ),
            (
                'Your recovery timeline',
                'Rehab is phased: early protection and range of motion, then strength and control, then '
                'return to daily activities, work, and recreation. We set realistic milestones and adjust '
                'your program every visit.',
            ),
        ],
        'benefits': [
            'Rehab plans aligned with your surgeon guidelines',
            'Hands on therapy plus supervised exercise progression',
            'Home programs with clear instructions between appointments',
            'Convenient Calgary location with free parking',
        ],
        'faqs': [
            (
                'When should I start physiotherapy after surgery?',
                'Timing depends on your surgery type and surgeon orders. Contact us with your discharge '
                'instructions and we will advise on the right start date.',
            ),
        ],
    },
    'balance-vestibular': {
        'meta_description': _meta(
            'Balance and Vestibular Physiotherapy Calgary',
            'Calgary physiotherapy for dizziness, vertigo, and balance problems.',
        ),
        'intro': (
            f'Feeling unsteady, dizzy, or lightheaded can limit everyday life in {CITY}, from walking icy '
            f'sidewalks in winter to moving around your home. Our balance and vestibular program at our '
            f'Calgary {CLINIC_SEO} addresses dizziness, balance disorders, and fall prevention.'
        ),
        'sections': [
            (
                'Conditions we address',
                'Benign paroxysmal positional vertigo, vestibular neuritis, balance loss after injury '
                'or illness, age related balance decline, and dizziness linked to neck or concussion issues.',
            ),
            (
                'Vestibular rehabilitation',
                'Vestibular physiotherapy uses specific head movements, habituation exercises, and balance '
                'training to retrain your brain and inner ear system. BPPV can often improve significantly '
                'within one to three sessions.',
            ),
            (
                'Fall prevention in Calgary',
                'For older adults and anyone at fall risk, we assess gait, strength, and reaction time, then '
                'build a practical program to improve stability at home and in the community.',
            ),
        ],
        'benefits': [
            'Evidence based vestibular rehab techniques',
            'Reduced dizziness and improved daily confidence',
            'Personalized balance and strengthening exercises',
            'Safer mobility through Calgary changing seasons',
        ],
        'faqs': [
            (
                'Can vestibular therapy help vertigo?',
                'Yes. BPPV is one of the most treatable causes of vertigo. Our physiotherapists perform '
                'repositioning maneuvers and teach you how to manage symptoms.',
            ),
        ],
    },
    'pregnancy-postnatal': {
        'meta_description': _meta(
            'Pregnancy and Postnatal Physiotherapy Calgary',
            'Safe Calgary physiotherapy and massage for pregnancy pain and postpartum recovery.',
        ),
        'intro': (
            f'Pregnancy and new motherhood bring enormous change to your body. Our {CITY} '
            f'{CLINIC_SEO} in Calgary offers pregnancy and postnatal physiotherapy and massage therapy for '
            f'back and pelvic pain, diastasis recti, pelvic floor concerns, and safe return to exercise after birth.'
        ),
        'sections': [
            (
                'During pregnancy',
                'Low back pain, SI joint pain, rib discomfort, carpal tunnel symptoms, and pelvic girdle '
                'pain are common. We use safe manual techniques, taping, exercise, and education to keep you '
                'comfortable and active through all trimesters.',
            ),
            (
                'After birth',
                'Postnatal care covers pelvic floor recovery, abdominal separation, cesarean or perineal '
                'scar management, breastfeeding posture, and gradual return to walking, running, or gym '
                'training when you are ready.',
            ),
            (
                'Pelvic health connection',
                'Many pregnancy and postnatal issues overlap with pelvic floor function. Our team coordinates '
                'pelvic health assessment with your broader physiotherapy and massage plan.',
            ),
        ],
        'benefits': [
            'Trimester appropriate evidence based care',
            'Support for both vaginal and cesarean recovery',
            'Practical advice for sleep, feeding posture, and daily tasks',
            'Flexible appointments at our Calgary clinic',
        ],
        'faqs': [
            (
                'When can I start postnatal physiotherapy?',
                'Many patients begin around six weeks postpartum or sooner for specific concerns. We will '
                'guide you based on your delivery type and symptoms.',
            ),
        ],
    },
    'chronic-pain': {
        'meta_description': _meta(
            'Chronic Pain Physiotherapy and Massage Calgary',
            'Calgary chronic pain care with physiotherapy, massage therapy, and acupuncture.',
        ),
        'intro': (
            f'Living with chronic pain in {CITY} affects work, sleep, mood, and relationships. At our Calgary '
            f'{CLINIC_SEO}, chronic pain management combines physiotherapy, massage therapy, and acupuncture '
            f'to improve function, even when pain has persisted for months or years.'
        ),
        'sections': [
            (
                'A whole person approach',
                'Chronic pain is influenced by tissue health, nervous system sensitivity, stress, sleep, and '
                'activity levels. We address all of these with a plan that goes beyond short term relief.',
            ),
            (
                'Conditions we support',
                'Persistent back and neck pain, fibromyalgia, headaches, arthritis discomfort, neuropathic '
                'pain, and pain after injury that has not fully resolved.',
            ),
            (
                'Building capacity over time',
                'Graded exercise, pacing strategies, massage therapy, manual therapy, and pain education help '
                'you do more of what matters, whether that is working, hiking in the foothills, or playing with '
                'your kids.',
            ),
        ],
        'benefits': [
            'Physiotherapy and massage therapy under one Calgary roof',
            'Focus on function and quality of life',
            'Self management tools you can use long term',
            'Extended health insurance receipts provided',
        ],
        'faqs': [
            (
                'Will treatment eliminate my pain completely?',
                'Goals vary by person. Many patients achieve meaningful pain reduction and significant '
                'improvement in daily activity. We set honest, measurable goals together.',
            ),
        ],
    },
    'pelvic-health': {
        'meta_description': _meta(
            'Pelvic Health Physiotherapy Calgary',
            'Pelvic floor physiotherapy for incontinence, pain, and postpartum recovery in Calgary.',
        ),
        'intro': (
            f'Pelvic health concerns are common but often untreated. Our {CITY} {CLINIC_SEO} provides pelvic '
            f'floor physiotherapy in a professional, supportive environment for bladder leakage, pelvic pain, '
            f'prolapse symptoms, and postnatal pelvic recovery.'
        ),
        'sections': [
            (
                'Who benefits from pelvic physiotherapy',
                'Women and men of all ages, including postpartum patients, perimenopausal women, athletes '
                'with pelvic floor dysfunction, and men after prostate surgery.',
            ),
            (
                'What to expect',
                'Your first visit includes a detailed history and, with your consent, an internal or external '
                'assessment of pelvic floor muscle function. Treatment may include exercise, manual techniques, '
                'breathing coordination, and lifestyle modifications.',
            ),
            (
                'Common goals',
                'Reduce leakage with cough, sneeze, or sport; lessen pelvic pain; improve core and floor '
                'coordination; prepare for or recover from childbirth; return to intimacy without discomfort.',
            ),
        ],
        'benefits': [
            'Private, respectful one on one care',
            'Evidence based pelvic floor rehabilitation',
            'Coordination with your doctor or specialist if needed',
            'Calgary clinic serving northeast Calgary',
        ],
        'faqs': [
            (
                'Do I need a referral for pelvic physiotherapy in Alberta?',
                'Referral requirements depend on your insurance plan. Many extended health policies cover '
                'pelvic physiotherapy without a doctor note.',
            ),
        ],
    },
    'concussion-recovery': {
        'meta_description': _meta(
            'Concussion Recovery Physiotherapy Calgary',
            'Graduated return to sport and work programs after concussion in Calgary.',
        ),
        'intro': (
            f'Concussions are common in Calgary sport, recreation, and motor vehicle accidents. Our concussion '
            f'recovery program at our Calgary {CLINIC_SEO} supports safe, step by step return to school, work, '
            f'and sport using current concussion management guidelines.'
        ),
        'sections': [
            (
                'Symptoms we help manage',
                'Headache, dizziness, brain fog, light and noise sensitivity, neck pain, balance issues, '
                'and exercise intolerance after concussion.',
            ),
            (
                'Graduated return to activity',
                'Rest is important early on, but prolonged inactivity can delay recovery. We guide a '
                'structured progression back to cognitive and physical activity based on your symptoms.',
            ),
            (
                'Vestibular and neck care',
                'Many post concussion symptoms involve the neck and balance systems. Our team integrates '
                'vestibular rehab and cervical treatment when indicated.',
            ),
        ],
        'benefits': [
            'Individualized return to play or return to work plans',
            'Baseline and progress tracking throughout recovery',
            'Coordination with physicians and athletic trainers',
            'Calgary clinic experienced in sport related concussion',
        ],
        'faqs': [
            (
                'How long does concussion recovery take?',
                'Most adults recover within two to four weeks, but timelines vary. Early guidance reduces '
                'the risk of prolonged symptoms.',
            ),
        ],
    },
    'acupuncture-wellness': {
        'meta_description': _meta(
            'Acupuncture Calgary Wellness Clinic',
            'Acupuncture for pain relief, stress, and recovery at our Calgary physiotherapy and massage clinic.',
        ),
        'intro': (
            f'Acupuncture complements the core services at our Calgary {CLINIC_SEO} in {CITY}. Whether you '
            f'seek relief from chronic pain, tension headaches, stress, or support during injury recovery, our '
            f'registered acupuncturist provides safe, personalized treatment alongside physiotherapy and massage.'
        ),
        'sections': [
            (
                'How acupuncture helps',
                'Fine needles stimulate specific points to modulate pain signals, reduce muscle tension, '
                'support circulation, and promote relaxation. Modern research supports its use for many '
                'musculoskeletal and stress related conditions.',
            ),
            (
                'What we treat',
                'Back and neck pain, headaches, arthritis discomfort, sports injuries, stress and insomnia, '
                'and complementary support alongside physiotherapy or massage therapy.',
            ),
            (
                'Your first session',
                'We review your health history, discuss goals, and explain the treatment process. Most '
                'patients find acupuncture comfortable and leave feeling relaxed.',
            ),
        ],
        'benefits': [
            'Natural drug free pain and stress relief',
            'Complements physiotherapy and massage therapy',
            'Many Alberta extended health plans cover acupuncture',
            'Holistic wellness at our Calgary clinic',
        ],
        'faqs': [
            (
                'Does acupuncture hurt?',
                'Needles are very thin. Most people feel a brief tap or dull ache, not sharp pain. Many '
                'patients find sessions deeply relaxing.',
            ),
        ],
    },
}


def _treatment_page(title, slug, primary=False):
    service_focus = (
        f'Book {title.lower()} at our leading Calgary physiotherapy and massage clinic in Calgary.'
        if primary
        else f'Professional {title.lower()} at our Calgary wellness clinic.'
    )
    return {
        'meta_description': _meta(title, service_focus),
        'intro': (
            f'Looking for {title.lower()} in {LOCATION_PHRASE}? Our Calgary {CLINIC_SEO} offers '
            f'{title.lower()} from experienced practitioners who take time to understand your goals, '
            f'whether you are recovering from injury, managing chronic pain, or improving everyday movement.'
        ),
        'sections': [
            (
                f'{title} at our Calgary clinic',
                f'{title} is a core part of how we help Calgarians move better and feel better. After a '
                f'detailed assessment, your practitioner explains your diagnosis and recommended course of '
                f'care in plain language.',
            ),
            (
                'What to expect at your appointment',
                'Your first visit includes a health history, physical assessment, and discussion of your '
                'goals. Treatment begins on day one where appropriate, and you leave with clear next steps '
                'and any home exercises or advice.',
            ),
            (
                'Insurance and booking',
                'We provide receipts for Alberta extended health benefits and can direct bill many insurers. '
                f'Book {title.lower()} online anytime. Choose your service, practitioner, and appointment time.',
            ),
        ],
        'benefits': [
            f'Experienced {title.lower()} practitioners in Calgary',
            'Personalized treatment plans',
            'Evening and Saturday appointments available',
            f'Convenient Calgary {CITY} location',
        ],
        'faqs': [
            (
                'Is physiotherapy or massage covered by insurance in Alberta?',
                'Most Alberta extended health plans cover physiotherapy, massage therapy, chiropractic, and '
                'acupuncture to varying degrees. Check your policy or call us for guidance.',
            ),
        ],
    }


def _build_treatment_pages():
    from website.content import all_treatments
    return {
        item['slug']: _treatment_page(item['title'], item['slug'], item.get('primary', False))
        for item in all_treatments()
    }


def get_page_content(section, slug):
    if section == 'focus-areas':
        content = FOCUS_AREA_PAGES.get(slug)
    elif section == 'treatments':
        content = _build_treatment_pages().get(slug)
    else:
        return None
    if content and content.get('faqs') and not content.get('faq_intro'):
        return {**content, 'faq_intro': DEFAULT_FAQ_INTRO}
    return content
