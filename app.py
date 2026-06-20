import streamlit as st
import openai
import requests
import json
import re
import time
from typing import Any, Dict, List, Optional

from ui.copy import COPY, THEME_LABELS, session_to_ui_lang
from ui.design_system import apply_styles
from ui.render import (
    render_assistant_bubble,
    render_assistant_projects,
    render_assistant_with_projects,
    render_config_error,
    render_contact_intro,
    render_contact_success,
    render_footer_links,
    render_header_profile,
    render_typing_indicator,
    render_user_bubble,
    render_welcome,
)


def rerun() -> None:
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def notify(message: str) -> None:
    if hasattr(st, "toast"):
        st.toast(message)
    else:
        st.info(message)


st.set_page_config(
    page_title="Jessica Kuijer - Assistant IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://github.com/jessicakuijer/chatbot-portfolio",
        "Report a bug": "https://github.com/jessicakuijer/chatbot-portfolio/issues",
        "About": "# Jessica Kuijer - Assistant IA\n\nAssistant IA personnel avec notifications temps réel",
    },
)

if not hasattr(openai, "OpenAI"):
    st.error(
        "Version incompatible du package `openai` (attendu ≥ 1.3). "
        "Vous utilisez probablement le Python système au lieu du virtualenv du projet.\n\n"
        "Arrêtez le serveur (Ctrl+C), puis lancez :\n\n"
        "`.venv/bin/streamlit run app.py`"
    )
    st.stop()

PROJECT_RE = re.compile(r"(projet|project|r[ée]alis|portfolio|construit|built|vignette)", re.I)
CONTACT_RE = re.compile(
    r"(disponib|dispo|available|recrut|embauch|opportun|contact|email|mail|hire|collabor|joindre|reach|coordonn)",
    re.I,
)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

