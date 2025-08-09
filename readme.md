# 🤖 Jessica Kuijer - Assistant IA Personnel

Un chatbot intelligent qui me représente 24h/24 et m'envoie des notifications en temps réel sur mon téléphone via Pushover.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://votre-app.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 À Propos

Cet assistant IA me représente sur mon site web personnel et discute de ma carrière, mes compétences et mes projets avec les visiteurs. Il capture automatiquement les contacts intéressés et me notifie instantanément via Pushover.

**Développé par Jessica Kuijer** - Développeuse Backend PHP/Python passionnée, actuellement consultante chez Sia Experience.

## ✨ Fonctionnalités

### 🤖 Intelligence Conversationnelle
- **Conversation en français** sur ma carrière et mes compétences
- **Personnalité authentique** avec ma passion pour la musique et aversion pour les kiwis 🥝❌
- **Connaissance approfondie** de mon parcours et projets récents
- **Réponses personnalisées** basées sur mon profil LinkedIn
- **Gestion robuste des erreurs** avec timeouts et retry automatique

### 📱 Notifications Temps Réel
- **Capture automatique** des contacts intéressés avec leurs emails
- **Alertes Pushover enrichies** avec timestamps et contexte détaillé
- **Suivi des questions** non résolues pour améliorer mon profil
- **Compteurs en temps réel** des conversations et contacts
- **Test de notifications** intégré dans l'interface

### 🛡️ Sécurité et Confidentialité
- **Données personnelles protégées** (pas de coordonnées dans le code public)
- **Clés API sécurisées** via Streamlit Secrets avec validation
- **Conformité RGPD** avec consentement explicite
- **Pas de stockage permanent** des conversations
- **Protection contre les boucles infinies** avec limite d'itérations

## 🛠️ Technologies Utilisées

- **[Streamlit](https://streamlit.io)** - Interface web interactive
- **[OpenAI GPT-4o-mini](https://openai.com)** - Intelligence artificielle conversationnelle
- **[Pushover](https://pushover.net)** - Notifications mobile temps réel
- **[PyPDF](https://pypdf.readthedocs.io/)** - Traitement des documents LinkedIn
- **Python 3.8+** - Langage de programmation

## 📱 Comment Fonctionne Pushover

### Notifications Automatiques
L'assistant m'envoie des notifications instantanées quand :
- 📧 **Contact capturé** : "📧 NOUVEAU CONTACT pour Jessica ! 👤 Marc Dupont 📧 marc@entreprise.com"
- ❓ **Question non résolue** : "❓ QUESTION NON RÉSOLUE ! Quelqu'un demande vos compétences en Kubernetes"

### Configuration Simple
1. **Compte gratuit** sur [pushover.net](https://pushover.net)
2. **App mobile** installée (iOS/Android)
3. **Clés API** configurées dans l'assistant
4. **7,500 notifications/mois** gratuites
5. **Test intégré** pour vérifier le fonctionnement

## 🔧 Installation

### 1. Prérequis
```bash
git clone https://github.com/votre-username/jessica-ai-assistant
cd jessica-ai-assistant
pip install -r requirements.txt
```

### 2. Configuration des Secrets
Créez `.streamlit/secrets.toml` :
```toml
OPENAI_API_KEY = "sk-votre-cle-openai"
PUSHOVER_USER = "votre-user-key-pushover"
PUSHOVER_TOKEN = "votre-token-app-pushover"
CONTACT_EMAIL = "votre-email@domaine.com"
```

### 3. Lancement
```bash
streamlit run app.py
```

## 💬 Exemples d'Utilisation

### Conversation Professionnelle
**Visiteur :** "Quelles sont vos compétences en Python ?"  
**Assistant :** "Je suis spécialisée en développement backend Python, notamment avec des frameworks comme Django et Flask. J'ai une expérience significative en API REST, bases de données, et intégration de services tiers..."

### Capture de Contact  
**Visiteur :** "Pouvez-vous me développer une application web ?"  
**Assistant :** "Je serais ravie de discuter de votre projet ! Pouvez-vous me donner votre email pour que nous puissions échanger plus en détail ?"

**→ Notification immédiate** sur mon téléphone avec les détails du contact.

## 🎯 Cas d'Usage Professionnels

### Portfolio Intelligent
- **Disponibilité 24h/24** → Visiteurs peuvent me "rencontrer" à tout moment
- **Qualification automatique** → Contacts pré-qualifiés me parviennent
- **Amélioration continue** → Questions manquées = profil à enrichir

### Recherche d'Emploi  
- **Recruteurs curieux** → Conversation naturelle sur mes compétences
- **Capture de leads** → Emails des recruteurs intéressés automatiquement
- **Veille opportunités** → Questions récurrentes = compétences demandées

### Freelance/Consulting
- **Premiers contacts** → Qualification sans mon intervention
- **Pas de prospect perdu** → Capture même en dehors des heures bureau
- **Intelligence commerciale** → Analyse des demandes fréquentes

## 📊 Métriques et Analytics

L'assistant suit automatiquement :
- **Nombre de conversations** initiées
- **Contacts capturés** avec emails  
- **Questions non résolues** pour amélioration
- **Notifications envoyées** via Pushover

## 🔒 Sécurité et Conformité

### Protection des Données
- ✅ **Coordonnées personnelles** exclues du code public
- ✅ **Clés API** stockées de manière sécurisée
- ✅ **Pas de stockage permanent** des conversations
- ✅ **Consentement explicite** pour la capture d'emails
- ✅ **Gestion d'erreurs robuste** avec timeouts

### Bonnes Pratiques
- Secrets jamais committées dans Git
- Notifications chiffrées via HTTPS
- Respect des quotas API Pushover
- Rate limiting pour éviter les abus

## 🚀 Évolutions Futures

### Version 2.0 - Intégrations Avancées
- [ ] **Google Calendar** - Planification automatique de rendez-vous 
- [ ] **Analytics dashboard** - Statistiques détaillées des conversations
- [ ] **CRM simple** - Stockage et suivi des contacts

### Version 3.0 - Multi-Canal
- [ ] **WhatsApp Business API** - Extension du chat
- [ ] **Telegram Bot** - Canal supplémentaire
- [ ] **Widget embeddable** - Intégration sur d'autres sites

---

💡 **Envie de tester ?** Rendez-vous sur l'assistant : [**Discuter avec Jessica IA**](https://chatbot-jessicakuijer-ai.streamlit.app/)

⭐ **Ce projet vous inspire ?** N'hésitez pas à lui donner une étoile sur GitHub !