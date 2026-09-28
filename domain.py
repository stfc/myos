import json
from myos.tools import run
from myos.cloud import Cloud
from myos.entitylist import EntityList


class Domain:
    def __init__(self, domain_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if domain_id:
            self._id = domain_id.strip()
        if name:
            self._name = name.strip()
        self._cloud = cloud
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} domain show {self._name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} domain show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)


    @property
    def name(self):
        """
        returns the name associated to this Domain
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the domain_id associated to this Domain
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def projects(self):
        """
        return the list of Projects in this Domain

        $ openstack --os-cloud admin project list --domain default --format json 
        [
          {
            "ID": "93da37ef58344f4bac74d0b8b101f591",
            "Name": "&Facts"
          },
          {
            "ID": "22dae50f357e468ca12a1fa1f27ca30a",
            "Name": "A-Aziz-Scratch-Space"
          },
          ...
          ...
        ]
        """
        from myos.project import Project
        cmd = f'openstack --os-cloud {self._cloud.name} project list --domain {self.name} --format json'
        results = run(cmd)
        projects = json.loads(results.out)
        out = EntityList()
        for project in projects:
            project_id = project['ID']
            out.append(Project(project_id=project_id))
        return out

    @property
    def users(self):
        """
        return the list of Users in this Domain

        $ openstack --os-cloud admin user list --domain jasmin --format json 
        [
          {
            "ID": "9c13fb710ddb74906be0791f08439e2581b9ba72a3f38599a4c5a7f50e5643ae",
            "Name": "mrichardson001"
          },
          {
            "ID": "665dd5f2f2327261b4a700c47072229c916f57936028b7f9abd51fdad5447048",
            "Name": "mnorton"
          },
          ...
          ...
        ]
        """
        from myos.user import User
        cmd = f'openstack --os-cloud {self._cloud.name} user list --domain {self.name} --format json'
        results = run(cmd)
        out = EntityList()
        users = json.loads(results.out)
        for user in users:
            user_id = user['ID']
            out.append(User(user_id=user_id))
        return out




if __name__ == '__main__':
    #domain = Domain(name="stfc")
    #print(domain.name)
    #print(domain.id)
    #domain = Domain(name='default')
    #projects = domain.projects
    #for project in projects:
    #    print(project.id)
    domain = Domain(name='jasmin')
    users = domain.users
    for user in users:
        print(user.id)




