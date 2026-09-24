"""
Smart Credit Advisor — client-facing Streamlit application.

This is the consumer-facing entry point: a friendly, step-by-step wizard that lets
someone with zero data-science background check their estimated loan repayment risk.

No model names, thresholds, or statistical jargon are ever shown here — that
information belongs to internal tooling, not to the end user.

All model loading and inference logic lives in prediction_engine.py and is never
duplicated here - this file calls it and renders the result. No model is trained,
tuned, recalibrated, or otherwise modified here.
"""

import math
import os
import sys
import textwrap
import traceback

import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from prediction_engine import (
    ArtifactLoadError,
    build_full_feature_row,
    load_artifacts,
    predict_classical,
    risk_tier,
)

from i18n import LANGUAGES, t


def html_block(raw: str) -> str:
    """Prepare a triple-quoted HTML fragment for st.markdown(unsafe_allow_html=True).

    Every such fragment in this file is written as an indented, multi-line
    f-string for readability in the source. Left as-is, that causes two
    separate problems once it reaches Streamlit's Markdown parser:
      1. Deep Python-source indentation (4+ spaces) on a line is read as an
         indented Markdown *code block*, so the raw HTML/SVG text gets
         printed on screen instead of being rendered.
      2. A blank line between nested tags (e.g. between <div> and its first
         child) ends the current HTML block, so everything after it is
         re-parsed as new Markdown - which then hits problem 1 again.
    Collapsing the whole fragment onto a single line (no newlines, no extra
    indentation) sidesteps both issues at once, since Markdown's block rules
    are line-based.
    """
    return " ".join(line.strip() for line in raw.splitlines() if line.strip())


# ---------------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ---------------------------------------------------------------------------
# Canonical option values
# ---------------------------------------------------------------------------

GENDER_OPTIONS = [
    "F",
    "M",
]

GENDER_LABEL_KEYS = {
    "F": "gender_female",
    "M": "gender_male",
}


FAMILY_OPTIONS = [
    "Married",
    "Single / not married",
    "Civil marriage",
    "Widow",
    "Separated",
]

FAMILY_LABEL_KEYS = {
    "Married": "family_married",
    "Single / not married": "family_single",
    "Civil marriage": "family_civil",
    "Widow": "family_widow",
    "Separated": "family_separated",
}


OCCUPATION_OPTIONS = [
    "Laborers",
    "Core staff",
    "Sales staff",
    "Managers",
    "Drivers",
    "High skill tech staff",
    "Accountants",
    "Other / not listed",
]

OCCUPATION_LABEL_KEYS = {
    "Laborers": "occ_laborers",
    "Core staff": "occ_core",
    "Sales staff": "occ_sales",
    "Managers": "occ_managers",
    "Drivers": "occ_drivers",
    "High skill tech staff": "occ_tech",
    "Accountants": "occ_accountants",
    "Other / not listed": "occ_other",
}


CONTRACT_OPTIONS = [
    "Cash loans",
    "Revolving loans",
]

CONTRACT_LABEL_KEYS = {
    "Cash loans": "contract_cash",
    "Revolving loans": "contract_revolving",
}


# ---------------------------------------------------------------------------
# IMPORTANT:
# The user-facing label is "Secondary", but the trained Home Credit pipeline
# expects the exact canonical category "Secondary / secondary special".
# ---------------------------------------------------------------------------

EDUCATION_OPTIONS = [
    "Secondary / secondary special",
    "Higher education",
    "Incomplete higher",
    "Lower secondary",
    "Academic degree",
]

EDUCATION_LABEL_KEYS = {
    "Secondary / secondary special": "edu_secondary",
    "Higher education": "edu_higher",
    "Incomplete higher": "edu_incomplete_higher",
    "Lower secondary": "edu_lower_secondary",
    "Academic degree": "edu_academic",
}


# ---------------------------------------------------------------------------
# Risk tier translation mapping
# ---------------------------------------------------------------------------