JESSICA_PROFILE = {
    "name": "Jessica Kuijer",
    "summary": """Je suis Jessica Kuijer, développeuse backend PHP / Python devenue product builder orientée IA. J'aime transformer des idées en produits concrets, utiles et robustes. Originaire de la région parisienne, je vis aujourd'hui en Seine-et-Marne pour un meilleur équilibre entre vie pro et perso (et plus de nature). Je m'intéresse autant à la technique qu'au produit, aux usages et à la valeur réelle pour les utilisateurs. J'intègre l'IA (OpenAI, automatisation, logique métier augmentée) quand elle fait sens — pas juste pour suivre une tendance. Actuellement, je suis ouverte à de nouveaux challenges où je peux allier backend, produit et IA. Mélomane (batterie, concerts, artistes), j'aime aussi partager cette énergie dans ce que je construis. Et détail important : je suis allergique aux kiwis 😄""",
    "linkedin_text": """Jessica Kuijer ♀
Développeuse web backend PHP / Python • Product-minded • Intégration IA
Seine-et-Marne, Île-de-France, France

Résumé
Je transforme des idées en produits web concrets, robustes… et utiles.
Développeuse backend PHP / Python, je conçois des solutions modernes en allant au-delà du code : je m'intéresse au produit, aux usages, et à la valeur réelle pour les utilisateurs.

Aujourd'hui, j'intègre des briques d'IA (OpenAI, automatisation, logique métier augmentée) pour créer des expériences plus intelligentes et efficaces — pas "parce que c'est tendance", mais parce que ça apporte une vraie valeur.

Actuellement, je suis à la recherche d'un nouveau challenge me permettant d'allier backend, vision produit et intégration de l'IA.

Ce qui me drive :
→ comprendre rapidement un contexte métier
→ structurer des solutions simples à partir de problématiques complexes
→ livrer des outils fiables, maintenables et évolutifs

Autodidacte, directe, engagée — j'aime faire avancer les projets et les équipes.

Je suis également mélomane (batterie, concerts, artistes) et j'aime partager cette passion.

Mobilité géographique :
• Île-de-France (déplacements possibles)
• Remote / hybride

Principales compétences
• PHP (Symfony), Python
• Architecture backend, API REST, API Platform
• SQL / PostgreSQL / MySQL / Elasticsearch
• Monorepo (Turborepo), Docker, CI/CD
• Stripe (paiement, SCA), WebSockets
• IA appliquée (OpenAI, automatisation, logique métier augmentée)
• Performance backend, optimisation de requêtes
• Approche produit & UX backend

Technologies complémentaires
• JavaScript, React, VueJS
• Git, GitHub, GitLab
• Méthodologies Agile, Scrum

Ce que je peux rapidement monter en compétences
• Cloud (AWS, GCP), Kubernetes
• Terraform, DevOps avancé
• GraphQL

Langues
• Français (langue maternelle)
• Anglais (professionnel)

Certifications & formations
• Certification OPQUAST - Qualité Web
• The Complete Agentic AI Engineering Course (2025)
• Scrum Developer (Sia)
• MOOC #WomenInDigital
• Fresque du Climat

Expérience Professionnelle

Expériences récentes
Développeuse web backend / Product-oriented
2021 - aujourd'hui
• Conception et développement de solutions web (PHP, Python)
• Intégration de briques IA dans des produits existants
• Approche orientée produit et valeur utilisateur

Sia Experience - Développeuse web backend
mai 2023 - août 2025 | Paris (mission terminée)
• Développement backend (PHP, Python) sur architectures complexes
• APIs REST, authentification JWT, SSO
• WebSockets et temps réel
• Participation à la conception produit et aux choix techniques

Carvivo - Développeuse web
2022
• TMA et évolutions produit sur outil SaaS
• Déploiements, QA, amélioration continue

MINDOZA - Développeuse web
2021 - 2022
• Développement multi-projets (Symfony, React, WordPress)
• APIs, back-offices, Docker

Feedback Lawyers - Développeuse web
2020
• Interface de recherche d'avocats (React + API)

Expérience complémentaire
• Formatrice : HTML, CSS et bases de Git pour des apprenantes chez Les DesCodeuses
• Intervention via Airskill (fondé par Frédéric Lossignol, mentor)

Projets récents
• Assistant IA personnel (inspiré de "Her") avec mémoire, voix et adaptation émotionnelle
• Application de préparation aux entretiens (IA)
• Music Discovery AI
• Projet cybersécurité grand public (diagnostic + assistant IA)
• Contributions produit et techniques sur la plateforme E-Motion (réservation, paiement, back-office, performance)

Approche
Je ne fais pas "juste du développement".
Je conçois des solutions utiles, durables et intelligentes — avec une vraie vision produit.""",
}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "notification_count" not in st.session_state:
    st.session_state.notification_count = 0
if "contact_count" not in st.session_state:
    st.session_state.contact_count = 0
if "current_language" not in st.session_state:
    st.session_state.current_language = "french"
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
if "last_error" not in st.session_state:
    st.session_state.last_error = None
if "theme" not in st.session_state:
    st.session_state.theme = "clair"


def get_openai_model() -> str:
    return st.secrets.get("OPENAI_MODEL", "gpt-5-mini")


def model_supports_temperature(model: str) -> bool:
    return not model.startswith("gpt-5")


def build_api_messages(history: List[Dict]) -> List[Dict]:
    """Strip UI-only fields before sending history to OpenAI."""
    return [
        {"role": m["role"], "content": m["content"]}
        for m in history
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]


def assistant_message_to_dict(message) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"role": "assistant", "content": message.content or ""}
    if message.tool_calls:
        payload["tool_calls"] = [
            {
                "id": tc.id,
                "type": tc.type,
                "function": {"name": tc.function.name, "arguments": tc.function.arguments},
            }
            for tc in message.tool_calls
        ]
    return payload


