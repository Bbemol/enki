# Enki

* Run `yarn`
* Serve Enki app with data from backend http://localhost:5000: `ng serve`

## How to run without auth to debug CSS on mobile localhost?
* Run `ng serve --configuration=noauth --host=192.168.1.48` (replace by your host IP address)
* Using this version of `ng serve` will throw a bunch of errors because no keycloak auth is achieved, this is normal. This is because it is necessary to be able to quickly debug CSS in the angular front-end app environment