# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
    config.vm.box = "lucid32"
    config.vm.forward_port 80, 4040
    config.ssh.max_tries = 150
    config.vm.share_folder("v-root", "/srv/vagrant", ".", :create => true, :owner => "vagrant", :group => "vagrant")
    config.vm.customize ["modifyvm", :id, "--rtcuseutc", "on"]
    config.vm.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]

  # Enable provisioning with chef solo, specifying a cookbooks path, roles
  # path, and data_bags path (all relative to this Vagrantfile), and adding 
  # some recipes and/or roles.
  #
  # config.vm.provision :chef_solo do |chef|
  #   chef.cookbooks_path = "../my-recipes/cookbooks"
  #   chef.roles_path = "../my-recipes/roles"
  #   chef.data_bags_path = "../my-recipes/data_bags"
  #   chef.add_recipe "mysql"
  #   chef.add_role "web"
  #
  #   # You may also specify custom JSON attributes:
  #   chef.json = { :mysql_password => "foo" }
  # end

    config.vm.provision :shell, :inline => "apt-get update"
    config.vm.provision :shell, :inline => "gem update chef"
    #config.vm.provision :shell, :inline => "umount -a -t vboxsf && mount -t vboxsf -o uid=`id -u vagrant`,gid=`id -g vagrant` v-root /srv/vagrant"
    config.vm.provision :chef_solo do |chef|
        chef.json = {
            :env => 'vagrant'
        }
        chef.encrypted_data_bag_secret_key_path = "/Users/Tom/Sites/data_bag_key"
        chef.cookbooks_path = ["deploy/cookbooks", "deploy/site-cookbooks"]
        chef.roles_path = "deploy/roles"
        chef.data_bags_path = "deploy/data_bags"
        chef.add_role("tomusher-blog")
    end
end
