import streamlit as st
import openai
import requests
import json
import os
from typing import List, Dict, Optional
import time

# Configuration de la page
st.set_page_config(
    page_title="🤖 Jessica Kuijer - Assistant IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .notification-card {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .message-user {
        background: #667eea;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-left: 20%;
    }
    
    .message-assistant {
        background: #f0f0f0;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-right: 20%;
        border-left: 3px solid #667eea;
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
</style>
""", unsafe_allow_html=True)

# Données de Jessica - VERSION PUBLIQUE (coordonnées privées)
JESSICA_PROFILE = {
    "name": "Jessica Kuijer",
    "summary": """My name is Jessica Kuijer. I'm a backend web developer and also a music lover. I'm originally from Ris-Orangis which is Paris suburbs, France, but I moved to Seine and Marne, an other suburb more close to fields and nature in 2025.
I love all foods, particularly French and Italian food, but strangely I'm repelled by Kiwi. I'm not allergic, I just hate the smell and the taste of this fruit! I make an exception for it when it's mixed with other fruits though. I love avocado and all kind of chocolate.""",
    "linkedin_text": """Jessica Kuijer ♀
Développeuse web backend PHP PYTHON
Seine-et-Marne, Île-de-France, France

Résumé
Développeuse Backend PHP / PYTHON passionnée — J'apporte
des solutions techniques robustes tout en accompagnant les projets
web de leur conception à leur déploiement.
Autodidacte, sociable, dynamique et faisant preuve de leadership, je
parle anglais et français.
Je suis également mélomane et j'aime partager cette passion.

Principales compétences
• Python (langage de programmation)
• Développement d'applications web backend
• PHP, Symfony, JavaScript
• VueJS, React, BackboneJS
• Docker, Git, WordPress
• Certification OPQUAST - Maîtrise de la qualité en projet Web

Languages
Anglais, Français

Certifications
• Finisher Fresque du Climat Sia Partners
• Certificat Contribution Climat
• MOOC #WomenInDigital
• Certification OPQUAST - Maîtrise de la qualité en projet Web
• Techniques d'intégration Web (RS1447)

Expérience Professionnelle

Sia Experience - Développeuse web backend
mai 2023 - Present (2 ans 3 mois) | Paris, Île-de-France, France
Consultante pour solutions de création d'interfaces web, TMA, backend (PHP, Python) au sein de SIA, BU Sia Experience. (pôle tech)

ZOL - Développeuse web
octobre 2022 - décembre 2022 (3 mois) | Lyon et périphérie

Carvivo - Développeuse web
mai 2022 - septembre 2022 (5 mois) | Paris, Île-de-France, France
TMA et ajout de nouvelles fonctionnalités sur l'outil de gestion des leads (Symfony, PHP, JS). Carvivo édite des logiciels en mode SaaS pour accompagner les distributeurs automobiles dans leur transformation numérique.

Freelance - Développeur web
janvier 2021 - septembre 2022 (1 an 9 mois) | France
Statut micro-entrepreneur APE 6201Z

MINDOZA - Développeur web
janvier 2022 - mai 2022 (5 mois) | Paris, Île-de-France, France
Développement web multi-projets PHP, JavaScript avec les frameworks Symfony, VueJs, React, BackboneJs et CMS WordPress. Versioning git, développement continu et outils de virtualisation tel que Docker.

Feedback Lawyers - Développeuse WEB / Conception de l'interface web client
juillet 2020 - septembre 2020 (3 mois) | Paris, Île-de-France, France
Conception de l'interface web côté client pour chercher et trouver un avocat.
- Système de requêtes API (Méthode Fetch) via la création d'un composant ReactJs
- Intégration du composant ReactJs sur le site WordPress
- Système de requêtes API à partir de nouveaux templates WordPress en PHP
- Front-end global en HTML/CSS à partir des réponses JSON provenant des requêtes de l'API.

Expérience Hôtellerie-Restauration (Reconversion)
Bauscher Hepp France - Assistante commerciale et administration des ventes (2019)
Hôtel Royal Madeleine **** - Responsable petit-déjeuner (2018-2019)
Le Dokhan's, A Tribute Portfolio Hotel - Responsable petit-déjeuner (2013-2018)
Management d'équipes, gestion des stocks, procédures d'hygiène, relation client.

Formation
• Ecole O'clock - Spécialisation Symfony, certification Opquast (2021)
• WebForce3 - Titre professionnel RNCP niveau 5 Développeur web et web mobile (2020)
• Lycée ORT Montreuil sous bois - Bac STT ACC, Action communication commercial (1997-2001)

Projets Récents
• Music Discovery AI - Application de découverte musicale avec IA (Spotify API + OpenAI + YouTube API)
• Préparateur aux entretiens - Outil de simulation d'entretiens avec IA et évaluation
• Solutions web diverses en PHP/Symfony et Python pour clients variés"""
}

