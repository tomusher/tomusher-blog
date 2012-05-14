id = "tomusher-blog"
deploy_to = "/srv/www/tomusher-blog"
owner = "tomusher"
group = "tomusher"
revision = "HEAD"
repository = "git://github.com/tomusher/tomusher-blog.git"

include_recipe "python"

%w{libxml2-dev libxslt1-dev libjpeg-dev}.each do |pkg|
    package pkg do
        action :install
    end
end

group group do
    gid 2101
end

user owner do
    uid 2001
    gid group
    shell "/bin/bash"
end

directory deploy_to do
    owner owner
    group group
    mode '0755'
    recursive true
end

%w{logs shared static media media/uploads}.each do |dir|
    directory "#{deploy_to}/#{dir}" do
        owner owner
        group group
        mode '0755'
        recursive true
    end
end

secret = Chef::EncryptedDataBagItem.load_secret("/tmp/encrypted_data_bag_secret")
django_admin = Chef::EncryptedDataBagItem.load("passwords", "django_admin", secret)
django_secret = Chef::EncryptedDataBagItem.load("keys", "django_secret", secret)
embedly_key = Chef::EncryptedDataBagItem.load("keys", "embedly_key", secret)

template "#{deploy_to}/shared/initial_data.json" do
    source "initial_data.json.erb"
    owner owner
    group group
    mode "644"
    variables(
        :password => django_admin["password"]
    )
end

template "#{deploy_to}/shared/secrets.py" do
    source "secrets.py.erb"
    owner owner
    group group
    mode "644"
    variables(
        :secret_key => django_secret["key"],
        :embedly_key => embedly_key["key"]
    )
end

env = python_virtualenv "#{deploy_to}/env" do
    action :create
    interpreter "python2.6"
end

template "#{node[:nginx][:dir]}/sites-available/#{id}" do
    source "#{id}.conf.erb"
    owner "root"
    group "root"
    mode "644"
    notifies :restart, resources(:service => "nginx")
end

nginx_site "#{id}"
nginx_site "default" do
    enable false
end

postgresql_database_user "tomusher" do
    connection ({:host => "127.0.0.1", :username => 'postgres'})
    owner 'postgres'
    password "hLj6itWmnBKgaru1bZFY"
    action :create
end

postgresql_database "tomusher" do
    connection ({:host => "127.0.0.1", :username => 'postgres'})
    owner 'postgres'
    action :create
end

postgresql_database_user "tomusher" do
    connection ({:host => "127.0.0.1", :username => 'postgres'})
    owner "postgres"
    database_name "tomusher"
    action :grant
end

node.default[:gunicorn][:virtualenv] = env.path
include_recipe "gunicorn"
include_recipe "supervisor"

gunicorn_config "#{deploy_to}/gunicorn.conf" do
    listen "0.0.0.0:13742"
    action :create
end

supervisor_service id do
    action :enable
    if node[:env]=="vagrant":
        base_command = "#{deploy_to}/env/bin/gunicorn_django"
    else
        base_command = "newrelic-admin run-program #{deploy_to}/env/bin/gunicorn_django"
    end
    environment ({"NEW_RELIC_CONFIG_FILE" => "/tmp/newrelic.ini"})
    command "#{base_command} -c #{deploy_to}/gunicorn.conf"
    directory "#{deploy_to}/current/source/"
    autostart false
    user owner
end

if node[:env]=="vagrant"
    execute "umount" do
        command "umount -a -t vboxsf"
    end
    execute "mount" do
        command "mount -t vboxsf -o uid=`id -u tomusher`,gid=`id -g tomusher` v-root #{deploy_to}/current"
    end
    link "#{deploy_to}/current/source/secrets.py" do
        to "#{deploy_to}/shared/secrets.py"
    end
    link "#{deploy_to}/current/source/initial_data.json" do
        to "#{deploy_to}/shared/initial_data.json"
    end
    execute "#{deploy_to}/env/bin/pip install -r #{deploy_to}/current/requirements.txt"
    execute "syncdb" do
        command "#{deploy_to}/env/bin/python #{deploy_to}/current/source/manage.py syncdb --noinput"
        user owner
        group owner
    end
    execute "collectstatic" do
        command "#{deploy_to}/env/bin/python #{deploy_to}/current/source/manage.py collectstatic --noinput"
        user owner
        group owner
    end
else
    deploy_revision id do
        action :deploy
        revision revision
        repository repository
        user owner
        group group
        deploy_to "#{deploy_to}"
        shallow_clone true
        purge_before_symlink{[]}
        create_dirs_before_symlink([])
        symlinks({})
        migrate true
        migration_command "#{deploy_to}/env/bin/python source/manage.py migrate"
        symlink_before_migrate({
            "secrets.py" => "source/secrets.py",
            "initial_data.json" => "source/initial_data.json"
        })
        before_migrate do
            execute "pip" do
                command "#{deploy_to}/env/bin/pip install -r #{release_path}/requirements.txt"
                user owner
                group owner
            end
        end
        before_restart do
            execute "syncdb" do
                command "#{deploy_to}/env/bin/python #{release_path}/source/manage.py syncdb --noinput"
                user owner
                group owner
            end
            execute "collectstatic" do
                command "#{deploy_to}/env/bin/python #{deploy_to}/current/source/manage.py collectstatic --noinput"
                user owner
                group owner
            end
        end
    end
end
   
supervisor_service id do
    action :restart
end