def create_chat_completion(client, messages: List[Dict], *, tools=None, temperature: float = 0.7):
    model = get_openai_model()
    params: Dict[str, Any] = {"model": model, "messages": messages}
    if tools is not None:
        params["tools"] = tools
    if model_supports_temperature(model):
        params["temperature"] = temperature
    return client.chat.completions.create(**params)

tools = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Utilise cet outil pour enregistrer qu'un utilisateur est intéressé par Jessica et a fourni son email",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "L'adresse email de l'utilisateur"},
                    "name": {"type": "string", "description": "Le nom de l'utilisateur, s'il l'a fourni"},
                    "phone": {"type": "string", "description": "Le numéro de téléphone de l'utilisateur, s'il l'a fourni"},
                    "notes": {
                        "type": "string",
                        "description": "Informations importantes: type de projet, budget, timeline, compétences recherchées, etc.",
                    },
                },
                "required": ["email"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "record_unknown_question",
            "description": "Utilise TOUJOURS cet outil pour enregistrer toute question à laquelle tu n'as pas pu répondre",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "La question à laquelle tu n'as pas pu répondre"}
                },
                "required": ["question"],
                "additionalProperties": False,
            },
        },
    },
]


def is_projects_query(text: str) -> bool:
    return bool(PROJECT_RE.search(text or ""))


def is_contact_query(text: str) -> bool:
    return bool(CONTACT_RE.search(text or "")) and not re.search(r"kiwi", text or "", re.I)


def send_pushover_notification(message: str, pushover_user: str, pushover_token: str) -> bool:
    if not pushover_user or not pushover_token:
        return False
    try:
        payload = {
            "user": pushover_user,
            "token": pushover_token,
            "message": message,
            "title": "🤖 Jessica Kuijer - Assistant IA",
            "priority": 0,
            "sound": "pushover",
        }
        response = requests.post("https://api.pushover.net/1/messages.json", data=payload, timeout=10)
        if response.status_code == 200:
            st.session_state.notification_count += 1
            return True
        if st.session_state.get("_show_pushover_ui", True):
            st.error(f"Erreur Pushover: {response.status_code} - {response.text}")
        return False
    except requests.exceptions.Timeout:
        if st.session_state.get("_show_pushover_ui", True):
            st.error("Timeout lors de l'envoi de la notification Pushover")
        return False
    except Exception as e:
        if st.session_state.get("_show_pushover_ui", True):
            st.error(f"Erreur Pushover : {str(e)}")
        return False


def record_user_details(
    email: str,
    name: str = "Nom non fourni",
    phone: str = "Non fourni",
    notes: str = "Aucune note",
    show_ui: bool = True,
):
    pushover_user = st.session_state.get("pushover_user")
    pushover_token = st.session_state.get("pushover_token")
    phone_info = f"📱 Téléphone: {phone}" if phone and phone != "Non fourni" else "📱 Téléphone: Non fourni"
    message = f"""📧 NOUVEAU CONTACT pour Jessica !

👤 Nom: {name}
📧 Email: {email}
{phone_info}
📝 Notes: {notes}

🌐 Via: Jessica Kuijer Assistant IA
⏰ {time.strftime('%d/%m/%Y à %H:%M')}"""
    if pushover_user and pushover_token:
        st.session_state._show_pushover_ui = show_ui
        success = send_pushover_notification(message, pushover_user, pushover_token)
        st.session_state._show_pushover_ui = True
        if success:
            st.session_state.contact_count += 1
            if show_ui:
                st.success("✅ Jessica sera notifiée sur son téléphone !")
            return {"recorded": "ok", "message": "Contact enregistré avec succès"}
        if show_ui:
            st.warning("⚠️ Contact enregistré mais notification échouée")
        return {"recorded": "partial", "message": "Contact enregistré, notification échouée"}
    if show_ui:
        st.info("💾 Contact enregistré (pas de notification configurée)")
    return {"recorded": "ok", "message": "Contact enregistré localement"}


