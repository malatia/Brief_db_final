from app import engine
from sqlalchemy import text
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd

plt.switch_backend('Agg')

def one_variable(variable):
    """Cette fonction permet de créer un graphique camembert et de retourner les noms d'une catégorie dans la BDD (cette catégorie étant une table dont le nom est indiqué par l'argument "variable")
        Elle ne récupère pas dynamiquement les données à partir de l'argument passé. D'où la grande présence de "if"s répétitifs.
    Args:
        variable (str): Nom de la table dans la BDD. Passée automatiquement par un formulaire

    Returns:
        [List]: [Une liste contenant les noms de la catégorie demandée]
    """

    #On récupère les données dont on va avoir besoin pour créer le grahpique et afficher les noms. On fait une aggrégation dans la deuxieme requete
    variable = variable.lower()
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT {variable}.{variable}_name as name FROM {variable}"))
        result2 = conn.execute(text(f"SELECT count(user.user_id), {variable}.{variable}_name as name  FROM {variable}  JOIN user on user.{variable}_id = {variable}.{variable}_id GROUP BY {variable}.{variable}_name;"))

    #On récupère les différentes lignes renvoyées dans une liste 
    name_list = [row.name for row in result]
    data = [row for row in result2]

    #Ce dataframe est là pour faciliter l'affichage des données 
    df = pd.DataFrame(data, columns=["count", "job"])
    #On configure ce qu'il faut pour pouvoir créer un graphique à partir des données 
    plt.rcParams['figure.figsize']=[16,8]
    arr = np.array(df["count"])
    labels = df["job"].values.tolist()
    plt.pie(arr, labels = labels, autopct = '%1.2f%%')
    plt.legend(title = "Proportion des jobs")
    #On enregistre la figure à un chemin générique que l'on affiche ensuite dans le HTML
    plt.savefig("app/static/fig.png")
    plt.close()
    
    return name_list

def two_variables(variable1, variable2):
    """Cette fonction fait en substance la même chose que la précédente, à ceci près qu'elle prend deux catégories en entrée et fais un autre type de graphique.txt


    Args:
        variable1 ([str]): [Nom de la table 1 dans la BDD. Passée automatiquement par un formulaire]
        variable2 ([str]): [Nom de la table 2 dans la BDD. Passée automatiquement par un formulaire]

    Returns:
        [list]:  [Une liste contenant les noms de la catégorie demandée]]
        [list]:  [Une liste contenant les noms de la catégorie demandée]]
    """
    
    variable1 = variable1.lower()    
    variable2 = variable2.lower()
    #On récupère les noms des différentes catégories, ainsi que les associations entre ces différentes catégories
    with engine.connect() as conn:
        result1 = conn.execute(text(f"SELECT {variable1}.{variable1}_name FROM {variable1}"))
        result2 = conn.execute(text(f"SELECT {variable2}.{variable2}_name FROM {variable2}")) 
        result3 = conn.execute(text(f"SELECT {variable1}.{variable1}_name as cat1, {variable2}.{variable2}_name as cat2, user.fullname FROM {variable1} JOIN user on user.{variable1}_id={variable1}.{variable1}_id JOIN {variable2} on {variable2}.{variable2}_id = user.{variable2}_id;"))

    #On récupère les lignes dans des dataframes 
    data1 = [row for row in result1]   
    data2 = [row for row in result2]
    data3 = [row for row in result3]
    #On met les noms à renvoyer dans des listes 
    name_list1 = [instance[0] for instance in data1]
    name_list2 = [instance[0] for instance in data2]
    #On crée un dataframe avec nos deux données, et on s'en sert pour faire un graphique
    df = pd.DataFrame(data3, columns=[variable1, variable2, "user"])
    df.plot(kind="scatter", x=variable1, y=variable2, rot="vertical")
    plt.savefig("app/static/fig.png")
    plt.close()
    return name_list1, name_list2


def specific_variable(name, cat):
    """Cette fonction sert à afficher toutes les lignes de la base de données concernées par nom particulier d'une catégorie donnée.

    Args:
        name ([str]): [Nom précis sur lequel on veut des informations au sein de la catégorie]
        cat ([str]): [Nom de la catégorie(job, domain etc) au sein de laquelle se trouve l'instance particulière que l'on cherche ]

    Returns:
        [dict]: [Retourne un dictionnaire crée à partir des lignes renvoyées par les requetes ]
        [list]: [Retourne une liste contenant les "clés" (les nom des colonnes)renvoyées par les requetes ]
    """
    cat = cat.lower()
    with engine.connect() as conn:
        query = (f"Select user.user_id, user.fullname,user.email, job.job_name, domain.domain_name, city.city_name,country.country_name, movie.movie_name " 
        "FROM user "              
        "JOIN job ON job.job_id=user.job_id " 
        "JOIN domain ON domain.domain_id=user.domain_id " 
        "JOIN city ON city.city_id=user.city_id "  
        "JOIN country ON country.country_id=user.country_id "
        f"JOIN movie ON movie.movie_id=user.movie_id where {cat}.{cat}_name='{name}';")
        result = conn.execute(query)
    dict_list = [row._asdict() for row in result]
    keys = [key for key in dict_list[0].keys()]

    return dict_list, keys
    
