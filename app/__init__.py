from flask import Flask
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine


user = ""
passw = ""
db_name = ""
port = "3306"

#Connection à la base de données 
engine = create_engine(f"mysql+pymysql://{user}:{passw}@127.0.0.1:{port}/{db_name}")


# Initialisation de l'app
app = Flask(__name__, instance_relative_config=True)

# ici on charge les vues, sinon l'application ne trouvera pas les routes
from app import views

# Load the config file
app.config.from_object('config')