def record_unknown_question(question: str):
    pushover_user = st.session_state.get("pushover_user")
    pushover_token = st.session_state.get("pushover_token")
    message = f"""❓ QUESTION NON RÉSOLUE pour Jessica !

🤔 Question: {question}

💡 Suggestion: Jessica devrait enrichir son profil avec cette information.

🌐 Via: Jessica Kuijer Assistant IA
⏰ {time.strftime('%d/%m/%Y à %H:%M')}"""
    if pushover_user and pushover_token:
        success = send_pushover_notification(message, pushover_user, pushover_token)
        if success and st.session_state.get("_show_pushover_ui", True):
            st.info("📱 Jessica sera notifiée pour améliorer son profil")
        return {"recorded": "ok", "message": "Question enregistrée pour amélioration"}
    if st.session_state.get("_show_pushover_ui", True):
        st.info("💾 Question enregistrée localement")
    return {"recorded": "ok", "message": "Question enregistrée localement"}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        try:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            if tool_name == "record_user_details":
                result = record_user_details(**arguments, show_ui=False)
                result["message_for_ai"] = (
                    "Contact enregistré avec succès. Vous pouvez maintenant répondre à la question de l'utilisateur."
                )
            elif tool_name == "record_unknown_question":
                result = record_unknown_question(**arguments)
                result["message_for_ai"] = (
                    "Question enregistrée pour amélioration. Expliquez poliment que vous n'avez pas cette information mais que vous l'avez notée."
                )
            else:
                result = {"error": f"Outil {tool_name} non reconnu"}
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        except Exception as e:
            st.error(f"Erreur dans l'exécution de l'outil {tool_call.function.name}: {str(e)}")
            results.append(
                {"role": "tool", "content": json.dumps({"error": str(e)}), "tool_call_id": tool_call.id}
            )
    return results


def translate_profile_to_english(profile: dict, openai_client) -> dict:
    try:
        text_to_translate = f"""
Nom: {profile['name']}
Résumé: {profile['summary']}

Profil LinkedIn:
{profile['linkedin_text']}
        """.strip()
        response = create_chat_completion(
            openai_client,
            [
                {
                    "role": "system",
                    "content": (
                        "Tu es un traducteur professionnel français-anglais. Traduis le profil de Jessica Kuijer "
                        "en anglais en gardant le style professionnel et authentique. Retourne la traduction au "
                        "format JSON avec les clés 'name', 'summary', et 'linkedin_text'."
                    ),
                },
                {"role": "user", "content": f"Traduis ce profil en anglais: {text_to_translate}"},
            ],
            temperature=0.3,
        )
        translated_content = response.choices[0].message.content
        if translated_content.strip().startswith("{"):
            return json.loads(translated_content)
        return {"name": profile["name"], "summary": translated_content, "linkedin_text": translated_content}
    except Exception as e:
        st.error(f"Erreur lors de la traduction: {str(e)}")
        return profile


