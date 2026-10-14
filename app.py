import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Gestisce le politiche CORS per permettere le chiamate JavaScript/AJAX

# ===========================================================
# CONFIGURAZIONE DATABASE MYSQL
# ===========================================================
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "24081998ggg"),
    "database": os.environ.get("DB_NAME", "agenziaimmobiliaregreco")
}


def get_db_connection():
    """Crea e restituisce la connessione al database MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


# ===========================================================
# ROTTE PER LE PAGINE HTML (Frontend)
# ===========================================================

@app.route("/")
def home():
    """Pagina principale (Home Page)"""
    return render_template('agenziaimmobiliaregreco.html')


@app.route("/chisiamo")
def chisiamo():
    """Pagina Chi Siamo"""
    return render_template('chisiamo.html')


@app.route("/lavoraconnoi")
def lavoraconnoi():
    """Pagina Lavora Con Noi"""
    return render_template('Lavoraconnoi.html')


@app.route("/proprieta")
def proprieta():
    """Pagina del catalogo Proprietà"""
    return render_template('proprieta.html')


@app.route("/contatti")
def contatti():
    """Pagina dei Contatti"""
    return render_template('contatti.html')


@app.route("/admin")
def admin():
    """Pagina del Pannello Amministratore"""
    return render_template('admin.html')


# ===========================================================
# ROTTE API (Backend REST)
# ===========================================================

# -----------------------------------------------------------
# API 1: Ottenere la lista degli immobili (o un singolo immobile tramite ?id=)
# -----------------------------------------------------------
@app.route('/api/immobili', methods=['GET'])
def get_immobili():
    immobile_id = request.args.get('id')
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if immobile_id:
            cursor.execute("SELECT * FROM immobili WHERE id = %s", (immobile_id,))
            immobile = cursor.fetchone()
            if not immobile:
                return jsonify({"error": "Immobile non trovato"}), 404
            return jsonify(immobile), 200
        else:
            cursor.execute("SELECT * FROM immobili ORDER BY data_inserimento DESC")
            immobili = cursor.fetchall()
            return jsonify(immobili), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# -----------------------------------------------------------
# API 2: Aggiungere un nuovo immobile (Pannello Admin/Aggiunta)
# -----------------------------------------------------------
@app.route('/api/immobili', methods=['POST'])
def aggiungi_immobile():
    data = request.json

    # Validazione base dei dati richiesti
    if not data or not data.get('titolo'):
        return jsonify({"success": False, "error": "Il campo 'titolo' è obbligatorio."}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
              INSERT INTO immobili
              (titolo, tipo_contratto, tipologia, via, civico, prezzo, descrizione, immagini, video_url)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
        val = (
            data.get('titolo'),
            data.get('tipo_contratto'),
            data.get('tipologia'),
            data.get('via'),
            data.get('civico'),
            data.get('prezzo'),
            data.get('descrizione'),
            data.get('immagini'),
            data.get('video_url')
        )

        cursor.execute(sql, val)
        conn.commit()
        return jsonify({
            "success": True,
            "message": "Immobile inserito con successo!",
            "id": cursor.lastrowid
        }), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# -----------------------------------------------------------
# API 3: Ricezione messaggi dal modulo di contatto
# -----------------------------------------------------------
@app.route('/api/contatti', methods=['POST'])
def invia_contatto():
    data = request.json

    if not data or not data.get('nome') or not data.get('email') or not data.get('messaggio'):
        return jsonify({"success": False, "error": "I campi nome, email e messaggio sono obbligatori."}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
              INSERT INTO messaggi_contatti (nome, email, telefono, messaggio, immobile_id)
              VALUES (%s, %s, %s, %s, %s)
              """
        val = (
            data.get('nome'),
            data.get('email'),
            data.get('telefono'),
            data.get('messaggio'),
            data.get('immobile_id')
        )

        cursor.execute(sql, val)
        conn.commit()
        return jsonify({"success": True, "message": "Messaggio inviato con successo!"}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ===========================================================
# AVVIO SERVER
# ===========================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)