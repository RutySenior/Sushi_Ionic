import pymysql

class DatabaseWrapper:
    def __init__(self):
        self.config = {
            'host': 'mysql-221cedb1-iisgalvanimi-9701.j.aivencloud.com',
            'user': 'avnadmin',
            'password': 'AVNS_v5ZY1LueloCJza2Bkdd', # Inserisci la tua password
            'database': 'sushi_db',
            'cursorclass': pymysql.cursors.DictCursor
        }

    def __execute_read(self, query, params=None):
        conn = pymysql.connect(**self.config)
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def __execute_write(self, query, params=None):
        conn = pymysql.connect(**self.config)
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

    # --- CATEGORIE ---
    def get_tutte_categorie(self):
        return self.__execute_read("SELECT * FROM categorie")

    # --- MENU (PRODOTTI) ---
    def get_menu_completo(self):
        return self.__execute_read("""
            SELECT p.*, c.nome as categoria_nome 
            FROM prodotti p 
            JOIN categorie c ON p.categoria_id = c.id
        """)

    def inserisci_prodotto(self, nome, prezzo, immagine_url, categoria_id):
        sql = "INSERT INTO prodotti (nome, prezzo, immagine_url, categoria_id) VALUES (%s, %s, %s, %s)"
        return self.__execute_write(sql, (nome, prezzo, immagine_url, categoria_id))

    def modifica_prodotto(self, id_prodotto, nome, prezzo, immagine_url, categoria_id):
        sql = "UPDATE prodotti SET nome=%s, prezzo=%s, immagine_url=%s, categoria_id=%s WHERE id=%s"
        return self.__execute_write(sql, (nome, prezzo, immagine_url, categoria_id, id_prodotto))

    def elimina_prodotto(self, id_prodotto):
        return self.__execute_write("DELETE FROM prodotti WHERE id=%s", (id_prodotto,))

    # --- TAVOLI E ORDINI ---
    def get_id_tavolo_da_codice(self, codice_tavolo):
        res = self.__execute_read("SELECT id FROM tavoli WHERE codice_tavolo = %s", (codice_tavolo,))
        if res:
            return res[0]['id']
        return self.__execute_write("INSERT INTO tavoli (codice_tavolo) VALUES (%s)", (codice_tavolo,))

    def crea_nuovo_ordine(self, tavolo_id, utente_nome, lista_prodotti):
        # Inserisce la testata
        ordine_id = self.__execute_write(
            "INSERT INTO ordini (tavolo_id, utente_nome, stato) VALUES (%s, %s, 'Inviato')",
            (tavolo_id, utente_nome)
        )
        # Inserisce i dettagli (ciclo sui prodotti scelti)
        for p in lista_prodotti:
            self.__execute_write(
                "INSERT INTO ordine_dettagli (ordine_id, prodotto_id, quantita) VALUES (%s, %s, %s)",
                (ordine_id, p['id'], p['quantita'])
            )
        return ordine_id

    def get_tutti_ordini_staff(self):
        # Per il pannello staff: vede tutto raggruppato
        return self.__execute_read("""
            SELECT o.id, o.utente_nome, o.stato, o.data_ora, t.codice_tavolo,
                   GROUP_CONCAT(CONCAT(p.nome, ' x', od.quantita) SEPARATOR ', ') as dettaglio_piatti
            FROM ordini o
            JOIN tavoli t ON o.tavolo_id = t.id
            JOIN ordine_dettagli od ON o.id = od.ordine_id
            JOIN prodotti p ON od.prodotto_id = p.id
            GROUP BY o.id
            ORDER BY o.data_ora DESC
        """)

    def get_ordini_per_tavolo(self, codice_tavolo):
        # Per l'app cliente: vede solo il suo tavolo
        return self.__execute_read("""
            SELECT o.id, o.utente_nome, o.stato, o.data_ora
            FROM ordini o
            JOIN tavoli t ON o.tavolo_id = t.id
            WHERE t.codice_tavolo = %s
            ORDER BY o.data_ora DESC
        """, (codice_tavolo,))

    def aggiorna_stato_ordine(self, ordine_id, nuovo_stato):
        return self.__execute_write("UPDATE ordini SET stato = %s WHERE id = %s", (nuovo_stato, ordine_id))