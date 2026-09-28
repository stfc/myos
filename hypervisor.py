import json
import re
from myos.tools import run
from myos.cloud import Cloud
from myos.aggregate import Aggregate
from myos.entitylist import EntityList

class Hypervisor:
    def __init__(self, hypervisor_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if hypervisor_id:
            self._id = hypervisor_id.strip()
        if name:
            name = name.strip()
            if "." not in name:
                name += ".nubes.rl.ac.uk"
            self._name = name
        self._cloud = cloud
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} hypervisor show {self._name} --format json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} hypervisor show {self._id} --format json'
        results = run(cmd)
        self._data_d = json.loads(results.out)


    @property
    def hostname(self):
        """
        returns the hostname associated to this Hypervisor
        """
        if not self._name:
            self._get_data()
            return self._data_d['hypervisor_hostname']
        else:
            return self._name

    @property
    def name(self):
        """
        returns the hostname associated to this Hypervisor
        name and hostname are the same thing for this class
        """
        return self.hostname

    @property
    def id(self):
        """
        returns the hypervisor_id associated to this Hypervisor
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def uptime(self):
        """
        returns, if possible, the number of days
        since last time this HV was rebooted
        """
        try:
            match = re.search(r'(\d+)\s+days', self._data_d['uptime'])
            if match:
                out = int(match.group(1))
            else:
                out = None
        except:
            out = None
        return out

    @property 
    def status(self):
        """
        returns the status of this Hypervisor
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['status']

    @property 
    def state(self):
        """
        returns the state of this Hypervisor
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['state']

    @property
    def aggregate(self):
        """
        returns an Aggregate object 
        we assume a Hypervisor has one and only one Aggregate
        """
        if not self._data_d:
            self._get_data()
        aggregate_name = self._data_d['aggregates'][0]
        return Aggregate(name=aggregate_name)

    @property
    def servers(self):
        """
        returns the list of Servers running on this Hypervisor

        $ openstack --os-cloud admin server list --host hv-a100x8-8.nubes.rl.ac.uk --all-projects --format json
        [
          {
            "ID": "79b3b46d-c7d8-47d2-a59d-ce5ded79b63b",
            "Name": "vwn-gpu-2025-12-05-21-03-17-0",
            "Status": "ACTIVE",
            "Networks": {
              "Internal": [
                "172.16.112.77"
              ]
            },
            "Image": "rocky-8-aqml",
            "Flavor": "g-a100-80gb-2022.x1",
            "Project ID": "2d8252b430c2405da24d74df2004c24b"
          },
          ...
          ...
        ]
        """
        from myos.server import Server
        cmd = f'openstack --os-cloud {self._cloud.name} server list --host {self.name} --all-projects --format json'
        results = run(cmd)
        servers_l = json.loads(results.out)
        out = EntityList()
        for server in servers_l:
            server_id = server['ID']
            out.append(Server(server_id=server_id, cloud=self._cloud))
        return out


    # ========================================================== 
    #   perform actions
    # ========================================================== 

    def enable(self):
        """
        Enable this Hypervisor 

        example:
            openstack --os-cloud admin compute service set --enable hv399.nubes.rl.ac.uk nova-compute
        """
        cmd = f'openstack --os-cloud {self._cloud.name} compute service set --enable {self.name} nova-compute'
        results = run(cmd)
        return results

    def disable(self, reason=""):
        """
        Disable this Hypervisor 

        example:
            openstack --os-cloud admin compute service set --disable hv399.nubes.rl.ac.uk nova-compute
        """
        cmd = f'openstack --os-cloud {self._cloud.name} compute service set --disable {self.name} --disable-reason {reason} nova-compute'
        results = run(cmd)
        return results




if __name__ == '__main__':
    hv = Hypervisor(name='hv300.nubes.rl.ac.uk')
    hv = Hypervisor(name='hv-a100x8-8.nubes.rl.ac.uk')
    print(hv.id)
    print(hv.status)
    print(hv.state)
    print(len(hv.servers))