def create_system_prompt(language: str = "french", openai_client=None) -> str:
    profile = JESSICA_PROFILE
    contact_linkedin = st.secrets.get("CONTACT_LINKEDIN", "https://www.linkedin.com/in/jessicakuijer/")
    if language == "english":
        if openai_client:
            try:
                profile = translate_profile_to_english(profile, openai_client)
            except Exception as e:
                st.warning(f"⚠️ Impossible de traduire le profil en anglais: {str(e)}")
        return f"""You are Jessica Kuijer, a backend web developer specialized in PHP (Symfony) and Python, evolving into a product-oriented AI builder. You represent Jessica on her personal website and answer questions about her career, skills, and experience.

IMPORTANT INSTRUCTIONS:
- You ARE Jessica Kuijer, speak in first person ("I am", "My experience", "My skills")
- Be professional, warm, and engaging
- Respond in English
- If you don't know the answer to a question, ALWAYS use the record_unknown_question tool, then politely explain that you don't have this information but have noted it for improvement
- If the user seems interested in collaboration or leaves their email, use record_user_details, then continue answering their question or ask for more details about their project
- If the user seems to have a job opening or talks to me about a project, then ask for their email, phone number (if possible) and information about the position or project, use record_user_details, then continue the conversation about the opportunity
- IMPORTANT: After using any tool, ALWAYS continue the conversation naturally - don't stop there!
- Highlight your evolution from developer to product builder, your ability to design useful solutions, and your use of AI when it brings real value
- Don't hesitate to mention your passion for building meaningful products, your interest in cybersecurity and user protection, and your aversion to kiwis if relevant!
- IMPORTANT: NEVER say that you are freelancing or working as a freelancer. If asked about your current situation, say that you are open to new opportunities or looking for new challenges, without mentioning freelance work.

PROFESSIONAL CONTACT:
- Professional email: {contact_linkedin}
- You can give this information if someone wants to contact you directly

YOUR PROFILE:
Name: {profile['name']}
Personal summary: {profile['summary']}

COMPLETE LINKEDIN PROFILE:
{profile['linkedin_text']}

RECENT PROJECTS TO MENTION:
- Personal AI Assistant (inspired by "Her") combining OpenAI and Claude with emotional/contextual routing and adaptive behavior
- Interview preparation application with AI (Streamlit + OpenAI)
- Music Discovery AI (Spotify API + OpenAI + YouTube API)
- E-Motion platform: beyond backend development, involvement in product thinking, architecture (monorepo, API Platform), performance, payments (Stripe), and user experience improvements
- Cybersecurity awareness project: interactive diagnostic test, accessible educational content, and AI assistant to help users protect themselves
- Teaching experience: HTML, CSS, and Git basics for learners at "Les DesCodeuses", through Airskill (founded by Frédéric Lossignol)
- Various web and AI-powered solutions in PHP/Symfony and Python for clients

With this context, discuss naturally with the user while remaining Jessica Kuijer. Be authentic, product-driven, and focused on creating meaningful impact."""

    return f"""Tu es Jessica Kuijer, développeuse web backend spécialisée en PHP (Symfony) et Python, en évolution vers un rôle de product builder orienté IA. Tu représentes Jessica sur son site web personnel et tu réponds aux questions concernant sa carrière, ses compétences et son expérience.

INSTRUCTIONS IMPORTANTES :
- Tu ES Jessica Kuijer, parle à la première personne ("Je suis", "Mon expérience", "Mes compétences")
- Sois professionnelle, chaleureuse et engageante
- Réponds en français mais si l'utilisateur te demande de répondre en anglais alors reprends JESSICA_PROFILE en traduisant en anglais l'intégralité du texte et réponds en anglais
- Si tu ne connais pas la réponse à une question, utilise OBLIGATOIREMENT l'outil record_unknown_question, puis explique poliment que tu n'as pas cette information mais que tu l'as notée pour amélioration
- Si l'utilisateur semble intéressé par une collaboration ou laisse son email, utilise record_user_details, puis continue à répondre à sa question ou demande plus de détails sur son projet
- Si l'utilisateur semble avoir un poste à pourvoir ou me parler d'un projet, alors demande lui son email, son téléphone (si possible) et des informations sur le poste ou le projet, utilise record_user_details, puis continue la conversation sur l'opportunité
- IMPORTANT : Après avoir utilisé un outil, CONTINUE TOUJOURS la conversation naturellement - ne t'arrête pas là !
- Mets en avant ton évolution de développeuse vers product builder, ta capacité à concevoir des solutions utiles et ton usage de l'IA quand elle apporte une vraie valeur
- N'hésite pas à mentionner ton intérêt pour la cybersécurité, la protection des utilisateurs, et ton aversion pour les kiwis si c'est pertinent !
- IMPORTANT : Ne dis JAMAIS que tu es freelance ou indépendante. Si on te pose la question sur ta situation actuelle, réponds que tu es à l'écoute de nouvelles opportunités ou en recherche de nouveaux challenges, sans mentionner de statut freelance.

CONTACT PROFESSIONNEL :
- Email professionnel : {contact_linkedin}
- LinkedIn : {contact_linkedin}
- Tu peux donner cette information si quelqu'un veut te contacter directement

TON PROFIL :
Nom : {profile['name']}
Résumé personnel : {profile['summary']}

PROFIL LINKEDIN COMPLET :
{profile['linkedin_text']}

PROJETS RÉCENTS À MENTIONNER :
- Assistant IA personnel inspiré du film "Her" (OpenAI + Claude, routing émotionnel, comportement adaptatif)
- Application de préparation aux entretiens avec IA (Streamlit + OpenAI)
- Music Discovery AI (Spotify API + OpenAI + YouTube API)
- Plateforme E-Motion : contribution au-delà du backend (vision produit, architecture monorepo, API Platform, Stripe, optimisation des performances et UX)
- Projet cybersécurité grand public : test interactif, guide accessible et assistant IA
- Expérience de formation : cours HTML, CSS et bases de Git pour des apprenantes chez "Les DesCodeuses", via Airskill (fondé par Frédéric Lossignol)
- Diverses solutions web et IA en PHP/Symfony et Python pour mes clients

Avec ce contexte, discute naturellement avec l'utilisateur en restant Jessica Kuijer. Sois authentique, orientée produit et tournée vers l'impact."""


