# 🤖 Jessica Kuijer - Assistant IA Personnel

Un chatbot intelligent qui me représente 24h/24 et m'envoie des notifications en temps réel sur mon téléphone via Pushover.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://votre-app.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 À Propos

Cet assistant IA me représente sur mon site web personnel et discute de ma carrière, mes compétences et mes projets avec les visiteurs. Il capture automatiquement les contacts intéressés et me notifie instantanément via Pushover.

**Développé par Jessica Kuijer** - Développeuse Backend PHP/Python passionnée, actuellement consultante chez Sia Experience.

## ✨ Fonctionnalités

### 🤖 Intelligence Conversationnelle
- **Conversation multilingue** en français (par défaut) et en anglais
- **Détection automatique** de la langue demandée par l'utilisateur
- **Traduction dynamique** du profil complet via OpenAI
- **Personnalité authentique** avec ma passion pour la musique et aversion pour les kiwis 🥝❌
- **Connaissance approfondie** de mon parcours et projets récents
- **Réponses personnalisées** basées sur mon profil LinkedIn
- **Conversation continue** après capture de contacts ou questions non résolues
- **Gestion robuste des erreurs** avec timeouts et retry automatique

### 📱 Notifications Temps Réel
- **Capture automatique** des contacts intéressés avec leurs emails et téléphones
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
- 📧 **Contact capturé** : "📧 NOUVEAU CONTACT pour Jessica ! 👤 Marc Dupont 📧 marc@entreprise.com 📱 06 12 34 56 78"
- ❓ **Question non résolue** : "❓ QUESTION NON RÉSOLUE ! Quelqu'un demande vos compétences en Kubernetes"

### Informations Capturées
L'assistant capture automatiquement :
- **👤 Nom** de l'utilisateur (si fourni)
- **📧 Email** (obligatoire pour le contact)
- **📱 Téléphone** (optionnel, pour rappel direct)
- **📝 Notes** sur le projet ou la demande
- **⏰ Timestamp** de la prise de contact

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

### 3. Configuration du Thème (Optionnel)
Le fichier `.streamlit/config.toml` est automatiquement créé pour forcer le thème clair. Si vous voulez personnaliser :

```toml
[theme]
base = "light"  # Forcer le thème clair
primaryColor = "#667eea"  # Couleur principale
backgroundColor = "#ffffff"  # Fond blanc
textColor = "#000000"  # Texte noir
```

### 4. Lancement
```bash
streamlit run app.py
```

## 🌐 Fonctionnalités Multilingues

### Détection Automatique de Langue
L'assistant détecte automatiquement quand l'utilisateur demande à Jessica de parler en anglais :

**Mots-clés déclencheurs :**
- 🇫🇷 **Français** : "parle français", "speak french", "change de langue"
- 🇬🇧 **Anglais** : "parle anglais", "speak english", "switch to english"

## 🎨 Interface et Thème

### Thème Clair Forcé
- **Mode clair par défaut** pour une lisibilité optimale sur tous les appareils
- **CSS personnalisé** avec couleurs forcées pour éviter les problèmes de contraste
- **Configuration Streamlit** via `.streamlit/config.toml` pour maintenir le thème
- **Amélioration de l'accessibilité** avec des couleurs de texte contrastées
- **Compatibilité multi-appareils** (mobile, tablette, desktop)

### Traduction Dynamique du Profil
- **Profil complet traduit** en temps réel via OpenAI
- **Maintien de la personnalité** authentique de Jessica
- **Cohérence linguistique** tout au long de la conversation
- **Basculement automatique** entre français et anglais

### Interface Adaptative
- **Indicateur de langue** dans la sidebar
- **Boutons de changement** manuel de langue
- **Messages de confirmation** lors du changement
- **Persistance de la langue** choisie dans la session

## 💬 Exemples d'Utilisation

### Conversation Professionnelle
**Visiteur :** "Quelles sont vos compétences en Python ?"  
**Assistant :** "Je suis spécialisée en développement backend Python, notamment avec des frameworks comme Django et Flask. J'ai une expérience significative en API REST, bases de données, et intégration de services tiers..."

### Conversation Continue et Naturelle
**Visiteur :** "J'ai un projet e-commerce à développer. Mon email est contact@entreprise.com"  
**Assistant :** "📧 Merci pour votre email ! Je l'ai noté pour vous recontacter. Parlons de votre projet e-commerce ! Quelles fonctionnalités souhaitez-vous ? Avez-vous une idée du budget et du délai ?"  
**→ Conversation continue** sur le projet après capture du contact

**Visiteur :** "Connaissez-vous Kubernetes ?"  
**Assistant :** "❓ Je n'ai pas encore d'expérience avec Kubernetes, mais j'ai noté cette question pour améliorer mon profil ! En attendant, je peux vous parler de mes compétences en Docker et déploiement que j'utilise actuellement..."  
**→ Conversation continue** sur d'autres sujets après enregistrement de la question

### Conversation Multilingue
**Visiteur :** "Can you speak English?"  
**Assistant :** "🇬🇧 Jessica will now respond in English! Of course! I'm Jessica Kuijer, a backend web developer specialized in PHP and Python. I'd be happy to discuss my skills and experience in English..."

**Visiteur :** "Parle français maintenant"  
**Assistant :** "🇫🇷 Jessica répondra maintenant en français ! Bien sûr, je peux continuer notre conversation en français..."

### Capture de Contact  
**Visiteur :** "Pouvez-vous me développer une application web ?"  
**Assistant :** "Je serais ravie de discuter de votre projet ! Pouvez-vous me donner votre email et votre téléphone pour que nous puissions échanger plus en détail ?"

**→ Notification immédiate** sur mon téléphone avec les détails du contact (email + téléphone).

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

### Version 2.0 - Intégrations Avancées ✅
- [x] **Support multilingue** - Conversation en français et anglais
- [x] **Traduction dynamique** - Profil traduit en temps réel
- [x] **Détection automatique** - Changement de langue intelligent
- [x] **Conversation continue** - Flux naturel après capture de contacts
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