TIER_KEYS = {
    "success": (
        "tier_low_title",
        "tier_low_desc",
    ),
    "caution": (
        "tier_moderate_title",
        "tier_moderate_desc",
    ),
    "warning": (
        "tier_high_title",
        "tier_high_desc",
    ),
    "danger": (
        "tier_veryhigh_title",
        "tier_veryhigh_desc",
    ),
}


TOTAL_STEPS = 5


# ---------------------------------------------------------------------------
# Session defaults
# ---------------------------------------------------------------------------

if "lang" not in st.session_state:
    st.session_state.lang = "ar"

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "step" not in st.session_state:
    st.session_state.step = 0

if "result" not in st.session_state:
    st.session_state.result = None

if "form" not in st.session_state:
    st.session_state.form = dict(
        age_years=35,
        gender="F",
        family_status="Married",
        num_children=0,
        years_employed=5.0,
        occupation="Core staff",
        annual_income=180_000,
        contract_type="Cash loans",
        loan_amount=500_000,
        goods_price=480_000,
        annuity_amount=25_000,
        has_bureau_history=True,
        has_previous_application=True,
        education="Secondary / secondary special",
        owns_car=False,
        owns_realty=True,
    )


lang = st.session_state.lang


def tr(key: str) -> str:
    return t(lang, key)


# ---------------------------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title=tr("brand_title"),
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------------------------
# Theme tokens
# ---------------------------------------------------------------------------

THEMES = {
    "dark": {
        "bg": "#0E1420",
        "bg_alt": "#151C2C",
        "surface": "#1A2233",
        "surface_2": "#212B40",
        "border": "#2B3650",
        "text": "#E7EAF0",
        "text_muted": "#8D97AC",
        "accent": "#22B8C8",
        "accent_soft": "rgba(34,184,200,0.14)",
        "success": "#3FB27F",
        "success_soft": "rgba(63,178,127,0.14)",
        "caution": "#D6A84A",
        "caution_soft": "rgba(214,168,74,0.14)",
        "warning": "#D97B3F",
        "warning_soft": "rgba(217,123,63,0.14)",
        "danger": "#C64B4B",
        "danger_soft": "rgba(198,75,75,0.14)",
        "shadow": "0 20px 60px -20px rgba(0,0,0,0.55)",
    },
    "light": {
        "bg": "#F5F7FA",
        "bg_alt": "#EDF0F5",
        "surface": "#FFFFFF",
        "surface_2": "#F0F3F8",
        "border": "#DCE2EC",
        "text": "#1B2430",
        "text_muted": "#5C6579",
        "accent": "#0E8C9B",
        "accent_soft": "rgba(14,140,155,0.10)",
        "success": "#227A55",
        "success_soft": "rgba(34,122,85,0.10)",
        "caution": "#9C7A1E",
        "caution_soft": "rgba(156,122,30,0.10)",
        "warning": "#B15A1F",
        "warning_soft": "rgba(177,90,31,0.10)",
        "danger": "#A6342F",
        "danger_soft": "rgba(166,52,47,0.10)",
        "shadow": "0 20px 50px -24px rgba(30,40,60,0.25)",
    },
}


t_ = THEMES[
    st.session_state.theme
]

is_rtl = LANGUAGES[lang]["dir"] == "rtl"

direction = (
    "rtl"
    if is_rtl
    else "ltr"
)

align_start = (
    "right"
    if is_rtl
    else "left"
)


# ---------------------------------------------------------------------------
# Global CSS
# ---------------------------------------------------------------------------

