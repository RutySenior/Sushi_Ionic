from flask import Flask, request, jsonify
from flask_cors import CORS
from databasewrapper import DatabaseWrapper

app = Flask(__name__)
CORS(app)
db = DatabaseWrapper()

# --- API PUBBLICHE (CLIENTE) ---

@app.route('/api/categorie', methods=['GET'])
def get_categorie():
    return jsonify(db.get_tutte_categorie())

@app.route('/api/menu', methods=['GET'])
def get_menu():
    return jsonify(db.get_menu_completo())

@app.route('/api/ordina', methods=['POST'])
def ordina():
    data = request.json # {codice_tavolo, utente_nome, prodotti: [{id, quantita}]}
    tavolo_id = db.get_id_tavolo_da_codice(data['codice_tavolo'])
    id_ordine = db.crea_nuovo_ordine(tavolo_id, data['utente_nome'], data['prodotti'])
    return jsonify({"messaggio": "Ordine ricevuto", "id": id_ordine})

@app.route('/api/stato-tavolo/<codice_tavolo>', methods=['GET'])
def stato_tavolo(codice_tavolo):
    return jsonify(db.get_ordini_per_tavolo(codice_tavolo))

# --- API STAFF (PANNELLO ADMIN) ---

@app.route('/api/staff/ordini', methods=['GET'])
def get_ordini_staff():
    return jsonify(db.get_tutti_ordini_staff())

@app.route('/api/staff/ordine-stato', methods=['PATCH'])
def cambia_stato():
    data = request.json
    db.aggiorna_stato_ordine(data['id_ordine'], data['nuovo_stato'])
    return jsonify({"status": "ok"})

@app.route('/api/staff/menu', methods=['POST'])
def aggiungi_piatto():
    d = request.json
    db.inserisci_prodotto(d['nome'], d['prezzo'], d['immagine_url'], d['categoria_id'])
    return jsonify({"status": "creato"})

@app.route('/api/staff/menu/<int:id>', methods=['DELETE'])
def elimina_piatto(id):
    db.elimina_prodotto(id)
    return jsonify({"status": "eliminato"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)