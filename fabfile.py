from fabric.api import *

def prod():
    env.user = 'tom'
    env.hosts = ['178.79.138.225:2200']

    env.site_path = '/srv/www/tomusher'
    env.repo_path = '{0}/repo'.format(env.site_path)
    env.source_path = '{0}/source'.format(env.repo_path)
    env.activate = 'source /srv/envs/tomusher/bin/activate'

def venv(command):
    sudo(env.activate + '&&' + command, user=env.user)

def requirements():
    with cd(env.repo_path):
        with prefix(env.activate):
            run("pip install -r requirements.txt")

def update():
    with cd(env.repo_path):
        run("git pull")
        
    with cd(env.source_path):
        with prefix(env.activate):
            run("./manage.py migrate")
            run("./manage.py collectstatic")
    hup()

def hup():
    sudo("kill -HUP `cat /var/run/mdrpartners.pid`")
