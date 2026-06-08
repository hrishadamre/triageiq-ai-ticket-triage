# utils/styles.py — shared CSS + sidebar for TriageIQ
# All pages call inject() + add_sidebar() after set_page_config()

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Barlow:wght@300;400;500&display=swap" rel="stylesheet">'

BASE_CSS = """
<style>
*,*::before,*::after{box-sizing:border-box}

[data-testid="stAppViewContainer"]{
  background:#080a0f;
  background-image:
    repeating-linear-gradient(0deg,transparent,transparent 39px,rgba(255,255,255,.018) 39px,rgba(255,255,255,.018) 40px),
    repeating-linear-gradient(90deg,transparent,transparent 39px,rgba(255,255,255,.018) 39px,rgba(255,255,255,.018) 40px);
}

/* Sidebar — scoped carefully, do NOT override collapse button or SVGs */
[data-testid="stSidebar"]{
  background:#0c0e14 !important;
  border-right:1px solid #1e2235 !important;
  min-width:220px !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span:not([data-testid]),
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] label{
  font-family:'Barlow',sans-serif !important;
  color:#6b7280 !important;
}
/* Keep collapse toggle visible */
[data-testid="stSidebarCollapseButton"]{
  color:#f59e0b !important;
  opacity:1 !important;
}
[data-testid="stSidebarCollapseButton"] svg{
  fill:#f59e0b !important;
}

.block-container{padding:2rem 3rem !important;max-width:1400px}
#MainMenu,footer,header{visibility:hidden}
[data-testid="stDecoration"]{display:none}

/* ── Page header ── */
.tiq-page-header{padding:36px 0 20px;border-bottom:1px solid #1e2235;margin-bottom:28px}
.tiq-eyebrow{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.2em;margin-bottom:6px}
.tiq-h1{font-family:'Barlow Condensed',sans-serif;font-size:2.4rem;font-weight:800;color:#f0f0f0;text-transform:uppercase;letter-spacing:.06em;margin:0;line-height:1}
.tiq-sub{font-family:'Barlow',sans-serif;font-size:.88rem;color:#4a5568;margin-top:6px}

/* ── Section label ── */
.tiq-section{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#f59e0b;text-transform:uppercase;letter-spacing:.2em;margin:32px 0 14px;display:flex;align-items:center;gap:12px}
.tiq-section::after{content:'';flex:1;height:1px;background:#1e2235}

/* ── Sidebar logo ── */
.sb-logo{display:flex;align-items:center;gap:10px;padding:20px 16px 16px;border-bottom:1px solid #1e2235;margin-bottom:8px}
.sb-hex{width:28px;height:28px;background:linear-gradient(135deg,#f59e0b,#ef4444);clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);flex-shrink:0}
.sb-name{font-family:'Barlow Condensed',sans-serif;font-size:1.2rem;font-weight:800;color:#f0f0f0 !important;text-transform:uppercase;letter-spacing:.1em;line-height:1}
.sb-tag{font-family:'JetBrains Mono',monospace;font-size:.52rem;color:#4a5568 !important;letter-spacing:.1em;text-transform:uppercase;margin-top:2px}
.sb-nav-label{font-family:'JetBrains Mono',monospace;font-size:.55rem;color:#2d3148 !important;text-transform:uppercase;letter-spacing:.15em;padding:12px 16px 4px;display:block}
.sb-status{display:flex;align-items:center;gap:6px;padding:8px 16px 16px;border-top:1px solid #1e2235;margin-top:8px}
.sb-dot{width:6px;height:6px;border-radius:50%;background:#4ade80;box-shadow:0 0 6px #4ade80;animation:sbpulse 2s infinite;flex-shrink:0}
@keyframes sbpulse{0%,100%{opacity:1}50%{opacity:.3}}
.sb-status-txt{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#4ade80 !important;letter-spacing:.1em}

/* ── Generic utils ── */
.tiq-missing{border:1px dashed #1e2235;border-radius:2px;padding:20px;font-family:'JetBrains Mono',monospace;font-size:.68rem;color:#374151;text-align:center;margin:8px 0}

/* ── Widget overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label{
  font-family:'JetBrains Mono',monospace !important;
  font-size:.62rem !important;color:#f59e0b !important;
  text-transform:uppercase;letter-spacing:.12em
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea{
  background:#080a0f !important;border:1px solid #1e2235 !important;
  color:#e2e8f0 !important;border-radius:2px !important;
  font-family:'Barlow',sans-serif !important
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus{
  border-color:#f59e0b !important;box-shadow:0 0 0 1px #f59e0b33 !important
}
div[data-testid="stSelectbox"]>div>div{
  background:#080a0f !important;border:1px solid #1e2235 !important;
  border-radius:2px !important;color:#e2e8f0 !important
}
.stButton>button{
  background:#f59e0b !important;color:#080a0f !important;
  border:none !important;border-radius:2px !important;
  font-family:'Barlow Condensed',sans-serif !important;
  font-size:1rem !important;font-weight:700 !important;
  text-transform:uppercase;letter-spacing:.1em;padding:12px 32px !important
}
.stButton>button:hover{background:#d97706 !important}
div[data-testid="stExpander"]{
  background:#0c0e14 !important;border:1px solid #1e2235 !important;border-radius:2px !important
}
div[data-testid="stExpander"] summary{
  font-family:'JetBrains Mono',monospace !important;
  font-size:.65rem !important;color:#f59e0b !important;text-transform:uppercase;letter-spacing:.1em
}
/* Page link nav items in sidebar */
[data-testid="stSidebarNavLink"]{
  border-radius:2px !important;
  font-family:'Barlow Condensed',sans-serif !important;
  font-size:.9rem !important;font-weight:600 !important;
  text-transform:uppercase !important;letter-spacing:.06em !important;
  color:#6b7280 !important;padding:8px 16px !important;
  transition:color .15s !important;
}
[data-testid="stSidebarNavLink"]:hover{color:#f59e0b !important;background:#0e1117 !important}
[data-testid="stSidebarNavLink"][aria-current="page"]{
  color:#f59e0b !important;background:#0e1117 !important;
  border-left:2px solid #f59e0b !important;
}
</style>
"""

