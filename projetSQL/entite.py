class Produit:
    def __init__(self,conn,nom,prix,type_prod,produits_id=None):
        self.nom = nom 
        self.type_prod = type_prod
        self.prix = prix
        self.produits_id = produits_id
        self.conn = conn
    def ajouter_en_base(self):
        cur = self.conn.cursor()
        cur.execute("insert into produits (nom,prix,type_prod) values (?,?,?);",
        (self.nom,self.prix,self.type_prod))
        self.conn.commit()
        self.produits_id = cur.lastrowid
    @staticmethod
    def modifier_prix(conn,prix,id):
        cur = conn.cursor()
        cur.execute("update produits set prix = ? where produits_id = ?;",(prix,id))
        conn.commit()
    @staticmethod
    def supprimer(conn,id):
        cur = conn.cursor()
        cur.execute("delete from produits where produits_id = ?;",(id,))
        conn.commit()
    @staticmethod
    def recuperer_prix_par_id(conn, produits_id):
        cur = conn.cursor()
        cur.execute("SELECT prix FROM produits WHERE produits_id = ?;", (produits_id,))
        view = cur.fetchone()
        return view 

from werkzeug.security import generate_password_hash,check_password_hash
from sqlite3 import IntegrityError
class Clients:
    def __init__(self,conn,nom,prenom,email,mdp_hash,adresse=None,clients_id=None):
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.clients_id = clients_id
        self.conn = conn
        self.email = str.lower(email)
        self.mdp_hash = generate_password_hash(mdp_hash)
    def ajouter_en_base(self):
        cur = self.conn.cursor()
        try:
            cur.execute("insert into clients (nom,prenom,adresse,email,mdp_hash) values (?,?,?,?,?);",(self.nom,self.prenom,self.adresse,self.email,self.mdp_hash))
        except IntegrityError:
            message = {"message":"Cet email existe déjà"}
            return (message,400)
        self.conn.commit()
        self.clients_id = cur.lastrowid
        message = {"message":"Création du compte réussie."}
        return (message,200)
    @staticmethod
    def modifier_client(conn,nom,prenom,adresse,id):
        cur = conn.cursor()
        cur.execute("update clients set nom = ?, prenom = ?, adresse = ? where clients_id = ?;",(nom,prenom,adresse,id))
        conn.commit()
    @staticmethod
    def supprimer(conn,id):
        cur = conn.cursor()
        cur.execute("delete from clients where clients_id = ?;",(id,))
        conn.commit()
    @staticmethod
    def connexion(conn,email,mdp):
        email = str.lower(email)
        cur = conn.cursor()
        cur.execute("select mdp_hash,clients_id from clients where email = ?",(email,))
        view = cur.fetchone()
        if view is None:
            message = {"message":"email ou mot de passe incorrect."}
            return (message,400)
        else:
            check = check_password_hash(view[0],mdp)
            if check == True:
                message = {"message":"Authentification réussie.",
                           "id":view[1]}
                return (message,200)
            else:
                message = {"message":"email ou mot de passe incorrect."}
                return (message,400)

class Commandes:
    def __init__(self,conn,date_comm,clients_id,liste_produits,commandes_id=None):
        self.conn = conn
        self.date_comm = date_comm
        self.clients_id = clients_id
        self.commandes_id = commandes_id
        self.liste_produits = liste_produits
    def ajouter_en_base(self):      
        cur = self.conn.cursor()
        cur.execute("insert into commandes (date_comm,clients_id) values (?,?);",(self.date_comm,self.clients_id))
        self.conn.commit()
        self.commandes_id= cur.lastrowid
        for produits_id , quantite , prix_unitaire in self.liste_produits:
            self.ajouter_commandes(produits_id,quantite,prix_unitaire)
    def ajouter_commandes(self,produits_id,quantite,prix_unitaire): 
        cur = self.conn.cursor()
        cur.execute("insert into details_comm (commandes_id,produits_id,quantite,prix_unitaire) values (?,?,?,?);",(self.commandes_id,produits_id,quantite,prix_unitaire))
        self.conn.commit()
    @staticmethod
    def afficher(conn,id):
        cur = conn.cursor()
        requete = """select cl.nom,cl.prenom,cl.adresse,p.produits_id,p.nom,p.type_prod,c.date_comm,c.commandes_id,d.quantite,d.prix_unitaire
        from clients as cl
        join commandes as c on c.clients_id = cl.clients_id
        join details_comm as d on d.commandes_id = c.commandes_id
        join produits as p on p.produits_id = d.produits_id
        where c.commandes_id = ?;
        """
        cur.execute(requete,(id,))
        view= cur.fetchall()
        return view,cur
    @staticmethod
    def modifier(conn, date_comm, clients_id, id):
        cur = conn.cursor()
        cur.execute("update commandes set date_comm = ?, clients_id = ? where commandes_id = ?;", (date_comm, clients_id, id))
        conn.commit()
    
    @staticmethod
    def supprimer(conn, id):
        cur = conn.cursor()
        cur.execute("delete from details_comm where commandes_id = ?;", (id,))
        cur.execute("delete from commandes where commandes_id = ?;", (id,))
        conn.commit()


