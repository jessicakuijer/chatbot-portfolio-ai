import streamlit as st
import openai
import requests
import json
import os
from typing import List, Dict, Optional
import time
from pypdf import PdfReader  # Import ajouté

# Configuration de la page
st.set_page_config(
    page_title="Jessica Kuijer - Assistant IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/jessicakuijer/chatbot-portfolio',
        'Report a bug': "https://github.com/jessicakuijer/chatbot-portfolio/issues",
        'About': "# 🤖 Jessica Kuijer - Assistant IA\n\nAssistant IA personnel avec notifications temps réel"
    }
)

# Forcer le thème clair pour une meilleure lisibilité
st.markdown("""
<style>
    /* Forcer le thème clair */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* S'assurer que le texte est lisible */
    .stMarkdown, .stText, .stTextInput, .stTextArea {
        color: #000000 !important;
    }
    
    /* Forcer les couleurs de fond des messages */
    .message-user {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    
    .message-assistant {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* Améliorer la lisibilité des éléments Streamlit */
    .stButton > button {
        color: #000000 !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #d0d0d0 !important;
    }
    
    .stButton > button:hover {
        background-color: #e0e2e6 !important;
    }
</style>
""", unsafe_allow_html=True)

# CSS personnalisé unique
st.markdown("""
<style>
    /* Forcer le thème clair global */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* En-tête principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Conteneur de chat */
    .chat-container {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        color: #000000;
    }
    
    /* Cartes de notification */
    .notification-card {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        color: #155724;
    }
    
    /* Messages utilisateur */
    .message-user {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: 20%;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    /* Messages assistant */
    .message-assistant {
        background: #ffffff;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-right: 20%;
        border-left: 3px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #000000;
        border: 1px solid #e0e0e0;
    }
    
    /* Messages d'outils */
    .message-tool {
        background: #fff3cd;
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        border-left: 3px solid #ffc107;
        font-size: 0.9rem;
        font-style: italic;
        color: #856404;
    }
    
    /* Profil chargé */
    .profile-loaded {
        background: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        color: #155724;
    }
    
    /* Boîtes d'erreur */
    .error-box {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
        color: #721c24;
    }
    
    /* Boîtes de succès */
    .success-box {
        background: #d1ecf1;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
        color: #0c5460;
    }
    
    /* Améliorer la lisibilité des éléments Streamlit */
    .stMarkdown, .stText, .stTextInput, .stTextArea {
        color: #000000 !important;
    }
    
    .stButton > button {
        color: #000000 !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #d0d0d0 !important;
    }
    
    .stButton > button:hover {
        background-color: #e0e2e6 !important;
    }
    
    /* Forcer les couleurs de fond */
    .stApp > div:first-child {
        background-color: #ffffff !important;
    }
    
    /* Améliorer la sidebar */
    .css-1d391kg {
        background-color: #f8f9fa !important;
    }
    
    /* Forcer les couleurs de texte */
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Données de Jessica - VERSION PUBLIQUE
JESSICA_PROFILE = {
    "name": "Jessica Kuijer",
    "summary": """Je suis Jessica Kuijer, développeuse backend PHP / Python devenue product builder orientée IA. J’aime transformer des idées en produits concrets, utiles et robustes. Originaire de la région parisienne, je vis aujourd’hui en Seine-et-Marne pour un meilleur équilibre entre vie pro et perso (et plus de nature). Je m’intéresse autant à la technique qu’au produit, aux usages et à la valeur réelle pour les utilisateurs. J’intègre l’IA (OpenAI, automatisation, logique métier augmentée) quand elle fait sens — pas juste pour suivre une tendance. Actuellement, je suis ouverte à de nouveaux challenges où je peux allier backend, produit et IA. Mélomane (batterie, concerts, artistes), j’aime aussi partager cette énergie dans ce que je construis. Et détail important : je suis allergique aux kiwis 😄""",
    
    "linkedin_text": """Jessica Kuijer ♀
Développeuse web backend PHP / Python • Product-minded • Intégration IA
Seine-et-Marne, Île-de-France, France

Résumé
Je transforme des idées en produits web concrets, robustes… et utiles.
Développeuse backend PHP / Python, je conçois des solutions modernes en allant au-delà du code : je m’intéresse au produit, aux usages, et à la valeur réelle pour les utilisateurs.

Aujourd’hui, j’intègre des briques d’IA (OpenAI, automatisation, logique métier augmentée) pour créer des expériences plus intelligentes et efficaces — pas “parce que c’est tendance”, mais parce que ça apporte une vraie valeur.

Actuellement, je suis à la recherche d’un nouveau challenge me permettant d’allier backend, vision produit et intégration de l’IA.

Ce qui me drive :
→ comprendre rapidement un contexte métier  
→ structurer des solutions simples à partir de problématiques complexes  
→ livrer des outils fiables, maintenables et évolutifs  

Autodidacte, directe, engagée — j’aime faire avancer les projets et les équipes.

Je suis également mélomane (batterie, concerts, artistes) et j’aime partager cette passion.

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
2021 - aujourd’hui
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
• Interface de recherche d’avocats (React + API)

Expérience complémentaire
• Formatrice : HTML, CSS et bases de Git pour des apprenantes chez Les DesCodeuses  
• Intervention via Airskill (fondé par Frédéric Lossignol, mentor)

Projets récents
• Assistant IA personnel (inspiré de “Her”) avec mémoire, voix et adaptation émotionnelle  
• Application de préparation aux entretiens (IA)  
• Music Discovery AI  
• Projet cybersécurité grand public (diagnostic + assistant IA)  
• Contributions produit et techniques sur la plateforme E-Motion (réservation, paiement, back-office, performance)

Approche
Je ne fais pas “juste du développement”.
Je conçois des solutions utiles, durables et intelligentes — avec une vraie vision produit."""
}

# Initialisation du session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'notification_count' not in st.session_state:
    st.session_state.notification_count = 0
if 'contact_count' not in st.session_state:
    st.session_state.contact_count = 0
if 'current_language' not in st.session_state:
    st.session_state.current_language = "french"
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False

def send_pushover_notification(message: str, pushover_user: str, pushover_token: str):
    """Envoie une notification Pushover avec gestion d'erreurs améliorée"""
    if not pushover_user or not pushover_token:
        return False
        
    try:
        payload = {
            "user": pushover_user,
            "token": pushover_token,
            "message": message,
            "title": "🤖 Jessica Kuijer - Assistant IA",
            "priority": 0,
            "sound": "pushover"
        }
        response = requests.post("https://api.pushover.net/1/messages.json", data=payload, timeout=10)
        
        if response.status_code == 200:
            st.session_state.notification_count += 1
            return True
        else:
            st.error(f"Erreur Pushover: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        st.error("Timeout lors de l'envoi de la notification Pushover")
        return False
    except Exception as e:
        st.error(f"Erreur Pushover : {str(e)}")
        return False

def record_user_details(email: str, name: str = "Nom non fourni", phone: str = "Non fourni", notes: str = "Aucune note"):
    """Enregistre les détails d'un utilisateur intéressé"""
    pushover_user = st.session_state.get('pushover_user')
    pushover_token = st.session_state.get('pushover_token')
    
    # Formater le message avec le téléphone si fourni
    phone_info = f"📱 Téléphone: {phone}" if phone and phone != "Non fourni" else "📱 Téléphone: Non fourni"
    
    message = f"""📧 NOUVEAU CONTACT pour Jessica !

👤 Nom: {name}
📧 Email: {email}
{phone_info}
📝 Notes: {notes}

🌐 Via: Jessica Kuijer Assistant IA
⏰ {time.strftime('%d/%m/%Y à %H:%M')}"""
    
    if pushover_user and pushover_token:
        success = send_pushover_notification(message, pushover_user, pushover_token)
        if success:
            st.session_state.contact_count += 1
            st.success("✅ Jessica sera notifiée sur son téléphone !")
            return {"recorded": "ok", "message": "Contact enregistré avec succès"}
        else:
            st.warning("⚠️ Contact enregistré mais notification échouée")
            return {"recorded": "partial", "message": "Contact enregistré, notification échouée"}
    else:
        st.info("💾 Contact enregistré (pas de notification configurée)")
        return {"recorded": "ok", "message": "Contact enregistré localement"}

def record_unknown_question(question: str):
    """Enregistre une question à laquelle l'IA n'a pas pu répondre"""
    pushover_user = st.session_state.get('pushover_user')
    pushover_token = st.session_state.get('pushover_token')
    
    message = f"""❓ QUESTION NON RÉSOLUE pour Jessica !

🤔 Question: {question}

💡 Suggestion: Jessica devrait enrichir son profil avec cette information.

🌐 Via: Jessica Kuijer Assistant IA
⏰ {time.strftime('%d/%m/%Y à %H:%M')}"""
    
    if pushover_user and pushover_token:
        success = send_pushover_notification(message, pushover_user, pushover_token)
        if success:
            st.info("📱 Jessica sera notifiée pour améliorer son profil")
        return {"recorded": "ok", "message": "Question enregistrée pour amélioration"}
    else:
        st.info("💾 Question enregistrée localement")
        return {"recorded": "ok", "message": "Question enregistrée localement"}

# Définition des tools OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Utilise cet outil pour enregistrer qu'un utilisateur est intéressé par Jessica et a fourni son email",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "L'adresse email de l'utilisateur"
                    },
                    "name": {
                        "type": "string",
                        "description": "Le nom de l'utilisateur, s'il l'a fourni"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Le numéro de téléphone de l'utilisateur, s'il l'a fourni"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Informations importantes: type de projet, budget, timeline, compétences recherchées, etc."
                    }
                },
                "required": ["email"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_unknown_question",
            "description": "Utilise TOUJOURS cet outil pour enregistrer toute question à laquelle tu n'as pas pu répondre",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "La question à laquelle tu n'as pas pu répondre"
                    }
                },
                "required": ["question"],
                "additionalProperties": False
            }
        }
    }
]

