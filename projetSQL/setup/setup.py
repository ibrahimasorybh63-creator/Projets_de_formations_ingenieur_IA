from app import get_conn
from base import creer_base
from seed import remplir_base
from recommendations.baseline import recalculer_taux_vente
creer_base()
remplir_base()
recalculer_taux_vente(conn=get_conn())
print("Opération de setup réussie.")