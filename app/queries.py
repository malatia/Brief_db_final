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

    #il y aura beaucoup de code répété, je ne commenterai donc que le premier bloc, les autres étant quasiments identiques
    if variable == "Job":
        #On récupère les données dont on va avoir besoin pour créer le grahpique et afficher les noms. On fait une aggrégation dans la deuxieme requete
        with engine.connect() as conn:
            result = conn.execute(text("SELECT job.job_name FROM job"))
            result2 = conn.execute(text("SELECT count(user.user_id), job.job_name  FROM job  JOIN user on user.job_id = job.job_id GROUP BY job.job_name;"))

        #On récupère les différentes lignes renvoyées dans une liste 
        name_list = [row.job_name for row in result]
        data = [row for row in result2]

        #Ce dataframe est là pour faciliter l'affichage des données 
        job_df = pd.DataFrame(data, columns=["count", "job"])
        #On configure ce qu'il faut pour pouvoir créer un graphique à partir des données 
        plt.rcParams['figure.figsize']=[16,8]
        job_arr = np.array(job_df["count"])
        job_labels = job_df["job"].values.tolist()
        plt.pie(job_arr, labels = job_labels, autopct = '%1.2f%%')
        plt.legend(title = "Proportion des jobs")
        #On enregistre la figure à un chemin générique que l'on affiche ensuite dans le HTML
        plt.savefig("app/static/fig.png")
        plt.close()

    elif variable == "City":
        with engine.connect() as conn:
            result = conn.execute(text("SELECT city.city_name FROM city"))
            result2 = conn.execute(text("SELECT count(user.user_id), city.city_name  FROM city  JOIN user on user.city_id = city.city_id GROUP BY city.city_name;"))

        name_list = [row.city_name for row in result]
        data = [row for row in result2]
        city_df = pd.DataFrame(data, columns=["count", "city"])
        plt.rcParams['figure.figsize']=[16,8]
        city_arr = np.array(city_df["count"])
        city_labels = city_df["city"].values.tolist()
        plt.pie(city_arr, labels = city_labels, autopct = '%1.2f%%')
        plt.legend(title = "Proportion des cities")
        plt.savefig("app/static/fig.png")
        plt.close()

    elif variable == "Movie":
        with engine.connect() as conn:
            result = conn.execute(text("SELECT movie.movie_name FROM movie"))
            result2 = conn.execute(text("SELECT count(user.user_id), movie.movie_name  FROM movie  JOIN user on user.movie_id = movie.movie_id GROUP BY movie.movie_name;"))

        name_list = [row.movie_name for row in result]
        data = [row for row in result2]
        movie_df = pd.DataFrame(data, columns=["count", "movie"])
        plt.rcParams['figure.figsize']=[16,8]
        movie_arr = np.array(movie_df["count"])
        movie_labels = movie_df["movie"].values.tolist()
        plt.pie(movie_arr, labels = movie_labels, autopct = '%1.2f%%')
        plt.legend(title = "Proportion des movies")
        plt.savefig("app/static/fig.png")
        plt.close()

    elif variable == "Country":
        with engine.connect() as conn:
            result = conn.execute(text("SELECT country.country_name FROM country"))
            result2 = conn.execute(text("SELECT count(user.user_id), country.country_name  FROM country  JOIN user on user.country_id = country.country_id GROUP BY country.country_name;"))

        name_list = [row.country_name for row in result]
        data = [row for row in result2]
        country_df = pd.DataFrame(data, columns=["count", "country"])
        plt.rcParams['figure.figsize']=[16,8]
        country_arr = np.array(country_df["count"])
        country_labels = country_df["country"].values.tolist()
        plt.pie(country_arr, labels = country_labels, autopct = '%1.2f%%')
        plt.legend(title = "Proportion des countries")
        plt.savefig("app/static/fig.png")
        plt.close()

    elif variable == "Domain":
        with engine.connect() as conn:
            result = conn.execute(text("SELECT domain.domain_name FROM domain"))
            result2 = conn.execute(text("SELECT count(user.user_id), domain.domain_name  FROM domain  JOIN user on user.domain_id = domain.domain_id GROUP BY domain.domain_name;"))
        
        name_list = [row.domain_name for row in result]        
        data = [row for row in result2]
        domain_df = pd.DataFrame(data, columns=["count", "domain"])
        plt.rcParams['figure.figsize']=[16,8]
        domain_arr = np.array(domain_df["count"])
        domain_labels = domain_df["domain"].values.tolist() 
        plt.pie(domain_arr, labels = domain_labels, autopct = '%1.2f%%')
        plt.legend(title = "Proportion des domains")
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
        "FROM User "              
        "JOIN job ON job.job_id=user.job_id " 
        "JOIN domain ON domain.domain_id=user.domain_id " 
        "JOIN city ON city.city_id=user.city_id "  
        "JOIN country ON country.country_id=user.country_id "
        f"JOIN movie ON movie.movie_id=user.movie_id where {cat}.{cat}_name='{name}';")
        result = conn.execute(query)
    dict_list = [row._asdict() for row in result]
    keys = [key for key in dict_list[0].keys()]

    return dict_list, keys
    