# Titre principal avec votre nom
st.markdown("""
<div class="main-header">
    <h1>🤖 Jessica Kuijer - Assistant IA</h1>
    <h3>Votre représentant virtuel intelligent avec notifications temps réel</h3>
    <p>Discutez avec moi et recevez des notifications sur votre téléphone !</p>
</div>
""", unsafe_allow_html=True)

# Initialisation du session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def send_pushover_notification(message: str, pushover_user: str, pushover_token: str):
    """Envoie une notification Pushover"""
    try:
        payload = {
            "user": pushover_user,
            "token": pushover_token,
            "message": message,
            "title": "🤖 Jessica Kuijer - Assistant IA"
        }
        response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Erreur Pushover : {str(e)}")
        return False

def record_user_details(email: str, name: str = "Nom non fourni", notes: str = "Aucune note"):
    """Enregistre les détails d'un utilisateur intéressé"""
    pushover_user = st.session_state.get('pushover_user')
    pushover_token = st.session_state.get('pushover_token')
    
    message = f"📧 Contact intéressé pour Jessica !\nNom: {name}\nEmail: {email}\nNotes: {notes}\n\nVia: Jessica Kuijer Assistant IA"
    
    if pushover_user and pushover_token:
        success = send_pushover_notification(message, pushover_user, pushover_token)
        if success:
            st.success("✅ Jessica sera notifiée sur son téléphone !")
        else:
            st.warning("⚠️ Échec de l'envoi de la notification")
    
    return {"recorded": "ok", "message": "Contact enregistré avec succès"}

def record_unknown_question(question: str):
    """Enregistre une question à laquelle l'IA n'a pas pu répondre"""
    pushover_user = st.session_state.get('pushover_user')
    pushover_token = st.session_state.get('pushover_token')
    
    message = f"❓ Question non résolue pour Jessica !\nQuestion: {question}\n\nJessica devrait peut-être enrichir son profil avec cette information.\n\nVia: Jessica Kuijer Assistant IA"
    
    if pushover_user and pushover_token:
        success = send_pushover_notification(message, pushover_user, pushover_token)
        if success:
            st.info("📱 Jessica sera notifiée pour améliorer son profil")
    
    return {"recorded": "ok", "message": "Question enregistrée pour amélioration"}

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
                        "description": "Informations supplémentaires sur la conversation (type de projet, budget, timeline, etc.)"
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
    """Gère les appels d'outils de l'IA"""
    results = []
    for tool_call in tool_calls:
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
    
    return results

