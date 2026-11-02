
import streamlit as st
from optimizer import optimize_source

st.set_page_config(
    page_title="FoldLab | Constant Folding Optimizer",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Professional UI Styling ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #F5F7FB;
        color: #182238;
    }

    [data-testid="stHeader"] {
        background: rgba(245,247,251,0.95);
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #101B35 0%, #233D70 100%);
        padding: 32px 36px;
        border-radius: 20px;
        color: white;
        margin-bottom: 26px;
        box-shadow: 0 10px 30px rgba(20, 38, 75, 0.12);
    }

    .hero-label {
        display: inline-block;
        color: #C7D7FF;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.6px;
        margin-bottom: 12px;
    }

    .hero h1 {
        color: white;
        font-size: clamp(26px, 3vw, 38px);
        font-weight: 800;
        letter-spacing: -1.2px;
        margin: 0 0 10px 0;
    }

    .hero p {
        color: #D6E0F5;
        font-size: 15px;
        line-height: 1.7;
        max-width: 760px;
        margin: 0;
    }

    .section-heading {
        color: #182238;
        font-size: 19px;
        font-weight: 750;
        margin: 10px 0 5px 0;
    }

    .section-caption {
        color: #738097;
        font-size: 13px;
        margin-bottom: 15px;
    }

    .panel {
        background: white;
        border: 1px solid #E4E9F2;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 16px;
    }

    .panel-label {
        color: #344563;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .metric-card {
        background: white;
        border: 1px solid #E3E9F3;
        border-radius: 14px;
        padding: 19px 20px;
        min-height: 105px;
    }

    .metric-label {
        color: #77849A;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #172644;
        font-size: 28px;
        font-weight: 800;
    }

    .metric-note {
        color: #8B97AA;
        font-size: 11px;
        margin-top: 5px;
    }

    .trace-item {
        background: white;
        border: 1px solid #E5EAF2;
        border-left: 4px solid #456BE6;
        border-radius: 9px;
        padding: 13px 16px;
        margin-bottom: 9px;
        color: #344563;
        font-size: 13px;
        line-height: 1.6;
    }

    .footer {
        border-top: 1px solid #E3E8F0;
        margin-top: 35px;
        padding-top: 18px;
        text-align: center;
        color: #8994A7;
        font-size: 12px;
    }

    div.stButton > button[kind="primary"] {
        background: #3459D5;
        border: 1px solid #3459D5;
        color: white;
        border-radius: 10px;
        min-height: 45px;
        font-weight: 700;
        transition: 0.2s ease;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #2748B6;
        border-color: #2748B6;
        color: white;
    }

    div.stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 39px;
    }

    div[data-testid="stTextArea"] textarea {
        background: #FCFDFF;
        border: 1px solid #DCE3EF;
        border-radius: 10px;
        color: #182238;
        font-family: Consolas, monospace;
        font-size: 14px;
        line-height: 1.7;
    }

    div[data-testid="stSelectbox"] {
        background: transparent;
    }

    div[data-testid="stTabs"] button {
        font-weight: 650;
    }

    @media (max-width: 700px) {
        .hero {
            padding: 24px 20px;
        }
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# ---------- Sample Programs ----------
SAMPLES = {
    "Arithmetic Expressions": """int a = 10 + 20;
int b = 5 * 4 + 2;
int c = (3 + 7) * 2;
int d = x + 6 * 3;
int e = 100 - 30;""",

    "Nested Expressions": """int a = ((2 + 3) * 4) - 5;
int b = (8 - 3) * (2 + 4);
int c = 10 + 2 * (6 - 1);
int d = x + (10 * 2) - 1;
return (5 + 5) * (3 + 2);""",

    "Conditions and Loops": """int a = 10 + 20;
if (10 > 5) {
    int result = 4 * 5;
}
while (2 + 3 < 10) {
    int value = (6 + 4) * 2;
}""",

    "Negative and Mixed Values": """int a = -5 + 12;
int b = 4 * (7 - 2);
int c = x + 3 * 4;
int d = 100 / 5 + 3;""",

    "Custom Source Code": "",
}


# ---------- Header ----------
st.markdown("""
<div class="hero">
    <div class="hero-label">COMPILER CONSTRUCTION PROJECT</div>
    <h1>Constant Folding Optimizer</h1>
    <p>
        Simplify constant expressions at compile time. Explore source code,
        inspect optimization steps, and compare the original program
        with its optimized version.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------- Source Code Editor ----------
st.markdown('<div class="section-heading">Source Code Workspace</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="section-caption">Select an example or enter your own supported C-style source code.</div>',
    unsafe_allow_html=True,
)

top_left, top_right = st.columns([3, 2])

with top_left:
    sample_name = st.selectbox(
        "Sample program",
        list(SAMPLES.keys()),
    )

with top_right:
    st.markdown("<div style='height: 29px'></div>", unsafe_allow_html=True)
    load_sample = st.button(
        "Load Sample Program",
        use_container_width=True,
    )

if "source_code" not in st.session_state:
    st.session_state.source_code = SAMPLES["Arithmetic Expressions"]

if load_sample:
    st.session_state.source_code = SAMPLES[sample_name]

source_code = st.text_area(
    "Write or edit your source code",
    key="source_code",
    height=260,
    label_visibility="collapsed",
    placeholder="Enter your C-style source code here...",
)

run = st.button(
    "⚡  Optimize Source Code",
    type="primary",
    use_container_width=True,
)

if run:
    result = optimize_source(source_code)
    st.session_state.optimization_result = {
        "original": source_code,
        "optimized": result.code,
        "logs": result.logs,
        "folded": result.folded_count,
        "changed": result.changed_lines,
        "lines": result.original_lines,
    }

# ---------- Results ----------
if "optimization_result" in st.session_state:
    result = st.session_state.optimization_result

    st.markdown("---")
    st.markdown(
        '<div class="section-heading">Optimization Overview</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-caption">Summary of the latest optimization run.</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">EXPRESSIONS FOLDED</div>
            <div class="metric-value">{result["folded"]}</div>
            <div class="metric-note">Constant expressions replaced</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">LINES CHANGED</div>
            <div class="metric-value">{result["changed"]}</div>
            <div class="metric-note">Source lines modified</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SOURCE LINES</div>
            <div class="metric-value">{result["lines"]}</div>
            <div class="metric-note">Lines in submitted program</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    original_tab, optimized_tab, trace_tab = st.tabs([
        "  Code Comparison  ",
        "  Optimized Output  ",
        "  Optimization Trace  ",
    ])

    with original_tab:
        left, right = st.columns(2, gap="medium")

        with left:
            st.markdown("**Original Source Code**")
            st.code(result["original"] or "// Empty source",
                    language="c")

        with right:
            st.markdown("**Optimized Source Code**")
            st.code(result["optimized"] or "// Empty source",
                    language="c")

    with optimized_tab:
        st.markdown("**Final Optimized Program**")
        st.code(result["optimized"] or "// Empty source",
                language="c")

        st.download_button(
            "↓  Download Optimized Code (.c)",
            data=result["optimized"],
            file_name="optimized_code.c",
            mime="text/plain",
            use_container_width=True,
        )

    with trace_tab:
        st.markdown("**Transformation Log**")
        st.caption(
            "Each entry records a constant expression evaluated by the optimizer."
        )

        for item in result["logs"]:
            st.markdown(
                f'<div class="trace-item">{item}</div>',
                unsafe_allow_html=True,
            )

    st.success("Optimization run completed.")

    with st.expander("About this optimization"):
        st.write(
            "Constant folding evaluates expressions containing only "
            "constant operands. If an expression includes a variable, "
            "its constant subexpressions may still be simplified. "
            "This application does not perform constant propagation "
            "or remove conditional branches."
        )

# ---------- Footer ----------
st.markdown("""
<div class="footer">
    Constant Folding Optimizer &nbsp; · &nbsp;
    Compiler Construction &nbsp; · &nbsp;
    Educational Project
</div>
""", unsafe_allow_html=True)
