"""HTML render helpers for the Jessica IA assistant UI."""

import html
from typing import Any, Dict, List, Optional


def esc(text: Any) -> str:
    return html.escape(str(text)) if text is not None else ""


def render_header_profile(name: str, status: str) -> str:
    return f"""
<div class="jk-profile">
  <div class="jk-avatar-wrap">
    <div class="jk-avatar">JK</div>
    <span class="jk-online"></span>
  </div>
  <div>
    <div class="jk-profile-name">{esc(name)}</div>
    <div class="jk-profile-status">{esc(status)}</div>
  </div>
</div>
"""


def render_welcome(greeting: str, subtitle: str, prompts_title: str) -> str:
    return f"""
<div class="jk-welcome">
  <div class="jk-avatar jk-avatar-lg">JK</div>
  <h1>{esc(greeting)}</h1>
  <p class="jk-welcome-sub">{esc(subtitle)}</p>
  <div style="width:100%;max-width:600px;">
    <div class="jk-prompts-title">{esc(prompts_title)}</div>
  </div>
</div>
"""


def render_user_bubble(content: str) -> str:
    return f"""
<div class="jk-msg-row user">
  <div class="jk-bubble user">{esc(content)}</div>
</div>
"""


def render_assistant_bubble(content: str, *, card: bool = False) -> str:
    card_class = " card" if card else ""
    return f"""
<div class="jk-msg-row assistant{' card' if card else ''}">
  <div class="jk-avatar jk-avatar-sm">JK</div>
  <div class="jk-bubble assistant{card_class}">{esc(content)}</div>
</div>
"""


def render_projects_cards(projects: List[Dict[str, str]]) -> str:
    cards = []
    for p in projects:
        cards.append(f"""
<div class="jk-project-card">
  <div class="jk-project-head">
    <div class="jk-project-mono">{esc(p['mono'])}</div>
    <span class="jk-project-tag">{esc(p['tag'])}</span>
  </div>
  <div class="jk-project-title">{esc(p['title'])}</div>
  <div class="jk-project-desc">{esc(p['desc'])}</div>
</div>
""")
    grid = "".join(cards)
    return f'<div class="jk-projects-grid">{grid}</div>'


def render_assistant_projects(intro: str, projects: List[Dict[str, str]]) -> str:
    return f"""
<div class="jk-msg-row assistant card">
  <div class="jk-avatar jk-avatar-sm">JK</div>
  <div>
    <div class="jk-bubble assistant card">{esc(intro)}</div>
    {render_projects_cards(projects)}
  </div>
</div>
"""


def render_assistant_with_projects(content: str, projects: List[Dict[str, str]]) -> str:
    return f"""
<div class="jk-msg-row assistant card">
  <div class="jk-avatar jk-avatar-sm">JK</div>
  <div>
    <div class="jk-bubble assistant card">{esc(content)}</div>
    {render_projects_cards(projects)}
  </div>
</div>
"""


def render_contact_intro(content: str) -> str:
    return f"""
<div class="jk-msg-row assistant card">
  <div class="jk-avatar jk-avatar-sm">JK</div>
  <div>
    <div class="jk-bubble assistant card">{esc(content)}</div>
  </div>
</div>
"""


def render_contact_success(title: str, message: str) -> str:
    return f"""
<div class="jk-contact-card">
  <div class="jk-contact-success">
    <div class="jk-contact-check">✓</div>
    <div class="jk-contact-done-title">{esc(title)}</div>
    <div class="jk-contact-done-msg">{esc(message)}</div>
  </div>
</div>
"""


def render_typing_indicator() -> str:
    return """
<div class="jk-typing-row">
  <div class="jk-avatar jk-avatar-sm">JK</div>
  <div class="jk-typing-bubble">
    <span class="jk-dot jk-dot-1"></span>
    <span class="jk-dot jk-dot-2"></span>
    <span class="jk-dot jk-dot-3"></span>
  </div>
</div>
"""


def render_config_error(title: str, body: str, secrets: str, contact: str) -> str:
    return f"""
<div class="jk-error-panel">
  <h3>⚠️ {esc(title)}</h3>
  <p>{esc(body)}</p>
  <p><strong>{esc(secrets)}</strong></p>
  <p>{esc(contact)}</p>
</div>
"""


def render_footer_links(linkedin: str, portfolio: str) -> str:
    return f"""
<div class="jk-footer-links">
  <a href="{esc(linkedin)}" target="_blank">LinkedIn</a>
  ·
  <a href="{esc(portfolio)}" target="_blank">Portfolio</a>
</div>
"""
