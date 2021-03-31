import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    APPLICATION_ROOT = os.environ['APPLICATION_ROOT']
    NAMESPACE = 'default'
    HELM_REPOSITORY_CACHE="/root/.extensions"
    REGISTRY_PROJECT = os.environ['REGISTRY_PROJECT']
    VERSION = os.environ['VERSION']