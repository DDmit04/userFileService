from dependency.DependencyInjector import DependencyInjector
from model.DatabaseInit import database

di_container = DependencyInjector(database)
