"""
i18n.py — All user-facing text for the client-facing loan risk experience,
in four languages.

This file intentionally contains ONLY plain-language, non-technical copy:
no model names, no statistical terms, no internal thresholds.

The goal is that a first-time visitor with zero data-science background
understands every word on screen.
"""

from __future__ import annotations


LANGUAGES = {
    "ar": {"label": "العربية", "flag": "🇪🇬", "dir": "rtl"},
    "en": {"label": "English", "flag": "🇬🇧", "dir": "ltr"},
    "de": {"label": "Deutsch", "flag": "🇩🇪", "dir": "ltr"},
    "fr": {"label": "Français", "flag": "🇫🇷", "dir": "ltr"},
}


TXT: dict[str, dict[str, str]] = {

    # ===========================================================
    # ARABIC
    # ===========================================================

    "ar": {
        "brand_title": "المستشار الائتماني الذكي",

        "brand_tagline":
            "قدّر مستوى مخاطر القرض في أقل من دقيقة — "
            "بذكاء اصطناعي مُدرَّب على بيانات ائتمانية حقيقية.",

        "theme_to_light": "الوضع الفاتح",
        "theme_to_dark": "الوضع الداكن",
        "language_label": "اللغة",

        "hero_cta": "ابدأ التقييم",

        "hero_note":
            "بياناتك تُستخدم فقط لحساب النتيجة، "
            "ولا يتم حفظها أو مشاركتها مع أي جهة.",

        "progress_step": "خطوة",
        "progress_of": "من",

        # -------------------------------------------------------
        # Steps
        # -------------------------------------------------------

        "step1_title": "بياناتك الشخصية",
        "step1_hint": "معلومات أساسية عنك",

        "step2_title": "العمل والدخل",
        "step2_hint": "وظيفتك الحالية ودخلك السنوي",

        "step3_title": "تفاصيل القرض",
        "step3_hint": "القرض اللي بتفكر تطلبه",

        "step4_title": "السجل الائتماني والممتلكات",
        "step4_hint": "خبرتك مع الجهات المالية وما تملكه",

        "step5_title": "مراجعة أخيرة",
        "step5_hint": "تأكد من بياناتك قبل ما نطلع لك النتيجة",

        # -------------------------------------------------------
        # Fields
        # -------------------------------------------------------

        "age_label": "العمر (بالسنين)",

        "gender_label": "النوع",
        "gender_female": "أنثى",
        "gender_male": "ذكر",

        "family_label": "الحالة الاجتماعية",
        "family_married": "متزوج/ة",
        "family_single": "أعزب/عزباء",
        "family_civil": "زواج عرفي",
        "family_widow": "أرمل/ة",
        "family_separated": "منفصل/ة",

        "children_label": "عدد الأطفال",

        "years_employed_label":
            "سنوات الخبرة في وظيفتك الحالية",

        "occupation_label": "طبيعة العمل",

        "occ_laborers": "عامل",
        "occ_core": "موظف إداري",
        "occ_sales": "مبيعات",
        "occ_managers": "مدير",
        "occ_drivers": "سائق",
        "occ_tech": "تخصص فني عالي",
        "occ_accountants": "محاسب",
        "occ_other": "أخرى",

        "income_label": "الدخل السنوي (بالجنيه)",

        "contract_label": "نوع القرض",
        "contract_cash": "قرض نقدي",
        "contract_revolving": "قرض متجدد (بطاقة ائتمان)",

        "loan_amount_label": "المبلغ المطلوب",

        "goods_price_label": "سعر السلعة (إن وُجدت)",
        "goods_price_hint":
            "لو القرض مش لشراء سلعة معينة، اترك القيمة كما هي.",

        "annuity_label": "القسط السنوي المتوقع",

        "bureau_history_label":
            "هل لديك تاريخ ائتماني مسجل لدى جهة تمويل أخرى؟",

        "previous_app_label":
            "هل سبق وتقدمت لهذه الجهة من قبل؟",

        "education_label": "المؤهل الدراسي",

        "edu_secondary": "ثانوي",
        "edu_higher": "جامعي",
        "edu_incomplete_higher": "جامعي غير مكتمل",
        "edu_lower_secondary": "أقل من ثانوي",
        "edu_academic": "دراسات عليا",

        "owns_car_label": "تمتلك سيارة",
        "owns_realty_label": "تمتلك عقار",

        "yes_label": "نعم",
        "no_label": "لا",

        # -------------------------------------------------------
        # Buttons
        # -------------------------------------------------------

        "btn_back": "السابق",
        "btn_next": "التالي",
        "btn_submit": "احسب النتيجة",
        "btn_restart": "تقييم جديد",
        "btn_edit": "تعديل البيانات",

        # -------------------------------------------------------
        # Review
        # -------------------------------------------------------

        "review_title": "راجع بياناتك",

        "review_intro":
            "لو كل حاجة صح، اضغط على \"احسب النتيجة\" "
            "وهنطلعلك التقييم فورًا.",

        "loading_text": "بنحلل بياناتك الآن…",

        # -------------------------------------------------------
        # Results
        # -------------------------------------------------------

        "result_title": "نتيجتك",

        "result_prob_caption":
            "مخاطر السداد المقدّرة",

        "tier_low_title": "مخاطر تعثر منخفضة",

        "tier_low_desc":
            "بناءً على البيانات اللي دخلتها، "
            "مؤشرات المخاطر تبدو منخفضة، مع وجود قدرة متوقعة جيدة على السداد.",

        "tier_moderate_title": "مخاطر تعثر متوسطة",

        "tier_moderate_desc":
            "البيانات تشير إلى مستوى متوسط من المخاطر. "
            "بعض العوامل المالية ممكن تتحسن لتقليل مستوى المخاطر.",

        "tier_high_title": "يحتاج إلى مراجعة",

        "tier_high_desc":
            "البيانات الحالية تشير إلى وجود بعض مؤشرات المخاطر. "
            "ده مش معناه رفض، لكن يُفضّل مراجعة وضعك المالي قبل التقديم.",

        "tier_veryhigh_title": "مخاطر تعثر مرتفعة حاليًا",

        "tier_veryhigh_desc":
            "البيانات الحالية تشير إلى مستوى مرتفع من مخاطر السداد "
            "بالنسبة للمبلغ المطلوب. ممكن تجربة مبلغ أقل أو تحسين بعض العوامل المالية.",

        "tips_title": "نصائح ممكن تقلل المخاطر",

        "tip_income":
            "دخل ثابت وموثّق يساعد على تحسين قدرتك المتوقعة على السداد.",

        "tip_amount":
            "طلب مبلغ يتناسب مع دخلك يساعد على تقليل الضغط المالي.",

        "tip_history":
            "وجود تاريخ ائتماني إيجابي سابق يمكن أن يكون عاملًا مساعدًا.",

        "tip_employment":
            "الاستقرار الوظيفي لفترة أطول يمكن أن يدعم القدرة المتوقعة على السداد.",

        "disclaimer":
            "هذا تقدير تعليمي وتوضيحي فقط بناءً على نموذج ذكاء اصطناعي تجريبي، "
            "وليس قرارًا نهائيًا أو رسميًا من أي جهة تمويل حقيقية.",

        # -------------------------------------------------------
        # Errors
        # -------------------------------------------------------

        "load_error_title": "تعذّر تشغيل الخدمة",

        "load_error_body":
            "حصلت مشكلة تقنية أثناء تجهيز النظام. برجاء المحاولة لاحقًا.",

        "predict_error":
            "حصل خطأ أثناء حساب النتيجة. "
            "برجاء مراجعة بياناتك والمحاولة مرة أخرى.",

        "footer_note":
            "تجربة تعليمية لعرض قدرات الذكاء الاصطناعي في تقييم مخاطر الائتمان.",
    },


    # ===========================================================
    # ENGLISH
    # ===========================================================

    "en": {
        "brand_title": "Smart Credit Advisor",

        "brand_tagline":
            "Estimate your loan repayment risk in under a minute — "
            "powered by AI trained on real credit data.",

        "theme_to_light": "Light mode",
        "theme_to_dark": "Dark mode",
        "language_label": "Language",

        "hero_cta": "Start My Assessment",

        "hero_note":
            "Your information is only used to calculate your result — "
            "it isn't stored or shared with anyone.",

        "progress_step": "Step",
        "progress_of": "of",

        # Steps
        "step1_title": "About You",
        "step1_hint": "A few basic details",

        "step2_title": "Work & Income",
        "step2_hint": "Your current job and yearly earnings",

        "step3_title": "Loan Details",
        "step3_hint": "The loan you're considering",

        "step4_title": "Credit History & Assets",
        "step4_hint": "Your financial track record and what you own",

        "step5_title": "Final Review",
        "step5_hint":
            "Double-check everything before we calculate your result",

        # Fields
        "age_label": "Age (years)",

        "gender_label": "Gender",
        "gender_female": "Female",
        "gender_male": "Male",

        "family_label": "Marital status",
        "family_married": "Married",
        "family_single": "Single",
        "family_civil": "Civil marriage",
        "family_widow": "Widowed",
        "family_separated": "Separated",

        "children_label": "Number of children",

        "years_employed_label": "Years at your current job",

        "occupation_label": "Occupation",
        "occ_laborers": "Laborer",
        "occ_core": "Office staff",
        "occ_sales": "Sales staff",
        "occ_managers": "Manager",
        "occ_drivers": "Driver",
        "occ_tech": "High-skill technical staff",
        "occ_accountants": "Accountant",
        "occ_other": "Other",

        "income_label": "Annual income",

        "contract_label": "Loan type",
        "contract_cash": "Cash loan",
        "contract_revolving": "Revolving loan (credit card)",

        "loan_amount_label": "Requested amount",

        "goods_price_label": "Price of goods (if any)",
        "goods_price_hint":
            "If the loan isn't for a specific item, leave the value as it is.",

        "annuity_label": "Expected yearly installment",

        "bureau_history_label":
            "Do you have credit history with another lender?",

        "previous_app_label":
            "Have you applied with this lender before?",

        "education_label": "Education level",

        "edu_secondary": "Secondary",
        "edu_higher": "Higher education",
        "edu_incomplete_higher": "Incomplete higher education",
        "edu_lower_secondary": "Below secondary",
        "edu_academic": "Academic degree",

        "owns_car_label": "Owns a car",
        "owns_realty_label": "Owns real estate",

        "yes_label": "Yes",
        "no_label": "No",

        # Buttons
        "btn_back": "Back",
        "btn_next": "Next",
        "btn_submit": "Calculate My Result",
        "btn_restart": "Start a new assessment",
        "btn_edit": "Edit my details",

        # Review
        "review_title": "Review your details",

        "review_intro":
            "If everything looks right, tap \"Calculate My Result\" "
            "to get your assessment instantly.",

        "loading_text": "Analyzing your profile…",

        # Results
        "result_title": "Your Result",

        "result_prob_caption":
            "Estimated repayment risk",

        "tier_low_title": "Low estimated default risk",

        "tier_low_desc":
            "Based on what you shared, the indicators suggest relatively low "
            "repayment risk and a strong expected ability to repay.",

        "tier_moderate_title": "Moderate estimated default risk",

        "tier_moderate_desc":
            "The current information indicates a moderate level of risk. "
            "Some financial factors could be improved to reduce that risk.",

        "tier_high_title": "Needs a closer look",

        "tier_high_desc":
            "The current information shows some risk indicators. "
            "This isn't a rejection — it may be worth reviewing your finances before applying.",

        "tier_veryhigh_title": "Higher estimated default risk",

        "tier_veryhigh_desc":
            "The current information suggests a higher level of repayment risk "
            "for the requested amount. You may consider a smaller amount or improving other factors.",

        "tips_title": "Ways to reduce risk",

        "tip_income":
            "A steady, documented income can support stronger repayment ability.",

        "tip_amount":
            "Requesting an amount that fits your income can reduce financial pressure.",

        "tip_history":
            "A positive prior credit history can be a helpful factor.",

        "tip_employment":
            "Longer job stability can support stronger expected repayment ability.",

        "disclaimer":
            "This is an educational, illustrative estimate from an experimental AI model — "
            "not a final or official decision from any real lender.",

        # Errors
        "load_error_title": "Service unavailable",

        "load_error_body":
            "A technical issue occurred while preparing the system. "
            "Please try again later.",

        "predict_error":
            "Something went wrong while calculating your result. "
            "Please check your details and try again.",

        "footer_note":
            "An educational demo showcasing AI in credit risk assessment.",
    },


    # ===========================================================
    # GERMAN
    # ===========================================================

    "de": {
        "brand_title": "Intelligenter Kreditberater",

        "brand_tagline":
            "Schätzen Sie Ihr Rückzahlungsrisiko in weniger als einer Minute — "
            "mit KI, trainiert auf echten Kreditdaten.",

        "theme_to_light": "Heller Modus",
        "theme_to_dark": "Dunkler Modus",
        "language_label": "Sprache",

        "hero_cta": "Bewertung starten",

        "hero_note":
            "Ihre Angaben werden nur zur Berechnung des Ergebnisses verwendet — "
            "sie werden nicht gespeichert oder weitergegeben.",

        "progress_step": "Schritt",
        "progress_of": "von",

        "step1_title": "Über Sie",
        "step1_hint": "Ein paar grundlegende Angaben",

        "step2_title": "Beruf & Einkommen",
        "step2_hint":
            "Ihre aktuelle Tätigkeit und Ihr Jahreseinkommen",

        "step3_title": "Kreditdetails",
        "step3_hint":
            "Der Kredit, den Sie in Betracht ziehen",

        "step4_title": "Kredithistorie & Vermögen",
        "step4_hint":
            "Ihre finanzielle Vorgeschichte und Ihr Besitz",

        "step5_title": "Letzte Überprüfung",
        "step5_hint":
            "Prüfen Sie alles, bevor wir Ihr Ergebnis berechnen",

        "age_label": "Alter (Jahre)",

        "gender_label": "Geschlecht",
        "gender_female": "Weiblich",
        "gender_male": "Männlich",

        "family_label": "Familienstand",
        "family_married": "Verheiratet",
        "family_single": "Ledig",
        "family_civil": "Eheähnliche Gemeinschaft",
        "family_widow": "Verwitwet",
        "family_separated": "Getrennt lebend",

        "children_label": "Anzahl der Kinder",

        "years_employed_label":
            "Jahre in der aktuellen Anstellung",

        "occupation_label": "Beruf",
        "occ_laborers": "Arbeiter/in",
        "occ_core": "Bürokraft",
        "occ_sales": "Vertriebsmitarbeiter/in",
        "occ_managers": "Führungskraft",
        "occ_drivers": "Fahrer/in",
        "occ_tech": "Hochqualifizierte Fachkraft",
        "occ_accountants": "Buchhalter/in",
        "occ_other": "Sonstiges",

        "income_label": "Jahreseinkommen",

        "contract_label": "Kreditart",
        "contract_cash": "Barkredit",
        "contract_revolving":
            "Revolvierender Kredit (Kreditkarte)",

        "loan_amount_label": "Gewünschter Betrag",

        "goods_price_label":
            "Warenpreis (falls zutreffend)",

        "goods_price_hint":
            "Wenn keine bestimmte Ware finanziert wird, "
            "lassen Sie den Wert unverändert.",

        "annuity_label": "Erwartete jährliche Rate",

        "bureau_history_label":
            "Haben Sie eine Kredithistorie bei einem anderen Anbieter?",

        "previous_app_label":
            "Haben Sie bereits zuvor bei diesem Anbieter beantragt?",

        "education_label": "Bildungsniveau",

        "edu_secondary": "Sekundarschule",
        "edu_higher": "Hochschulbildung",
        "edu_incomplete_higher":
            "Unvollständige Hochschulbildung",
        "edu_lower_secondary": "Unter Sekundarschule",
        "edu_academic": "Akademischer Grad",

        "owns_car_label": "Besitzt ein Auto",
        "owns_realty_label": "Besitzt Immobilien",

        "yes_label": "Ja",
        "no_label": "Nein",

        "btn_back": "Zurück",
        "btn_next": "Weiter",
        "btn_submit": "Ergebnis berechnen",
        "btn_restart": "Neue Bewertung starten",
        "btn_edit": "Angaben bearbeiten",

        "review_title": "Überprüfen Sie Ihre Angaben",

        "review_intro":
            "Wenn alles stimmt, tippen Sie auf \"Ergebnis berechnen\", "
            "um sofort Ihre Bewertung zu erhalten.",

        "loading_text": "Ihr Profil wird analysiert…",

        "result_title": "Ihr Ergebnis",

        "result_prob_caption":
            "Geschätztes Rückzahlungsrisiko",

        "tier_low_title":
            "Niedriges Rückzahlungsrisiko",

        "tier_low_desc":
            "Basierend auf Ihren Angaben deuten die Indikatoren auf ein relativ "
            "niedriges Rückzahlungsrisiko und eine gute erwartete Rückzahlungsfähigkeit hin.",

        "tier_moderate_title":
            "Mittleres Rückzahlungsrisiko",

        "tier_moderate_desc":
            "Die aktuellen Angaben weisen auf ein mittleres Risiko hin. "
            "Einige finanzielle Faktoren könnten verbessert werden.",

        "tier_high_title":
            "Genauere Prüfung nötig",

        "tier_high_desc":
            "Die aktuellen Angaben zeigen einige Risikofaktoren. "
            "Dies ist keine Ablehnung — eine Überprüfung Ihrer Finanzen kann sinnvoll sein.",

        "tier_veryhigh_title":
            "Höheres Rückzahlungsrisiko",

        "tier_veryhigh_desc":
            "Die aktuellen Angaben deuten bei dem gewünschten Betrag auf ein höheres "
            "Rückzahlungsrisiko hin. Ein geringerer Betrag oder andere Verbesserungen könnten helfen.",

        "tips_title":
            "So können Sie das Risiko reduzieren",

        "tip_income":
            "Ein stabiles, nachgewiesenes Einkommen kann die Rückzahlungsfähigkeit unterstützen.",

        "tip_amount":
            "Ein Betrag, der zu Ihrem Einkommen passt, kann den finanziellen Druck reduzieren.",

        "tip_history":
            "Eine positive frühere Kredithistorie kann hilfreich sein.",

        "tip_employment":
            "Längere Beschäftigungsstabilität kann die erwartete Rückzahlungsfähigkeit unterstützen.",

        "disclaimer":
            "Dies ist eine anschauliche, lehrreiche Schätzung eines experimentellen KI-Modells — "
            "keine endgültige oder offizielle Entscheidung eines echten Kreditgebers.",

        "load_error_title": "Dienst nicht verfügbar",

        "load_error_body":
            "Bei der Vorbereitung des Systems ist ein technisches Problem aufgetreten. "
            "Bitte versuchen Sie es später erneut.",

        "predict_error":
            "Bei der Berechnung Ihres Ergebnisses ist ein Fehler aufgetreten. "
            "Bitte überprüfen Sie Ihre Angaben und versuchen Sie es erneut.",

        "footer_note":
            "Eine Lern-Demo zur Veranschaulichung von KI in der Kreditrisikobewertung.",
    },


    # ===========================================================
    # FRENCH
    # ===========================================================

    "fr": {
        "brand_title": "Conseiller de Crédit Intelligent",

        "brand_tagline":
            "Estimez votre risque de remboursement en moins d'une minute — "
            "grâce à une IA entraînée sur des données de crédit réelles.",

        "theme_to_light": "Mode clair",
        "theme_to_dark": "Mode sombre",
        "language_label": "Langue",

        "hero_cta": "Commencer l'évaluation",

        "hero_note":
            "Vos informations ne servent qu'à calculer votre résultat — "
            "elles ne sont ni conservées ni partagées.",

        "progress_step": "Étape",
        "progress_of": "sur",

        "step1_title": "À propos de vous",
        "step1_hint": "Quelques informations de base",

        "step2_title": "Emploi et revenus",
        "step2_hint":
            "Votre emploi actuel et vos revenus annuels",

        "step3_title": "Détails du prêt",
        "step3_hint":
            "Le prêt que vous envisagez",

        "step4_title": "Historique de crédit et biens",
        "step4_hint":
            "Votre historique financier et ce que vous possédez",

        "step5_title": "Vérification finale",
        "step5_hint":
            "Vérifiez tout avant de calculer votre résultat",

        "age_label": "Âge (ans)",

        "gender_label": "Sexe",
        "gender_female": "Femme",
        "gender_male": "Homme",

        "family_label": "Statut familial",
        "family_married": "Marié(e)",
        "family_single": "Célibataire",
        "family_civil": "Union libre",
        "family_widow": "Veuf/veuve",
        "family_separated": "Séparé(e)",

        "children_label": "Nombre d'enfants",

        "years_employed_label":
            "Années dans l'emploi actuel",

        "occupation_label": "Profession",
        "occ_laborers": "Ouvrier(ère)",
        "occ_core": "Employé(e) de bureau",
        "occ_sales": "Personnel commercial",
        "occ_managers": "Cadre / Manager",
        "occ_drivers": "Chauffeur(euse)",
        "occ_tech":
            "Personnel technique hautement qualifié",
        "occ_accountants": "Comptable",
        "occ_other": "Autre",

        "income_label": "Revenu annuel",

        "contract_label": "Type de prêt",
        "contract_cash": "Prêt personnel",
        "contract_revolving":
            "Prêt renouvelable (carte de crédit)",

        "loan_amount_label": "Montant demandé",

        "goods_price_label":
            "Prix du bien (le cas échéant)",

        "goods_price_hint":
            "Si le prêt ne finance pas un bien précis, "
            "laissez la valeur telle quelle.",

        "annuity_label":
            "Mensualité annuelle prévue",

        "bureau_history_label":
            "Avez-vous un historique de crédit chez un autre organisme ?",

        "previous_app_label":
            "Avez-vous déjà fait une demande auprès de cet organisme ?",

        "education_label": "Niveau d'études",

        "edu_secondary": "Secondaire",
        "edu_higher": "Enseignement supérieur",
        "edu_incomplete_higher":
            "Études supérieures inachevées",
        "edu_lower_secondary":
            "Inférieur au secondaire",
        "edu_academic":
            "Diplôme universitaire avancé",

        "owns_car_label": "Possède une voiture",
        "owns_realty_label":
            "Possède un bien immobilier",

        "yes_label": "Oui",
        "no_label": "Non",

        "btn_back": "Précédent",
        "btn_next": "Suivant",
        "btn_submit": "Calculer mon résultat",
        "btn_restart": "Nouvelle évaluation",
        "btn_edit": "Modifier mes informations",

        "review_title":
            "Vérifiez vos informations",

        "review_intro":
            "Si tout est correct, appuyez sur \"Calculer mon résultat\" "
            "pour obtenir votre évaluation instantanément.",

        "loading_text":
            "Analyse de votre profil…",

        "result_title": "Votre résultat",

        "result_prob_caption":
            "Risque de remboursement estimé",

        "tier_low_title":
            "Risque de remboursement faible",

        "tier_low_desc":
            "D'après vos informations, les indicateurs suggèrent un risque de remboursement "
            "relativement faible et une bonne capacité de remboursement attendue.",

        "tier_moderate_title":
            "Risque de remboursement modéré",

        "tier_moderate_desc":
            "Les informations actuelles indiquent un niveau de risque modéré. "
            "Certains facteurs financiers pourraient être améliorés.",

        "tier_high_title":
            "Nécessite un examen approfondi",

        "tier_high_desc":
            "Les informations actuelles montrent certains indicateurs de risque. "
            "Ce n'est pas un refus — il peut être utile d'examiner vos finances avant de faire une demande.",

        "tier_veryhigh_title":
            "Risque de remboursement élevé",

        "tier_veryhigh_desc":
            "Les informations actuelles suggèrent un risque de remboursement plus élevé "
            "pour le montant demandé. Un montant inférieur ou d'autres améliorations pourraient aider.",

        "tips_title":
            "Comment réduire le risque",

        "tip_income":
            "Un revenu stable et justifié peut renforcer votre capacité de remboursement.",

        "tip_amount":
            "Demander un montant adapté à votre revenu peut réduire la pression financière.",

        "tip_history":
            "Un historique de crédit positif peut être un facteur favorable.",

        "tip_employment":
            "Une stabilité professionnelle plus longue peut soutenir votre capacité de remboursement.",

        "disclaimer":
            "Il s'agit d'une estimation pédagogique et illustrative issue d'un modèle d'IA expérimental — "
            "et non d'une décision finale ou officielle d'un organisme de crédit réel.",

        "load_error_title":
            "Service indisponible",

        "load_error_body":
            "Un problème technique est survenu lors de la préparation du système. "
            "Veuillez réessayer plus tard.",

        "predict_error":
            "Une erreur est survenue lors du calcul de votre résultat. "
            "Veuillez vérifier vos informations et réessayer.",

        "footer_note":
            "Une démonstration pédagogique de l'IA appliquée à l'évaluation du risque de crédit.",
    },
}


def t(lang: str, key: str) -> str:
    """Fetch a translated string, falling back to English then the raw key."""
    return TXT.get(lang, TXT["en"]).get(
        key,
        TXT["en"].get(key, key),
    )