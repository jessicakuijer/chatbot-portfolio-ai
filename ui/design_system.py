"""Design tokens and global CSS for the Jessica IA assistant."""

import re

import streamlit as st

THEMES = {
    "clair": {
        "--bg": "#ffffff",
        "--surface": "#ffffff",
        "--surface-2": "#f4f4f5",
        "--fg": "#18181b",
        "--fg-muted": "#71717a",
        "--border": "#e7e7ea",
        "--accent": "#4f46e5",
        "--accent-fg": "#ffffff",
        "--assistant-bubble": "#f4f4f5",
        "--user-bubble": "#4f46e5",
        "--user-fg": "#ffffff",
        "--shadow": "0 1px 2px rgba(0,0,0,.04), 0 10px 30px rgba(0,0,0,.06)",
        "--composer-bg": "#ffffff",
        "--btn-bg": "#ffffff",
        "--btn-fg": "#18181b",
        "--btn-border": "#e7e7ea",
        "--font-body": "'Hanken Grotesk', system-ui, sans-serif",
        "--font-display": "'Hanken Grotesk', system-ui, sans-serif",
    },
    "sombre": {
        "--bg": "#0a0a0b",
        "--surface": "#141416",
        "--surface-2": "#1d1d20",
        "--fg": "#f4f4f5",
        "--fg-muted": "#9b9ba4",
        "--border": "#404045",
        "--accent": "#8b8bf6",
        "--accent-fg": "#0a0a0b",
        "--assistant-bubble": "#1d1d20",
        "--user-bubble": "#8b8bf6",
        "--user-fg": "#0a0a0b",
        "--shadow": "0 1px 2px rgba(0,0,0,.5), 0 14px 34px rgba(0,0,0,.5)",
        "--composer-bg": "#141416",
        "--btn-bg": "#252528",
        "--btn-fg": "#f4f4f5",
        "--btn-border": "#52525b",
        "--font-body": "'Hanken Grotesk', system-ui, sans-serif",
        "--font-display": "'Hanken Grotesk', system-ui, sans-serif",
    },
    "editorial": {
        "--bg": "#faf6f0",
        "--surface": "#fffdf9",
        "--surface-2": "#f1e9dd",
        "--fg": "#211c17",
        "--fg-muted": "#7d7165",
        "--border": "#e6dccd",
        "--accent": "#c2613f",
        "--accent-fg": "#fffaf3",
        "--assistant-bubble": "#fffdf9",
        "--user-bubble": "#c2613f",
        "--user-fg": "#fffaf3",
        "--shadow": "0 1px 2px rgba(120,80,40,.06), 0 14px 32px rgba(120,80,40,.12)",
        "--composer-bg": "#fffdf9",
        "--btn-bg": "#fffdf9",
        "--btn-fg": "#211c17",
        "--btn-border": "#e6dccd",
        "--font-body": "'Hanken Grotesk', system-ui, sans-serif",
        "--font-display": "'Instrument Serif', Georgia, serif",
    },
}

FONT_LINK = (
    "https://fonts.googleapis.com/css2?"
    "family=Hanken+Grotesk:wght@400;500;600;700;800"
    "&family=Instrument+Serif:ital@0;1&display=swap"
)


def theme_css_vars(theme: str) -> str:
    tokens = THEMES.get(theme, THEMES["clair"])
    return "\n".join(f"  {k}: {v};" for k, v in tokens.items())


def _escape_css_selectors(css: str) -> str:
    """Streamlit markdown treats :hover / :nth-child as emoji — escape selector colons."""
    selector_start = re.compile(
        r"^(\s*)(\.|#|@|[a-zA-Z\[]|div|section|header|footer|button)",
    )
    out: list[str] = []
    for line in css.splitlines():
        if "{" in line and selector_start.match(line):
            before, after = line.split("{", 1)
            before = re.sub(r":([a-zA-Z-]+(?:\([^)]*\))?)", r"\\3A \1", before)
            line = before + "{" + after
        out.append(line)
    return "\n".join(out)


