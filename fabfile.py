from fabric.api import *

def prod():
    env.user = 'root'
    env.hosts = ['178.79.138.225']

    env.site_path = '/srv/www/tomusher-blog'
    env.repo_path = '{0}/current'.format(env.site_path)
    env.source_path = '{0}/current/source'.format(env.repo_path)
    env.activate = 'source /srv/www/tomusher-blog/env/bin/activate'
    env.data_bag_key_path = '/Users/Tom/Sites/data_bag_key'

def vagrant():
    env.user = 'root'
    env.hosts = ['127.0.0.1:2222']

    env.site_path = '/srv/www/tomusher-blog'
    env.repo_path = '{0}/current'.format(env.site_path)
    env.source_path = '{0}/current/source'.format(env.repo_path)
    env.activate = 'source /srv/www/tomusher-blog/env/bin/activate'
    env.data_bag_key_path = '/Users/tomusher/.keys/data_bag_key'

def bootstrap():
    with lcd('deploy'):
        local('librarian-chef install')
        local('fix node:{0} deploy_chef'.format(env.host))

def cook():
    with lcd('deploy'):
        put(env.data_bag_key_path, '/tmp/encrypted_data_bag_secret')
        local('fix node:{0} role:tomusher-blog'.format(env.host))

def reload():
    run("supervisorctl restart tomusher-blog")

def autosync():
    "Automatically synchronise changes. For testing only."
    import watchdog
    from watchdog.observers import Observer
    import time
    import os

    class RsyncEventHandler(watchdog.events.PatternMatchingEventHandler):
        def on_any_event(self, event):
            run("/srv/www/tomusher-blog/env/bin/python /srv/www/tomusher-blog/current/source/manage.py collectstatic --noinput")
            reload()

    observer = Observer()
    observer.schedule(RsyncEventHandler(patterns=["*.css","*.js","*.py","*.html"]), path=os.getcwd(), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
