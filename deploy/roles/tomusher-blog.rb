name "tomusher-blog"
description "Tomusher.com Blog"

run_list(
    "recipe[apt]",
    "recipe[git]",
    "recipe[build-essential]",
    "recipe[nginx]",
    "recipe[postgresql::server]",
    "recipe[tomusher-blog]"
)
