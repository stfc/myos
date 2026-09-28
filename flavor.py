import json
from myos.tools import run
from myos.cloud import Cloud
from myos.entitylist import EntityList

#  
#  $ openstack --os-cloud admin flavor show l3.micro --format json
#  {
#    "OS-FLV-DISABLED:disabled": false,
#    "OS-FLV-EXT-DATA:ephemeral": 0,
#    "access_project_ids": null,
#    "description": null,
#    "disk": 100,
#    "id": "300f36c7-603d-4c69-80d1-1dc610c309b8",
#    "name": "l3.micro",
#    "os-flavor-access:is_public": true,
#    "properties": {
#      "accounting:per_unit_cost_": "0.00803197370188318",
#      "accounting:per_unit_cost_0.0076": "0.00803197370188318",
#      "accounting:per_unit_cost_2017": "0.0097",
#      "accounting:per_unit_cost_2018": "0.0097",
#      "accounting:per_unit_cost_2019": "0.0097",
#      "accounting:per_unit_cost_2020": "0.0097",
#      "accounting:per_unit_cost_2021": "0.0061",
#      "accounting:per_unit_cost_2022": "0.0076",
#      "accounting:per_unit_cost_2023": "0.00895946042127653",
#      "accounting:per_unit_cost_2024": "0.00814399936892479",
#      "accounting:total_unit_cost_": "0.0321278948075327",
#      "accounting:total_unit_cost_0.0076": "0.0321278948075327",
#      "accounting:total_unit_cost_2017": "0.0388",
#      "accounting:total_unit_cost_2018": "0.0388",
#      "accounting:total_unit_cost_2019": "0.0388",
#      "accounting:total_unit_cost_2020": "0.0388",
#      "accounting:total_unit_cost_2021": "0.7564",
#      "accounting:total_unit_cost_2022": "0.0304",
#      "accounting:total_unit_cost_2023": "0.0358378416851061",
#      "accounting:total_unit_cost_2024": "0.0325759974756992",
#      "accounting:unit": "core",
#      "aggregate_instance_extra_specs:hosttype": "localamd",
#      "aggregate_instance_extra_specs:local-storage-type": "nvme",
#      "hw:cpu_policy": "dedicated",
#      "hw:vif_multiqueue_enabled": "true"
#    },
#    "ram": 16384,
#    "rxtx_factor": 1.0,
#    "swap": 0,
#    "vcpus": 4
#  }
#  



class Flavor:
    def __init__(self, flavor_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if flavor_id:
            self._id = flavor_id.strip()
        if name:
            self._name = name.strip()
        self._cloud = cloud
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} flavor show {self._name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} flavor show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)


    @property
    def name(self):
        """
        returns the name associated to this Flavor
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the flavor_id associated to this Flavor
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def disk(self):
        """
        returns the Disk associated to this Flavor
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['disk']

    @property
    def ram(self):
        """
        returns the RAM associated to this Flavor
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['ram']

    @property
    def cpu(self):
        """
        returns the vcpu associated to this Flavor
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['vcpus']

    @property
    def servers(self):
        """
        returns all Servers using this Flavor

        $ openstack --os-cloud admin server list --flavor l3.micro --all-projects --format json --column ID
        [
           ...
           ...
            {
              "ID": "99082bba-317b-4f9f-a41b-c7b017f76aac"
            },
            {
              "ID": "cf1ca0a0-f3c8-4266-8f60-5add79b1b7bb"
            },
            {
              "ID": "2a965539-3259-4acc-a43c-ea3e6775b396"
            },
           ...
           ...
        ]
        """
        from myos.server import Server
        cmd = f'openstack --os-cloud {self._cloud.name} server list --flavor {self.name} --all-projects --format json --column ID'
        results = run(cmd)
        servers_l = json.loads(results.out)
        out = EntityList()
        for server in servers_l:
            server_id = server['ID']
            out.append(Server(server_id=server_id))
        return out


    @property
    def hypervisors(self):
        """
        returns all Hypervisor compatible with this Flavor

        this method is implemented in python
        an equivalent using the command line would be something like this

                # 1. Set your cloud environment variable (equivalent to cloud="admin")
                export OS_CLOUD=admin
                
                # 2. Fetch the flavor specs, find matching aggregates, and list their hosts
                openstack aggregate list -f json | jq -r --argjson specs "$(
                  openstack flavor show g-v100.large -f json | jq '
                    .properties |
                    {
                      hosttype: ."aggregate_instance_extra_specs:hosttype",
                      storage: ."aggregate_instance_extra_specs:local-storage-type"
                    }
                  '
                )" '
                  .[] |
                  select(.Properties.hosttype == $specs.hosttype and .Properties."local-storage-type" == $specs.storage) |
                  .Hosts[]
                '
        """
        from myos.hypervisor import Hypervisor
        import openstack

        conn = openstack.connect(cloud=self._cloud.name)
        flavor = conn.compute.find_flavor(self.name)
        flavor_hosttype = flavor.extra_specs.get("aggregate_instance_extra_specs:hosttype")
        flavor_storage_type = flavor.extra_specs.get("aggregate_instance_extra_specs:local-storage-type")
        out = EntityList()
        for agg in conn.compute.aggregates():
            if agg.metadata.get("hosttype") == flavor_hosttype and\
               agg.metadata.get("local-storage-type") == flavor_storage_type:
                    for hypervisor_name in agg.hosts:
                        out.append(Hypervisor(name=hypervisor_name))
        return out




        



if __name__ == '__main__':
    flavor = Flavor(name="l3.micro")
    print(flavor.name)
    #print(flavor.id)
    print(flavor.disk)
    print(flavor.ram)
    print(flavor.cpu)



