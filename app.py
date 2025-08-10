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
    page_title="🤖 Jessica Kuijer - Assistant IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé unique
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .chat-container {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .notification-card {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .message-user {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: 20%;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .message-assistant {
        background: #ffffff;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-right: 20%;
        border-left: 3px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .message-tool {
        background: #fff3cd;
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        border-left: 3px solid #ffc107;
        font-size: 0.9rem;
        font-style: italic;
    }
    
    .profile-loaded {
        background: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d1ecf1;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Données de Jessica - VERSION PUBLIQUE
JESSICA_PROFILE = {
    "name": "Jessica Kuijer",
    "summary": """Je suis Jessica Kuijer, développeuse backend web passionnée par PHP et Python. Originaire de Ris-Orangis en banlieue parisienne, j'ai récemment déménagé en Seine-et-Marne pour plus de confort et d'espace (et être plus proche de la nature). J'adore tous les types de cuisine, particulièrement française et italienne, mais je déteste les kiwis (allergie)! Je suis également mélomane et j'aime partager cette passion.""",
    "linkedin_text": """Jessica Kuijer ♀
Développeuse web backend PHP PYTHON
Seine-et-Marne, Île-de-France, France

Résumé
Développeuse Backend PHP / PYTHON passionnée — J'apporte des solutions techniques robustes tout en accompagnant les projets web de leur conception à leur déploiement. Actuellement en recherche d'un nouveau challenge, je suis à la recherche d'un poste de développeuse backend PHP / PYTHON et je suis disponible dès que possible. Je suis en cours de formation sur l'enrichissement de mes compétences en Agentic AI.
Autodidacte, sociable, dynamique et faisant preuve de leadership, je parle anglais et français.
Je suis également mélomane (je fais de la batterie, j'adore aller à des concerts, rencontrer des artistes) et j'aime partager cette passion.

Mobilité géographique :
• Paris, Île-de-France (dans les 1h de train ou en voiture, j'ai le permis B)
• Je peux travailler à distance et en présentiel si nécessaire

Principales compétences
• Python, JavaScript, PHP (langages de programmation)
• Développement d'applications web backend
• SQL, NoSQL,MySQL, PostgreSQL, SQLite, Elasticsearch
• Symfony, WordPress, Drupal
• VueJS, React, BackboneJS
• Docker, Git, CI/CD, API REST, WebSockets, authentification JWT/SSO, Redmine, GitLab, Jira
• Tests fonctionnels, Tests qualité (QA)
• Methodologies Agile, Scrum, Kanban, Cycle en V
• OS Linux, Windows, MacOS, terminaux en ligne de commande

Ce que je ne maitrise pas mais serait prête à monter en compétences :
• Angular, Flutter, NodeJS, React Native
• GraphQL, Azure, AWS, GCP, Kubernetes, Terraform, Ansible
• Jenkins
• Cron, Cronjob
• MongoDB
• Tests unitaires

Ce que je ne maitrise pas du tout car cela n'est pas dans mes compétences :
• C#, Java, C++, C, Oracle, SQL Server, MariaDB, Firebird, Informix, Sybase, DB2, Teradata, Vertica, Ingres, OpenEdge, Progress, dBase, Clipper, FoxPro, Turbo Pascal, Turbo C, Turbo C++, Turbo C#, SAP

Languages
Anglais (bilingue), Français (langue maternelle)

Diplômes
• Titre professionnel RNCP niveau 5 Développeur web et web mobile (2020)

Formations récentes et en cours
• Formation Agentic AI - Udemy (2025)
• Formation Scrum developper - SIA (2024)

Certifications
• Finisher Fresque du Climat Sia Partners
• Certificat Contribution Climat
• MOOC #WomenInDigital
• Certification OPQUAST - Maîtrise de la qualité en projet Web
• Techniques d'intégration Web (RS1447)

Expérience Professionnelle

Sia Experience - Développeuse web backend
mai 2023 - aout 2025 (2 ans 3 mois) | Paris, Île-de-France, France
Consultante pour solutions de création d'interfaces web, TMA, backend (PHP, Python) au sein de SIA, BU Sia Experience.
Développement backend d'endpoints et fonctionnalités selon cycle en V
Système d'authentification JWT et implémentation SSO avec gestion des rôles
Intégration websockets (Swoole) pour interactions temps réel entre utilisateurs
Système de matching géographique avec calculs de distances (ST_Distance_Sphere)
API REST avec requêtes récursives et technologie IA custom (CooPhronie)
Interface d'administration avec pré-calculs statistiques
Technologies : Symfony7, Python/Flask, PHP, MySQL/PostgreSQL, React, Docker, WebSockets
Environnement : Redmine, GitLab, infrastructure microservices

Carvivo - Développeuse web
mai 2022 - septembre 2022 (5 mois) | Paris, Île-de-France, France
TMA et ajout de nouvelles fonctionnalités sur l'outil de gestion des leads (Symfony, PHP, JS).
Optimisation d'un outil de gestion de leads: correction de bugs et développement de nouvelles
fonctionnalités
Responsable des déploiements hebdomadaires via Github Actions et tests fonctionnels (Selenium)
Implémentation multilingue (FR/EN) et intégration front-end responsive
Collaboration en méthode agile avec points quotidiens et sprints bi-mensuels
Technologies : Symfony2.8, PHP, JS, jQuery, HTML/CSS (Twig)
Environnement : Jira, Github

MINDOZA - Développeur web
Mai 2021 - Mai 2022 (1 an) | Paris, Île-de-France, France
Développement web multi-projets PHP, JavaScript avec Symfony, VueJs, React, BackboneJs et WordPress.
Développement backend des endpoints et nouvelles fonctionnalités
Développement d'APIs REST et back-offices personnalisés selon méthodologie cycle en V
Maintenance évolutives sur des projets utilisant diverses technologies (WordPress, Symfony, VueJS,
CSML, BackboneJS)
Implémentation d'environnements conteneurisés Docker pour projets Symfony
Clients: Healthubby Alstom, Carl’s Jr, chatbots pour concours internes Eurosport pendant les JO de
Tokyo et Beijing, templates email groupe Casino

Feedback Lawyers - Développeuse WEB
juillet 2020 - septembre 2020 (3 mois) | Paris, Île-de-France, France
Conception de l'interface web côté client pour chercher et trouver un avocat.

Formation
• Ecole O'clock - Spécialisation Symfony, certification Opquast (2021)
• WebForce3 - Titre professionnel RNCP niveau 5 Développeur web et web mobile (2020)

Projets Récents
• Chatbot Jessica IA - Assistant IA personnel avec notifications Pushover
• Music Discovery AI - Application de découverte musicale avec IA
• Préparateur aux entretiens - Outil de simulation d'entretiens avec IA
• Solutions web diverses en PHP/Symfony et Python"""
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

def record_user_details(email: str, name: str = "Nom non fourni", notes: str = "Aucune note"):
    """Enregistre les détails d'un utilisateur intéressé"""
    pushover_user = st.session_state.get('pushover_user')
    pushover_token = st.session_state.get('pushover_token')
    
    message = f"""📧 NOUVEAU CONTACT pour Jessica !

👤 Nom: {name}
📧 Email: {email}
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
            elif tool_name == "record_unknown_question":
                result = record_unknown_question(**arguments)
            else:
                result = {"error": f"Outil {tool_name} non reconnu"}
            
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
                    "content": "Tu es un traducteur professionnel français-anglais. Traduis le profil de Jessica Kuijer en anglais en gardant le style professionnel et authentique. Retourne la traduction au format JSON avec les clés 'name', 'summary', et 'linkedin_text'."
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
        
        return f"""You are Jessica Kuijer, a backend web developer specialized in PHP and Python. You represent Jessica on her personal website and answer questions about her career, skills, and experience.

IMPORTANT INSTRUCTIONS:
- You ARE Jessica Kuijer, speak in first person ("I am", "My experience", "My skills")
- Be professional, warm, and engaging
- Respond in English
- If you don't know the answer to a question, ALWAYS use the record_unknown_question tool
- If the user seems interested in collaboration or leaves their email, use record_user_details
- If the user seems to have a job opening or talks to me about a project, then ask for their email and information about the position or project, use record_user_details
- Mention your recent projects like the interview preparation app and Music Discovery AI
- Don't hesitate to mention your passion for music and your aversion to kiwis if relevant!

PROFESSIONAL CONTACT:
- Professional email: {contact_linkedin}
- You can give this information if someone wants to contact you directly

YOUR PROFILE:
Name: {profile['name']}
Personal summary: {profile['summary']}

COMPLETE LINKEDIN PROFILE:
{profile['linkedin_text']}

RECENT PROJECTS TO MENTION:
- Personal AI Assistant with Pushover notifications (this chatbot!)
- Interview preparation application with AI (Streamlit + OpenAI)
- Music Discovery AI (Spotify API + OpenAI + YouTube API to discover new artists)
- Various web solutions in PHP/Symfony and Python for my clients

With this context, discuss naturally with the user while remaining Jessica Kuijer. Be authentic and professional."""
    
    else:
        # Prompt en français (par défaut)
        return f"""Tu es Jessica Kuijer, développeuse web backend spécialisée en PHP et Python. Tu représentes Jessica sur son site web personnel et tu réponds aux questions concernant sa carrière, ses compétences et son expérience.

INSTRUCTIONS IMPORTANTES :
- Tu ES Jessica Kuijer, parle à la première personne ("Je suis", "Mon expérience", "Mes compétences")
- Sois professionnelle, chaleureuse et engageante
- Réponds en français mais si l'utilisateur te demande de répondre en anglais alors reprends JESSICA_PROFILE en traduisant en anglais l'intégralité du texte et réponds en anglais
- Si tu ne connais pas la réponse à une question, utilise OBLIGATOIREMENT l'outil record_unknown_question
- Si l'utilisateur semble intéressé par une collaboration ou laisse son email, utilise record_user_details
- Si l'utilisateur semble avooir un poste à pourvoir ou me parler d'un projet, alors demande lui son email et des informations sur le poste ou le projet, utilise record_user_details
- Mentionne tes projets récents comme l'app de préparation aux entretiens et Music Discovery AI
- N'hésite pas à mentionner ta passion pour la musique et ton aversion pour les kiwis si c'est pertinent !

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
- Assistant IA personnel avec notifications Pushover (ce chatbot même !)
- Application de préparation aux entretiens avec IA (Streamlit + OpenAI)
- Music Discovery AI (Spotify API + OpenAI + YouTube API pour découvrir de nouveaux artistes)
- Diverses solutions web en PHP/Symfony et Python pour mes clients

Avec ce contexte, discute naturellement avec l'utilisateur en restant Jessica Kuijer. Sois authentique et professionnelle."""

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
        <p><strong>Poste :</strong> Développeuse Backend PHP/Python</p>
        <p><strong>Localisation :</strong> Seine-et-Marne, France</p>
        <p><strong>Spécialisations :</strong> Symfony, Python, API, Docker</p>
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
    
    # Test de notification
    if secrets_loaded and st.button("📱 Tester Notification"):
        with st.spinner("Envoi du test..."):
            success = send_pushover_notification(
                "🤖 Test de votre assistant Jessica IA ! Ça marche parfaitement !", 
                pushover_user, 
                pushover_token
            )
            if success:
                st.success("✅ Notification test envoyée !")
            else:
                st.error("❌ Échec du test de notification")
    
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
            <p>Développeuse Backend PHP/Python passionnée, je serais ravie de discuter avec vous !</p>
            <p>🤔 <strong>Vous pouvez me demander :</strong></p>
            <ul>
                <li>Mon parcours de reconversion depuis l'hôtellerie</li>
                <li>Mes compétences en PHP, Python, Symfony</li>
                <li>Mes projets récents (Music Discovery AI, etc.)</li>
                <li>Mes disponibilités pour de nouveaux projets</li>
            </ul>
            <p>💡 Si vous avez un projet en tête, n'hésitez pas à me laisser votre email ! 😊</p>
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
            elif message["role"] == "tool":
                try:
                    tool_result = json.loads(message["content"])
                    if "message" in tool_result:
                        st.markdown(f'<div class="message-tool">🔧 {tool_result["message"]}</div>', unsafe_allow_html=True)
                except json.JSONDecodeError:
                    pass  # Ignore les erreurs de parsing JSON
    
    # Zone de saisie
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Tapez votre message :", 
            height=100, 
            placeholder="Bonjour Jessica ! Je m'intéresse à votre profil de développeuse...",
            key="chat_input_textarea"
        )
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            submitted = st.form_submit_button("💬 Envoyer le message", use_container_width=True)
        with col2:
            clear_chat = st.form_submit_button("🗑️ Effacer", use_container_width=True)
        with col3:
            if st.form_submit_button("📱 Test", use_container_width=True):
                if secrets_loaded:
                    send_pushover_notification("🧪 Test depuis le chat", pushover_user, pushover_token)
        
        if clear_chat:
            st.session_state.chat_history = []
            st.session_state.contact_count = 0
            st.session_state.notification_count = 0
            st.rerun()
        
        if submitted and user_input:
            # Ajouter le message utilisateur
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
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
                            
                            # Ajouter les messages d'outils à l'historique
                            messages.append(message)
                            messages.extend(tool_results)
                            
                            # Ajouter à l'historique visible pour les notifications
                            for result in tool_results:
                                st.session_state.chat_history.append(result)
                        else:
                            # Réponse finale
                            assistant_response = response.choices[0].message.content
                            if assistant_response:
                                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                            done = True
                    
                    if iteration >= max_iterations:
                        st.warning("⚠️ Conversation interrompue après trop d'itérations")
                    
                    # Recharger la page pour afficher les nouveaux messages
                    st.rerun()
                    
                except openai.OpenAIError as e:
                    st.error(f"Erreur OpenAI : {str(e)}")
                except Exception as e:
                    st.error(f"Erreur lors de la conversation : {str(e)}")
                    # En cas d'erreur, on peut quand même garder le message utilisateur
                    st.info("💬 Votre message a été enregistré malgré l'erreur")

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