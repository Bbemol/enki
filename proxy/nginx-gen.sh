docker run --detach \
    --name nginx-proxy-gen \
    --volumes-from nginx-proxy \
    --volume /root/enki/proxy/data/templates/nginx.tmpl:/etc/docker-gen/templates/nginx.tmpl:ro \
    --volume /var/run/docker.sock:/tmp/docker.sock:ro \
    jwilder/docker-gen \
    -notify-sighup nginx-proxy -watch -wait 5s:30s /etc/docker-gen/templates/nginx.tmpl /etc/nginx/conf.d/default.conf