def detect_language_switch(text: str) -> Optional[str]:
    english_keywords = [
        "english", "anglais", "speak english", "parle anglais", "réponds en anglais",
        "can you speak english", "peux-tu parler anglais", "in english", "en anglais",
        "switch to english", "passe en anglais", "change language", "change de langue",
    ]
    french_keywords = [
        "french", "français", "speak french", "parle français", "réponds en français",
        "can you speak french", "peux-tu parler français", "en français", "switch to french",
    ]
    lower = text.lower()
    if any(k in lower for k in english_keywords):
        return "english"
    if any(k in lower for k in french_keywords):
        return "french"
    return None


def queue_user_message(text: str):
    if not text or not text.strip() or st.session_state.is_processing:
        return
    st.session_state.chat_history.append({"role": "user", "content": text.strip()})
    st.session_state.is_processing = True


def append_contact_card():
    lang = session_to_ui_lang(st.session_state.current_language)
    t = COPY[lang]
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": t["contactIntro"],
            "kind": "contact",
            "contact_submitted": False,
        }
    )


def reset_conversation():
    st.session_state.chat_history = []
    st.session_state.is_processing = False
    st.session_state.last_error = None


def process_openai_response(openai_api_key: str, user_input: str):
    lang = session_to_ui_lang(st.session_state.current_language)
    t = COPY[lang]
    language = st.session_state.current_language
    switch = detect_language_switch(user_input)
    if switch == "english":
        language = "english"
        st.session_state.current_language = "english"
        notify(t["langSwitchEn"])
    elif switch == "french":
        language = "french"
        st.session_state.current_language = "french"
        notify(t["langSwitchFr"])

    client = openai.OpenAI(api_key=openai_api_key)
    messages = [
        {"role": "system", "content": create_system_prompt(language, client)},
        *build_api_messages(st.session_state.chat_history),
    ]
    done = False
    max_iterations = 5
    iteration = 0
    assistant_response = None
    st.session_state.last_error = None

    while not done and iteration < max_iterations:
        iteration += 1
        response = create_chat_completion(client, messages, tools=tools, temperature=0.7)
        finish_reason = response.choices[0].finish_reason
        if finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_results = handle_tool_calls(message.tool_calls)
            messages.append(assistant_message_to_dict(message))
            messages.extend(tool_results)
            continue
        assistant_response = response.choices[0].message.content
        done = True

    if iteration >= max_iterations:
        st.session_state.last_error = "Conversation interrompue après trop d'itérations."

    if assistant_response:
        msg: Dict[str, Any] = {"role": "assistant", "content": assistant_response, "kind": "text"}
        if is_projects_query(user_input):
            msg["show_projects"] = True
        st.session_state.chat_history.append(msg)
    elif not st.session_state.last_error:
        fallback = (
            "Désolée, je n'ai pas pu répondre pour le moment. Réessayez dans un instant."
            if language == "french"
            else "Sorry, I couldn't reply just now. Please try again in a moment."
        )
        st.session_state.chat_history.append({"role": "assistant", "content": fallback, "kind": "text"})

    if is_contact_query(user_input):
        has_open_contact = any(
            m.get("kind") == "contact" and not m.get("contact_submitted")
            for m in st.session_state.chat_history
        )
        if not has_open_contact:
            append_contact_card()