def build_css(theme: str) -> str:
    vars_block = theme_css_vars(theme)
    return f"""
@import url('{FONT_LINK}');

:root {{
{vars_block}
}}

@keyframes msgIn {{ from {{ transform: translateY(9px); opacity: 0; }} to {{ transform: none; opacity: 1; }} }}
@keyframes dotBlink {{ 0%, 80%, 100% {{ opacity: .25; transform: translateY(0); }} 40% {{ opacity: 1; transform: translateY(-2px); }} }}
@keyframes fadeUp {{ from {{ transform: translateY(14px); opacity: 0; }} to {{ transform: none; opacity: 1; }} }}

/* Streamlit overrides */
section[data-testid="stSidebar"] {{ display: none !important; }}
header[data-testid="stHeader"],
.stApp > header {{
  display: none !important;
  height: 0 !important;
  min-height: 0 !important;
}}
footer {{ visibility: hidden; height: 0 !important; }}
#MainMenu {{ visibility: hidden; }}
.stApp .decoration {{
  display: none !important;
  height: 0 !important;
  width: 0 !important;
}}
.main .element-container {{
  margin-bottom: 0.35rem;
}}
.stApp {{
  background: var(--bg) !important;
  color: var(--fg) !important;
  font-family: var(--font-body) !important;
}}
.reportview-container .main .block-container,
.stApp [data-testid="stAppViewContainer"] .main .block-container,
.stApp .main .block-container {{
  padding-top: 0.75rem !important;
  padding-bottom: 0.75rem !important;
  max-width: 960px !important;
  margin-left: auto !important;
  margin-right: auto !important;
}}
.block-container {{
  padding-top: 0.75rem !important;
  padding-bottom: 0.75rem !important;
  max-width: 960px !important;
}}
div.jk-prompts-grid {{
  display: none !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}}
/* Legacy empty layout hooks — must not reserve space */
div.jk-shell,
div.jk-main,
div.jk-main-inner,
div.jk-header,
div.jk-composer-wrap,
div.jk-composer-inner,
div.jk-prompts {{
  display: none !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}}
/* Header rows (two horizontal blocks) */
.main .block-container div[data-testid="stHorizontalBlock"]:first-of-type,
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2),
.main .block-container div.row-widget.stHorizontal:first-of-type,
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) {{
  align-items: center !important;
  gap: 10px !important;
  flex-wrap: wrap !important;
}}
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2),
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) {{
  padding-bottom: 12px !important;
  margin-bottom: 8px !important;
  border-bottom: 1px solid var(--border);
}}
.main .block-container div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"],
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) div[data-testid="column"],
.main .block-container div.row-widget.stHorizontal:first-of-type div[data-testid="column"],
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) div[data-testid="column"] {{
  padding-left: 4px !important;
  padding-right: 4px !important;
}}
.main .block-container div[data-testid="stHorizontalBlock"]:first-of-type .stButton,
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton,
.main .block-container div.row-widget.stHorizontal:first-of-type .stButton,
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) .stButton {{
  width: auto !important;
}}
.main .block-container div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button,
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton > button,
.main .block-container div.row-widget.stHorizontal:first-of-type .stButton > button,
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) .stButton > button {{
  width: auto !important;
  min-width: max-content !important;
  white-space: nowrap !important;
  border-radius: 999px !important;
  font-family: var(--font-body) !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  padding: 8px 16px !important;
  min-height: 36px !important;
  line-height: 1.2 !important;
  border: 1px solid var(--border) !important;
  background: var(--btn-bg, var(--surface)) !important;
  color: var(--btn-fg, var(--fg)) !important;
}}
.main .block-container div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[kind="primary"],
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton > button[kind="primary"],
.main .block-container div.row-widget.stHorizontal:first-of-type .stButton > button[kind="primary"],
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) .stButton > button[kind="primary"] {{
  background: var(--accent) !important;
  color: var(--accent-fg) !important;
  border-color: transparent !important;
}}
/* Theme toggle group — row 2, columns 2-4 */
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(2),
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(3),
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(4),
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(2),
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(3),
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(4) {{
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 3px 4px !important;
}}
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(2) .stButton > button,
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(3) .stButton > button,
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(4) .stButton > button,
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(2) .stButton > button,
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(3) .stButton > button,
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(4) .stButton > button {{
  border: none !important;
  background: transparent !important;
  color: var(--fg-muted) !important;
  padding: 6px 14px !important;
  min-height: 32px !important;
}}
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(2) .stButton > button[kind="primary"],
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(3) .stButton > button[kind="primary"],
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(4) .stButton > button[kind="primary"],
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(2) .stButton > button[kind="primary"],
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(3) .stButton > button[kind="primary"],
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(4) .stButton > button[kind="primary"] {{
  background: var(--accent) !important;
  color: var(--accent-fg) !important;
}}
/* Language toggle group — row 2, columns 5-6 */
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(5),
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(6),
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(5),
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(6) {{
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 3px 4px !important;
}}
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(5) .stButton > button,
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(6) .stButton > button,
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(5) .stButton > button,
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(6) .stButton > button {{
  border: none !important;
  background: transparent !important;
  color: var(--fg-muted) !important;
  padding: 6px 14px !important;
  min-width: 42px !important;
  min-height: 32px !important;
}}
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(5) .stButton > button[kind="primary"],
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(6) .stButton > button[kind="primary"],
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(5) .stButton > button[kind="primary"],
.main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div:nth-child(6) .stButton > button[kind="primary"] {{
  background: var(--accent) !important;
  color: var(--accent-fg) !important;
}}
.jk-disclaimer {{
  text-align: center;
  font-size: 11.5px;
  color: var(--fg-muted);
  margin-top: 10px;
}}
.jk-footer-links {{
  text-align: center;
  font-size: 11px;
  color: var(--fg-muted);
  margin-top: 6px;
}}
.jk-footer-links a {{ color: var(--accent); text-decoration: none; }}

/* Header profile */
.jk-profile {{ display: flex; align-items: center; gap: 12px; min-width: 0; }}
.jk-avatar-wrap {{ position: relative; flex: none; }}
.jk-avatar {{
  width: 42px; height: 42px; border-radius: 50%;
  background: var(--accent); color: var(--accent-fg);
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 15px; letter-spacing: -0.02em;
}}
.jk-avatar-lg {{
  width: 72px; height: 72px; font-size: 26px;
  box-shadow: var(--shadow); margin-bottom: 22px;
}}
.jk-avatar-sm {{
  width: 32px; height: 32px; font-size: 11px; flex: none; margin-top: 2px;
}}
.jk-online {{
  position: absolute; right: -1px; bottom: -1px;
  width: 12px; height: 12px; border-radius: 50%;
  background: #22c55e; border: 2.5px solid var(--surface);
}}
.jk-profile-name {{ font-weight: 700; font-size: 15px; letter-spacing: -0.01em; line-height: 1.2; color: var(--fg); }}
.jk-profile-status {{ font-size: 12.5px; color: var(--fg-muted); line-height: 1.3; }}

/* Welcome */
.jk-welcome {{
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; text-align: center;
  padding: 28px 0 20px;
  animation: fadeUp .5s ease both;
}}
.jk-welcome h1 {{
  margin: 0 0 12px; font-family: var(--font-display);
  font-weight: 700; font-size: clamp(28px, 5vw, 42px);
  letter-spacing: -0.02em; line-height: 1.1; color: var(--fg) !important;
}}
.jk-welcome-sub {{
  margin: 0 0 36px; max-width: 520px; font-size: 16.5px;
  line-height: 1.6; color: var(--fg-muted);
}}
.jk-prompts-title {{
  font-size: 12px; font-weight: 700; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--fg-muted); margin-bottom: 14px;
}}

/* Messages */
.jk-msg-row {{ display: flex; gap: 12px; margin: 0 0 18px; animation: msgIn .35s ease both; }}
.jk-msg-row.user {{ justify-content: flex-end; }}
.jk-msg-row.assistant {{ justify-content: flex-start; align-items: flex-end; }}
.jk-msg-row.assistant.card {{ align-items: flex-start; }}
.jk-bubble {{
  max-width: 78%; padding: 12px 16px; border-radius: 18px;
  font-size: 15px; line-height: 1.58; white-space: pre-wrap;
}}
.jk-bubble.user {{
  background: var(--user-bubble); color: var(--user-fg);
  border-bottom-right-radius: 6px;
}}
.jk-bubble.assistant {{
  background: var(--assistant-bubble); color: var(--fg);
  border: 1px solid var(--border); border-bottom-left-radius: 6px;
}}
.jk-bubble.card {{ max-width: 100%; }}

/* Project cards */
.jk-projects-grid {{
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;
  max-width: 520px; width: 100%; margin-top: 12px;
}}
.jk-project-card {{
  display: flex; flex-direction: column; gap: 8px; padding: 14px;
  border-radius: 16px; border: 1px solid var(--border);
  background: var(--surface); box-shadow: var(--shadow);
}}
.jk-project-head {{ display: flex; align-items: center; gap: 10px; }}
.jk-project-mono {{
  width: 38px; height: 38px; border-radius: 11px;
  background: var(--accent); color: var(--accent-fg);
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 14px; flex: none;
}}
.jk-project-tag {{
  font-size: 10.5px; font-weight: 700; letter-spacing: .07em;
  text-transform: uppercase; color: var(--accent);
}}
.jk-project-title {{ font-weight: 700; font-size: 14.5px; line-height: 1.25; color: var(--fg); }}
.jk-project-desc {{ font-size: 13px; line-height: 1.45; color: var(--fg-muted); }}

/* Contact success */
.jk-contact-card {{
  padding: 18px; border-radius: 18px; border: 1px solid var(--border);
  background: var(--surface); box-shadow: var(--shadow);
  max-width: 420px; width: 100%; margin-top: 12px;
}}
.jk-contact-success {{ text-align: center; padding: 6px 4px; }}
.jk-contact-check {{
  width: 46px; height: 46px; border-radius: 50%;
  background: var(--accent); color: var(--accent-fg);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 12px; font-size: 22px; font-weight: 700;
}}
.jk-contact-done-title {{ font-weight: 700; font-size: 15px; margin-bottom: 5px; color: var(--fg); }}
.jk-contact-done-msg {{ font-size: 13.5px; color: var(--fg-muted); line-height: 1.5; }}

/* Typing indicator */
.jk-typing-row {{ display: flex; align-items: flex-end; gap: 12px; margin: 0 0 18px; }}
.jk-typing-bubble {{
  display: flex; align-items: center; gap: 5px;
  padding: 15px 18px; border-radius: 18px; border-bottom-left-radius: 6px;
  background: var(--assistant-bubble); border: 1px solid var(--border);
}}
.jk-dot {{
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--fg-muted); animation: dotBlink 1.2s infinite;
}}
.jk-dot-2 {{ animation-delay: .2s; }}
.jk-dot-3 {{ animation-delay: .4s; }}

/* Error panel */
.jk-error-panel {{
  max-width: 520px; margin: 24px auto; padding: 28px;
  border-radius: 18px; border: 1px solid var(--border);
  background: var(--surface); box-shadow: var(--shadow); text-align: center;
}}
.jk-error-panel h3 {{ color: var(--fg) !important; margin-top: 0; }}
.jk-error-panel p, .jk-error-panel li {{ color: var(--fg-muted); }}

/* Header controls — legacy selectors kept for safety */
.jk-header div[data-testid="stHorizontalBlock"] {{ gap: 8px !important; align-items: center; flex-wrap: wrap; }}
.jk-header .stButton > button {{
  border-radius: 999px !important; font-family: var(--font-body) !important;
  font-size: 13px !important; font-weight: 600 !important;
  padding: 7px 14px !important; min-height: 0 !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important; color: var(--fg) !important;
}}
.jk-header .stButton > button[kind="primary"] {{
  background: var(--accent) !important; color: var(--accent-fg) !important;
  border-color: transparent !important;
}}
.jk-controls {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }}
.jk-controls div[data-testid="stHorizontalBlock"] {{ gap: 8px !important; align-items: center; }}
.jk-controls .stButton > button {{
  border-radius: 999px !important; font-family: var(--font-body) !important;
  font-size: 13px !important; font-weight: 600 !important;
  padding: 7px 14px !important; min-height: 0 !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important; color: var(--fg) !important;
}}
.jk-controls .stButton > button[kind="primary"] {{
  background: var(--accent) !important; color: var(--accent-fg) !important;
  border-color: transparent !important;
}}
.jk-seg-wrap {{
  display: inline-flex; align-items: center;
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: 999px; padding: 3px; gap: 0;
}}
.jk-seg-wrap div[data-testid="column"] {{ padding: 0 !important; }}
.jk-seg-wrap .stButton > button {{
  padding: 6px 13px !important; border: none !important;
  background: transparent !important; color: var(--fg-muted) !important;
  box-shadow: none !important;
}}
.jk-seg-wrap .stButton > button[kind="primary"] {{
  background: var(--accent) !important; color: var(--accent-fg) !important;
}}

/* Prompt buttons — third horizontal block on welcome screen */
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"],
.main .block-container div.row-widget.stHorizontal:nth-of-type(3) div[data-testid="column"] {{
  padding: 4px 6px !important;
}}
.main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(3) .stButton > button,
.main .block-container div.row-widget.stHorizontal:nth-of-type(3) .stButton > button {{
  display: flex !important; align-items: center !important; justify-content: space-between !important;
  text-align: left !important; padding: 16px 18px !important; border-radius: 16px !important;
  border: 1px solid var(--border) !important; background: var(--btn-bg, var(--surface)) !important;
  color: var(--fg) !important; font-size: 15px !important; font-weight: 500 !important;
  min-height: 56px !important; width: 100% !important;
  box-shadow: var(--shadow) !important;
}}

/* Composer */
.main .block-container [data-testid="stForm"],
.main .block-container form[data-testid="stForm"],
.main .block-container .stForm {{
  border-top: 1px solid var(--border);
  padding-top: 12px !important;
  margin-top: 12px !important;
}}
.main .block-container [data-testid="stForm"] [data-testid="stHorizontalBlock"],
.main .block-container form[data-testid="stForm"] div.row-widget.stHorizontal,
.main .block-container .stForm div.row-widget.stHorizontal {{
  align-items: flex-end !important;
  gap: 8px !important;
}}
.main .block-container [data-testid="stForm"] .stTextInput > div > div > input,
.main .block-container form[data-testid="stForm"] .stTextInput > div > div > input,
.main .block-container .stForm .stTextInput > div > div > input {{
  border-radius: 20px !important;
  border: 1px solid var(--border) !important;
  background: var(--composer-bg) !important;
  box-shadow: var(--shadow) !important;
  color: var(--fg) !important;
  font-family: var(--font-body) !important;
  font-size: 15.5px !important;
  padding: 14px 18px !important;
}}
.main .block-container [data-testid="stForm"] .stFormSubmitButton > button,
.main .block-container form[data-testid="stForm"] .stFormSubmitButton > button,
.main .block-container .stForm .stFormSubmitButton > button {{
  width: 40px !important; height: 40px !important;
  min-height: 40px !important; border-radius: 14px !important;
  background: var(--accent) !important; color: var(--accent-fg) !important;
  border: none !important; font-size: 18px !important; font-weight: 700 !important;
  padding: 0 !important;
}}

/* Contact form */
.jk-contact-form-wrap {{
  max-width: 420px; margin-top: 12px;
  padding: 18px; border-radius: 18px; border: 1px solid var(--border);
  background: var(--surface); box-shadow: var(--shadow);
}}
.jk-contact-form-wrap label, .jk-contact-form-wrap p {{
  color: var(--fg) !important;
}}
.jk-contact-form-wrap .stTextInput input,
.jk-contact-form-wrap .stTextArea textarea {{
  border-radius: 11px !important;
  border: 1px solid var(--border) !important;
  background: var(--surface-2) !important;
  color: var(--fg) !important;
  font-family: var(--font-body) !important;
}}
.jk-contact-form-wrap .stButton > button {{
  width: 100%; border-radius: 12px !important;
  background: var(--accent) !important; color: var(--accent-fg) !important;
  font-weight: 700 !important; border: none !important;
}}

/* Global Streamlit widgets — override native light theme (Streamlit 1.x) */
.stApp .stButton > button,
.stApp .stFormSubmitButton > button,
.stApp button[kind="secondary"],
.stApp button.stSecondary {{
  background-color: var(--btn-bg, var(--surface-2)) !important;
  background: var(--btn-bg, var(--surface-2)) !important;
  color: var(--btn-fg, var(--fg)) !important;
  border: 1px solid var(--btn-border, var(--border)) !important;
  box-shadow: none !important;
}}
.stApp .stButton > button[kind="primary"],
.stApp .stFormSubmitButton > button[kind="primary"],
.stApp button[kind="primary"],
.stApp button.stPrimary {{
  background-color: var(--accent) !important;
  background: var(--accent) !important;
  color: var(--accent-fg) !important;
  border-color: var(--accent) !important;
}}
.stApp .stTextInput > div > div > input,
.stApp .stTextInput input,
.stApp .stTextArea textarea {{
  background-color: var(--surface-2) !important;
  color: var(--fg) !important;
  border-color: var(--border) !important;
}}
.stApp .stTextInput label,
.stApp .stTextArea label,
.stApp .stMarkdown p,
.stApp .stMarkdown li {{
  color: var(--fg) !important;
}}

@media (max-width: 640px) {{
  .stApp .main .block-container {{
    padding-left: 14px !important;
    padding-right: 14px !important;
    max-width: 100% !important;
  }}

  /* Navbar — row 1: profile full width, actions side by side */
  .main .block-container div[data-testid="stHorizontalBlock"]:first-of-type,
  .main .block-container div.row-widget.stHorizontal:first-of-type {{
    flex-wrap: wrap !important;
    align-items: center !important;
    gap: 8px !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 120 !important;
    background: var(--surface) !important;
    border-bottom: 1px solid var(--border) !important;
    margin-left: -14px !important;
    margin-right: -14px !important;
    padding: 10px 14px 8px !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child,
  .main .block-container div.row-widget.stHorizontal:first-of-type > div[data-testid="column"]:first-child {{
    flex: 1 1 100% !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:nth-child(2),
  .main .block-container div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:nth-child(3),
  .main .block-container div.row-widget.stHorizontal:first-of-type > div[data-testid="column"]:nth-child(2),
  .main .block-container div.row-widget.stHorizontal:first-of-type > div[data-testid="column"]:nth-child(3) {{
    flex: 1 1 calc(50% - 4px) !important;
    width: calc(50% - 4px) !important;
    max-width: calc(50% - 4px) !important;
    min-width: 0 !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:nth-child(3):not(:has(.stButton)),
  .main .block-container div.row-widget.stHorizontal:first-of-type > div[data-testid="column"]:nth-child(3):not(:has(.stButton)) {{
    display: none !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:nth-child(2):last-child,
  .main .block-container div.row-widget.stHorizontal:first-of-type > div[data-testid="column"]:nth-child(2):last-child {{
    flex: 1 1 100% !important;
    width: 100% !important;
    max-width: 100% !important;
  }}

  /* Navbar — row 2: hide spacer, center theme + language pills */
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2),
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) {{
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 8px !important;
    position: sticky !important;
    top: 92px !important;
    z-index: 110 !important;
    background: var(--surface) !important;
    border-bottom: 1px solid var(--border) !important;
    margin-left: -14px !important;
    margin-right: -14px !important;
    padding: 8px 14px 10px !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:first-child,
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:first-child {{
    display: none !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"],
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"] {{
    flex: 0 1 auto !important;
    width: auto !important;
    min-width: 0 !important;
    padding-left: 2px !important;
    padding-right: 2px !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(2),
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(3),
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(4),
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(2),
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(3),
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(4) {{
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    padding: 2px 3px !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(5),
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(6),
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(5),
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(6) {{
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    padding: 2px 3px !important;
  }}

  /* Compact profile + header buttons */
  .jk-profile {{ gap: 10px; }}
  .jk-profile-status {{ display: none; }}
  .jk-profile-name {{ font-size: 14px; }}
  .jk-avatar {{ width: 36px; height: 36px; font-size: 13px; }}
  .jk-online {{ width: 10px; height: 10px; }}
  .main .block-container div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button,
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton > button,
  .main .block-container div.row-widget.stHorizontal:first-of-type .stButton > button,
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) .stButton > button {{
    font-size: 12px !important;
    padding: 7px 12px !important;
    min-height: 34px !important;
    width: 100% !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(2) .stButton > button,
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(3) .stButton > button,
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(4) .stButton > button,
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(2) .stButton > button,
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(3) .stButton > button,
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(4) .stButton > button {{
    padding: 5px 10px !important;
    min-height: 30px !important;
  }}
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(5) .stButton > button,
  .main .block-container div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div[data-testid="column"]:nth-child(6) .stButton > button,
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(5) .stButton > button,
  .main .block-container div.row-widget.stHorizontal:nth-of-type(2) > div[data-testid="column"]:nth-child(6) .stButton > button {{
    padding: 5px 12px !important;
    min-width: 38px !important;
    min-height: 30px !important;
  }}

  .jk-projects-grid {{ grid-template-columns: 1fr; }}
  .jk-bubble {{ max-width: 92%; }}
  .jk-welcome {{ padding: 18px 0 12px; }}
  .jk-welcome-sub {{ font-size: 15px; margin-bottom: 24px; }}

  /* Welcome prompts — stack only the grid below the anchor marker */
  .element-container:has(.jk-prompts-grid) + .element-container [data-testid="stHorizontalBlock"],
  .element-container:has(.jk-prompts-grid) + .element-container div.row-widget.stHorizontal {{
    flex-direction: column !important;
  }}
  .element-container:has(.jk-prompts-grid) + .element-container [data-testid="column"] {{
    flex: 1 1 100% !important;
    width: 100% !important;
    max-width: 100% !important;
  }}
}}
"""


def apply_styles(theme: str) -> None:
    css = _escape_css_selectors(build_css(theme))
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def inject_css(theme: str) -> str:
    """Deprecated — use apply_styles(). Kept for compatibility."""
    return f"<style>{_escape_css_selectors(build_css(theme))}</style>"
