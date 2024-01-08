#  a puppet config that sets up your web servers for the deployment of web_static

exec { 'install_nginx':
  command => 'apt-get -y update && apt-get install -y nginx',
  path    => '/usr/bin/:/usr/local/bin/:/bin/',
  unless  => 'which nginx'
}

file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}

$html_content = @(END)
<html>
    <head>
    </head>
    <body>
        <h1>Adam is almost a Full Stack Software Engineer</h1>
    </body>
</html>
| END

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => $html_content,
  owner   => 'ubuntu',
  group   => 'ubuntu'
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}

exec { 'update_nginx_default':
  command => 'sed -i "0,/location \\/ {/s||location \\/hbnb_static\\/ {\\n\\t\\talias \\/data\\/web_static\\/current\\/;\\n\\t}\\n\\n\\t&|" /etc/nginx/sites-available/default',
  path    => '/usr/bin/:/usr/local/bin/:/bin/'
}

exec { 'restart_nginx':
  command => 'service nginx restart',
  path    => '/usr/bin/:/usr/local/bin/:/bin/',
  require => Exec['update_nginx_default']
}
