import json
from myos.tools import run
from myos.cloud import Cloud
from myos.entitylist import EntityList

class Image:
    def __init__(self, image_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if image_id:
            self._id = image_id.strip()
        if name:
            self._name = name.strip()
        self._cloud = cloud
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} image show {self._name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} image show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)


    @property
    def name(self):
        """
        returns the name associated to this Image
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the image_id associated to this Image
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def status(self):
        """
        returns the stautus of this Image
        """
        if not self._data_d:
            self._data_d()
        return self._data_d['status']

    @property
    def servers(self):
        """
        returns all Servers using this Image

        $ openstack --os-cloud admin server list --image  rocky-8-aqml--all-projects --format json --column ID
        [
           ...
           ...
           {
             "ID": "b12a35c0-73d6-437b-a0a4-40c8482831ec"
           },
           {
             "ID": "d3bd597d-db34-49cd-bf5d-eb757e02fb4d"
           },
           ...
           ...
        ]
        """
        from myos.server import Server
        cmd = f'openstack --os-cloud {self._cloud.name} server list --image {self.name} --all-projects --format json --column ID'
        results = run(cmd)
        servers_l = json.loads(results.out)
        out = EntityList()
        for server in servers_l:
            server_id = server['ID']
            out.append(Server(server_id=server_id))
        return out



if __name__ == '__main__':
    image = Image(name="rocky-8-aqml")
    print(image.name)
    print(image.id)
