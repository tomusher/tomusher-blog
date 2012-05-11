from fabric.api import *

def prod():
    env.user = 'tomusher'
    env.hosts = ['178.79.138.225:2200']

    env.site_path = '/srv/www/tomusher-blog'
    env.repo_path = '{0}/current'.format(env.site_path)
    env.source_path = '{0}/current/source'.format(env.repo_path)
    env.activate = 'source /srv/www/tomusher-blog/env/bin/activate'

def init():
    local('cd deploy && librarian-chef install')

def venv(command):
    sudo(env.activate + '&&' + command, user=env.user)

def requirements():
    with cd(env.repo_path):
        with prefix(env.activate):
            run("pip install -r requirements.txt")

def reload():
    sudo("supervisorctl restart tomusher-blog")