def liste_produits(conn):
    cur = conn.cursor()
    cur.execute("select * from produits")
    view = cur.fetchall()
    return view

IMAGES_PRODUITS = {
    "Riz (sac 25kg)":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3T4QXSf5BIkwVSlElHthzbKnSPvTOLwvKbgjBsky1AA&s=10" , 
    "Huile végétale (5L)": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ81emGOdiyINW44IrIOpeMIedzOp6cwgl9w6hFeIA-gg&s=10",
    "Sucre (1kg)": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3h06wWEJM-1CMWlJ5mdp4ECxrINDnPwq2lyudjt0aLw&s=10",
    "Farine de blé (1kg)": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGd98B44Qvgl5lMrrR7uUkmBO2zAew4bIUKz9f4jE3_w&s=10" , 
    "Lait en poudre (400g)": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSk6-enq8J_GaYurAZpf9R0-eYJBRTst3Cj-cpTH4U0Ug&s", 
    "Pâtes alimentaires (500g)": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcZBsOZABqxYXKagLfVCkl28MmNnWYfjBdHcqpZAJSag&s=10" ,
    "Tomate concentrée (boîte)": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRu3IGGNWUvpyjPyx37fn8rFQi8kQie44KCyR1zIAPkFw&s=10", 
    "Riz (sac 5kg)": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTFpjhzX27s83owKj78TKrZvbGSj3ejZGGJBdRLK9TOA&s=10",
    "Riz parfumé (sac 10kg)":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTekgjbgbtsTcR-GyJlNvdVRIGrMjn66_wNkPKUpKTjZg&s=10",
    "Haricot rouge (1kg)":"   https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQe6DZbwvnjnKlwFF4zf1IGOZLdlFm6BIniaJW2tp0IUw&s=10",
    "Maïs moulu (1kg)":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZEOSoIFDgEEGZLNuLyajVFIrvncz4z7O7Zs4MBGLxfQ&s=10",
    "Semoule de blé (1kg)":"      https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRC7o4u-jjS_Z5VVbAK41pD_lDe5CjMZ9h0s1T6XQHePg&s=10",
    "Oignons (filet 5kg)":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTjaCEinbi8SneJkWHZtASw_JHkrjZO9alv-eTdRQsEbw&s=10",
    "Pomme de terre (5kg)":"        https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzLy2HD4z5AK5ahyqBY5ej3u4RPZvVwKC6gVUoH-v2JA&s=10",
    "Ail (sachet 250g)":"         https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlILx6B6bNIyahjTYcAVPdWjy1tvP-gELvEavrpo-Alg&s=10",
    "Piment sec (250g)":"        https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgD_vikR_GoMMIXkcTBM2zIIu36iJwXI3Zc6_7X4jATA&s=10",
    "Sel de cuisine (1kg)":"        https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-HsJlk6YwGQyomn-WhJAEb_LaK2A3v45TSrGSPhxCWg&s=10",
    "Cube Maggi (paquet)":"         https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUoR7i25sayzTdoF3YrSUfj0sWb0j5E4HgIO6UwRkJcA&s=10",
    "Vinaigre (500ml)":"          https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_1SodJ8ACiLmuFGEKn81ypXnCEVExPNv_r9sOpb42qA&s",
    "Mayonnaise (400g)":"       https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjGortz79b2sLhqjqSOKRx250CJtlc8CwrDiEYOT9f4Q&s=10",
    "Sardines en boîte":"        https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5tzpaCyADZrS2a8wxmCWwTmWf8ycVw-Qri_TKymBvbA&s=10",
    "Thon en boîte":"        https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQat5B4yfyYp09ClRNPcSMAPXeKoHithFSv9ERzEib1SQ&s=10",
    "Corned-beef (boîte)":"           https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyXOv10DEyL8HiaLSR2lHbMX8lxKdDzqsmCfNHq7TljA&s=10",
    "Biscuits (paquet)":"          https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRasZO5JObxK_bnEWadkV9gMOTmvQg0-h0NlI_ZQvC6AQ&s",
    "Chocolat en poudre (400g)":"         https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7F5sXzpQc9nI5WNBZkM7TM7PAGfoUntZkAMa0JMKrOg&s=10",
    "Confiture (400g)":"         https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0cI0150tngRAwQL6zjpy4WG9ExfxEkvFSOZwTUA5G5A&s",
    "Beurre (250g)":" https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWcQSYKhoc5uXUACFyytF4DDSSNS2bgVOOgv_mMtyhXQ&s=10",
    "Œufs (plateau de 30)":"          https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoQS2nxVFinkPEjSsSC7vB2pCy8SWqshfj4eKh1qiuAQ&s=10",
    "Pain de mie":"          https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmXUillDcwR7XueANeuY4XBksecVWRqxfY4EaUYf44Pw&s=10",
    "Miel naturel (500ml)":"             https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaFTEm8ONpbcWoB1yCS0dE2L23vy7majRisV-W8Mj-dg&s=10",
    "Savon de Marseille":"       https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwg6tii75lStoej-axN3pDv_Ca5Fp6BZjwXHCeO1-B9g&s=10",
    "Dentifrice":"           https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAmGx4KaK0OPs0CGxMLZ-JYQ-CGX5jywPFQsfQA0DMxg&s=10",
    "Shampoing (250ml)":"          https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1Fvl00CNjkQi5KBYzGIevV_74VSSqnaB45jeKyQwfLA&s=10",
    "Papier hygiénique (pack 4)":"           https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwA3FGpZaFwXEHxedVizdtYr8mfQzYaHd7563vbXHfBA&s=10",
    "Gel douche (500ml)":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRiP1VjfPdBS0exR0YhqnNrEo13PCF5KvsgGA6Ltg87g&s=10",
    "Brosse à dents (unité)":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgs5GTt_Ieq2xujHjb3uSVaZ5o1LzPbTmNuzHCcfqDAg&s=10",
    "Coton-tiges (paquet)":"   https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEczhPgfecd-1MfN1QkP3lvMeP6Im0guGzRxvf_3HHdg&s=10",
    "Serviettes hygiéniques (paquet)":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlVJ9Bg_myNuiopa7siYpIFgsXgDZ-b_UL0HQicGjkUg&s=10",
    "Couches bébé (paquet)":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4pdq4-XSC1PLSS0kob0vOTaEktgsrNI9vZdxFdKOIuA&s=10",
    "Déodorant roll-on":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2AQuXpOY1b1i-oUW22ljBbBNPtctY0hb1HSHIwctGRQ&s",
    "Crème hydratante (200ml)":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUYAon6rmhJAEjMMBaehppWzH7zVgPAy9x8zqbvSj5fA&s=10",
    "Rasoir jetable (lot de 3)":"  https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtU1_9Ir2T5jucXjFKJDP60daRz2_H33SVF9s-Ewd-qA&s=10   ",
    "Mousse à raser":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5ihwkHPfbv5oL06KEXh2pKkuC54q8eRXpbKm4Sb1rtA&s=10",
    "Savon liquide pour mains (500ml)":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRT1zlKl5liQuLPUUbVkqeQRZgFLb5aZEYq0DrcX_18Q&s=10",
    "Lingettes bébé (paquet)":"   https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrNcpzQwNTgHX_nLVDQM3Oq8o9UJQSCZ0zH9yE23mERA&s=10",
    "Talc pour bébé":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9Jxj_9xaLihu6TzixwfJsKJ_w-sSgOTBmf5dzuFUbPw&s=10",
    "Bain moussant (500ml)":"   https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYPRRbRLs8NY39OuDOgJ4UjCoc2htGmPb-Dge5rMg19g&s=10",
    "Cure-dents (boîte)":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGk9Bx4z3OixRTIIS7bGWV77no-t7ndRcxAzPRjweHOw&s=10    ",
    "Cahier 100 pages":"   https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbmoXz4YeYWPiIQ2-TRhsgTqnrWXPH3VSnLsFkUqXSuQ&s=10",
    "Stylo bic (unité)":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1SnPZV1lFnnDq96JjVQzCoSZxuUFCJwyRut2As2bW_Q&s=10",
    "Crayon à papier (unité)":"   https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_5LJkqV5ERTAjqHTamw7QpGxkYkSzMkyTzA00W-3D-A&s=10",
    "Gomme":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1y2nZvwBldn2pGahNp79W6LVgexZ0hfentHVL8MApoQ&s=10",
    "Taille-crayon":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOEgKS0OwwBXr6rBDB5AF81khvu12k9POeq-kakfZjbQ&s=10",
    "Règle 30cm":"   https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOEgKS0OwwBXr6rBDB5AF81khvu12k9POeq-kakfZjbQ&s=10",
    "Classeur A4":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSX8kJEk75rzKi3ulHiEsBL5zYKHUs5mrlU1tBi0ZwFiA&s=10",
    "Feuilles A4 (rame 500)":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSiI3G3kRF00kwBF0sps8bIZ7YingIqjiNN6OotqoAuQ&s=10",
    "Surligneur (lot de 4)":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdpQdRVFHqYfecabN8Bu4pHW0Ab4wrrieUvaW1wusOwg&s=10",
    "Colle en bâton":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJo4owhHVvLesmiW3soaggTEA5rtcaorzyxUYTwaZXOA&s=10",
    "Ciseaux":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwk5TIv5KHGtxh07L004Hqa0fUVJaU714pKW6ogB50LA&s=10",
    "Agrafeuse":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgVWiuCqJsMYxNE-2iKHgwZxleTRHaJWyEMWzAGW6oCw&s=10",
    "Agrafes (boîte)":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiInLJ7XOwJtCsuoF5Qj4jSjc5sgIGMnVW3aCYiT4OYw&s=10",
    "Sac à dos scolaire":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTttIifZafs8oDcrmlz7ioWjru6c4Obzv99APoKZNfZuA&s",
    "Trousse":" https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJbZPCfG0TR-tvAiQMeT8G1s8W2qYxdMJb9XjQqml5Fw&s=10",
    "Marqueur permanent (lot de 3)":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBy0wWIB7eO8Sh6zbnUHEsVn1JprbsreE2FUp9iJfuFA&s=10",
    "Cahier de brouillon":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmOlboK5YGLk9seXQy-T7FDMs_-liS-4vtnGvMAmLj-w&s=10",
    "Chargeur téléphone (câble USB-C)":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgnLS3pC12ayg4x7oyJpF95k35VMyi4eXJnrYNyL5ALg&s",
    "Écouteurs filaires":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyPvnUto7xxi8sc9ToOMk81ZWd7_MSv2TzmZFdFyzgLQ&s=10",
    "Écouteurs Bluetooth":"     https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYeAhmpDNk9zhkBxCnd7X20vEDu1ENLnhqKNAtOFadLw&s=10",
    "Powerbank 10000mAh":"   https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGmY_UGUa5U5tY3A7Vd7HsOeBogYEfkk9nok_aVVBf1Q&s=10",
    "Rallonge électrique (5m)":"    https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrBX8-awVi4X-X_IiQ7YxjuCVoR-_v4nVbIeF8J6qHQg&s=10",
    "Multiprise 4 prises":"      https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSv47fEtHTd8u7w3XRuzOiVI6CAkIdU92GQt5MpOK1hWg&s",
    "Lampe torche LED":"",
    "Radio portable":"",
    "Câble HDMI (2m)":"",
    "Souris USB":"",
    "Clavier USB":"",
    "Casque audio filaire":"",
    "Ventilateur de bureau USB":"",
    "Adaptateur secteur universel":"",
    "Batterie rechargeable AA (lot de 4)":"",
    "Thé vert (boîte 25 sachets)":"",
    "Boisson gazeuse (1.5L)":"",
    "Boisson gazeuse (canette 33cl)":"",
    "Jus d'orange (1L)":"",
    "Eau minérale (pack 6x1.5L)":"",
    "Sirop de fruit (750ml)":"",
    "Lait concentré sucré":"",
    "Yaourt à boire (1L)":"",
    "Bissap (jus local, 1L)":"",
    "Gingembre (jus local, 1L)":"",
    "Café moulu (250g)":"",
    "Boisson énergisante (canette)":"",
    "Nescafé 3 en 1 (boîte 10 sticks)":"",
}