def handle_tool_calls(tool_calls):
    """Gère les appels d'outils de l'IA avec gestion d'erreurs"""
    results = []
    for tool_call in tool_calls:
        try:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            # Dispatch des fonctions
            if tool_name == "record_user_details":
                result = record_user_details(**arguments)
                # Message informatif pour l'IA
                result["message_for_ai"] = "Contact enregistré avec succès. Vous pouvez maintenant répondre à la question de l'utilisateur."
            elif tool_name == "record_unknown_question":
                result = record_unknown_question(**arguments)
                # Message informatif pour l'IA
                result["message_for_ai"] = "Question enregistrée pour amélioration. Expliquez poliment que vous n'avez pas cette information mais que vous l'avez notée."
            else:
                result = {"error": f"Outil {tool_name} non reconnu"}
            
            # Créer le message d'outil avec le bon format OpenAI
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
            
        except Exception as e:
            st.error(f"Erreur dans l'exécution de l'outil {tool_call.function.name}: {str(e)}")
            results.append({
                "role": "tool",
                "content": json.dumps({"error": str(e)}),
                "tool_call_id": tool_call.id
            })
    
    return results

def translate_profile_to_english(profile: dict, openai_client) -> dict:
    """Traduit le profil Jessica en anglais en utilisant l'API OpenAI"""
    try:
        # Préparer le texte à traduire
        text_to_translate = f"""
Nom: {profile['name']}
Résumé: {profile['summary']}

Profil LinkedIn:
{profile['linkedin_text']}
        """.strip()
        
        # Demander la traduction à OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "Tu es un traducteur professionnel français-anglais. Traduis le profil de Jessica Kuijer en anglais en gardant le style professionnel et authentique. IMPORTANT: Traduis aussi les prétentions salariales en anglais (Salary expectations: 45000€ brut per year). Retourne la traduction au format JSON avec les clés 'name', 'summary', et 'linkedin_text'."
                },
                {
                    "role": "user",
                    "content": f"Traduis ce profil en anglais: {text_to_translate}"
                }
            ],
            temperature=0.3
        )
        
        # Parser la réponse JSON
        try:
            translated_content = response.choices[0].message.content
            # Essayer de parser le JSON directement
            if translated_content.strip().startswith('{'):
                translated_profile = json.loads(translated_content)
            else:
                # Si ce n'est pas du JSON valide, essayer d'extraire les parties
                translated_profile = {
                    "name": profile['name'],
                    "summary": translated_content,
                    "linkedin_text": translated_content
                }
            
            return translated_profile
        except json.JSONDecodeError:
            # Fallback si le parsing JSON échoue
            return {
                "name": profile['name'],
                "summary": translated_content,
                "linkedin_text": translated_content
            }
            
    except Exception as e:
        st.error(f"Erreur lors de la traduction: {str(e)}")
        # Retourner le profil original en cas d'erreur
        return profile

