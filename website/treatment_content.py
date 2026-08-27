"""Patient focused content for Our Treatments detail pages."""

CITY = 'Calgary'

DEFAULT_FAQ_INTRO = (
    'Common questions about what to expect, recovery, and booking at our Calgary clinic.'
)


def _meta(title, focus):
    return (
        f'{title} in {CITY}, Alberta. {focus} '
        f'Learn how we assess, treat, and track recovery at Medpro Physio.'
    )


def _page(
    *,
    slug,
    title,
    summary,
    intro,
    typical_sessions,
    first_improvement,
    recovery_timeline,
    benefits,
    assessment_steps,
    treatment_methods,
    recovery_phases,
    case_studies,
    faqs,
    meta_focus,
    benefits_heading='What this treatment helps with',
):
    return {
        'slug': slug,
        'title': title,
        'summary': summary,
        'meta_description': _meta(title, meta_focus),
        'description': f'<p>{intro}</p>',
        'typical_sessions': typical_sessions,
        'first_improvement': first_improvement,
        'recovery_timeline': recovery_timeline,
        'benefits_heading': benefits_heading,
        'benefits': benefits,
        'assessment_steps': assessment_steps,
        'treatment_methods': treatment_methods,
        'recovery_phases': recovery_phases,
        'case_studies': case_studies,
        'faqs': faqs,
        'faq_intro': DEFAULT_FAQ_INTRO,
    }