URL_DEFAUT = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT74agWtD3ZTsfPtk4IRuz-wJRWudiBNxQEGZn-oNs2Ig&s=10"

def enrichir_produits(produits):
    produits_enrichis = []
    for p in produits:
        produits_enrichis.append({
            "id": p[0],
            "nom": p[1],
            "prix": p[2],
            "type": p[3],
            "prix_promo": p[4],
            "image_url": IMAGES_PRODUITS.get(p[1], URL_DEFAUT)  # p[1] au lieu de p[0]
        })
    return produits_enrichis
def liste_clients(conn):
    cur = conn.cursor()
    cur.execute("select * from clients")
    view = cur.fetchall()
    return view
def liste_commandes(conn):
    cur = conn.cursor()
    cur.execute("select * from commandes")
    view = cur.fetchall()
    return view
def commandes_detaillees(conn):
    cur = conn.cursor()
    requete = """select c.commandes_id, cl.nom, cl.prenom, c.date_comm,
                        p.nom, p.type_prod, d.quantite, d.prix_unitaire,
                        c.clients_id,p.produits_id
                 from commandes as c
                 join clients as cl on c.clients_id = cl.clients_id
                 join details_comm as d on d.commandes_id = c.commandes_id
                 join produits as p on p.produits_id = d.produits_id
                 order by c.commandes_id;
              """
    cur.execute(requete)
    view = cur.fetchall()
    return view
