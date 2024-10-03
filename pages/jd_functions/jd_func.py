def select_graph_height(x):
    if x >= 10:
        jd_graph_height = 600
    elif 3 < x < 10:
        jd_graph_height = 500
    else:
        jd_graph_height = 300
    return jd_graph_height


def liste_cluster_options():
    cluster_options = {
        "Groupe A" : ['VERSAILLES', 'PARIS'],
        "Groupe B" : ['ANGERS', 'DIJON', 'CAEN', 'POITIERS', 'RIOM', 'BOURGES', 'LIMOGES', 'AGEN'],
        "Groupe C" : ['DOUAI', 'AMIENS', 'CHAMBERY', 'ROUEN', 'GRENOBLE', 'COLMAR', 'LYON', 'REIMS', 'METZ', 'TOULOUSE'],
        "Groupe D" : ['RENNES', 'ORLEANS', 'NANCY', 'BESANCON', 'NIMES', 'AIX EN PROVENCE', 'MONTPELLIER', 'BORDEAUX', 'PAU'],
    }
    return cluster_options

def sidebar_signature():
    signature = """
    <b>Réalisation</b><br>
    Ministère de la Justice<br>
    Direction des services judiciaires <br>
    Pôle de l'Evaluation et de la Prospective
    """
    return signature