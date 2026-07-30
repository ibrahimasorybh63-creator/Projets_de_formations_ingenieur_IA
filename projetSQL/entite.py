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
    
class Clients:
    def __init__(self,conn,nom,prenom,adresse=None,clients_id=None):
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.clients_id = clients_id
        self.conn = conn
    def ajouter_en_base(self):
        cur = self.conn.cursor()
        cur.execute("insert into clients (nom,prenom,adresse) values (?,?,?);",(self.nom,self.prenom,self.adresse))
        self.conn.commit()
        self.clients_id = cur.lastrowid
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
                        p.nom, p.type_prod, d.quantite, d.prix_unitaire
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
                "nom": ligne[1],
                "prenom": ligne[2],
                "date": ligne[3],
                "produits": []
            }
        commandes[id_ligne]["produits"].append({
            "nom": ligne[4],
            "type": ligne[5],
            "quantite": ligne[6],
            "prix_unitaire": ligne[7]
        })
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