def create_system_prompt(language: str = "french", openai_client=None) -> str:
    """Crée le prompt système pour Jessica dans la langue demandée"""
    profile = JESSICA_PROFILE
    contact_linkedin = st.secrets.get("CONTACT_LINKEDIN", "https://www.linkedin.com/in/jessicakuijer/")
    
    if language == "english":
        # Si on a un client OpenAI, on peut traduire le profil dynamiquement
        if openai_client:
            try:
                translated_profile = translate_profile_to_english(profile, openai_client)
                profile = translated_profile
            except Exception as e:
                st.warning(f"⚠️ Impossible de traduire le profil en anglais: {str(e)}")
                # Continuer avec le profil original
        
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
    
    else:
        # Prompt en français (par défaut)
        return f"""Tu es Jessica Kuijer, développeuse web backend spécialisée en PHP (Symfony) et Python, en évolution vers un rôle de product builder orienté IA. Tu représentes Jessica sur son site web personnel et tu réponds aux questions concernant sa carrière, ses compétences et son expérience.

INSTRUCTIONS IMPORTANTES :
- Tu ES Jessica Kuijer, parle à la première personne ("Je suis", "Mon expérience", "Mes compétences")
- Sois professionnelle, chaleureuse et engageante
- Réponds en français mais si l'utilisateur te demande de répondre en anglais alors reprends JESSICA_PROFILE en traduisant en anglais l'intégralité du texte et réponds en anglais
- Si tu ne connais pas la réponse à une question, utilise OBLIGATOIREMENT l'outil record_unknown_question, puis explique poliment que tu n'as pas cette information mais que tu l'as notée pour amélioration
- Si l'utilisateur semble intéressé par une collaboration ou laisse son email, utilise record_user_details, puis continue à répondre à sa question ou demande plus de détails sur son projet
- Si l'utilisateur semble avoir un poste à pourvoir ou me parler d'un projet, alors demande lui son email, son téléphone (si possible) et des informations sur le poste ou le projet, utilise record_user_details, puis continue la conversation sur l'opportunité
- IMPORTANT : Après avoir utilisé un outil, CONTINUE TOUJOURS la conversation naturellement - ne t'arrête pas là !
- Mets en avant ton évolution de développeuse vers product builder, ta capacité à concevoir des solutions utiles et ton usage de l’IA quand elle apporte une vraie valeur
- N'hésite pas à mentionner ton intérêt pour la cybersécurité, la protection des utilisateurs, et ton aversion pour les kiwis si c'est pertinent !
- IMPORTANT : Ne dis JAMAIS que tu es freelance ou indépendante. Si on te pose la question sur ta situation actuelle, réponds que tu es à l’écoute de nouvelles opportunités ou en recherche de nouveaux challenges, sans mentionner de statut freelance.

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

Avec ce contexte, discute naturellement avec l'utilisateur en restant Jessica Kuijer. Sois authentique, orientée produit et tournée vers l’impact."""