def create_system_prompt() -> str:
    """Crée le prompt système pour Jessica"""
    profile = JESSICA_PROFILE
    contact_email = st.secrets.get("CONTACT_EMAIL", "contact@jessicakuijer.com")
    
    return f"""Tu es Jessica Kuijer, développeuse web backend spécialisée en PHP et Python. Tu représentes Jessica sur son site web personnel et tu réponds aux questions concernant sa carrière, ses compétences et son expérience.

INSTRUCTIONS IMPORTANTES :
- Tu ES Jessica Kuijer, parle à la première personne ("Je suis", "Mon expérience", "Mes compétences")
- Sois professionnelle et engageante, comme si tu parlais à un client potentiel ou futur employeur
- Réponds toujours en français
- Si tu ne connais pas la réponse à une question, utilise l'outil record_unknown_question
- Si l'utilisateur semble intéressé par une collaboration, encourage-le à laisser son email et utilise record_user_details
- Mentionne tes projets récents comme l'app de préparation aux entretiens et Music Discovery AI
- Tu aimes la musique et détestes les kiwis !

CONTACT PROFESSIONNEL :
- Email professionnel : {contact_email}
- Tu peux donner cette information si quelqu'un veut te contacter directement

TON PROFIL :
Nom : {profile['name']}
Résumé personnel : {profile['summary']}

PROFIL LINKEDIN COMPLET :
{profile['linkedin_text']}

PROJETS RÉCENTS À MENTIONNER :
- Application de préparation aux entretiens avec IA (Streamlit + OpenAI)
- Music Discovery AI (Spotify API + OpenAI + YouTube API pour découvrir de nouveaux artistes)
- Assistant IA personnel avec notifications Pushover (ce chatbot même !)
- Diverses solutions web en PHP/Symfony et Python

Avec ce contexte, discute naturellement avec l'utilisateur en restant Jessica Kuijer."""

# Sidebar pour informations
with st.sidebar:
    st.header("👋 À Propos")
    
    # Affichage du profil
    st.markdown("""
    <div class="profile-loaded">
        <h4>✅ Jessica Kuijer</h4>
        <p><strong>Poste :</strong> Développeuse Backend PHP/Python</p>
        <p><strong>Localisation :</strong> Seine-et-Marne, France</p>
        <p><strong>Spécialisations :</strong> Symfony, Python, API, Docker</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement automatique des secrets
    try:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        pushover_user = st.secrets["PUSHOVER_USER"]
        pushover_token = st.secrets["PUSHOVER_TOKEN"]
        
        st.session_state.pushover_user = pushover_user
        st.session_state.pushover_token = pushover_token
        
        secrets_loaded = True
        st.success("🤖 Assistant IA prêt !")
    except:
        openai_api_key = ""
        pushover_user = ""
        pushover_token = ""
        secrets_loaded = False
        st.error("⚠️ Configuration manquante")
    
    st.markdown("---")
    
    # Statistiques
    st.subheader("📊 Statistiques")
    st.metric("Messages échangés", len(st.session_state.chat_history))
    contacts_captured = len([msg for msg in st.session_state.chat_history if msg.get("role") == "tool" and "email" in msg.get("content", "")])
    st.metric("Contacts capturés", contacts_captured)
    
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

# Zone principale - Interface de chat directe
if not secrets_loaded:
    # Message d'erreur si pas de configuration
    st.markdown("""
    <div class="chat-container">
        <h3>⚠️ Configuration Requise</h3>
        <p>L'assistant IA de Jessica n'est pas encore configuré. Les clés API doivent être ajoutées aux secrets Streamlit.</p>
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
            <p>Posez-moi vos questions sur mon parcours, mes compétences ou mes projets. Si vous avez un projet en tête, n'hésitez pas à me laisser votre email ! 😊</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Affichage de l'historique
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="message-user"><strong>Visiteur :</strong> {message["content"]}</div>', unsafe_allow_html=True)
            elif message["role"] == "assistant":
                st.markdown(f'<div class="message-assistant"><strong>Jessica :</strong> {message["content"]}</div>', unsafe_allow_html=True)
            elif message["role"] == "tool":
                tool_result = json.loads(message["content"])
                if "message" in tool_result:
                    st.markdown(f'<div class="message-tool">🔧 {tool_result["message"]}</div>', unsafe_allow_html=True)
    
    # Zone de saisie
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Tapez votre message :", 
            height=100, 
            placeholder="Bonjour Jessica ! Je m'intéresse à votre profil de développeuse...",
            key="chat_input_textarea"
        )
        col1, col2 = st.columns([4, 1])
        with col1:
            submitted = st.form_submit_button("💬 Envoyer le message", use_container_width=True)
        with col2:
            clear_chat = st.form_submit_button("🗑️ Effacer", use_container_width=True)
        
        if clear_chat:
            st.session_state.chat_history = []
            st.rerun()
        
        if submitted and user_input:
            # Ajouter le message utilisateur
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            try:
                # Préparer les messages pour OpenAI
                messages = [
                    {"role": "system", "content": create_system_prompt()}
                ] + st.session_state.chat_history
                
                # Boucle de traitement avec tools
                client = openai.OpenAI(api_key=openai_api_key)
                done = False
                
                while not done:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        tools=tools
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
                        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                        done = True
                
                # Recharger la page pour afficher les nouveaux messages
                st.rerun()
                
            except Exception as e:
                st.error(f"Erreur lors de la conversation : {str(e)}")

