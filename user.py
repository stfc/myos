import json
from myos.tools import run

from myos.project import Project
from myos.domain import Domain
from myos.cloud import Cloud
from myos.entitylist import EntityList


class User:
    def __init__(self, user_id=None, name=None, domain_name=None, cloud=Cloud()):
        self._cloud = cloud
        self._id = None
        self._name = None
        self._domain = None
        if user_id:
            self._id = user_id.strip()
        if name:
            self._name = name.strip()
            self._domain = Domain(name=domain_name)
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} user show {self._name} --domain {self._domain.name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} user show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def name(self):
        """
        returns the name associated to this User
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def domain(self):
        """
        returns the Domain associated to this User
        """
        if not self._domain:
            self._get_data()
            domain_id = self._data_d['domain_id']
            return Domain(domain_id=domain_id)
        else:
            return self._domain

    @property
    def id(self):
        """
        returns the user_id associated to this User
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def email(self):
        """
        returns the email associated to this User ID
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['email']


    @property
    def description(self):
        """
        returns the description associated to this User ID
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['description']

    @property
    def projects(self):
        """
        returns the list of Projects this user has access to
        """
        # 
        # FIXME this is not working fine
        #
        cmd = f'openstack --os-cloud {self._cloud.name} role assignment list --user {self.name} --names --user-domain {self.domain.name} --format json'
        results = run(cmd)
        projects_l  = json.loads(results.out)
        # output is like this
        #
        # [
        #  {
        #      "Role": "user",
        #      "User": "wup22514@stfc",
        #      "Group": "",
        #      "Project": "J-C-Bejar-Scratch-Space@default",
        #      "Domain": "",
        #      "System": "",
        #      "Inherited": false
        #    },
        #    {
        #      "Role": "user",
        #      "User": "wup22514@stfc",
        #      "Group": "",
        #      "Project": "Tier-1 Prod Internal@default",
        #      "Domain": "",
        #      "System": "",
        #      "Inherited": false
        #    }
        #  ]
        #
        out = EntityList()
        for proj in projects_l:
            project_name = proj['Project'].split('@')[0]
            out.append(Project(name=project_name))
        return out

    @property
    def servers(self):
        """
        returns all Servers created by this User
        """
        from myos.server import Server
        cmd = f'openstack --os-cloud {self._cloud.name} server list --user {self.name} --user-domain {self.domain.name} --all-projects --format json'
        # 
        # output looks like this
        #
        # laptop : /tmp $ openstack --os-cloud admin server list --user ea5c942075e14ea0a778ca63d0d8c332 --user-domain default --all-projects --format json
        # [
        #   {
        #     "ID": "4027da2e-c42b-411b-88f7-cc41f431959a",
        #     "Name": "vwn-gpu-2025-12-17-13-17-19-0",
        #     "Status": "ACTIVE",
        #     "Networks": {
        #       "Internal": [
        #         "172.16.103.45"
        #       ]
        #     },
        #     "Image": "rocky-8-aqml",
        #     "Flavor": "g-a100-80gb-2022.x1",
        #     "Project ID": "2d8252b430c2405da24d74df2004c24b"
        #   },
        #   {
        #     "ID": "9734feb4-b6b4-443d-847b-b3887230662c",
        #     "Name": "vwn-gpu-2025-12-17-11-17-48-0",
        #     "Status": "ACTIVE",
        #     "Networks": {
        #       "Internal": [
        #         "172.16.110.178"
        #       ]
        #     },
        #     "Image": "rocky-8-aqml",
        #     "Flavor": "g-a100-80gb-2022.x1",
        #     "Project ID": "2d8252b430c2405da24d74df2004c24b"
        #   },
        #   ....
        #   ....
        # ]
        #
        results = run(cmd)
        servers_l  = json.loads(results.out)
        out = EntityList()
        for server in servers_l:
            server_id = server['ID']
            out.append(Server(server_id=server_id))
        return out


class UserGroup:
    #
    #   $ openstack --os-cloud admin group show --domain jasmin glo-fhicc-U-vcloud_admins
    #   +-------------+------------------------------------------------------------------+
    #   | Field       | Value                                                            |
    #   +-------------+------------------------------------------------------------------+
    #   | description | cluster:vio-group                                                |
    #   | domain_id   | f6fc1289348e49f1b9c32af2f680c9b3                                 |
    #   | id          | 50b756eb08c83d1dac679f417b8514d314114a797fec953af38b40e9a26be133 |
    #   | name        | glo-fhicc-U-vcloud_admins                                        |
    #   +-------------+------------------------------------------------------------------+
    #   
    def __init__(self, group_id=None, name=None, domain_name=None, cloud=Cloud()):
        self._cloud = cloud
        self._id = None
        self._name = None
        self._domain = None
        if group_id:
            self._id = group_id
        if name:
            self._name = name
            self._domain = Domain(name=domain_name)
        self._data_d = {}

    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} group show {self._name} --domain {self._domain.name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} group show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def name(self):
        """
        returns the name associated to this User Group
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def domain(self):
        """
        returns the Domain associated to this User Group
        """
        if not self._domain:
            self._get_data()
            domain_id = self._data_d['domain_id']
            return Domain(domain_id=domain_id)
        else:
            return self._domain

    @property
    def id(self):
        """
        returns the user_id associated to this User Group
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def description(self):
        """
        returns the description associated to this User Group
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['description']

    @property
    def users(self):
        """
        returns the list of Users in this User Group
        """
        cmd = f'openstack --os-cloud {self._cloud.name} user list --group {self.id} -f json -c ID'
        results = run(cmd)
        users_l  = json.loads(results.out)
        out = EntityList()
        for user in users_l:
            user_id = user['ID']
            out.append(User(user_id=user_id))
        return out




if __name__ == '__main__':
    #u = User(name="admin-wup22514")
    #u = User(name="wup22514@stfc")
    u = User(name="wup22514")
    #u = User(user_id="d0b0337d0d3aff182ebb41ff5581ea057c18daeaaeda3b3cc56adce83d6b67d1")

    print(u.name)
    print(u.id)
    #print(u.email)
    #print(u.description)
    #print(u.domain.name)
    #print(u.domain.id)
    #print(len(u.projects))
    #pp = u.projects
    #for p in pp:
    #    print(p.name)
    #    print(p.id)

