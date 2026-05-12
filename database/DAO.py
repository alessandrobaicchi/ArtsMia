from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():

    # Questo è il "prototipo" di un metodo del DAO
    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []    # E' una lista di artObject
        query = """ select *
                    from objects o """
        cursor.execute(query)
        # Questa query ci restituisce le righe del result set sotto forma di dizionario, quindi row sarà un dizionario.
        # E io osso fare l'unpacking di questo dizionario con la notazione doppio asterisco (**).

        # ------------------------ Come impacchetto i dati in output restituiti dal DB? ----------------------------
        # Creo un DTO associato alle righe delle tabelle che sto leggendo.
        # Per mappare per bene il database in Python dovremmo creare un DTO per ogni tabella che CONTIENE DATI.
        # In questo caso un DTO per artists, un DTO per objects e un DTO per exibitions.
        # ----------------------------------------------------------------------------------------------------------

        for row in cursor:
            res.append(ArtObject(**row))
            # Alla fine **row non fa altro che fare:
            # res.append(ArtObject(object_id = row["object_id"], ...))

        cursor.close()
        conn.close()
        return res



    # Con questo metodo, per ogni coppia di nodi passati, si calcola il peso tra questa coppia.
    @staticmethod
    def getEdgesPeso(v1, v2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        # Questa query, dati due ID dà il peso.
        query = """ 
                    select eo1.object_id as o1, eo2.object_id as o2, count(*) as peso
                    from exhibition_objects eo1, exhibition_objects eo2  
                    where eo1.exhibition_id = eo2.exhibition_id
                    and eo1.object_id < eo2.object_id 
                    and eo1.object_id = %s and eo2.object_id = %s
                    group by eo1.object_id, eo2.object_id
                """
        cursor.execute(query, (v1.object_id, v2.object_id))
        # I parametri v1 e v2 passati al metodo sono degli artObject.
        # Ma alla query devo passargli gli id dei due artObject.

        for row in cursor:
            res.append(row["peso"])

        cursor.close()
        conn.close()

        # Può capitare che non ci sia un peso per la coppia di oggetti analizzata, e questo lo devo gestire.
        # E' importante mettere questo if DOPO i due .close(), perché l'if ha una return. Se invece metto
        # prima l'if Python mi dà errore di chiusura della connessione (pool...).
        if len(res) == 0:
            return None

        return res



    # Questo metodo modifica la query rispetto a quella in getEdgesPeso() e conseguentemente non più parametrico
    @staticmethod
    def getAllEdges(idMapAO):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []    # Alla fine sarà una lista che contiene gli archi(ArtObject1, ArtObject2, peso)
        # Questa query, dati due ID dà il peso.
        query = """
                    select eo1.object_id as o1, eo2.object_id as o2, count(*) as peso
                    from exhibition_objects eo1, exhibition_objects eo2  
                    where eo1.exhibition_id = eo2.exhibition_id
                    and eo1.object_id < eo2.object_id 
                    group by eo1.object_id, eo2.object_id  
                    order by peso desc
                """
        cursor.execute(query)

        for row in cursor:
            # Posso rappresentare l'output della query come segue oppure definire una classe ad hoc (Arco)
            #res.append((o1, o2, peso))

            #res.append(Arco(o1, o2, row["peso"]))
            # Chi sono o1 e o2?
            # Per scelta, ho deciso che nella classe Arco ci siano artObject. Però l'output della query sono object_id.
            # Devo recuperare i dettagli dello oggetto artObject, e ci sono due modi per farlo.
            # 1) Complico ulteriormente la query (facendo dei join).
            # 2) Assumo di passare a getAllEdges() un idMap contenente tutti gli artObject.
            #    Questo idMap ha come chiavi tutti gli object_id e come valori l'artObject associato.
            # Seguo la strada 2) e il risultato è il seguente.
            res.append(Arco(idMapAO[row["o1"]], idMapAO[row["o2"]], row["peso"]))
            # Quindi mi recupero il campo o1 da row, e poi mi recupero l'artObject dalla chiave primaria dell'artObject.
        cursor.close()
        conn.close()

        # Può capitare che non ci sia un peso per la coppia di oggetti analizzata, e questo lo devo gestire.
        # E' importante mettere questo if DOPO i due .close(), perché l'if ha una return. Se invece metto
        # prima l'if Python mi dà errore di chiusura della connessione (pool...).
        if len(res) == 0:
            return None

        return res