from database.DB_connect import DBConnect
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



    @staticmethod
    def getEdgesPeso(v1, v2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []  # E' una lista di ...
        query = """ 
                    select eo1.object_id as o1, eo2.object_id as o2, count(*) as peso
                    from exhibition_objects eo1, exhibition_objects eo2  
                    where eo1.exhibition_id = eo2.exhibition_id
                    and eo1.object_id < eo2.object_id 
                    and eo1.object_id = %s and eo2.object_id = %s
                    group by eo1.object_id, eo2.object_id
                """
        cursor.execute(query, (v1, v2))


        for row in cursor:
            res.append(ArtObject(**row))


        cursor.close()
        conn.close()
        return res