import os

from dependency.default_dependency_injector import DefaultDependencyInjector
from dependency.minio_dependency_injector import MinioDependencyInjector

mode = os.environ.get("MODE", "DEFAULT")
di_container = DefaultDependencyInjector()
if mode == 'MINIO':
    di_container = MinioDependencyInjector()
