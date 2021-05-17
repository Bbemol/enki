# Enki

# Installation

This is a little trick to redirect to keycloak from localhost 
```
echo "localhost keycloak" >> /etc/hosts
```
or add it manually with your bests text editor 

You need to create global default network with 
```
docker network create --driver=bridge enki_default
``` 

Add these lines in /etc/hosts 
```
localhost       keycloak
127.0.0.1       keycloak
127.0.0.1       minio
```

# Keycloak
```
cd authentication
```
Copy example.env to .env 
```
cp example.env .env
``` 
Change variables if needed

```
 docker-compose -f docker-compose.yml up 
```
wait keycloak startup
``` 
docker-compose -f docker-compose.provision.yml run --rm keycloak-provision
```

or with make 
```
make upd && sleep 5 && make provision 
```


Get kong client secret from Keycloak admin in Client section and change it in .env file
# Kong Api Gateway

```
cd kong
```
Copy example.env to .env 
```
cp example.env .env
``` 
Change CLIENT_SECRET with keycloak kong client

With make 
```
make setup && sleep 5 && make build-provision && sleep 5 && make provision 
```

# Backend
```
cd backend
```

```
docker-compose -f docker-compose.yml up
```
or with make 
```
make build && make upd && make seed
```

It's now possible to post new "affaires" in postman with this endpoint:

```
http://localhost:5000/api/v1/echanges/messages
```

You can access affairs from:
```
http://localhost:5000/api/enki/v1/affairs
```
You can generate affairs running
```
docker exec backend_enki-api_1 flask create-affairs --number=10 --dept_code=77 --event_type=incendie
```

# FrontEnd
```
cd front
```

```
yarn
```

and run angular
```
ng serve 
```

Go to http://localhost:1337
You can login with:
Login: maire@chelles.fr
PWD: defaultpassword


### Design system
````
cd design-system
````

Develop
```
make up
````

Deploy to heroku
Merge all design-system modifications to `main` branch
and run
```
make deploy
```
(you have to be logged in to heroku to have access, and ask admin a collab access)

# Elasticsearch and Kibana
```
cd elk
```
```
docker-compose -f docker-compose.yml up
```
or with make 
```
make upd
```