TREATMENT_PAGES = {
    'physiotherapy': _page(
        slug='physiotherapy',
        title='Physiotherapy',
        summary='Hands on assessment and treatment for pain, injury, and mobility in Calgary.',
        intro=(
            'Physiotherapy helps you move with less pain and more confidence. We assess how your '
            'body moves, identify what is driving your symptoms, and build a plan that fits your '
            'daily life, work, and activity goals.'
        ),
        typical_sessions='6 to 12 visits',
        first_improvement='2 to 4 sessions',
        recovery_timeline='4 to 12 weeks',
        meta_focus='Evidence based physiotherapy with clear assessment and recovery planning.',
        benefits=[
            'Pain relief and improved movement',
            'Clear home exercise plan',
            'Progress tracked each visit',
            'Return to work and sport safely',
        ],
        assessment_steps=[
            ('Health history', 'We review your pain pattern, past injuries, work demands, sleep, and activity level.'),
            ('Movement screen', 'We watch how you bend, walk, squat, and reach to find movement limits.'),
            ('Hands on testing', 'Joint, muscle, and nerve tests help us pinpoint the source of symptoms.'),
            ('Goal setting', 'You tell us what success looks like. We set realistic milestones together.'),
        ],
        treatment_methods=[
            ('Manual therapy', 'Joint mobilisation and soft tissue work to reduce stiffness and pain.'),
            ('Exercise therapy', 'Targeted strengthening and mobility drills you can repeat at home.'),
            ('Pain education', 'We explain what is happening so you know what helps and what to avoid.'),
            ('Activity planning', 'We adjust load for work, sport, and daily tasks as you improve.'),
        ],
        recovery_phases=[
            ('Calm symptoms', 'Week 1 to 2', 'Reduce pain flare ups and restore basic movement.'),
            ('Rebuild strength', 'Week 3 to 6', 'Progress loading with guided exercises and hands on care.'),
            ('Return to activity', 'Week 6 to 12', 'Sport or work specific drills and independence plan.'),
        ],
        case_studies=[
            {
                'patient_label': 'Office worker, 42',
                'issue': 'Lower back pain after long desk hours',
                'approach': (
                    'We started with a movement screen and found limited hip hinge and weak deep core '
                    'activation after long sitting. Treatment combined manual therapy for the lower back, '
                    'progressive core stability drills, and a simple desk break routine every 45 minutes.'
                ),
                'outcome': (
                    'Daily pain dropped from a 7 to a 2 within five weeks. He returned to gym training '
                    'with a modified program and now manages occasional flare ups with his home exercises. '
                    'He has not missed work since finishing the plan.'
                ),
                'timeline': '8 weeks',
            },
            {
                'patient_label': 'Recreational runner, 29',
                'issue': 'Knee pain during longer runs',
                'approach': (
                    'A running gait review showed early heel strike and weak left glute medius. We used '
                    'hip strengthening, cadence cues, and a graded return from walk run intervals to '
                    'full distance over eight weeks.'
                ),
                'outcome': (
                    'Knee pain during runs resolved by week six. She completed a local 10K without pain '
                    'and continues a twice weekly strength routine to stay injury free. '
                    'Her longest run is now back to pre injury distance.'
                ),
                'timeline': '10 weeks',
            },
        ],
        faqs=[
            ('Does physiotherapy hurt?', 'Some techniques may feel firm, but treatment should stay tolerable. We adjust based on your feedback.'),
            ('How often should I come?', 'Most patients start weekly, then space visits as symptoms improve.'),
            ('Will I get exercises to do at home?', 'Yes. Home exercises are a core part of recovery and are tailored to your level.'),
        ],
    ),
    'massage-therapy': _page(
        slug='massage-therapy',
        title='Massage Therapy',
        summary='Therapeutic massage to ease muscle tension, stress, and recovery in Calgary.',
        intro=(
            'Massage therapy targets tight muscles, stress related tension, and recovery after '
            'activity or injury. Your therapist assesses which areas need focus and chooses '
            'techniques that match your comfort level and goals.'
        ),
        typical_sessions='4 to 8 visits',
        first_improvement='1 to 2 sessions',
        recovery_timeline='2 to 8 weeks',
        meta_focus='Therapeutic massage with assessment driven treatment plans.',
        benefits=[
            'Reduced muscle tension',
            'Better sleep and stress relief',
            'Faster recovery after activity',
            'Improved range of motion',
        ],
        assessment_steps=[
            ('Consultation', 'We discuss pain areas, stress levels, activity, and any health conditions.'),
            ('Posture check', 'We observe how you sit and stand to find patterns driving tension.'),
            ('Palpation', 'We locate tight bands, trigger points, and areas of restricted movement.'),
            ('Treatment plan', 'We agree on pressure level, focus areas, and session frequency.'),
        ],
        treatment_methods=[
            ('Swedish techniques', 'Rhythmic strokes to improve circulation and general relaxation.'),
            ('Deep tissue focus', 'Slower pressure on chronic tight areas when appropriate.'),
            ('Trigger point release', 'Targeted pressure to reduce referred pain from muscle knots.'),
            ('Stretching guidance', 'Simple stretches to maintain gains between sessions.'),
        ],
        recovery_phases=[
            ('Relief', 'Session 1 to 2', 'Noticeable easing of tension and improved comfort.'),
            ('Maintenance', 'Week 2 to 4', 'Muscle tone improves with regular sessions and self care.'),
            ('Prevention', 'Ongoing', 'Monthly or seasonal visits to manage stress and activity load.'),
        ],
        case_studies=[
            {
                'patient_label': 'Teacher, 38',
                'issue': 'Neck and shoulder tension from screen work',
                'approach': (
                    'Assessment showed tight upper traps and forward head posture from marking papers and '
                    'screen time. We used focused neck and shoulder massage, upper back release, and '
                    'short classroom friendly stretch breaks she could do between classes.'
                ),
                'outcome': (
                    'Headaches went from several per week to rare within a month. She now works full '
                    'teaching days with much less neck tension. Monthly maintenance sessions help her '
                    'stay comfortable through the school year.'
                ),
                'timeline': '5 weeks',
            },
        ],
        faqs=[
            ('What should I wear?', 'Comfortable clothing. Most areas are treated while you are draped on the table.'),
            ('Is deep tissue always better?', 'No. Pressure is matched to your goals and tissue response.'),
            ('Can massage help with injury recovery?', 'Yes, especially when combined with physiotherapy for structured rehab.'),
        ],
    ),
    'manual-therapy': _page(
        slug='manual-therapy',
        title='Manual Therapy',
        summary='Hands on joint and soft tissue techniques to restore comfortable movement.',
        intro=(
            'Manual therapy uses skilled hands on techniques to improve joint mobility and reduce '
            'muscle restriction. It is often combined with exercise so improvements last beyond '
            'the treatment table.'
        ),
        typical_sessions='4 to 8 visits',
        first_improvement='1 to 3 sessions',
        recovery_timeline='3 to 8 weeks',
        meta_focus='Skilled manual therapy integrated with active rehabilitation.',
        benefits=[
            'Improved joint mobility',
            'Less muscle guarding',
            'Faster progress with exercise',
            'Targeted relief for stiff areas',
        ],
        assessment_steps=[
            ('Joint range testing', 'We measure how far each joint moves and where it feels blocked.'),
            ('Soft tissue exam', 'We check muscle tone, tenderness, and movement quality.'),
            ('Functional test', 'We see how restrictions affect daily tasks like reaching or bending.'),
            ('Safety screen', 'We rule out issues that need medical referral before hands on work.'),
        ],
        treatment_methods=[
            ('Joint mobilisation', 'Graded movements to improve joint glide and reduce stiffness.'),
            ('Soft tissue release', 'Techniques to ease tight fascia and muscle layers.'),
            ('Neural mobilisation', 'Gentle nerve gliding when nerve tension contributes to symptoms.'),
            ('Home follow up', 'Simple mobility drills to keep gains between visits.'),
        ],
        recovery_phases=[
            ('Mobility gains', 'Week 1 to 2', 'Notice easier movement after early sessions.'),
            ('Stability', 'Week 2 to 5', 'Strengthening supports new range of motion.'),
            ('Independence', 'Week 5+', 'Self management with occasional tune up visits.'),
        ],
        case_studies=[
            {
                'patient_label': 'Warehouse worker, 45',
                'issue': 'Stiff mid back when lifting',
                'approach': (
                    'We found stiff thoracic extension and poor lifting mechanics when loading pallets. '
                    'Sessions included thoracic joint mobilisation, rib cage mobility work, and coached '
                    'repetitions of safe lifting patterns with load he uses on the job.'
                ),
                'outcome': (
                    'Morning stiffness that used to last an hour cleared within four weeks. He returned '
                    'to full warehouse shifts without pain at the end of the day. He still uses the '
                    'warm up routine before heavy lifting days.'
                ),
                'timeline': '6 weeks',
            },
        ],
        faqs=[
            ('Will I hear cracking sounds?', 'Sometimes joints release with movement. We never force a manipulation.'),
            ('Is manual therapy only for backs?', 'No. We use it for shoulders, hips, neck, and other joints.'),
            ('How long do results last?', 'Lasting change usually needs exercise alongside hands on care.'),
        ],
    ),
    'exercise-rehab': _page(
        slug='exercise-rehab',
        title='Exercise Rehabilitation',
        summary='Structured exercise programs to rebuild strength, balance, and function.',
        intro=(
            'Exercise rehabilitation turns assessment findings into a step by step training plan. '
            'We progress load safely so you rebuild capacity for work, sport, and daily life.'
        ),
        typical_sessions='8 to 16 visits',
        first_improvement='3 to 5 sessions',
        recovery_timeline='6 to 16 weeks',
        meta_focus='Progressive exercise programs tailored to your injury and goals.',
        benefits=[
            'Stronger, more resilient movement',
            'Lower reinjury risk',
            'Clear progression each week',
            'Confidence returning to activity',
        ],
        assessment_steps=[
            ('Strength testing', 'We measure key muscle groups related to your injury.'),
            ('Balance and control', 'We check single leg stability and movement quality.'),
            ('Load tolerance', 'We find what weight, reps, or duration you can handle today.'),
            ('Program design', 'We map phases from basic activation to full activity.'),
        ],
        treatment_methods=[
            ('Activation drills', 'Wake up underactive muscles before loading.'),
            ('Resistance training', 'Bands, weights, and bodyweight progressions.'),
            ('Plyometric prep', 'Jump and landing drills when ready for higher demand.'),
            ('Sport or work simulation', 'Tasks that mirror what you need to return to.'),
        ],
        recovery_phases=[
            ('Foundation', 'Week 1 to 3', 'Build baseline strength and movement control.'),
            ('Capacity', 'Week 4 to 8', 'Increase volume and introduce functional patterns.'),
            ('Performance', 'Week 8+', 'Return to sport or job specific demands.'),
        ],
        case_studies=[
            {
                'patient_label': 'Hockey player, 22',
                'issue': 'Groin strain during season',
                'approach': (
                    'Testing showed reduced hip abduction strength and poor single leg control on the '
                    'injured side. Rehab progressed from band walks and bridges to on ice skating '
                    'simulation drills and sport specific cutting patterns over twelve weeks.'
                ),
                'outcome': (
                    'He returned to league play at full speed in week ten with no groin recurrence. '
                    'Strength testing matched his uninjured side before clearance. He continues a '
                    'twice weekly hip program during the season.'
                ),
                'timeline': '12 weeks',
            },
        ],
        faqs=[
            ('Do I need a gym?', 'No. We start with bands and bodyweight. Gym access helps later phases.'),
            ('Will exercises hurt?', 'Some muscle effort is normal. Sharp pain means we adjust the plan.'),
            ('Can I keep training?', 'Often yes, with modified loads while injured tissue heals.'),
        ],
    ),
    'kinesiology': _page(
        slug='kinesiology',
        title='Kinesiology',
        summary='Exercise science based coaching for strength, balance, and healthy movement.',
        intro=(
            'Kinesiology focuses on how your body performs during movement. We use exercise '
            'science to improve strength, endurance, balance, and movement habits for injury '
            'recovery or performance goals.'
        ),
        typical_sessions='6 to 12 visits',
        first_improvement='2 to 4 sessions',
        recovery_timeline='6 to 12 weeks',
        meta_focus='Exercise based kinesiology for recovery and performance in Calgary.',
        benefits=[
            'Better movement efficiency',
            'Improved strength and endurance',
            'Personalized training plan',
            'Education on safe exercise form',
        ],
        assessment_steps=[
            ('Fitness baseline', 'We test strength, flexibility, and cardiovascular readiness.'),
            ('Movement analysis', 'We review squat, lunge, and gait patterns on video when helpful.'),
            ('Goal review', 'Weight loss, return to sport, or injury prevention targets guide the plan.'),
            ('Program outline', 'We set weekly structure with clear milestones.'),
        ],
        treatment_methods=[
            ('Corrective exercise', 'Drills to fix compensations found in assessment.'),
            ('Strength programming', 'Progressive sets and reps matched to your level.'),
            ('Balance training', 'Single leg and reactive drills for stability.'),
            ('Education', 'Form cues and pacing so you train safely on your own.'),
        ],
        recovery_phases=[
            ('Learn', 'Week 1 to 2', 'Master basic patterns with light load.'),
            ('Build', 'Week 3 to 6', 'Increase volume and introduce compound movements.'),
            ('Maintain', 'Week 6+', 'Independent program with periodic check ins.'),
        ],
        case_studies=[
            {
                'patient_label': 'New to fitness, 55',
                'issue': 'Fear of exercise after knee soreness',
                'approach': (
                    'She was nervous about exercise after knee soreness on stairs. We built confidence '
                    'with seated strength work, then progressed to supported squats, balance drills, and '
                    'a gentle walking plan that increased by five minutes each week.'
                ),
                'outcome': (
                    'Within ten weeks she walks 30 minutes most days without knee pain. She strength '
                    'trains twice weekly at her community gym with a program we designed together. '
                    'She reports feeling steadier on stairs and when getting up from chairs.'
                ),
                'timeline': '10 weeks',
            },
        ],
        faqs=[
            ('How is kinesiology different from physiotherapy?', 'Kinesiology leans heavily on exercise coaching. Physio may include more hands on care.'),
            ('Do I need equipment?', 'We start minimal. Bands and simple home items work well.'),
            ('Can kinesiology help before surgery?', 'Yes. Prehab improves outcomes for many joint procedures.'),
        ],
    ),
    'dry-needling': _page(
        slug='dry-needling',
        title='Dry Needling',
        summary='Targeted needle techniques to release muscle trigger points and reduce pain.',
        intro=(
            'Dry needling uses thin needles into tight muscle bands to reduce trigger point '
            'activity and pain. It is combined with movement and exercise so relief lasts.'
        ),
        typical_sessions='3 to 6 visits',
        first_improvement='1 to 2 sessions',
        recovery_timeline='2 to 6 weeks',
        meta_focus='Safe dry needling integrated with movement based rehab.',
        benefits=[
            'Quick relief for muscle knots',
            'Improved muscle activation',
            'Less referred pain',
            'Pairs well with exercise rehab',
        ],
        assessment_steps=[
            ('Trigger point map', 'We locate tight bands and referred pain patterns.'),
            ('Medical screen', 'We confirm needling is appropriate for your health history.'),
            ('Consent and education', 'We explain sensations, risks, and aftercare.'),
            ('Movement link', 'We connect needle targets to how you move daily.'),
        ],
        treatment_methods=[
            ('Local needling', 'Brief insertion into identified trigger points.'),
            ('Movement after care', 'Gentle activation exercises post session.'),
            ('Soft tissue work', 'Manual release when needed alongside needling.'),
            ('Load management', 'Adjust activity until tissue settles.'),
        ],
        recovery_phases=[
            ('Post session', 'Day 1', 'Mild soreness possible. Light movement encouraged.'),
            ('Integration', 'Week 1 to 2', 'Combine needling with stretching and strengthening.'),
            ('Resolution', 'Week 2 to 6', 'Symptoms fade as movement improves.'),
        ],
        case_studies=[
            {
                'patient_label': 'Trades worker, 36',
                'issue': 'Persistent shoulder knot from overhead work',
                'approach': (
                    'We mapped a persistent infraspinatus trigger point referring pain into the deltoid. '
                    'Dry needling was paired with rotator cuff activation exercises and scapular '
                    'stability drills performed before and after overhead work shifts.'
                ),
                'outcome': (
                    'Night pain that kept him awake eased after the second session. By week four he '
                    'could complete a full day of overhead work without needing ice at home. '
                    'He still does a ten minute shoulder routine before demanding jobs.'
                ),
                'timeline': '4 weeks',
            },
        ],
        faqs=[
            ('Is dry needling the same as acupuncture?', 'No. Dry needling targets muscle trigger points. Acupuncture follows traditional meridian theory.'),
            ('Does it hurt?', 'You may feel a brief twitch or ache. Most patients tolerate it well.'),
            ('Are there side effects?', 'Mild soreness for a day is common. We review risks before treatment.'),
        ],
    ),
    'balance-fall-prevention': _page(
        slug='balance-fall-prevention',
        title='Balance & Fall Prevention',
        summary='Assessment and training to improve steadiness and reduce fall risk.',
        intro=(
            'Balance and fall prevention programs assess why you feel unsteady and train the '
            'systems that keep you upright: vision, inner ear, strength, and reaction time.'
        ),
        typical_sessions='8 to 12 visits',
        first_improvement='3 to 5 sessions',
        recovery_timeline='8 to 12 weeks',
        meta_focus='Evidence based balance training for older adults and injury recovery.',
        benefits=[
            'Greater confidence walking',
            'Stronger legs and core',
            'Faster balance reactions',
            'Safer home and community mobility',
        ],
        assessment_steps=[
            ('Fall history', 'We review past falls, medications, and home hazards.'),
            ('Balance tests', 'Timed stands, tandem walk, and reach tests show baseline risk.'),
            ('Strength screen', 'Leg power and ankle stability predict steadiness.'),
            ('Goal plan', 'We target tasks that matter: stairs, snow, or crowded spaces.'),
        ],
        treatment_methods=[
            ('Static balance', 'Narrow base and single leg holds with support as needed.'),
            ('Dynamic drills', 'Walking turns, stepping over obstacles, and dual tasks.'),
            ('Strength work', 'Sit to stand, calf raises, and hip abductor training.'),
            ('Home safety tips', 'Simple changes to reduce trip hazards.'),
        ],
        recovery_phases=[
            ('Confidence', 'Week 1 to 3', 'Feel steadier on even ground with guided drills.'),
            ('Challenge', 'Week 4 to 8', 'Uneven surfaces and faster reactions.'),
            ('Independence', 'Week 8+', 'Home program and optional maintenance classes.'),
        ],
        case_studies=[
            {
                'patient_label': 'Retiree, 72',
                'issue': 'Near falls on icy sidewalks',
                'approach': (
                    'Balance testing showed slow reactive stepping and weak quadriceps on both sides. '
                    'We used single leg stands, tandem walking, sit to stand power drills, and outdoor '
                    'practice on uneven paths with a walking pole for confidence.'
                ),
                'outcome': (
                    'Near falls on icy sidewalks stopped after six weeks of consistent practice. She '
                    'used a cane through winter and walked neighborhood paths independently by spring. '
                    'She still does her home balance routine three times per week.'
                ),
                'timeline': '12 weeks',
            },
        ],
        faqs=[
            ('Am I too old to improve balance?', 'Most people improve with consistent practice at any age.'),
            ('Do I need special equipment?', 'We start with chairs and walls. Progress to balance pads when ready.'),
            ('Can this help after a stroke?', 'Often yes, as part of a broader rehab plan tailored to your needs.'),
        ],
    ),
    'joint-mobilisation': _page(
        slug='joint-mobilisation',
        title='Joint Mobilisation',
        summary='Gentle joint techniques to improve glide, reduce stiffness, and ease pain.',
        intro=(
            'Joint mobilisation applies controlled pressures to stiff joints so they move more '
            'freely. It is graded from light to firm based on your comfort and tissue irritability.'
        ),
        typical_sessions='4 to 8 visits',
        first_improvement='1 to 3 sessions',
        recovery_timeline='3 to 8 weeks',
        meta_focus='Skilled joint mobilisation for stiffness and restricted movement.',
        benefits=[
            'Less joint stiffness',
            'Smoother daily movement',
            'Better exercise tolerance',
            'Pairs with strengthening',
        ],
        assessment_steps=[
            ('Joint scan', 'We test each affected joint’s range and end feel.'),
            ('Irritability check', 'We note if tissues are easily flared to set treatment intensity.'),
            ('Functional link', 'We connect joint limits to tasks like dressing or driving.'),
            ('Plan', 'We choose grade of mobilisation and supporting exercises.'),
        ],
        treatment_methods=[
            ('Oscillatory mobilisation', 'Rhythmic joint movements to reduce pain and stiffness.'),
            ('Sustained glide', 'Held pressures at range limits when appropriate.'),
            ('Muscle release', 'Soft tissue work around guarded joints.'),
            ('Active range', 'You move through new range immediately after treatment.'),
        ],
        recovery_phases=[
            ('Opening range', 'Week 1 to 2', 'Easier basic movements like turning the neck or bending the knee.'),
            ('Loading', 'Week 3 to 5', 'Strengthen through improved range.'),
            ('Maintenance', 'Week 5+', 'Home mobility routine keeps joints moving.'),
        ],
        case_studies=[
            {
                'patient_label': 'Cyclist, 48',
                'issue': 'Stiff ankle after sprain months ago',
                'approach': (
                    'Ankle dorsiflexion was limited months after the sprain, affecting his pedal stroke. '
                    'We combined grade III ankle mobilisations, calf eccentric loading, and a cycling '
                    'progression from trainer to short outdoor rides as range improved.'
                ),
                'outcome': (
                    'Morning ankle stiffness resolved by week five. He restored a full smooth pedal '
                    'stroke and completed a 50K charity ride without swelling afterward. '
                    'He keeps up calf mobility work before longer rides.'
                ),
                'timeline': '7 weeks',
            },
        ],
        faqs=[
            ('Is mobilisation the same as manipulation?', 'Mobilisation uses smaller graded movements. Manipulation is a quicker thrust technique.'),
            ('Will it fix arthritis?', 'It cannot reverse arthritis, but it often improves how the joint moves and feels.'),
            ('How soon will I feel change?', 'Many patients notice easier movement after the first few sessions.'),
        ],
    ),
    'sports-performance': _page(
        slug='sports-performance',
        title='Sports Performance',
        summary='Movement screening and training to boost power, speed, and injury resilience.',
        intro=(
            'Sports performance care identifies movement limits that cap your speed or power, then '
            'builds strength, agility, and recovery habits so you train harder with less downtime.'
        ),
        typical_sessions='8 to 16 visits',
        first_improvement='3 to 4 sessions',
        recovery_timeline='8 to 16 weeks',
        meta_focus='Performance focused training for Calgary athletes and active adults.',
        benefits=[
            'Higher power and speed',
            'Better movement efficiency',
            'Lower injury risk',
            'Sport specific progress tracking',
        ],
        assessment_steps=[
            ('Sport demands', 'We review your schedule, position, and performance goals.'),
            ('Movement screen', 'Jump, land, cut, and sprint mechanics on video when useful.'),
            ('Strength profile', 'We test asymmetries that predict injury or limit output.'),
            ('Periodisation', 'We align training phases with your competition calendar.'),
        ],
        treatment_methods=[
            ('Power development', 'Olympic lift progressions or plyometrics when appropriate.'),
            ('Agility drills', 'Change of direction and deceleration training.'),
            ('Mobility work', 'Targeted prep for hips, ankles, and thoracic spine.'),
            ('Recovery planning', 'Sleep, load monitoring, and soft tissue care.'),
        ],
        recovery_phases=[
            ('Foundation', 'Week 1 to 4', 'Fix asymmetries and build work capacity.'),
            ('Build', 'Week 5 to 10', 'Increase intensity and sport specific volume.'),
            ('Peak', 'Week 10+', 'Taper and performance testing before events.'),
        ],
        case_studies=[
            {
                'patient_label': 'Soccer player, 19',
                'issue': 'Hamstring tightness limiting sprint speed',
                'approach': (
                    'Video analysis showed reduced hip extension and hamstring tightness during sprinting. '
                    'We used Nordic hamstring progressions, hip flexor mobility, and sprint drill '
                    'progressions from submaximal runs to full pace over fourteen weeks.'
                ),
                'outcome': (
                    'His 20 meter sprint time improved by 0.15 seconds and he played a full season '
                    'without hamstring setbacks. He continues Nordic curls twice weekly in preseason. '
                    'Coaching staff noted cleaner acceleration form in late season games.'
                ),
                'timeline': '14 weeks',
            },
        ],
        faqs=[
            ('Is this only for elite athletes?', 'No. Recreational runners and gym goers benefit from structured performance work.'),
            ('Will this replace my coach?', 'We complement coaching with injury screening and corrective work.'),
            ('How often should I train?', 'Usually 2 to 3 sessions weekly plus your sport practice.'),
        ],
    ),
    'chiropractic': _page(
        slug='chiropractic',
        title='Chiropractic Care',
        summary='Spine and joint focused care to improve alignment, mobility, and pain relief.',
        intro=(
            'Chiropractic care assesses how your spine and joints move, then uses adjustments, '
            'mobilisation, and exercise to reduce pain and restore comfortable movement.'
        ),
        typical_sessions='6 to 10 visits',
        first_improvement='2 to 4 sessions',
        recovery_timeline='4 to 10 weeks',
        meta_focus='Chiropractic assessment and treatment for back, neck, and joint pain.',
        benefits=[
            'Improved spinal mobility',
            'Less back and neck pain',
            'Better posture awareness',
            'Integrated exercise advice',
        ],
        assessment_steps=[
            ('Posture and gait', 'We observe alignment during standing and walking.'),
            ('Spinal exam', 'Joint motion, muscle tension, and nerve screens as needed.'),
            ('Imaging review', 'We discuss any X rays or MRIs you bring.'),
            ('Care plan', 'We explain recommended techniques and expected timeline.'),
        ],
        treatment_methods=[
            ('Spinal adjustment', 'Controlled impulses to improve joint motion when appropriate.'),
            ('Mobilisation', 'Gentler rhythmic techniques for sensitive areas.'),
            ('Soft tissue therapy', 'Release tight muscles supporting the spine.'),
            ('Rehab exercises', 'Core and postural drills to maintain improvements.'),
        ],
        recovery_phases=[
            ('Relief', 'Week 1 to 2', 'Pain and stiffness often ease with early care.'),
            ('Correction', 'Week 3 to 6', 'Mobility and strength work support adjustments.'),
            ('Wellness', 'Ongoing', 'Periodic visits or home routine to prevent flare ups.'),
        ],
        case_studies=[
            {
                'patient_label': 'Driver, 50',
                'issue': 'Neck stiffness and headaches after long shifts',
                'approach': (
                    'Cervical range was limited in rotation and upper traps were constantly tight after '
                    'long driving shifts. Care included cervical mobilisation, upper back manual release, '
                    'and a stretching and strengthening plan he could do at rest stops.'
                ),
                'outcome': (
                    'Headache frequency dropped from four per week to one or two per month. Neck rotation '
                    'improved enough to check blind spots comfortably while driving. He uses his stretch '
                    'routine before every long haul shift now.'
                ),
                'timeline': '8 weeks',
            },
        ],
        faqs=[
            ('Are adjustments safe?', 'When performed after proper assessment, adjustments are generally safe. We adapt technique to your needs.'),
            ('Will I need ongoing care forever?', 'Many patients taper to occasional visits once symptoms settle.'),
            ('Do you take X rays in clinic?', 'We refer for imaging when clinically indicated.'),
        ],
    ),
    'acupuncture': _page(
        slug='acupuncture',
        title='Acupuncture',
        summary='Traditional needle therapy for pain relief, stress, and recovery support.',
        intro=(
            'Acupuncture uses fine needles at specific points to influence pain pathways and '
            'promote relaxation. We integrate it with physiotherapy or massage when a combined '
            'plan helps you recover faster.'
        ),
        typical_sessions='6 to 10 visits',
        first_improvement='2 to 4 sessions',
        recovery_timeline='4 to 12 weeks',
        meta_focus='Registered acupuncture for pain and wellness in Calgary.',
        benefits=[
            'Pain modulation',
            'Stress and sleep support',
            'Complements hands on rehab',
            'Minimal downtime after sessions',
        ],
        assessment_steps=[
            ('Traditional intake', 'We review sleep, digestion, stress, and pain patterns.'),
            ('Point selection', 'Points chosen based on your presentation and goals.'),
            ('Safety screen', 'We confirm needling is appropriate for your health history.'),
            ('Treatment rhythm', 'We set session frequency based on symptom severity.'),
        ],
        treatment_methods=[
            ('Body acupuncture', 'Fine needles left in place while you rest comfortably.'),
            ('Electro acupuncture', 'Gentle electrical stimulation when indicated for pain.'),
            ('Ear points', 'Short sessions for stress or craving support when relevant.'),
            ('Lifestyle advice', 'Sleep, pacing, and movement tips between visits.'),
        ],
        recovery_phases=[
            ('Initial series', 'Week 1 to 4', 'Weekly visits to build cumulative effect.'),
            ('Consolidation', 'Week 4 to 8', 'Symptoms stabilize with biweekly care.'),
            ('Maintenance', 'As needed', 'Monthly or seasonal tune ups for chronic issues.'),
        ],
        case_studies=[
            {
                'patient_label': 'Chronic pain patient, 47',
                'issue': 'Persistent neck pain despite exercise',
                'approach': (
                    'She had tried exercise alone with limited relief for persistent neck pain. We added '
                    'acupuncture twice weekly for four weeks alongside gentle cervical mobility and '
                    'breathing work to reduce muscle guarding around the upper shoulders.'
                ),
                'outcome': (
                    'Pain scores on a 0 to 10 scale dropped from 6 to 2 over ten weeks. She returned '
                    'to weekly yoga classes and sleeps through the night without neck waking her. '
                    'She now uses acupuncture monthly for maintenance during stressful periods.'
                ),
                'timeline': '10 weeks',
            },
        ],
        faqs=[
            ('Does acupuncture hurt?', 'Needles are thin. You may feel a brief pinch or dull ache.'),
            ('How many needles are used?', 'Often 8 to 15 depending on the treatment plan.'),
            ('Can I exercise after?', 'Light activity is fine. We advise if you should rest the day of treatment.'),
        ],
    ),
    'myofascial-release': _page(
        slug='myofascial-release',
        title='Myofascial Release',
        summary='Slow sustained pressure to ease fascial restriction and chronic tightness.',
        intro=(
            'Myofascial release targets the connective tissue around muscles. Sustained gentle '
            'pressure helps tight areas soften so movement feels freer and exercise works better.'
        ),
        typical_sessions='4 to 8 visits',
        first_improvement='2 to 3 sessions',
        recovery_timeline='4 to 8 weeks',
        meta_focus='Hands on myofascial release for chronic tightness and movement limits.',
        benefits=[
            'Less widespread tightness',
            'Improved flexibility',
            'Better exercise range',
            'Calmer nervous system response',
        ],
        assessment_steps=[
            ('Fascial scan', 'We glide hands over tissue to find restricted lines and zones.'),
            ('Movement tie in', 'We link restrictions to painful or limited movements.'),
            ('Sensitivity check', 'Pressure adjusted for chronic pain or fibromyalgia.'),
            ('Home plan', 'Foam roller or ball work when appropriate.'),
        ],
        treatment_methods=[
            ('Direct release', 'Sustained pressure held until tissue softens.'),
            ('Indirect release', 'Gentle positioning until tension eases.'),
            ('Cross fiber work', 'Broad strokes along muscle lines.'),
            ('Breathing cues', 'Relaxed breathing improves tissue response.'),
        ],
        recovery_phases=[
            ('Release', 'Week 1 to 2', 'Tissue feels looser after sessions. Mild soreness possible.'),
            ('Movement', 'Week 3 to 5', 'Stretch and strengthen through new range.'),
            ('Self care', 'Week 5+', 'Home tools maintain openness.'),
        ],
        case_studies=[
            {
                'patient_label': 'Desk worker, 40',
                'issue': 'Chronic hip and IT band tightness',
                'approach': (
                    'Fascial restrictions along the lateral hip and IT band were limiting comfortable '
                    'sitting and running. We used sustained myofascial release, glute strengthening, '
                    'and a gradual return to running from walk run intervals once tissue tolerated load.'
                ),
                'outcome': (
                    'He sits through two hour meetings without needing to stand and stretch constantly. '
                    'By week nine he completed a 5K run without lateral knee pain for the first time '
                    'in a year. He foam rolls and does glute activation before runs.'
                ),
                'timeline': '9 weeks',
            },
        ],
        faqs=[
            ('Is this like massage?', 'Similar hands on work, but focuses on fascia with longer holds.'),
            ('Will I be sore after?', 'Mild soreness for a day is common. We adjust intensity to your tolerance.'),
            ('How is it different from stretching?', 'Release works tissue before stretching so range gains last longer.'),
        ],
    ),
    'ultrasound-therapy': _page(
        slug='ultrasound-therapy',
        title='Ultrasound Therapy',
        summary='Therapeutic ultrasound to support tissue healing and reduce local pain.',
        intro=(
            'Therapeutic ultrasound uses sound waves to warm deep tissues and support healing in '
            'tendons and muscles. It is one tool in a broader rehab plan, not a standalone fix.'
        ),
        typical_sessions='6 to 10 visits',
        first_improvement='3 to 5 sessions',
        recovery_timeline='4 to 10 weeks',
        meta_focus='Ultrasound therapy as part of structured physiotherapy rehab.',
        benefits=[
            'Supports tendon healing',
            'Reduces local pain',
            'Prepares tissue for exercise',
            'Non invasive adjunct care',
        ],
        assessment_steps=[
            ('Tissue diagnosis', 'We confirm ultrasound suits your injury type.'),
            ('Area mapping', 'We identify exact treatment site and depth.'),
            ('Contraindication check', 'We avoid use over implants, infection, or pregnancy areas.'),
            ('Combined plan', 'We pair ultrasound with exercise and manual care.'),
        ],
        treatment_methods=[
            ('Pulsed ultrasound', 'Lower intensity for acute or sensitive tissue.'),
            ('Continuous ultrasound', 'Gentle heating for chronic tendon issues when appropriate.'),
            ('Exercise progression', 'Loading exercises after ultrasound prep.'),
            ('Education', 'Activity modification until tissue tolerates load.'),
        ],
        recovery_phases=[
            ('Acute care', 'Week 1 to 2', 'Pain control and protected movement.'),
            ('Loading', 'Week 3 to 6', 'Gradual strengthening of healed tissue.'),
            ('Return', 'Week 6+', 'Sport or work tasks reintroduced.'),
        ],
        case_studies=[
            {
                'patient_label': 'Tennis player, 35',
                'issue': 'Elbow tendon irritation',
                'approach': (
                    'Ultrasound was applied before each session to support tendon healing at the elbow. '
                    'We progressed from isometric wrist holds to slow eccentric lowering exercises with '
                    'increasing load as grip strength and pain levels allowed.'
                ),
                'outcome': (
                    'Grip pain during serves eased by week four. He returned to league tennis without '
                    'a brace at week eight and played a full tournament season. He still warms up with '
                    'eccentric wrist exercises before matches.'
                ),
                'timeline': '8 weeks',
            },
        ],
        faqs=[
            ('Will I feel heat?', 'You may feel gentle warmth. Sensation varies by settings.'),
            ('How long is each application?', 'Usually 5 to 8 minutes per area.'),
            ('Is ultrasound enough on its own?', 'No. Exercise and load management drive lasting recovery.'),
        ],
    ),
    'kinesio-taping': _page(
        slug='kinesio-taping',
        title='Kinesio Taping',
        summary='Elastic taping to support movement, reduce pain, and cue better posture.',
        intro=(
            'Kinesio taping uses flexible tape to give light support and sensory feedback. It helps '
            'some patients move with less pain while they build strength through exercise.'
        ),
        typical_sessions='3 to 6 visits',
        first_improvement='1 to 2 sessions',
        recovery_timeline='2 to 6 weeks',
        meta_focus='Therapeutic taping integrated with active rehabilitation.',
        benefits=[
            'Light support without rigidity',
            'Pain relief during movement',
            'Posture and movement cues',
            'Wearable for several days',
        ],
        assessment_steps=[
            ('Movement test', 'We see if tape changes pain or control during key tasks.'),
            ('Skin check', 'We confirm no allergy or irritation before application.'),
            ('Goal match', 'Tape used when it supports exercise goals, not as a crutch.'),
            ('Teach self care', 'We show how to remove tape safely.'),
        ],
        treatment_methods=[
            ('Pain relief taping', 'Decompressive strips over sore areas.'),
            ('Support taping', 'Facilitation patterns for weak muscles.'),
            ('Postural taping', 'Gentle reminders for desk or sport posture.'),
            ('Exercise pairing', 'Tape worn during rehab drills when helpful.'),
        ],
        recovery_phases=[
            ('Support', 'Week 1', 'Tape plus modified activity.'),
            ('Strength', 'Week 2 to 4', 'Less reliance on tape as muscles activate.'),
            ('Independence', 'Week 4+', 'Tape optional for sport or heavy days.'),
        ],
        case_studies=[
            {
                'patient_label': 'Volleyball player, 24',
                'issue': 'Shoulder pain when serving',
                'approach': (
                    'Scapular dyskinesis was contributing to pain during the serving motion. Kinesio '
                    'tape supported better shoulder positioning during early rehab while she completed '
                    'a rotator cuff and scapular stability program three times per week.'
                ),
                'outcome': (
                    'She served a full match with tape support by week three without post match pain. '
                    'By mid season she competed pain free without tape and maintained her starting '
                    'position. She still tapes for tournament weekends as a preventive measure.'
                ),
                'timeline': '5 weeks',
            },
        ],
        faqs=[
            ('How long does tape stay on?', 'Usually 3 to 5 days if skin tolerates it.'),
            ('Can I shower with it?', 'Yes. Pat dry afterward.'),
            ('Does tape replace bracing?', 'It is lighter than rigid braces. We choose based on injury needs.'),
        ],
    ),
    'mckenzie-method': _page(
        slug='mckenzie-method',
        title='McKenzie Method',
        summary='Mechanical assessment and repeated movements to centralize and reduce spine pain.',
        intro=(
            'The McKenzie method uses repeated movements and positions to find what reduces your '
            'spine or joint pain. You learn a specific exercise to self treat flare ups.'
        ),
        typical_sessions='4 to 8 visits',
        first_improvement='1 to 3 sessions',
        recovery_timeline='3 to 8 weeks',
        meta_focus='McKenzie mechanical diagnosis and therapy for spine and joint pain.',
        benefits=[
            'Clear directional preference',
            'Self treatment tool for flare ups',
            'Less reliance on passive care',
            'Fast assessment to exercise path',
        ],
        assessment_steps=[
            ('Repeated movement testing', 'We test which directions worsen or ease symptoms.'),
            ('Centralization check', 'We watch if leg or arm pain retreats toward the spine.'),
            ('Posture review', 'Sitting and standing habits that affect symptoms.'),
            ('Home program', 'One or two key exercises prescribed with precision.'),
        ],
        treatment_methods=[
            ('Directional exercise', 'Repeated bends, extensions, or side glides as indicated.'),
            ('Posture correction', 'Micro breaks and supported positions for desk work.'),
            ('Progression', 'Load added when symptoms centralize and stabilize.'),
            ('Prevention', 'You learn early warning signs and what to do.'),
        ],
        recovery_phases=[
            ('Centralization', 'Week 1', 'Peripheral pain may retreat with correct repeated movement.'),
            ('Stabilization', 'Week 2 to 4', 'Symptoms settle with daily exercise habit.'),
            ('Maintenance', 'Week 4+', 'Brief daily routine prevents recurrence.'),
        ],
        case_studies=[
            {
                'patient_label': 'Accountant, 44',
                'issue': 'Sciatica with leg pain when sitting',
                'approach': (
                    'Repeated extension movements centralised leg pain toward the lower back within two '
                    'sessions. He performed a specific extension based exercise routine every two hours '
                    'during workdays plus standing breaks to reduce prolonged flexed sitting.'
                ),
                'outcome': (
                    'Leg pain cleared completely by week three. Sitting tolerance returned to full '
                    'accounting workdays without needing to lie down after work. He still does his '
                    'two minute extension routine whenever he feels early back tightness.'
                ),
                'timeline': '5 weeks',
            },
        ],
        faqs=[
            ('Is McKenzie only for backs?', 'It is used for neck, back, and some extremity issues.'),
            ('What if movements hurt?', 'We find the direction that helps. Wrong direction is stopped immediately.'),
            ('Will I need to exercise forever?', 'A short daily routine often prevents future episodes.'),
        ],
    ),
    'ergonomic-training': _page(
        slug='ergonomic-training',
        title='Ergonomic Training',
        summary='Workstation and movement coaching to reduce strain from desk and physical jobs.',
        intro=(
            'Ergonomic training reviews how you work, whether at a desk or on a job site, and '
            'adjusts setup, pacing, and movement habits to reduce pain and fatigue.'
        ),
        typical_sessions='2 to 5 visits',
        first_improvement='1 session',
        recovery_timeline='2 to 6 weeks',
        meta_focus='Practical ergonomic assessment for Calgary office and trade workers.',
        benefits=[
            'Less neck and back strain',
            'Better desk or tool setup',
            'Smarter break habits',
            'Fewer work related flare ups',
        ],
        assessment_steps=[
            ('Work task review', 'We map your typical postures, tools, and hours.'),
            ('On site or photo review', 'Desk height, monitor, chair, or lifting tasks documented.'),
            ('Symptom pattern', 'We link pain to specific tasks or times of day.'),
            ('Action list', 'Prioritized changes you can make this week.'),
        ],
        treatment_methods=[
            ('Setup adjustments', 'Chair, screen, keyboard, and foot support recommendations.'),
            ('Microbreak plan', 'Short movement snacks through the shift.'),
            ('Strengthening', 'Postural endurance exercises for long tasks.'),
            ('Employer letter', 'Summary of recommendations when helpful for workplace changes.'),
        ],
        recovery_phases=[
            ('Quick wins', 'Week 1', 'Immediate setup tweaks reduce daily strain.'),
            ('Habit', 'Week 2 to 4', 'Breaks and exercises become routine.'),
            ('Sustain', 'Ongoing', 'Occasional check ins after job changes.'),
        ],
        case_studies=[
            {
                'patient_label': 'Software developer, 33',
                'issue': 'Wrist and neck pain with dual monitors',
                'approach': (
                    'Photo review showed monitors too low and wrists extended during typing. We raised '
                    'screens to eye level, brought the keyboard closer, and set hourly reminders for '
                    'ninety second mobility breaks targeting neck, wrists, and upper back.'
                ),
                'outcome': (
                    'Wrist and neck pain that built up by midday dropped noticeably within two weeks. '
                    'He has not lost a single coding day to pain since making the changes. His employer '
                    'approved a sit stand desk after our written recommendations.'
                ),
                'timeline': '3 weeks',
            },
        ],
        faqs=[
            ('Do you visit my workplace?', 'We can review photos or video. On site visits arranged when needed.'),
            ('Do I need new furniture?', 'Often small changes work. We recommend purchases only when justified.'),
            ('Will my employer pay?', 'Some WCB or workplace programs cover ergonomic assessments.'),
        ],
    ),
    'vestibular-therapy': _page(
        slug='vestibular-therapy',
        title='Vestibular Therapy',
        summary='Specialized rehab for dizziness, vertigo, and balance caused by inner ear issues.',
        intro=(
            'Vestibular therapy retrains your balance system when dizziness or vertigo affects '
            'daily life. We use targeted exercises and repositioning techniques based on assessment.'
        ),
        typical_sessions='6 to 12 visits',
        first_improvement='2 to 4 sessions',
        recovery_timeline='4 to 12 weeks',
        meta_focus='Vestibular rehabilitation for dizziness and vertigo in Calgary.',
        benefits=[
            'Less spinning and dizziness',
            'Steadier walking',
            'Confidence in crowds and cars',
            'Clear home exercise plan',
        ],
        assessment_steps=[
            ('Symptom history', 'We note triggers: head turns, rolling in bed, busy visuals.'),
            ('Oculomotor tests', 'Eye movement screens for vestibular dysfunction.'),
            ('Positional testing', 'Head positions to identify benign paroxysmal positional vertigo when present.'),
            ('Balance measures', 'Baseline scores guide progress tracking.'),
        ],
        treatment_methods=[
            ('Canalith repositioning', 'Epley or similar maneuvers for positional vertigo when indicated.'),
            ('Gaze stabilization', 'Exercises to keep vision clear during head movement.'),
            ('Habituation', 'Gradual exposure to motion that provokes symptoms.'),
            ('Balance retraining', 'Walking drills with head turns and dual tasks.'),
        ],
        recovery_phases=[
            ('Acute relief', 'Week 1 to 2', 'Positional vertigo often improves quickly after correct maneuver.'),
            ('Adaptation', 'Week 3 to 6', 'Daily exercises reduce dizziness with movement.'),
            ('Return', 'Week 6+', 'Driving, work, and sport resumed with confidence.'),
        ],
        case_studies=[
            {
                'patient_label': 'Retiree, 68',
                'issue': 'Room spinning when rolling in bed',
                'approach': (
                    'Positional testing confirmed benign paroxysmal positional vertigo in the right ear. '
                    'We performed the Epley maneuver in clinic and taught gaze stabilization exercises '
                    'to retrain eye head coordination during daily head movements.'
                ),
                'outcome': (
                    'Room spinning when rolling in bed stopped after the second visit. She maintained '
                    'gains with ten minutes of daily homework and had no recurrence at three month '
                    'follow up. She feels confident driving and grocery shopping again.'
                ),
                'timeline': '4 weeks',
            },
        ],
        faqs=[
            ('Will treatment make me more dizzy?', 'Some exercises briefly provoke symptoms. That is part of retraining.'),
            ('Do I need a doctor referral?', 'Helpful for complex cases. Many patients self refer.'),
            ('Can vestibular therapy help migraines?', 'Sometimes, when dizziness overlaps with migraine related vertigo.'),
        ],
    ),
    'postural-restoration': _page(
        slug='postural-restoration',
        title='Postural Restoration',
        summary='Breathing and alignment techniques to balance asymmetry and reduce strain.',
        intro=(
            'Postural restoration looks at how breathing, rib position, and hip alignment affect '
            'movement. Gentle drills retrain patterns that contribute to pain and stiffness.'
        ),
        typical_sessions='8 to 12 visits',
        first_improvement='3 to 5 sessions',
        recovery_timeline='8 to 12 weeks',
        meta_focus='Postural restoration techniques for chronic pain and movement imbalance.',
        benefits=[
            'Better breathing mechanics',
            'Reduced side to side asymmetry',
            'Less neck and back strain',
            'Improved athletic movement',
        ],
        assessment_steps=[
            ('Postural photos', 'Front and side views show rib and hip position.'),
            ('Breathing screen', 'We check diaphragm use and rib expansion.'),
            ('Movement asymmetry', 'Single leg and rotational tests reveal imbalances.'),
            ('Program selection', 'Exercises chosen for your pattern, left or right dominant.'),
        ],
        treatment_methods=[
            ('Positional breathing', 'Exercises that expand restricted rib zones.'),
            ('Ground based drills', 'Low load positions to reset pelvis and spine.'),
            ('Integration', 'Standing and walking drills that carry gains into life.'),
            ('Home consistency', 'Short daily breathing and mobility routine.'),
        ],
        recovery_phases=[
            ('Reset', 'Week 1 to 3', 'Learn positions that reduce tension.'),
            ('Reinforce', 'Week 4 to 8', 'Build endurance in new patterns.'),
            ('Apply', 'Week 8+', 'Sport and work tasks with improved alignment.'),
        ],
        case_studies=[
            {
                'patient_label': 'Runner, 37',
                'issue': 'Right hip pain and uneven stride',
                'approach': (
                    'Assessment showed left hip weakness and a shorter stride on the right. Postural '
                    'restoration drills focused on left hip grounding, diaphragmatic breathing, and '
                    'progressive single leg loading before reintroducing running volume.'
                ),
                'outcome': (
                    'Video gait analysis at week eight showed a more even stride length side to side. '
                    'Right hip pain resolved as he built weekly mileage slowly over eleven weeks. '
                    'He continues a short breathing and hip drill routine before every run.'
                ),
                'timeline': '11 weeks',
            },
        ],
        faqs=[
            ('Is this just posture coaching?', 'It goes deeper into breathing and neuromuscular patterns, not just sit up straight.'),
            ('Do I need special equipment?', 'Mostly floor space and a wall. Bands used in later phases.'),
            ('How often should I practice?', 'Daily short sessions work best for nervous system retraining.'),
        ],
    ),
    'electrical-stimulation': _page(
        slug='electrical-stimulation',
        title='Electrical Stimulation',
        summary='Controlled electrical currents to reduce pain, activate muscles, and support rehab.',
        intro=(
            'Electrical stimulation uses pads on the skin to deliver gentle current. It can calm '
            'pain, help weak muscles fire, and support recovery when combined with exercise.'
        ),
        typical_sessions='6 to 10 visits',
        first_improvement='2 to 4 sessions',
        recovery_timeline='4 to 10 weeks',
        meta_focus='Therapeutic electrical stimulation as part of physiotherapy rehab.',
        benefits=[
            'Pain relief during rehab',
            'Muscle activation when weak',
            'Swelling reduction in some cases',
            'Bridge to full exercise loading',
        ],
        assessment_steps=[
            ('Indication check', 'We confirm stimulation suits your injury and skin condition.'),
            ('Pad placement', 'Electrodes positioned for target muscles or pain areas.'),
            ('Sensitivity test', 'Intensity raised slowly to a strong but comfortable level.'),
            ('Exercise pairing', 'We combine with active movement when appropriate.'),
        ],
        treatment_methods=[
            ('TENS', 'Sensory level current for pain modulation.'),
            ('NMES', 'Stronger contraction to wake up inhibited muscles.'),
            ('Pre exercise priming', 'Stimulation before strength work on weak areas.'),
            ('Home guidance', 'When retail units help between visits.'),
        ],
        recovery_phases=[
            ('Pain control', 'Week 1 to 2', 'Easier participation in basic rehab.'),
            ('Activation', 'Week 3 to 5', 'Muscles fire better during exercise.'),
            ('Strength', 'Week 5+', 'Less stimulation needed as load tolerance grows.'),
        ],
        case_studies=[
            {
                'patient_label': 'Post knee surgery, 58',
                'issue': 'Quadriceps weakness after replacement',
                'approach': (
                    'Quadriceps activation was poor and he could not perform a straight leg raise after '
                    'surgery. NMES was used before each session to wake up the quads, followed by '
                    'sit to stand progressions and step ups as strength returned.'
                ),
                'outcome': (
                    'Quad strength testing met surgeon milestones on schedule at nine weeks. He walked '
                    'without a cane by week six and returned to light hiking by month three. '
                    'He finished formal physio with a home strength plan he still follows.'
                ),
                'timeline': '9 weeks',
            },
        ],
        faqs=[
            ('Will it shock me?', 'You feel tingling or muscle twitch, not a jolt. Intensity is always in your control.'),
            ('Who should avoid it?', 'Pregnancy over the area, pacemakers in the field, or broken skin.'),
            ('Is a home unit worth buying?', 'Sometimes for knee or shoulder protocols. We advise based on your plan.'),
        ],
    ),
    'concussion-management': _page(
        slug='concussion-management',
        title='Concussion Management',
        summary='Graduated return to school, work, and sport after concussion with symptom guided rehab.',
        intro=(
            'Concussion management helps you recover safely after a head injury from sport, recreation, '
            'or a motor vehicle accident. We track symptoms, guide activity progression, and address '
            'neck and balance issues that often prolong recovery.'
        ),
        typical_sessions='6 to 12 visits',
        first_improvement='2 to 4 sessions',
        recovery_timeline='2 to 8 weeks',
        meta_focus='Evidence based concussion rehab and return to activity planning in Calgary.',
        benefits=[
            'Step by step return to school, work, and sport',
            'Symptom tracking each visit',
            'Neck and vestibular care when needed',
            'Clear guidance on rest and activity',
        ],
        assessment_steps=[
            ('Symptom review', 'We document headache, dizziness, brain fog, light sensitivity, and sleep changes.'),
            ('Cognitive and physical load', 'We discuss screen time, work demands, and exercise tolerance.'),
            ('Neck and balance screen', 'Cervical and vestibular tests identify contributors to lingering symptoms.'),
            ('Return plan', 'We set realistic milestones for school, work, and sport based on your symptoms.'),
        ],
        treatment_methods=[
            ('Graduated activity', 'Structured progression back to thinking and physical tasks without symptom flare ups.'),
            ('Cervical treatment', 'Manual therapy and exercises when neck pain drives headache or dizziness.'),
            ('Vestibular rehab', 'Gaze stabilization and balance drills when dizziness persists after concussion.'),
            ('Education and pacing', 'Clear advice on sleep, hydration, and when to rest versus gently load.'),
        ],
        recovery_phases=[
            ('Relative rest', 'Days 1 to 7', 'Reduce triggers while maintaining light daily routine as tolerated.'),
            ('Gradual return', 'Week 2 to 4', 'Stepwise increase in cognitive and physical activity with symptom checks.'),
            ('Full activity', 'Week 4+', 'Return to sport or full work duties with confidence and a maintenance plan.'),
        ],
        case_studies=[
            {
                'patient_label': 'Hockey player, 17',
                'issue': 'Persistent headache and dizziness two weeks after concussion',
                'approach': (
                    'Assessment showed cervical joint stiffness and exercise intolerance. We combined neck '
                    'mobilisation, graded aerobic walking, and a return to play protocol aligned with '
                    'his school and team schedule.'
                ),
                'outcome': (
                    'Headache and dizziness resolved by week three. He completed return to play steps '
                    'without symptom relapse and returned to full contact practice at week five. '
                    'His school workload was back to normal with no missed exams.'
                ),
                'timeline': '5 weeks',
            },
        ],
        faqs=[
            ('How long does concussion recovery take?', 'Many people recover within two to four weeks. Early guidance reduces the risk of prolonged symptoms.'),
            ('Should I rest completely?', 'Brief rest helps early on, but prolonged inactivity can delay recovery. We guide safe activity progression.'),
            ('Do I need imaging before starting rehab?', 'Most concussions are diagnosed clinically. We coordinate with your physician if red flags appear.'),
        ],
    ),
    'psychology-counselling': _page(
        slug='psychology-counselling',
        title='Psychology Counselling',
        summary='Confidential counselling for stress, anxiety, injury recovery, and everyday mental wellness in Calgary.',
        intro=(
            'Psychology counselling gives you a private space to talk through stress, anxiety, mood changes, '
            'and the emotional side of pain or injury. We listen first, then help you build practical coping '
            'skills that fit work, family, and recovery at our northwest Calgary clinic.'
        ),
        typical_sessions='6 to 10 visits',
        first_improvement='2 to 4 sessions',
        recovery_timeline='6 to 12 weeks',
        meta_focus='Supportive counselling for stress, anxiety, and recovery related mental health.',
        benefits=[
            'A confidential place to talk and be heard',
            'Skills for stress, sleep, and anxiety',
            'Support during injury or chronic pain recovery',
            'Care coordinated with your physio or massage team when helpful',
        ],
        assessment_steps=[
            ('Welcome and goals', 'We learn what brought you in, what feels hardest right now, and what you want to change.'),
            ('History and context', 'We discuss mood, sleep, work, relationships, and any injury or health concerns.'),
            ('Safety and fit', 'We confirm counselling is the right next step and outline other supports if needed.'),
            ('A clear plan', 'You leave with session frequency, focus areas, and simple skills to try between visits.'),
        ],
        treatment_methods=[
            ('Talk therapy', 'Structured conversations that help you notice patterns and choose a different response.'),
            ('Coping skills', 'Breathing, grounding, and thought tools you can use during busy or painful days.'),
            ('Pain and recovery support', 'Help adjusting to injury, setbacks, or fear of movement alongside physical care.'),
            ('Practical planning', 'Small weekly goals for sleep, work, and relationships so progress feels manageable.'),
        ],
        recovery_phases=[
            ('Settle in', 'Sessions 1 to 2', 'Build trust, name the main concerns, and start one or two coping tools.'),
            ('Build skills', 'Sessions 3 to 6', 'Practice new responses to stress, worry, or low mood in daily life.'),
            ('Maintain gains', 'Session 6+', 'Space visits further apart and keep a plan for flare ups or busy seasons.'),
        ],
        case_studies=[
            {
                'patient_label': 'Warehouse worker, 38',
                'issue': 'Anxiety and poor sleep after a workplace back injury',
                'approach': (
                    'We focused on sleep routines, worry about returning to work, and simple grounding tools '
                    'he could use before shifts. Counselling was coordinated with his physiotherapy plan so '
                    'movement goals and mental load stayed aligned.'
                ),
                'outcome': (
                    'Sleep improved within three weeks and he returned to modified duties with less panic. '
                    'He kept a short evening wind-down routine and used two coping skills during flare ups. '
                    'He completed his WCB plan without dropping counselling early.'
                ),
                'timeline': '8 weeks',
            },
        ],
        faqs=[
            ('Is counselling confidential?', 'Yes. What you share stays private, except where we are legally required to act if someone is at immediate risk.'),
            ('Do I need a referral?', 'No. You can book psychology counselling directly. Bring insurance details if you plan to claim benefits.'),
            ('Can counselling help with injury recovery?', 'Yes. Stress, fear of movement, and low mood often slow physical recovery. Addressing them can make rehab easier to stick with.'),
        ],
    ),
}


def get_treatment_page(slug):
    return TREATMENT_PAGES.get(slug)


def all_treatment_content():
    return TREATMENT_PAGES
