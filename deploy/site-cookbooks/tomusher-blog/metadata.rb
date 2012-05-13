maintainer        "Tom Usher"
maintainer_email  "tom@tomusher.com"
description       "Installs tomusher-blog"
version           "0.1"

recipe "tomusher-blog", "Installs tomusher-blog"

depends "python"

%w{ ubuntu debian }.each do |os|
  supports os
end
