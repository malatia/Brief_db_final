from sqlalchemy.orm import relationship, declarative_base, Session
from sqlalchemy import select, Column, Integer, String, ForeignKey, create_engine
import pandas as pd

#Ici on crée les variables qui nous serviront pour la connection et la création de la bdd
Base = declarative_base()
user = ""
passw = ""
db_name = ""

#Création des classes qui serviriont de base aux table de la BDD
class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    fullname = Column(String(100))
    email = Column(String(100))
    job = relationship("Job", back_populates="users")
    job_id = Column('job_id', ForeignKey('job.job_id'), nullable=False)
    city = relationship("City", back_populates="users")
    city_id = Column('city_id', ForeignKey('city.city_id'), nullable=False)
    movie = relationship("Movie", back_populates="users")
    movie_id = Column('movie_id', ForeignKey('movie.movie_id'), nullable=False)
    domain = relationship("Domain", back_populates="users")
    domain_id = Column('domain_id', ForeignKey('domain.domain_id'), nullable=False)
    country = relationship("Country", back_populates="users") 
    country_id = Column('country_id', ForeignKey('country.country_id'), nullable=False) 

class Job(Base):
    __tablename__ = 'job'
    job_id = Column(Integer, primary_key=True)
    job_name = Column(String(100))
    users = relationship("User", back_populates="job")

class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(100))
    users = relationship("User", back_populates="city")

class Movie(Base):
    __tablename__ = 'movie'
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String(100))
    users = relationship("User", back_populates="movie")

class Domain(Base):
    __tablename__ = 'domain'
    domain_id = Column(Integer, primary_key=True)
    domain_name = Column(String(100))
    users = relationship("User", back_populates="domain")

class Country(Base):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String(100))
    users = relationship("User", back_populates="country")

def insert_rows(engine):
    #On lit le CSV et on récupère chaque possibilité unique pour chaque table
    data = pd.read_csv("db.csv")
    jobs = data["Job Title"].unique()
    cities = data["City"].unique()
    movies = data["Movie Genre"].unique()
    domains = data["Domain name"].unique()
    countries = data["Country"].unique()

    #On crée les tables qui n'ont pas de clés étrangères 
    with Session(engine) as session:
        for job in jobs:
            session.add(Job(job_name=job))
        for city in cities:
            session.add(City(city_name=city))
        for movie in movies:
            session.add(Movie(movie_name=movie))
        for domain in domains:
            session.add(Domain(domain_name=domain))
        for country in countries:
            session.add(Country(country_name=country))
        session.commit()

        #Maintenant on peut créer la table user vu que toutes les clés étrangères qui lui sont liées ont été insérées 
        for index, row in data.iterrows():
            job_name = row["Job Title"]
            job_id = session.execute(select(Job.job_id).where(Job.job_name == job_name))
            job_id = job_id.fetchone()[0]
            city_name = row["City"]
            city_id = session.execute(select(City.city_id).where(City.city_name == city_name))
            city_id = city_id.fetchone()[0]
            movie_name = row["Movie Genre"]
            movie_id = session.execute(select(Movie.movie_id).where(Movie.movie_name == movie_name))
            movie_id = movie_id.fetchone()[0]    
            domain_name = row["Domain name"]
            domain_id = session.execute(select(Domain.domain_id).where(Domain.domain_name == domain_name))
            domain_id = domain_id.fetchone()[0] 
            country_name = row["Country"] 
            country_id = session.execute(select(Country.country_id).where(Country.country_name == country_name))
            country_id = country_id.fetchone()[0] 
            fullname = row["FirstName LastName"]
            email = row["Email Address"]
            session.add(User(fullname = fullname, email = email, job_id = job_id, city_id = city_id, movie_id = movie_id, domain_id =domain_id, country_id = country_id))   
    session.commit()    


def main():
    #On fait la connection, on crée les tables 
    engine = create_engine(f"mysql+pymysql://{user}:{passw}:)@127.0.0.1:3306/{db_name}")
    Base.metadata.create_all(engine)
    #Et on insère les données 
    insert_rows(engine)

if __name__=="__main__":
    main()

    