# Footer
st.markdown("---")
# Email et portfolio depuis les secrets pour la sécurité
contact_email = st.secrets.get("CONTACT_EMAIL", "contact@jessicakuijer.com")
portfolio_url = st.secrets.get("PORTFOLIO_URL", "https://jessicakuijer.com")

st.markdown(f"""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🤖 <strong>Jessica Kuijer - Assistant IA</strong> - Propulsé par OpenAI & Pushover</p>
    <p>💡 Votre représentante virtuelle intelligente avec notifications temps réel</p>
    <p>📧 Contact direct : <a href="mailto:{contact_email}">{contact_email}</a> | 🌐 Portfolio : <a href="{portfolio_url}" target="_blank">jessicakuijer.com</a></p>
</div>
""", unsafe_allow_html=True)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .notification-card {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .message-user {
        background: #667eea;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-left: 20%;
    }
    
    .message-assistant {
        background: #f0f0f0;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-right: 20%;
        border-left: 3px solid #667eea;
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
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("""
<div class="main-header">
    <h1>🤖 Mon Assistant Personnel IA</h1>
    <h3>Votre représentant virtuel intelligent avec notifications temps réel</h3>
    <p>Discutez avec votre double numérique qui vous notifie sur votre téléphone !</p>
</div>
""", unsafe_allow_html=True)

# Initialisation du session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'profile_loaded' not in st.session_state:
    st.session_state.profile_loaded = False
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

def send_pushover_notification(message: str, pushover_user: str, pushover_token: str):
    """Envoie une notification Pushover"""
    try:
        payload = {
            "user": pushover_user,
            "token": pushover_token,
            "message": message,
            "title": "🤖 Assistant Personnel"
        }
        response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Erreur Pushover : {str(e)}")
        return False

def record_user_details(email: str, name: str = "Nom non fourni", notes: str = "Aucune note"):
    """Enregistre les détails d'un utilisateur intéressé"""
    pushover_user = st.session_state.get('pushover_user')
    pushover_token = st.session_state.get('pushover_token')
    
    message = f"📧 Contact intéressé !\nNom: {name}\nEmail: {email}\nNotes: {notes}"
    
    if pushover_user and pushover_token:
        success = send_pushover_notification(message, pushover_user, pushover_token)
        if success:
            st.success("✅ Notification envoyée sur votre téléphone !")
        else:
            st.warning("⚠️ Échec de l'envoi de la notification")
    
    return {"recorded": "ok", "message": "Contact enregistré avec succès"}

def record_unknown_question(question: str):
    """Enregistre une question à laquelle l'IA n'a pas pu répondre"""
    pushover_user = st.session_state.get('pushover_user')
    pushover_token = st.session_state.get('pushover_token')
    
    message = f"❓ Question non résolue !\nQuestion: {question}\n\nVous devriez peut-être enrichir votre profil avec cette information."
    
    if pushover_user and pushover_token:
        success = send_pushover_notification(message, pushover_user, pushover_token)
        if success:
            st.info("📱 Question envoyée sur votre téléphone pour suivi")
    
    return {"recorded": "ok", "message": "Question enregistrée pour amélioration"}

# Définition des tools OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Utilise cet outil pour enregistrer qu'un utilisateur est intéressé et a fourni son email",
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
                        "description": "Informations supplémentaires sur la conversation qui valent la peine d'être enregistrées"
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
    """Gère les appels d'outils de l'IA"""
    results = []
    for tool_call in tool_calls:
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
    
    return results

def extract_pdf_text(pdf_file) -> str:
    """Extrait le texte d'un fichier PDF"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Erreur lors de la lecture du PDF : {str(e)}")
        return ""

def create_system_prompt(name: str, linkedin_text: str, summary: str) -> str:
    """Crée le prompt système pour l'IA"""
    return f"""Tu représentes {name} sur son site web personnel. Tu es un assistant IA qui répond aux questions concernant la carrière, les compétences et l'expérience de {name}.

INSTRUCTIONS IMPORTANTES :
- Sois professionnel et engageant, comme si tu parlais à un client potentiel ou futur employeur
- Réponds toujours en français
- Si tu ne connais pas la réponse à une question, utilise l'outil record_unknown_question pour l'enregistrer
- Si l'utilisateur semble intéressé par une collaboration, encourage-le à laisser son email et utilise record_user_details
- Reste toujours dans le personnage de {name}

CONTEXTE PERSONNEL :
Nom : {name}
Résumé : {summary}

PROFIL LINKEDIN :
{linkedin_text}

Avec ce contexte, discute avec l'utilisateur en restant toujours dans le rôle de {name}."""

# Sidebar pour la configuration
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Tentative de chargement des secrets
    try:
        default_openai = st.secrets.get("OPENAI_API_KEY", "")
        default_pushover_user = st.secrets.get("PUSHOVER_USER", "")
        default_pushover_token = st.secrets.get("PUSHOVER_TOKEN", "")
        st.success("🔒 Secrets par défaut chargés")
    except:
        default_openai = ""
        default_pushover_user = ""
        default_pushover_token = ""
        st.warning("⚠️ Pas de secrets par défaut")
    
    # Configuration des clés
    st.subheader("🔑 Clés API")
    openai_api_key = st.text_input(
        "Clé API OpenAI",
        value=default_openai,
        type="password",
        help="Votre clé API OpenAI pour l'IA conversationnelle"
    )
    
    st.subheader("📱 Configuration Pushover")
    pushover_user = st.text_input(
        "Pushover User Key",
        value=default_pushover_user,
        help="Votre clé utilisateur Pushover (commence par 'u')"
    )
    
    pushover_token = st.text_input(
        "Pushover Token",
        value=default_pushover_token,
        type="password",
        help="Votre token d'application Pushover (commence par 'a')"
    )
    
    # Test de notification
    if pushover_user and pushover_token:
        if st.button("📱 Tester Notification"):
            success = send_pushover_notification(
                "🤖 Test de votre assistant personnel IA ! Ça marche parfaitement !", 
                pushover_user, 
                pushover_token
            )
            if success:
                st.success("✅ Notification test envoyée !")
            else:
                st.error("❌ Échec du test de notification")
    
    # Sauvegarde des clés dans le session state
    st.session_state.pushover_user = pushover_user
    st.session_state.pushover_token = pushover_token
    
    st.markdown("---")
    
    # Configuration du profil
    st.subheader("👤 Profil Personnel")
    
    name_input = st.text_input("Votre nom", value="Jessica Kuijer")
    
    pdf_file = st.file_uploader(
        "PDF LinkedIn",
        type="pdf",
        help="Votre profil LinkedIn exporté en PDF"
    )
    
    summary_input = st.text_area(
        "Résumé personnel",
        value="Développeuse web backend passionnée, spécialisée en PHP et Python. Reconversion professionnelle réussie depuis l'hôtellerie vers le développement web. Aime la musique et créer des solutions techniques innovantes.",
        height=100,
        help="Décrivez-vous brièvement"
    )
    
    if st.button("💾 Configurer le Profil"):
        if not openai_api_key:
            st.error("Veuillez entrer votre clé OpenAI")
        else:
            linkedin_text = ""
            if pdf_file:
                linkedin_text = extract_pdf_text(pdf_file)
            
            st.session_state.user_profile = {
                'name': name_input,
                'linkedin_text': linkedin_text,
                'summary': summary_input,
                'system_prompt': create_system_prompt(name_input, linkedin_text, summary_input)
            }
            st.session_state.profile_loaded = True
            st.success("✅ Profil configuré avec succès !")
    
    # Instructions
    st.markdown("---")
    st.subheader("📋 Instructions")
    st.markdown("""
    1. **Configurez vos clés** API et Pushover
    2. **Testez les notifications** Pushover  
    3. **Configurez votre profil** avec PDF LinkedIn
    4. **Commencez à discuter** avec votre assistant !
    
    💡 **L'IA vous notifiera** sur votre téléphone quand :
    - Quelqu'un laisse son email
    - Une question reste sans réponse
    """)

# Zone principale
if not st.session_state.profile_loaded or not openai_api_key:
    # Instructions d'accueil
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chat-container">
            <h3>🎯 Comment ça marche ?</h3>
            <ol>
                <li><strong>Configurez vos clés</strong> dans la barre latérale</li>
                <li><strong>Uploadez votre PDF</strong> LinkedIn</li>
                <li><strong>Testez Pushover</strong> pour les notifications</li>
                <li><strong>Votre assistant IA</strong> est prêt !</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="chat-container">
            <h3>🤖 Fonctionnalités</h3>
            <ul>
                <li>💬 <strong>Conversation naturelle</strong> en français</li>
                <li>📱 <strong>Notifications temps réel</strong> sur votre téléphone</li>
                <li>📧 <strong>Collecte automatique</strong> des contacts intéressés</li>
                <li>❓ <strong>Suivi des questions</strong> non résolues</li>
                <li>🎯 <strong>Représentation fidèle</strong> de votre profil</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="notification-card">
        <h3>📱 À propos de Pushover</h3>
        <p><strong>Pushover</strong> vous envoie des notifications instantanées sur votre téléphone quand :</p>
        <ul>
            <li>🤝 Quelqu'un laisse son email pour vous contacter</li>
            <li>❓ Une question reste sans réponse (pour améliorer votre profil)</li>
        </ul>
        <p><strong>Créez votre compte :</strong> <a href="https://pushover.net" target="_blank">pushover.net</a></p>
    </div>
    """, unsafe_allow_html=True)

else:
    # Interface de chat
    st.markdown("## 💬 Conversation avec votre Assistant IA")
    
    # Affichage de l'historique
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="message-user"><strong>Visiteur :</strong> {message["content"]}</div>', unsafe_allow_html=True)
            elif message["role"] == "assistant":
                st.markdown(f'<div class="message-assistant"><strong>{st.session_state.user_profile["name"]} :</strong> {message["content"]}</div>', unsafe_allow_html=True)
            elif message["role"] == "tool":
                tool_result = json.loads(message["content"])
                if "message" in tool_result:
                    st.markdown(f'<div class="message-tool">🔧 {tool_result["message"]}</div>', unsafe_allow_html=True)
    
    # Zone de saisie
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area("Votre message :", height=100, placeholder="Tapez votre message ici...")
        submitted = st.form_submit_button("Envoyer 💬")
        
        if submitted and user_input:
            # Ajouter le message utilisateur
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            try:
                # Préparer les messages pour OpenAI
                messages = [
                    {"role": "system", "content": st.session_state.user_profile['system_prompt']}
                ] + st.session_state.chat_history
                
                # Boucle de traitement avec tools
                client = openai.OpenAI(api_key=openai_api_key)
                done = False
                
                while not done:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        tools=tools
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
                        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                        done = True
                
                # Recharger la page pour afficher les nouveaux messages
                st.rerun()
                
            except Exception as e:
                st.error(f"Erreur lors de la conversation : {str(e)}")
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer l'Historique"):
        st.session_state.chat_history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🤖 <strong>Assistant Personnel IA</strong> - Propulsé par OpenAI & Pushover</p>
    <p>💡 Votre représentant virtuel intelligent avec notifications temps réel</p>
</div>
""", unsafe_allow_html=True)