def render_header(t: dict, has_chat: bool):
    """Header on two rows — Streamlit columns cannot nest."""
    row1 = st.columns([1.7, 1.05, 1.15])
    with row1[0]:
        st.markdown(render_header_profile(t["name"], t["status"]), unsafe_allow_html=True)
    with row1[1]:
        if st.button(f"✉ {t['contactBtn']}", key="btn_contact", type="primary"):
            append_contact_card()
            rerun()
    with row1[2]:
        if has_chat and st.button(f"↻ {t['reset']}", key="btn_reset"):
            reset_conversation()
            rerun()

    row2 = st.columns([1.4, 0.95, 0.95, 1.15, 0.62, 0.62])
    with row2[0]:
        pass
    for col, theme_key in zip(row2[1:4], ["clair", "sombre", "editorial"]):
        with col:
            if st.button(
                THEME_LABELS[theme_key],
                key=f"theme_{theme_key}",
                type="primary" if st.session_state.theme == theme_key else "secondary",
            ):
                st.session_state.theme = theme_key
                rerun()
    with row2[4]:
        if st.button(
            "FR",
            key="lang_fr",
            type="primary" if st.session_state.current_language == "french" else "secondary",
        ):
            st.session_state.current_language = "french"
            rerun()
    with row2[5]:
        if st.button(
            "EN",
            key="lang_en",
            type="primary" if st.session_state.current_language == "english" else "secondary",
        ):
            st.session_state.current_language = "english"
            rerun()


def render_chat_messages(t: dict):
    for idx, message in enumerate(st.session_state.chat_history):
        role = message.get("role")
        if role == "user":
            st.markdown(render_user_bubble(message["content"]), unsafe_allow_html=True)
            continue

        if role != "assistant":
            continue

        kind = message.get("kind", "text")
        if kind == "contact":
            st.markdown(render_contact_intro(message["content"]), unsafe_allow_html=True)
            if message.get("contact_submitted"):
                email = message.get("contact_email", "")
                done_msg = f"{t['contactDonePrefix']}{email}."
                st.markdown(render_contact_success(t["contactDoneTitle"], done_msg), unsafe_allow_html=True)
            else:
                with st.form(key=f"contact_form_{idx}"):
                    st.markdown(f"**{t['contactFormTitle']}**")
                    name = st.text_input(t["fName"], key=f"c_name_{idx}")
                    email = st.text_input(t["fEmail"], key=f"c_email_{idx}")
                    phone = st.text_input(t["fPhone"], key=f"c_phone_{idx}")
                    notes = st.text_area(t["fMsg"], key=f"c_msg_{idx}", height=68)
                    submitted = st.form_submit_button(t["fSubmit"], use_container_width=True)
                    if submitted:
                        if not EMAIL_RE.match((email or "").strip()):
                            st.error(t["contactErrorEmail"])
                        else:
                            record_user_details(
                                email=email.strip(),
                                name=name.strip() or "Nom non fourni",
                                phone=phone.strip() or "Non fourni",
                                notes=notes.strip() or "Aucune note",
                                show_ui=False,
                            )
                            st.session_state.chat_history[idx]["contact_submitted"] = True
                            st.session_state.chat_history[idx]["contact_email"] = email.strip()
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": t["contactThanks"], "kind": "text"}
                            )
                            rerun()
            continue

        if kind == "projects":
            st.markdown(render_assistant_projects(message["content"], t["projects"]), unsafe_allow_html=True)
        elif message.get("show_projects"):
            st.markdown(render_assistant_with_projects(message["content"], t["projects"]), unsafe_allow_html=True)
        else:
            st.markdown(render_assistant_bubble(message["content"]), unsafe_allow_html=True)


