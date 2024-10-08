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
        "Groupe A" : ['RENNES', 'ORLEANS', 'NANCY', 'BESANCON', 'NIMES', 'AIX EN PROVENCE', 'MONTPELLIER', 'BORDEAUX', 'PAU'],
        "Groupe B" : ['ANGERS', 'DIJON', 'CAEN', 'POITIERS', 'RIOM', 'BOURGES', 'LIMOGES', 'AGEN'],
        "Groupe C" : ['DOUAI', 'AMIENS', 'CHAMBERY', 'ROUEN', 'GRENOBLE', 'COLMAR', 'LYON', 'REIMS', 'METZ', 'TOULOUSE'],
        "Groupe D" : ['VERSAILLES', 'PARIS'],
    }
    return cluster_options

def sidebar_signature():
    signature = """
    <b>Réalisation</b><br>
    Ministère de la Justice<br>
    Direction des services judiciaires <br>
    Pôle de l’évaluation et de la prospective
    """
    return signature

def format_float(number):

  number_str = str(number)
  # Insert non-breaking spaces for thousands
  # number_str = number_str[::-1].replace(',', ' ', 3)[::-1]
  # Replace dots with commas
  number_str = number_str.replace('.', ',')



  return number_str

def format_thousands(number):
    # Check if the number is an integer by comparing it to its int equivalent
    if number == int(number):
        # Format the integer part with thousands separator and no decimals
        formatted_str = f"{int(number):,}"
    else:
        # Format with thousands separator and two decimal places for floats
        formatted_str = f"{number:,.2f}"
   
    # Replace commas with non-breaking spaces (using Unicode \u00A0 for non-breaking space)
    formatted_str = formatted_str.replace(",", "\u00A0")
   
    # Replace the dot with a comma (for decimals)
    formatted_str = formatted_str.replace(".", ",")
   
    return formatted_str