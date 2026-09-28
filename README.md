# Examples

A few examples on how to use this library

## info for a given user

```
$ python
Python 3.10.3 (v3.10.3:a342a49189, Mar 16 2022, 09:34:18) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from myos.user import User

>>> user = User(name='wup22514', domain_name='stfc')
>>> user.id
'd0b0337d0d3aff182ebb41ff5581ea057c18daeaaeda3b3cc56adce83d6b67d1'
>>> user.email
'neo@matrix.net'

>>> projects = user.projects
>>> for project in projects:
...     print(project.id, project.name)
...
11d48058d9484acfbce827e95fd5e9fc Tier-1 Test Internal
15098398e6fb4dffaa7fd4e8b8a15046 Jupyter-Training
2d8252b430c2405da24d74df2004c24b Condor
35429791ecb441f6ad8e95cccb3117f6 Cloud-Jupyter-Dev
8e20e5fce11349f295751d834aa361b0 Cloud-Jupyter-Prod
9c015225d10843babbc57009fc986b61 Tier-1 Prod External
cbaff02b43104ec3a0016a177fecaf2d Tier-1 Test External
ce3c1ed2fb19421e9bf0291a14e13256 ESC PSCS Grid Services team
f7c59f63597648caa654c3427f8d22d3 J-C-Bejar-Scratch-Space
fda22ac0ab7a46608a0783b74e1b5a43 Tier-1 Prod Internal
```

## info for a given project

```
$ python
Python 3.10.3 (v3.10.3:a342a49189, Mar 16 2022, 09:34:18) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from myos.project import Project
   
>>> project = Project(name='Condor')
>>> project.id
'2d8252b430c2405da24d74df2004c24b'

>>> users = project.users
>>> for user in users:
...     print(user.email)
...
neo@matrix.net
trinity@matrix.net
morpheus@matrix.net

>>> servers = project.servers
>>> for server in servers:
...    print(server.id)
...
7da973eb-794c-4557-bf87-e5987dd8efad
8802f035-f198-4129-9a87-f6ded8940db0
c05a14b1-046b-4e4c-bba2-2c164aee28dd
9749d097-5ee0-488b-9a7f-41eb6250659c
78fa7852-8f63-4f95-9334-f5310ea9b141
f297f3e8-dc1b-4729-971b-563872c0ab33
1de66266-6a5c-41de-ba41-eecc320f0f96
3adf6e50-ae3b-4788-994e-4f5fffacbfba
77deb760-3394-462a-983a-ef7500753efa
535def1c-13fb-4b1f-827f-6568eb10db64
53a98cbe-18a6-4e41-8ba8-a67518c2d8de
b12a35c0-73d6-437b-a0a4-40c8482831ec
d3bd597d-db34-49cd-bf5d-eb757e02fb4d
79b3b46d-c7d8-47d2-a59d-ce5ded79b63b
```


## info for a given server 

```
$ python
Python 3.10.3 (v3.10.3:a342a49189, Mar 16 2022, 09:34:18) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from myos.server import Server
   
>>> server = Server(server_id='79b3b46d-c7d8-47d2-a59d-ce5ded79b63b')
>>> server.name
'vwn-gpu-2025-12-05-21-03-17-0'

>>> server.user.email
'neo@matrix.net'

>>> server.image.name
'rocky-8-aqml'

>>> server.flavor.name
'g-a100-80gb-2022.x1'
>>> server.flavor.cpu
28
>>> server.flavor.ram
230400
>>> server.flavor.disk
1536
```

## info for a given user domain

```
$ python
Python 3.10.3 (v3.10.3:a342a49189, Mar 16 2022, 09:34:18) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from myos.domain import Domain
   
>>> domain = Domain(name='stfc')
>>> domain.id
'5b43841657b74888b449975636082a3f'

>>> users = domain.users
>>> len(users)
44953
>>> users[0].id
'd3bbf2f95d122b85a8be35a433e102af58bd5e2b3bf610c15f824081c66ddfb0'
>>> users[0].name
'bj6703'

>>> domain = Domain(name='default')
>>> projects = domain.projects
>>> for project in projects:
...     project.name
...
'&Facts'
'A-Aziz-Scratch-Space'
'A-Huggan-Scratch-Space'
'Ada'
'Ada-Dev'
'admin'
'AGreenbank-Scratch-Space'
   ...
   ...
```

## get the entire list of hypervisors

```
$ python
Python 3.10.3 (v3.10.3:a342a49189, Mar 16 2022, 09:34:18) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from myos.cloud import Cloud
   
>>> cloud = Cloud("admin")
>>> hypervisors = cloud.hypervisors
>>> len(hypervisors)
656
>>> hv = hypervisors[0]
>>> hv.hostname
'hv300.matrix.net'
```

## owners of all VMs in a hypervisor

```
$ python
Python 3.10.3 (v3.10.3:a342a49189, Mar 16 2022, 09:34:18) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from myos.hypervisor import Hypervisor

>>> hv = Hypervisor(name='hv1.matrix.net')
>>> servers = hv.servers
>>> for server in servers:
...    print(server.name, server.id, server.user.name, server.user.id, server.user.email)
...
node1 fc3ca316-c59a-4604-abf7 neo e093655abf neo@matrix.net
node2 ab3fff55-c00b-aa65-45ab trinity ad10f44b0d trinity@matrix.net
```


## for a Cloud different than the admin one

The default Cloud is `admin`. In case there is a need for a query under different credentials:

```
$ python
Python 3.10.3 (v3.10.3:a342a49189, Mar 16 2022, 09:34:18) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from myos.cloud import Cloud
>>> dev_cloud = Cloud("admin-dev")

>>> from myos.hypervisor import Hypervisor
>>> hv = Hypervisor(name="hv400.matrix.net", cloud=dev_cloud)
>>> ...
```
