import os

from dependency.boto_dependency_injector import MinioDependencyInjector
from dependency.default_dependency_injector import DefaultDependencyInjector

mode = os.environ.get("MODE", "DEFAULT")
di_container = DefaultDependencyInjector()
if mode == 'MINIO':
    di_container = MinioDependencyInjector()
