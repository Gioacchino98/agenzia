import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Gestisce le politiche CORS

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'mp4', 'mov', 'webm', 'avi'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    return mysql.connector.connect(**DB_CONFIG)


# ===========================================================
# ROTTE PER LE PAGINE HTML (Frontend)
# ===========================================================

@app.route("/")
def home():
    return render_template('agenziaimmobiliaregreco.html')


@app.route("/chisiamo")
def chisiamo():
    return render_template('chisiamo.html')


@app.route("/lavoraconnoi")
def lavoraconnoi():
    return render_template('Lavoraconnoi.html')


@app.route("/proprieta")
def proprieta():
    return render_template('proprieta.html')


@app.route("/contatti")
def contatti():
    return render_template('contatti.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


# ===========================================================
# ROTTE API (Backend REST)
# ===========================================================

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
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()


@app.route('/api/immobili', methods=['POST'])
def aggiungi_immobile():
    titolo = request.form.get('titolo')
    if not titolo:
        return jsonify({"success": False, "error": "Il campo 'titolo' è obbligatorio."}), 400

    tipo_contratto = request.form.get('tipo_contratto')
    tipologia = request.form.get('tipologia')
    via = request.form.get('via')
    civico = request.form.get('civico')
    prezzo = request.form.get('prezzo') or 0
    descrizione = request.form.get('descrizione')

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    immagini_salvate = []
    if 'immagini' in request.files:
        files = request.files.getlist('immagini')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                immagini_salvate.append(f"/static/uploads/{filename}")
    immagini_str = ",".join(immagini_salvate)

    video_url_path = None
    if 'video_file' in request.files:
        video_file = request.files['video_file']
        if video_file and allowed_file(video_file.filename):
            video_filename = secure_filename(video_file.filename)
            video_path = os.path.join(UPLOAD_FOLDER, video_filename)
            video_file.save(video_path)
            video_url_path = f"/static/uploads/{video_filename}"

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
        val = (titolo, tipo_contratto, tipologia, via, civico, prezzo, descrizione, immagini_str, video_url_path)

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
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()


@app.route('/api/immobili/<int:immobile_id>', methods=['PUT'])
def aggiorna_immobile(immobile_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT immagini FROM immobili WHERE id = %s", (immobile_id,))
        esistente = cursor.fetchone()
        if not esistente:
            return jsonify({"success": False, "error": "Immobile non trovato."}), 404

        immagini_esistenti = esistente['immagini'] or ""

        titolo = request.form.get('titolo')
        tipo_contratto = request.form.get('tipo_contratto')
        tipologia = request.form.get('tipologia')
        via = request.form.get('via')
        civico = request.form.get('civico')
        prezzo = request.form.get('prezzo') or 0
        descrizione = request.form.get('descrizione')

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        nuove_immagini = []
        if 'immagini' in request.files:
            files = request.files.getlist('immagini')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    nuove_immagini.append(f"/static/uploads/{filename}")

        if nuove_immagini:
            nuove_str = ",".join(nuove_immagini)
            if immagini_esistenti:
                immagini_finali = immagini_esistenti + "," + nuove_str
            else:
                immagini_finali = nuove_str
        else:
            immagini_finali = immagini_esistenti

        video_url_path = None
        if 'video_file' in request.files:
            video_file = request.files['video_file']
            if video_file and allowed_file(video_file.filename):
                video_filename = secure_filename(video_file.filename)
                video_path = os.path.join(UPLOAD_FOLDER, video_filename)
                video_file.save(video_path)
                video_url_path = f"/static/uploads/{video_filename}"

        if video_url_path:
            sql = """
                  UPDATE immobili
                  SET titolo=%s, \
                      tipo_contratto=%s, \
                      tipologia=%s, \
                      via=%s, \
                      civico=%s, \
                      prezzo=%s, \
                      descrizione=%s, \
                      immagini=%s, \
                      video_url=%s
                  WHERE id = %s
                  """
            val = (titolo, tipo_contratto, tipologia, via, civico, prezzo, descrizione, immagini_finali, video_url_path,
                   immobile_id)
        else:
            sql = """
                  UPDATE immobili
                  SET titolo=%s, \
                      tipo_contratto=%s, \
                      tipologia=%s, \
                      via=%s, \
                      civico=%s, \
                      prezzo=%s, \
                      descrizione=%s, \
                      immagini=%s
                  WHERE id = %s
                  """
            val = (titolo, tipo_contratto, tipologia, via, civico, prezzo, descrizione, immagini_finali, immobile_id)

        cursor.execute(sql, val)
        conn.commit()
        return jsonify({"success": True, "message": "Immobile aggiornato con successo!"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()


@app.route('/api/immobili/<int:immobile_id>', methods=['DELETE'])
def elimina_immobile(immobile_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM immobili WHERE id = %s"
        cursor.execute(sql, (immobile_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Immobile non trovato."}), 404

        return jsonify({"success": True, "message": "Immobile eliminato con successo!"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()


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
        val = (data.get('nome'), data.get('email'), data.get('telefono'), data.get('messaggio'),
               data.get('immobile_id'))

        cursor.execute(sql, val)
        conn.commit()
        return jsonify({"success": True, "message": "Messaggio inviato con successo!"}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)