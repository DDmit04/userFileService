from src.dependency.DependencyInjector import DependencyInjector
from src.model.DatabaseInit import database

di_container = DependencyInjector(database)