def inject(extra_css=""):
    """Inject fonts + base CSS. Call after set_page_config()."""
    import streamlit as st
    st.html(FONTS + BASE_CSS + (f"<style>{extra_css}</style>" if extra_css else ""))

def add_sidebar():
    """Renders a top navigation bar instead of a sidebar."""
    import streamlit as st
    st.markdown("""
<style>
[data-testid="stSidebar"]{display:none !important}
[data-testid="collapsedControl"]{display:none !important}
.tiq-topnav{
  display:flex;align-items:center;justify-content:space-between;
  padding:12px 0 12px;border-bottom:1px solid #1e2235;margin-bottom:28px;
}
.tiq-topnav-brand{display:flex;align-items:center;gap:10px}
.tiq-topnav-name{font-family:'Barlow Condensed',sans-serif;font-size:1.3rem;font-weight:800;color:#f0f0f0;text-transform:uppercase;letter-spacing:.1em;line-height:1}
.tiq-topnav-tag{font-family:'JetBrains Mono',monospace;font-size:.52rem;color:#4a5568;letter-spacing:.1em;text-transform:uppercase;margin-top:2px}
.tiq-topnav-links{display:flex;align-items:center;gap:4px}
.tiq-topnav-links a{
  font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#4a5568;
  text-transform:uppercase;letter-spacing:.1em;text-decoration:none;
  padding:6px 12px;border-radius:2px;transition:all .15s;border:1px solid transparent;
}
.tiq-topnav-links a:hover{color:#f59e0b;border-color:#f59e0b33;background:#0e1117}
.tiq-topnav-status{display:flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#4ade80;letter-spacing:.1em}
.tiq-topnav-dot{width:6px;height:6px;border-radius:50%;background:#4ade80;box-shadow:0 0 6px #4ade80}
</style>
<div class="tiq-topnav">
  <div class="tiq-topnav-brand">
    <div>
      <div class="tiq-topnav-name">🎯 TriageIQ</div>
      <div class="tiq-topnav-tag">BUDT751 // Group 2</div>
    </div>
  </div>
  <div class="tiq-topnav-links">
    <a href="/" target="_self">Home</a>
    <a href="/Dashboard" target="_self">Dashboard</a>
    <a href="/Live_Demo" target="_self">Live Demo</a>
    <a href="/Model_Performance" target="_self">Model Performance</a>
    <a href="/Responsible_AI" target="_self">Responsible AI</a>
  </div>
  <div class="tiq-topnav-status"><div class="tiq-topnav-dot"></div>SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)