def commandes_groupees(conn):
    commandes = {}
    resultat = commandes_detaillees(conn)
    for ligne in resultat:
        id_ligne = ligne[0]
        if id_ligne not in commandes:
            commandes[id_ligne] = {
                "client_id": ligne[8],
                "nom": ligne[1],
                "prenom": ligne[2],
                "date": ligne[3],
                "produits": [],
                "total":0
            }
        commandes[id_ligne]["produits"].append({
            "produit_id":ligne[9],
            "nom": ligne[4],
            "type": ligne[5],
            "quantite": ligne[6],
            "prix_unitaire": ligne[7]
        })
        commandes[id_ligne]['total'] += float(ligne[7]) * float(ligne[6])
    return commandes

def get_stats(conn):
    cur = conn.cursor()
    nb_clients = cur.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
    nb_produits = cur.execute("SELECT COUNT(*) FROM produits").fetchone()[0]
    nb_commandes = cur.execute("SELECT COUNT(*) FROM commandes").fetchone()[0]
    ca_total = cur.execute("SELECT SUM(quantite * prix_unitaire) FROM details_comm").fetchone()[0] or 0
    return {
        "nb_clients": nb_clients,
        "nb_produits": nb_produits,
        "nb_commandes": nb_commandes,
        "ca_total": ca_total
    }
def produits_les_plus_achetes(conn):
    cur = conn.cursor()
    resultat = cur.execute("""
        SELECT p.nom, SUM(d.quantite) as total_vendu
        FROM details_comm d
        JOIN produits p ON p.produits_id = d.produits_id
        GROUP BY p.produits_id
        ORDER BY total_vendu DESC
    """).fetchall()
    return resultat