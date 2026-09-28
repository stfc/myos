import json
from myos.tools import run
from myos.cloud import Cloud
from myos.entitylist import EntityList

class Aggregate:
    def __init__(self, aggregate_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if aggregate_id:
            self._id = aggregate_id.strip()
        if name:
            self._name = name.strip()
        self._cloud = cloud
        self._data_d = {}

    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} aggregate show {self._name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} aggregate show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def name(self):
        """
        returns the name associated to this Aggregate 
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the server_id associated to this Aggregate 
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def hypervisors(self):
        """
        returns the entire list of Hypervisors with this Aggregate
        """
        from myos.hypervisor import Hypervisor
        if not self._data_d:
            self._get_data()
        out = EntityList()
        for hypervisor_name in self._data_d["hosts"]:
            out.append(Hypervisor(name=hypervisor_name, cloud=self._cloud))
        return out
