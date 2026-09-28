# 🔎 Network Port Scanner

Un scanner de ports TCP développé en Python **Réseaux et 
Cybersécurité**.

Le projet permet d'analyser une cible autorisée, d'identifier les ports TCP ouverts, d'associer 
certains ports à leurs services courants et d'exporter les résultats dans un rapport texte.

---

## 🎯 Objectifs

Ce projet a été conçu pour mettre en pratique plusieurs concepts de réseaux et de cybersécurité :

- Communication TCP/IP
- Analyse des ports réseau
- Programmation Python
- Programmation concurrente
- Gestion des timeouts réseau
- Validation des entrées utilisateur
- Identification de services
- Gestion des erreurs
- Tests automatisés
- Gestion de versions avec Git
- Publication d'un projet avec GitHub

---

## ✨ Fonctionnalités

### 🔌 Scan TCP

Le scanner teste une plage de ports TCP sur une adresse IPv4.

Exemple :

```bash
python3 scanner.py 127.0.0.1 20 100