def render_composer(t: dict) -> Optional[str]:
    """Message input compatible with Streamlit versions without st.chat_input."""
    disabled = st.session_state.is_processing
    with st.form("jk_composer", clear_on_submit=True):
        col_input, col_send = st.columns([11, 1])
        with col_input:
            user_text = st.text_input(
                "message",
                placeholder=t["placeholder"],
                label_visibility="collapsed",
                disabled=disabled,
            )
        with col_send:
            submitted = st.form_submit_button("↑", use_container_width=True, disabled=disabled)
    if submitted and user_text and user_text.strip():
        return user_text.strip()
    return None


def render_welcome_prompts(t: dict):
    st.markdown(
        render_welcome(t["greetingLine1"], t["greetingSub"], t["promptsTitle"]),
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, prompt in enumerate(t["prompts"]):
        with cols[i % 2]:
            if st.button(f"{prompt}  ↗", key=f"prompt_{i}", use_container_width=True):
                queue_user_message(prompt)
                rerun()


# --- App bootstrap ---
apply_styles(st.session_state.theme)

try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    pushover_user = st.secrets["PUSHOVER_USER"]
    pushover_token = st.secrets["PUSHOVER_TOKEN"]
    st.session_state.pushover_user = pushover_user
    st.session_state.pushover_token = pushover_token
    secrets_loaded = True
except KeyError:
    openai_api_key = ""
    secrets_loaded = False

ui_lang = session_to_ui_lang(st.session_state.current_language)
t = COPY[ui_lang]
has_chat = len(st.session_state.chat_history) > 0

# Header
render_header(t, has_chat)

if not secrets_loaded:
    st.markdown(
        render_config_error(t["configErrorTitle"], t["configErrorBody"], t["configErrorSecrets"], t["configErrorContact"]),
        unsafe_allow_html=True,
    )
else:
    if st.session_state.last_error:
        st.error(st.session_state.last_error)

    if not has_chat and not st.session_state.is_processing:
        render_welcome_prompts(t)
    else:
        render_chat_messages(t)
        if st.session_state.is_processing:
            st.markdown(render_typing_indicator(), unsafe_allow_html=True)

    if (
        st.session_state.is_processing
        and st.session_state.chat_history
        and st.session_state.chat_history[-1]["role"] == "user"
    ):
        user_input = st.session_state.chat_history[-1]["content"]
        try:
            process_openai_response(openai_api_key, user_input)
        except openai.OpenAIError as e:
            st.session_state.last_error = f"Erreur OpenAI : {str(e)}"
        except Exception as e:
            st.session_state.last_error = f"Erreur lors de la conversation : {str(e)}"
        finally:
            st.session_state.is_processing = False
            rerun()

if secrets_loaded:
    chat_input = render_composer(t)
    st.markdown(f'<div class="jk-disclaimer">{t["disclaimer"]}</div>', unsafe_allow_html=True)
    contact_linkedin = st.secrets.get("CONTACT_LINKEDIN", "https://www.linkedin.com/in/jessicakuijer/")
    portfolio_url = st.secrets.get("PORTFOLIO_URL", "https://jessicakuijer.com")
    st.markdown(render_footer_links(contact_linkedin, portfolio_url), unsafe_allow_html=True)

    if chat_input:
        queue_user_message(chat_input)
        rerun()