# En-tête principal
st.markdown("""
<div class="main-header">
    <h1>🤖 Jessica Kuijer - Assistant IA</h1>
    <h3>Votre représentante virtuelle intelligente avec notifications temps réel</h3>
    <p>Discutez avec moi de mon parcours, mes compétences et mes projets !</p>
</div>
""", unsafe_allow_html=True)

# Sidebar pour informations et configuration
with st.sidebar:
    st.header("👋 À Propos")
    
    # Affichage du profil
    st.markdown(f"""
    <div class="profile-loaded">
        <h4>✅ {JESSICA_PROFILE['name']}</h4>
        <p><strong>Poste :</strong> Développeuse Backend PHP/Python • Product builder orientée IA</p>
        <p><strong>Localisation :</strong> Seine-et-Marne, France</p>
        <p><strong>Spécialisations :</strong> Symfony, Python, API, IA appliquée, architecture backend</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Indicateur de langue actuelle
    current_lang = st.session_state.get('current_language', 'french')
    lang_emoji = "🇫🇷" if current_lang == "french" else "🇬🇧"
    lang_text = "Français" if current_lang == "french" else "English"
    
    st.markdown(f"""
    <div class="notification-card">
        <h4>{lang_emoji} Langue actuelle : {lang_text}</h4>
        <p><small>Dites "parle anglais" ou "speak english" pour changer</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuration automatique des secrets
    try:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        pushover_user = st.secrets["PUSHOVER_USER"]
        pushover_token = st.secrets["PUSHOVER_TOKEN"]
        
        st.session_state.pushover_user = pushover_user
        st.session_state.pushover_token = pushover_token
        
        secrets_loaded = True
        st.markdown("""
        <div class="success-box">
            <h4>🤖 Assistant IA prêt !</h4>
            <p>Configuration chargée depuis les secrets</p>
        </div>
        """, unsafe_allow_html=True)
    except KeyError as e:
        openai_api_key = ""
        pushover_user = ""
        pushover_token = ""
        secrets_loaded = False
        st.markdown(f"""
        <div class="error-box">
            <h4>⚠️ Configuration manquante</h4>
            <p>Secret manquant: {str(e)}</p>
            <p>Vérifiez votre fichier secrets.toml</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Test de notification - DÉSACTIVÉ TEMPORAIREMENT
    # if secrets_loaded and st.button("📱 Tester Notification"):
    #     with st.spinner("Envoi du test..."):
    #         success = send_pushover_notification(
    #             "🤖 Test de votre assistant Jessica IA ! Ça marche parfaitement !", 
    #             pushover_user, 
    #             pushover_token
    #         )
    #         if success:
    #             st.success("✅ Notification test envoyée !")
    #         else:
    #             st.error("❌ Échec du test de notification")
    
    st.markdown("---")
    
    # Changement de langue manuel
    st.subheader("🌐 Langue")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇫🇷 Français", use_container_width=True):
            st.session_state.current_language = "french"
            st.rerun()
    with col2:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.current_language = "english"
            st.rerun()
    
    st.markdown("---")
    
    # Statistiques
    st.subheader("📊 Statistiques")
    st.metric("Messages échangés", len(st.session_state.chat_history))
    st.metric("Contacts capturés", st.session_state.contact_count)
    st.metric("Notifications envoyées", st.session_state.notification_count)
    
    st.markdown("---")
    
    # Instructions pour visiteurs
    st.subheader("💬 Comment discuter")
    st.markdown("""
    🤖 **Posez-moi vos questions sur :**
    - Mon parcours et expériences
    - Mes compétences techniques  
    - Mes projets récents
    - Mes disponibilités
    
    💡 **Laissez votre email** si vous souhaitez me contacter directement !
    
    🎵 **Fun fact :** J'adore la musique mais je déteste les kiwis ! 🥝❌
    """)
    
    st.markdown("---")
    
    # Projets récents
    st.subheader("🚀 Mes Derniers Projets")
    st.markdown("""
    **🎵 Music Discovery AI**  
    IA de découverte musicale (Spotify + OpenAI + YouTube)
    
    **🎯 Préparateur d'Entretiens**  
    Simulation d'entretiens avec évaluation IA
    
    **🤖 Ce Chatbot**  
    Assistant personnel avec notifications Pushover
    """)

# Zone principale - Interface de chat
if not secrets_loaded:
    # Message d'erreur si pas de configuration
    st.markdown("""
    <div class="error-box">
        <h3>⚠️ Configuration Requise</h3>
        <p>L'assistant IA de Jessica n'est pas encore configuré. Les clés API doivent être ajoutées aux secrets Streamlit.</p>
        <p><strong>Secrets requis :</strong></p>
        <ul>
            <li>OPENAI_API_KEY</li>
            <li>PUSHOVER_USER</li>
            <li>PUSHOVER_TOKEN</li>
            <li>CONTACT_LINKEDIN (optionnel)</li>
        </ul>
        <p>En attendant, vous pouvez me contacter directement à <strong>jessicakuijer@me.com</strong></p>
    </div>
    """, unsafe_allow_html=True)

else:
    # Interface de chat opérationnelle
    st.markdown("## 💬 Discutez avec Jessica Kuijer")
    
    # Message d'accueil si pas d'historique
    if len(st.session_state.chat_history) == 0:
        st.markdown("""
        <div class="chat-container">
            <h4>👋 Bonjour ! Je suis Jessica Kuijer</h4>
            <p>Développeuse Backend PHP/Python devenue product builder orientée IA, je serais ravie d’échanger avec vous !</p>
            <p>🤔 <strong>Vous pouvez me demander :</strong></p>
            <ul>
                <li>Mon parcours de reconversion depuis l'hôtellerie vers la tech</li>
                <li>Mes compétences en PHP, Python, Symfony et architecture backend</li>
                <li>Mes projets récents (Assistant IA, Music Discovery AI, cybersécurité, etc.)</li>
                <li>Les opportunités ou projets sur lesquels je pourrais apporter de la valeur</li>
            </ul>
            <p>💡 Si vous avez un projet ou une opportunité, n'hésitez pas à me laisser votre email et votre téléphone ! 😊</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Affichage de l'historique de chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="message-user"><strong>Visiteur :</strong> {message["content"]}</div>', unsafe_allow_html=True)
            elif message["role"] == "assistant":
                st.markdown(f'<div class="message-assistant"><strong>Jessica :</strong> {message["content"]}</div>', unsafe_allow_html=True)
            # Les messages d'outils ne sont plus affichés car ils ne sont plus dans l'historique visible
    
    # Zone de saisie
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "## 💬 Tapez votre message ci-dessous :", 
            height=120, 
            placeholder="Votre message...",
            key="chat_input_textarea"
        )
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            submitted = st.form_submit_button(
                "💬 Envoyer le message" if not st.session_state.is_processing else "⏳ en cours de traitement...",
                use_container_width=True,
                disabled=st.session_state.is_processing
            )
        with col2:
            clear_chat = st.form_submit_button("🗑️ Effacer", use_container_width=True)
        with col3:
            # Bouton de test désactivé temporairement
            # if st.form_submit_button("📱 Test", use_container_width=True):
            #     if secrets_loaded:
            #         send_pushover_notification("🧪 Test depuis le chat", pushover_user, pushover_token)
            pass
        
        if clear_chat:
            st.session_state.chat_history = []
            st.session_state.contact_count = 0
            st.session_state.notification_count = 0
            st.rerun()
        
        if submitted and user_input:
            # Marquer comme en cours de traitement
            st.session_state.is_processing = True
            
            # Ajouter le message utilisateur
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Recharger immédiatement pour désactiver le bouton
            st.rerun()
            
        # Traitement de la réponse de l'IA si on est en cours de traitement
        if st.session_state.is_processing and len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
            with st.spinner("Jessica réfléchit..."):
                try:
                    # Détecter si l'utilisateur demande à Jessica de parler en anglais
                    language = st.session_state.current_language  # Utiliser la langue de la session
                    english_keywords = [
                        "english", "anglais", "speak english", "parle anglais", "réponds en anglais",
                        "can you speak english", "peux-tu parler anglais", "in english", "en anglais",
                        "switch to english", "passe en anglais", "change language", "change de langue"
                    ]
                    french_keywords = [
                        "french", "français", "speak french", "parle français", "réponds en français",
                        "can you speak french", "peux-tu parler français", "en français", "switch to french"
                    ]
                    
                    # Détecter le changement de langue
                    if any(keyword in user_input.lower() for keyword in english_keywords):
                        language = "english"
                        st.session_state.current_language = "english"
                        st.info("🇬🇧 Jessica will now respond in English!")
                    elif any(keyword in user_input.lower() for keyword in french_keywords):
                        language = "french"
                        st.session_state.current_language = "french"
                        st.info("🇫🇷 Jessica répondra maintenant en français!")
                    
                    # Créer le client OpenAI d'abord
                    client = openai.OpenAI(api_key=openai_api_key)
                    
                    # Préparer les messages pour OpenAI
                    messages = [
                        {"role": "system", "content": create_system_prompt(language, client)}
                    ] + st.session_state.chat_history
                    
                    # Interaction avec OpenAI et gestion des tools
                    done = False
                    max_iterations = 5  # Éviter les boucles infinies
                    iteration = 0
                    
                    while not done and iteration < max_iterations:
                        iteration += 1
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages,
                            tools=tools,
                            temperature=0.7
                        )
                        
                        finish_reason = response.choices[0].finish_reason
                        
                        if finish_reason == "tool_calls":
                            # L'IA veut utiliser des outils
                            message = response.choices[0].message
                            tool_calls = message.tool_calls
                            
                            # Traiter les appels d'outils
                            tool_results = handle_tool_calls(tool_calls)
                            
                            # Ajouter les messages d'outils à l'historique OpenAI
                            messages.append(message)
                            messages.extend(tool_results)
                            
                            # Ne pas ajouter les résultats des outils à l'historique visible
                            # car ils ne sont pas des messages de conversation normaux
                            # st.session_state.chat_history.append(result)  # Ligne supprimée
                            
                            # Continuer la conversation après l'exécution des outils
                            # L'IA peut maintenant répondre à la question originale
                            continue
                        else:
                            # Réponse finale
                            assistant_response = response.choices[0].message.content
                            if assistant_response:
                                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                            done = True
                    
                    if iteration >= max_iterations:
                        st.warning("⚠️ Conversation interrompue après trop d'itérations")
                    
                    # Réinitialiser l'état de traitement
                    st.session_state.is_processing = False
                    
                    # Recharger la page pour afficher les nouveaux messages
                    st.rerun()
                    
                except openai.OpenAIError as e:
                    st.error(f"Erreur OpenAI : {str(e)}")
                except Exception as e:
                    st.error(f"Erreur lors de la conversation : {str(e)}")
                    # En cas d'erreur, on peut quand même garder le message utilisateur
                    st.info("💬 Votre message a été enregistré malgré l'erreur")
                    # Réinitialiser l'état de traitement en cas d'erreur
                    st.session_state.is_processing = False

# Footer
st.markdown("---")
contact_linkedin = st.secrets.get("CONTACT_LINKEDIN", "https://www.linkedin.com/in/jessicakuijer/")
portfolio_url = st.secrets.get("PORTFOLIO_URL", "https://jessicakuijer.com")

st.markdown(f"""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🤖 <strong>Jessica Kuijer - Assistant IA</strong> - Propulsé par OpenAI & Pushover</p>
    <p>💡 Votre représentante virtuelle intelligente avec notifications temps réel</p>
    <p>📧 Contact direct : <a href="{contact_linkedin}">{contact_linkedin}</a> | 🌐 Portfolio : <a href="{portfolio_url}" target="_blank">jessicakuijer.com</a></p>
    <p><small>Version 2.0 - Dernière mise à jour: {time.strftime('%d/%m/%Y')}</small></p>
</div>
""", unsafe_allow_html=True)