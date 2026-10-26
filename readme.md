# 🏡 Greco Immobiliare - Full-Stack Real Estate Management System

Un'applicazione web dinamica e moderna sviluppata per la gestione completa di un'agenzia immobiliare. Il progetto, nato originariamente in HTML statico, è stato migrato a un'architettura **Full-Stack** basata su **Flask (Python)** e **MySQL**, con un'interfaccia utente responsive realizzata in **Bootstrap 5**.

---

## 🚀 Tecnologie Utilizzate

* **Backend:** Python, Flask, Flask-CORS, Werkzeug
* **Database:** MySQL (gestione relazionale di immobili e messaggi)
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (Fetch API)
* **Gestione Media:** Upload locale sicuro per immagini multiple e video promozionali

---

## ✨ Funzionalità Principali

### 🌐 Lato Pubblico (Client-Side)
* **Home Page Dinamica:** Presentazione dell'agenzia con slideshow di sfondi e form di ricerca avanzata.
* **Filtri di Ricerca in Tempo Reale:** Possibilità di filtrare gli immobili per **Tipologia**, **Via/Indirizzo**, **Numero Civico** e **Prezzo Massimo**.
* **Catalogo Proprietà (`/proprieta`):** Caricamento dinamico degli annunci direttamente dal database MySQL, completi di carosello interattivo per la visualizzazione di foto multiple e riproduzione video integrata.
* **Form di Contatto e Candidature:** Moduli interattivi protetti da GDPR (`/contatti` e `/lavoraconnoi`) collegati al backend per il salvataggio dei messaggi e dei CV degli utenti.
* **Navigazione Fluida:** Sistema di routing server-side tramite Flask che elimina definitivamente gli errori 404 dovuti ai vecchi collegamenti statici.

### 🛠️ Pannello di Amministrazione (`/admin`)
* **Dashboard CRUD:** Interfaccia riservata agli amministratori per gestire l'inventario immobiliare.
* **Inserimento e Modifica Avanzata:** Possibilità di caricare nuovi immobili, aggiornare quelli esistenti e aggiungere nuove immagini (con accumulo automatico senza sovrascrivere le foto precedenti) o video.
* **Eliminazione Sicura:** Rimozione degli immobili dal database e dalla vista pubblica con un semplice click.

---

## 📂 Struttura del Database MySQL

Il sistema si appoggia su un database denominato `agenziaimmobiliaregreco` composto da due tabelle principali:
1. **`immobili`**: Memorizza i dettagli degli immobili (titolo, tipo contratto, tipologia, via, civico, prezzo, descrizione, percorsi immagini e video).
2. **`messaggi_contatti`**: Raccoglie le richieste inviate dai clienti tramite i form del sito, con supporto per il collegamento opzionale agli annunci specifici.

---

## ⚙️ Istruzioni per l'Installazione e l'Avvio

1. **Clona il repository:**
   ```bash
   git clone <URL_DEL_TUO_REPOSITORY>
   cd "Greco Immobiliare"