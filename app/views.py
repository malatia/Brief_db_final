from flask import render_template, request
from app import app
import os
from app import queries

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():       
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/results', methods=['GET', 'POST'])
def results():
    #Si on arrive ici par l'intérmédiaire du formulaire en POST
    if request.method == 'POST':

        #On supprime la figure crée précédemment si elle existe
        static_dir = os.path.join(basedir, 'static')
        if os.path.isfile(os.path.join(static_dir, "fig.png")):    
            os.remove(os.path.join(static_dir, "fig.png"))

        #On récupère les valeurs du formulaire    
        variable1 = request.form['variable1']
        variable2 = request.form['variable2']

        #Si une seule valeur est voulue on va créer un diagramme camembert 
        if variable2 == "--" or variable1 == variable2:
            results1 = queries.one_variable(variable1)
            results2 = None

        #Sinon on crée un scatterplot
        else:
            results1 , results2 = queries.two_variables(variable1, variable2)

    else:
        #Si on arrive pas ici par le formulaire(par exemple en mettant directement l'url), on affiche l'index à nouveau
        return render_template("index.html")   
            
        
    return render_template("results.html", results1=results1, results2=results2, cat=variable1, cat2=variable2)


@app.route('/results_specific/<name>/<cat>', methods=['GET'])
def results_specific(name,cat):
    #On récupère tout ce dont on a besoin à partir de la catégorie et du nom 
    dict_list, keys = queries.specific_variable(name, cat)

    return render_template("results_specific.html", dict_list=dict_list, keys=keys, cat=cat)
