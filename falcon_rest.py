import falcon
import docker
import json
import yaml
import os 


class Compose_create(object):
    def on_post(self, req, resp):
        template = {'version':'2.1', 'services':{'test_centos':{'build':'./docker_centos', 'container_name':'andy_centos_1', 'networks':{'network_andy':{'ipv4_address':'10.10.10.13'}}}}, 'networks':{'network_andy':{'driver':'bridge', 'ipam':{'driver':'default', 'config':[{'subnet':'10.10.10.0/24', 'gateway':'10.10.10.1'}]}}}}
        resp.status = falcon.HTTP_200
        recieved_params = req.stream.read()
        if recieved_params == 'create':
           with open('docker-compose.yml', 'w') as f:
                      
               yaml.dump(template,
                         f,
                         default_flow_style=False
               )
        else:
            print "invalid param"

class Compose_view(object):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        recieved_params = req.stream.read()
        if recieved_params == 'view':
           with open('docker-compose.yml', 'r') as f:
               resp.body = f.read()
        else:
            print "invalid param"
 
class Compose_remove(object):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        recieved_params = req.stream.read()
        if recieved_params == 'remove':
           os.remove('docker-compose.yml')
        else:
            print "invalid param"

class Docker_version(object):
    def on_get(self, req, resp): 
        resp.status = falcon.HTTP_200
        client = docker.from_env()
        resp.body = str(client.version()).encode() 
       

class Compose_up(object):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        recieved_params = req.stream.read()
        if recieved_params == 'compose up':
           os.system('docker-compose up -d')
        else:
            print "invalid param"

class Compose_down(object):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        recieved_params = req.stream.read()
        if recieved_params == 'compose down':
           os.system('docker-compose down')
        else:
            print "invalid param"

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
create_compose = Compose_create()
view_compose = Compose_view()
remove_compose = Compose_remove()
get_docker_version = Docker_version()
up_compose = Compose_up()
down_compose = Compose_down()


#create compose file
app.add_route('/api/compose/config/create/', create_compose)

#view compose file
app.add_route('/api/compose/config/view/', view_compose)

#remove compose file
app.add_route('/api/compose/config/remove/', remove_compose)

#get docker version
app.add_route('/api/docker/version/', get_docker_version)

#compose up
app.add_route('/api/compose/up/', up_compose)

#compose down
app.add_route('/api/compose/down/', down_compose)