st.markdown(
    html_block(f"""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=Tajawal:wght@400;500;700;800&display=swap'
    );

    html, body, [class*="css"] {{
        font-family:
            {"'Tajawal', 'Inter', sans-serif"
             if is_rtl
             else "'Inter', -apple-system, sans-serif"};
    }}

    .stApp {{
        background:
            radial-gradient(
                1200px 600px at 15% -10%,
                {t_['accent_soft']},
                transparent 60%
            ),
            {t_['bg']};

        color: {t_['text']};
        direction: {direction};
    }}

    #MainMenu,
    footer,
    header {{
        visibility: hidden;
    }}

    .block-container {{
        padding-top: 1.4rem;
        padding-bottom: 4rem;
        max-width: 640px;
    }}

    h1,
    h2,
    h3,
    .headline {{
        font-family:
            {"'Tajawal', sans-serif"
             if is_rtl
             else "'Space Grotesk', sans-serif"};

        letter-spacing: -0.01em;
    }}

    p,
    span,
    div,
    label {{
        text-align: {align_start};
    }}

    /* ---- Top controls ---- */

    .top-controls {{
        display: flex;
        justify-content: flex-end;
        gap: 0.5rem;
        margin-bottom: 0.6rem;
    }}

    div[data-testid="stSelectbox"] {{
        min-width: 128px;
    }}

    /* ---- Hero ---- */

    .hero {{
        text-align: center;
        padding: 2.6rem 1.6rem 2.2rem 1.6rem;
        border-radius: 22px;
        background:
            linear-gradient(
                160deg,
                {t_['surface']},
                {t_['bg_alt']}
            );

        border: 1px solid {t_['border']};
        box-shadow: {t_['shadow']};
        margin-bottom: 1.2rem;
    }}

    .hero .icon {{
        font-size: 2.6rem;
        margin-bottom: 0.6rem;
    }}

    .hero h1 {{
        font-size: 1.7rem;
        font-weight: 700;
        margin: 0 0 0.6rem 0;
        color: {t_['text']};
    }}

    .hero p {{
        text-align: center;
        color: {t_['text_muted']};
        font-size: 0.98rem;
        max-width: 460px;
        margin: 0 auto;
        line-height: 1.55;
    }}

    /* ---- Progress ---- */

    .progress-label {{
        color: {t_['text_muted']};
        font-size: 0.82rem;
        margin-bottom: 0.3rem;
        text-align: {align_start};
    }}

    /* ---- Step card ---- */

    .step-card {{
        background: {t_['surface']};
        border: 1px solid {t_['border']};
        border-radius: 18px;
        padding: 1.5rem 1.5rem 0.4rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: {t_['shadow']};
    }}

    .step-title {{
        font-family:
            {"'Tajawal', sans-serif"
             if is_rtl
             else "'Space Grotesk', sans-serif"};

        font-weight: 700;
        font-size: 1.12rem;
        color: {t_['text']};
        margin-bottom: 0.1rem;
    }}

    .step-hint {{
        color: {t_['text_muted']};
        font-size: 0.85rem;
        margin-bottom: 1.1rem;
    }}

    /* ---- Review rows ---- */

    .review-row {{
        display: flex;
        justify-content: space-between;
        padding: 0.62rem 0;
        border-top: 1px solid {t_['border']};
        font-size: 0.92rem;
    }}

    .review-row .k {{
        color: {t_['text_muted']};
    }}

    .review-row .v {{
        color: {t_['text']};
        font-weight: 600;
    }}

    /* ---- Result card ---- */

    .result-card {{
        border-radius: 22px;
        padding: 2rem 1.8rem;
        border: 1px solid {t_['border']};
        background:
            linear-gradient(
                160deg,
                {t_['surface']},
                {t_['surface_2']}
            );

        box-shadow: {t_['shadow']};
        text-align: center;
    }}

    .result-badge {{
        display: inline-block;
        padding: 0.35rem 1rem;
        border-radius: 999px;

        font-family:
            {"'Tajawal', sans-serif"
             if is_rtl
             else "'Space Grotesk', sans-serif"};

        font-weight: 700;
        font-size: 0.86rem;
        letter-spacing: 0.01em;
    }}

    .result-desc {{
        color: {t_['text_muted']};
        font-size: 0.95rem;
        margin-top: 0.9rem;
        line-height: 1.6;
        text-align: center;
    }}

    .result-note {{
        color: {t_['text_muted']};
        font-size: 0.78rem;
        margin-top: 0.75rem;
        line-height: 1.5;
        text-align: center;
        opacity: 0.9;
    }}

    .tips-card {{
        background: {t_['surface']};
        border: 1px solid {t_['border']};
        border-radius: 16px;
        padding: 1.3rem 1.5rem;
        margin-top: 1rem;
    }}

    .tips-card ul {{
        margin: 0.4rem 0 0 0;
        padding-{align_start}: 1.1rem;
        color: {t_['text']};
        font-size: 0.92rem;
        line-height: 1.85;
    }}

    .disclaimer-box {{
        color: {t_['text_muted']};
        font-size: 0.8rem;
        text-align: center;
        margin-top: 1rem;
        padding: 0.8rem 1rem;
        border: 1px dashed {t_['border']};
        border-radius: 12px;
    }}

    .footer-note {{
        text-align: center;
        color: {t_['text_muted']};
        font-size: 0.76rem;
        margin-top: 2.2rem;
    }}

    /* ---- Buttons ---- */

    div.stButton > button {{
        border-radius: 12px;
        padding: 0.8rem 1.3rem;
        font-weight: 700;

        font-family:
            {"'Tajawal', sans-serif"
             if is_rtl
             else "'Space Grotesk', sans-serif"};

        letter-spacing: 0.01em;

        transition:
            transform 0.12s ease,
            box-shadow 0.12s ease;

        width: 100%;
    }}

    div.stButton > button:hover {{
        transform: translateY(-1px);
    }}

    div.stButton > button:active {{
        transform: translateY(0px);
    }}

    div[data-testid="column"]:has(
        button[kind="primary"]
    ) div.stButton > button,

    button[kind="primary"] {{
        background:
            linear-gradient(
                160deg,
                {t_['accent']},
                {t_['accent']}
            ) !important;

        color: #06171A !important;
        border: none !important;

        box-shadow:
            0 10px 28px -10px
            {t_['accent']}66;
    }}

    hr {{
        border-color: {t_['border']};
    }}

    </style>
    """),
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

def switch_lang():
    st.session_state.lang = (
        st.session_state["_lang_select"]
    )


def toggle_theme():
    st.session_state.theme = (
        "light"
        if st.session_state.theme == "dark"
        else "dark"
    )


# ---------------------------------------------------------------------------
# Top controls
# ---------------------------------------------------------------------------

c_brand, c_lang, c_theme = st.columns(
    [3.2, 2.1, 1]
)


with c_brand:

    st.markdown(
        html_block(f'''
        <div style="
            font-weight:700;
            font-size:1rem;
            padding-top:0.55rem;
        ">
            💳 {tr("brand_title")}
        </div>
        '''),
        unsafe_allow_html=True,
    )


with c_lang:

    st.selectbox(
        tr("language_label"),
        options=list(LANGUAGES.keys()),
        format_func=lambda k:
            f"{LANGUAGES[k]['flag']} {LANGUAGES[k]['label']}",
        index=list(LANGUAGES.keys()).index(lang),
        key="_lang_select",
        on_change=switch_lang,
        label_visibility="collapsed",
    )


with c_theme:

    st.button(
        "🌙"
        if st.session_state.theme == "light"
        else "☀️",

        key="_theme_btn",

        help=(
            tr("theme_to_dark")
            if st.session_state.theme == "light"
            else tr("theme_to_light")
        ),

        on_click=toggle_theme,
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Load artifacts once
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def get_artifacts(root: str):
    return load_artifacts(root)


try:

    artifacts = get_artifacts(
        PROJECT_ROOT
    )

except ArtifactLoadError:

    st.markdown(
        f"### {tr('load_error_title')}"
    )

    st.error(
        tr("load_error_body")
    )

    print(
        traceback.format_exc()
    )

    st.stop()

except Exception:

    st.markdown(
        f"### {tr('load_error_title')}"
    )

    st.error(
        tr("load_error_body")
    )

    print(
        traceback.format_exc()
    )

    st.stop()


# ---------------------------------------------------------------------------
# Gauge
# ---------------------------------------------------------------------------

def gauge_svg(
    display_pct: float,
    tone_color: str,
    caption: str,
) -> str:

    """A restrained radial gauge (semi-circle arc)."""

    pct = max(
        0.0,
        min(1.0, display_pct),
    )

    angle = 180 * pct

    cx, cy, r = 120, 118, 92

    x = (
        cx
        + r
        * math.cos(
            math.radians(
                180 - angle
            )
        )
    )

    y = (
        cy
        - r
        * math.sin(
            math.radians(
                180 - angle
            )
        )
    )

    large_arc = (
        1
        if angle > 180
        else 0
    )

    svg = f'''
        <svg width="240" height="140" viewBox="0 0 240 140" xmlns="http://www.w3.org/2000/svg">
            <path d="M {cx-r} {cy} A {r} {r} 0 0 1 {cx+r} {cy}" fill="none" stroke="{t_['border']}" stroke-width="16" stroke-linecap="round" />
            <path d="M {cx-r} {cy} A {r} {r} 0 {large_arc} 1 {x} {y}" fill="none" stroke="{tone_color}" stroke-width="16" stroke-linecap="round" />
            <text x="{cx}" y="{cy-8}" text-anchor="middle" font-family="Space Grotesk, Tajawal, sans-serif" font-weight="700" font-size="30" fill="{t_['text']}">{pct*100:.0f}%</text>
            <text x="{cx}" y="{cy+16}" text-anchor="middle" font-family="Inter, Tajawal, sans-serif" font-size="11" fill="{t_['text_muted']}">{caption}</text>
        </svg>
    '''

    # IMPORTANT: this string gets embedded inside other HTML that is passed to
    # st.markdown(..., unsafe_allow_html=True). Streamlit's markdown parser
    # treats blank lines followed by heavily-indented lines as an indented
    # Markdown code block, which was causing the raw SVG source to be printed
    # on screen instead of being rendered. Collapsing everything onto a single
    # line with no leading whitespace avoids that entirely.
    return " ".join(line.strip() for line in svg.splitlines() if line.strip())


# ---------------------------------------------------------------------------
# Step helpers
# ---------------------------------------------------------------------------

def step_header(
    title_key: str,
    hint_key: str,
):

    st.markdown(
        html_block(f'''
        <div class="step-title">
            {tr(title_key)}
        </div>

        <div class="step-hint">
            {tr(hint_key)}
        </div>
        '''),
        unsafe_allow_html=True,
    )


def nav_buttons(
    back_enabled: bool,
    next_label_key: str = "btn_next",
):

    b1, b2 = st.columns(2)

    with b1:

        if back_enabled:

            if st.button(
                tr("btn_back"),
                key=f"back_{st.session_state.step}",
                use_container_width=True,
            ):

                st.session_state.step -= 1
                st.rerun()

        else:

            st.write("")

    with b2:

        clicked = st.button(
            tr(next_label_key),
            key=f"next_{st.session_state.step}",
            type="primary",
            use_container_width=True,
        )

    return clicked


# ===========================================================================
# STEP 0 — Landing
# ===========================================================================

if st.session_state.step == 0:

    st.markdown(
        html_block(f'''
        <div class="hero">

            <div class="icon">
                💳
            </div>

            <h1>
                {tr("brand_title")}
            </h1>

            <p>
                {tr("brand_tagline")}
            </p>

        </div>
        '''),
        unsafe_allow_html=True,
    )

    if st.button(
        tr("hero_cta"),
        type="primary",
        use_container_width=True,
    ):

        st.session_state.step = 1
        st.rerun()

    st.markdown(
        html_block(f'''
        <p class="footer-note">
            {tr("hero_note")}
        </p>
        '''),
        unsafe_allow_html=True,
    )


# ===========================================================================
# STEPS 1–5 — Data entry + review
# ===========================================================================

elif (
    1
    <= st.session_state.step
    <= TOTAL_STEPS
):

    st.markdown(
        html_block(f'''
        <div class="progress-label">
            {tr("progress_step")}
            {st.session_state.step}
            {tr("progress_of")}
            {TOTAL_STEPS}
        </div>
        '''),
        unsafe_allow_html=True,
    )

    st.progress(
        st.session_state.step
        / TOTAL_STEPS
    )

    f = st.session_state.form

    st.markdown(
        '<div class="step-card">',
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------------------------
    # STEP 1
    # -----------------------------------------------------------------------

    if st.session_state.step == 1:

        step_header(
            "step1_title",
            "step1_hint",
        )

        f["age_years"] = st.slider(
            tr("age_label"),
            18,
            75,
            f["age_years"],
        )

        f["gender"] = st.selectbox(
            tr("gender_label"),
            GENDER_OPTIONS,
            index=GENDER_OPTIONS.index(
                f["gender"]
            ),
            format_func=lambda v:
                tr(GENDER_LABEL_KEYS[v]),
        )

        f["family_status"] = st.selectbox(
            tr("family_label"),
            FAMILY_OPTIONS,
            index=FAMILY_OPTIONS.index(
                f["family_status"]
            ),
            format_func=lambda v:
                tr(FAMILY_LABEL_KEYS[v]),
        )

        f["num_children"] = st.number_input(
            tr("children_label"),
            0,
            15,
            f["num_children"],
            step=1,
        )


    # -----------------------------------------------------------------------
    # STEP 2
    # -----------------------------------------------------------------------

    elif st.session_state.step == 2:

        step_header(
            "step2_title",
            "step2_hint",
        )

        f["years_employed"] = st.slider(
            tr("years_employed_label"),
            0.0,
            45.0,
            f["years_employed"],
            step=0.5,
        )

        f["occupation"] = st.selectbox(
            tr("occupation_label"),
            OCCUPATION_OPTIONS,
            index=OCCUPATION_OPTIONS.index(
                f["occupation"]
            ),
            format_func=lambda v:
                tr(
                    OCCUPATION_LABEL_KEYS[v]
                ),
        )

        f["annual_income"] = st.number_input(
            tr("income_label"),
            min_value=0,
            value=f["annual_income"],
            step=5_000,
        )


    # -----------------------------------------------------------------------
    # STEP 3
    # -----------------------------------------------------------------------

    elif st.session_state.step == 3:

        step_header(
            "step3_title",
            "step3_hint",
        )

        f["contract_type"] = st.radio(
            tr("contract_label"),
            CONTRACT_OPTIONS,
            index=CONTRACT_OPTIONS.index(
                f["contract_type"]
            ),
            format_func=lambda v:
                tr(
                    CONTRACT_LABEL_KEYS[v]
                ),
            horizontal=True,
        )

        f["loan_amount"] = st.number_input(
            tr("loan_amount_label"),
            min_value=0,
            value=f["loan_amount"],
            step=10_000,
        )

        f["goods_price"] = st.number_input(
            tr("goods_price_label"),
            min_value=0,
            value=f["goods_price"],
            step=10_000,
            help=tr("goods_price_hint"),
        )

        f["annuity_amount"] = st.number_input(
            tr("annuity_label"),
            min_value=0,
            value=f["annuity_amount"],
            step=1_000,
        )


    # -----------------------------------------------------------------------
    # STEP 4
    # -----------------------------------------------------------------------

    elif st.session_state.step == 4:

        step_header(
            "step4_title",
            "step4_hint",
        )

        f["has_bureau_history"] = st.toggle(
            tr("bureau_history_label"),
            value=f["has_bureau_history"],
        )

        f["has_previous_application"] = st.toggle(
            tr("previous_app_label"),
            value=f["has_previous_application"],
        )

        f["education"] = st.selectbox(
            tr("education_label"),
            EDUCATION_OPTIONS,
            index=EDUCATION_OPTIONS.index(
                f["education"]
            ),
            format_func=lambda v:
                tr(
                    EDUCATION_LABEL_KEYS[v]
                ),
        )

        cc1, cc2 = st.columns(2)

        f["owns_car"] = cc1.toggle(
            tr("owns_car_label"),
            value=f["owns_car"],
        )

        f["owns_realty"] = cc2.toggle(
            tr("owns_realty_label"),
            value=f["owns_realty"],
        )


    # -----------------------------------------------------------------------
    # STEP 5 — Review
    # -----------------------------------------------------------------------

    elif st.session_state.step == 5:

        step_header(
            "review_title",
            "step5_hint",
        )

        st.caption(
            tr("review_intro")
        )


        def row(
            k_label,
            value,
        ):

            st.markdown(
                html_block(f'''
                <div class="review-row">
                    <span class="k">
                        {k_label}
                    </span>

                    <span class="v">
                        {value}
                    </span>
                </div>
                '''),
                unsafe_allow_html=True,
            )


        row(
            tr("age_label"),
            f["age_years"],
        )

        row(
            tr("gender_label"),
            tr(
                GENDER_LABEL_KEYS[
                    f["gender"]
                ]
            ),
        )

        row(
            tr("family_label"),
            tr(
                FAMILY_LABEL_KEYS[
                    f["family_status"]
                ]
            ),
        )

        row(
            tr("children_label"),
            f["num_children"],
        )

        row(
            tr("years_employed_label"),
            f["years_employed"],
        )

        row(
            tr("occupation_label"),
            tr(
                OCCUPATION_LABEL_KEYS[
                    f["occupation"]
                ]
            ),
        )

        row(
            tr("income_label"),
            f"{f['annual_income']:,}",
        )

        row(
            tr("contract_label"),
            tr(
                CONTRACT_LABEL_KEYS[
                    f["contract_type"]
                ]
            ),
        )

        row(
            tr("loan_amount_label"),
            f"{f['loan_amount']:,}",
        )

        row(
            tr("goods_price_label"),
            f"{f['goods_price']:,}",
        )

        row(
            tr("annuity_label"),
            f"{f['annuity_amount']:,}",
        )

        row(
            tr("education_label"),
            tr(
                EDUCATION_LABEL_KEYS[
                    f["education"]
                ]
            ),
        )

        row(
            tr("bureau_history_label"),
            (
                tr("yes_label")
                if f["has_bureau_history"]
                else tr("no_label")
            ),
        )

        row(
            tr("previous_app_label"),
            (
                tr("yes_label")
                if f["has_previous_application"]
                else tr("no_label")
            ),
        )

        row(
            tr("owns_car_label"),
            (
                tr("yes_label")
                if f["owns_car"]
                else tr("no_label")
            ),
        )

        row(
            tr("owns_realty_label"),
            (
                tr("yes_label")
                if f["owns_realty"]
                else tr("no_label")
            ),
        )


    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------------------------
    # Navigation / Submit
    # -----------------------------------------------------------------------

    if st.session_state.step == TOTAL_STEPS:

        clicked = nav_buttons(
            back_enabled=True,
            next_label_key="btn_submit",
        )

        if clicked:

            form_values = {

                "age_years":
                    f["age_years"],

                "years_employed":
                    f["years_employed"],

                "annual_income":
                    f["annual_income"],

                "loan_amount":
                    f["loan_amount"],

                "annuity_amount":
                    f["annuity_amount"],

                "goods_price":
                    f["goods_price"],

                "num_children":
                    f["num_children"],

                "has_bureau_history":
                    int(
                        f["has_bureau_history"]
                    ),

                "has_previous_application":
                    int(
                        f[
                            "has_previous_application"
                        ]
                    ),

                "gender":
                    f["gender"],

                # Canonical Home Credit category.
                "education":
                    f["education"],

                "family_status":
                    f["family_status"],

                "contract_type":
                    f["contract_type"],

                "owns_car":
                    f["owns_car"],

                "owns_realty":
                    f["owns_realty"],

                "occupation": (
                    None
                    if f["occupation"]
                    == "Other / not listed"
                    else f["occupation"]
                ),
            }


            with st.spinner(
                tr("loading_text")
            ):

                try:

                    feature_row = (
                        build_full_feature_row(
                            form_values,
                            artifacts.feature_lists[
                                "all_features"
                            ],
                        )
                    )

                    st.session_state.result = (
                        predict_classical(
                            artifacts,
                            feature_row,
                        )
                    )

                    st.session_state.step = 6

                    st.rerun()

                except Exception:

                    st.error(
                        tr("predict_error")
                    )

                    print(
                        traceback.format_exc()
                    )


    else:

        clicked = nav_buttons(
            back_enabled=(
                st.session_state.step > 1
            ),
        )

        if clicked:

            st.session_state.step += 1
            st.rerun()


# ===========================================================================
# STEP 6 — Result
# ===========================================================================

elif (
    st.session_state.step == 6
    and st.session_state.result is not None
):

    probability = float(
        st.session_state.result[
            "probability"
        ]
    )

    tier_label, tone = risk_tier(
        probability
    )

    title_key, desc_key = TIER_KEYS[
        tone
    ]

    # -----------------------------------------------------------------------
    # IMPORTANT:
    # The model predicts default probability.
    # Therefore, the gauge displays the estimated repayment risk directly.
    #
    # We intentionally DO NOT calculate:
    #     1 - probability
    #
    # because that would represent the complementary probability and could
    # incorrectly be interpreted as an approval or repayment guarantee.
    # -----------------------------------------------------------------------

    risk_percentage = probability


    st.markdown(
        f"### {tr('result_title')}"
    )


    gauge_html = gauge_svg(
        risk_percentage,
        t_[tone],
        tr("result_prob_caption"),
    )


    result_html = (
        f'<div class="result-card">'

        f'<span class="result-badge" '
        f'style="'
        f'background:{t_[tone + "_soft"]}; '
        f'color:{t_[tone]};'
        f'">'

        f'{tr(title_key)}'

        f'</span>'

        f'<div style="'
        f'margin-top:1.1rem; '
        f'display:flex; '
        f'justify-content:center;'
        f'">'

        f'{gauge_html}'

        f'</div>'

        f'<div class="result-desc">'
        f'{tr(desc_key)}'
        f'</div>'

        f'<div class="result-note">'
        f'{tr("result_scale_note")}'
        f'</div>'

        f'</div>'
    )


    st.markdown(
        html_block(result_html),
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------------------------
    # Risk-reduction tips
    # -----------------------------------------------------------------------

    if tone != "success":

        tips = [
            tr("tip_income"),
            tr("tip_amount"),
            tr("tip_history"),
            tr("tip_employment"),
        ]

        st.markdown(
            html_block(f'''
            <div class="tips-card">

                <div
                    class="step-title"
                    style="font-size:0.98rem;"
                >
                    {tr("tips_title")}
                </div>

                <ul>
                    {
                        ''.join(
                            f"<li>{tip}</li>"
                            for tip in tips
                        )
                    }
                </ul>

            </div>
            '''),
            unsafe_allow_html=True,
        )


    # -----------------------------------------------------------------------
    # Disclaimer
    # -----------------------------------------------------------------------

    st.markdown(
        html_block(f'''
        <div class="disclaimer-box">
            {tr("disclaimer")}
        </div>
        '''),
        unsafe_allow_html=True,
    )


    st.write("")


    # -----------------------------------------------------------------------
    # Restart
    # -----------------------------------------------------------------------

    if st.button(
        tr("btn_restart"),
        type="primary",
        use_container_width=True,
    ):

        st.session_state.step = 0
        st.session_state.result = None
        st.rerun()


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown(
    html_block(f'''
    <div class="footer-note">
        {tr("footer_note")}
    </div>
    '''),
    unsafe_allow_html=True,
)