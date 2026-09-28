import json
from myos.tools import run
from myos.cloud import Cloud
from myos.entitylist import EntityList

#
# example:
#
#   $ openstack --os-cloud admin loadbalancer show 42f4894e-ae68-4ff7-8b50-508be82ac52f -f json
#   {
#     "admin_state_up": true,
#     "availability_zone": null,
#     "created_at": "2026-04-09T12:34:56",
#     "description": "Kubernetes API Load Balancer",
#     "flavor_id": null,
#     "id": "42f4894e-ae68-4ff7-8b50-508be82ac52f",
#     "listeners": [
#       {
#         "id": "b93671b1-a385-4a09-824a-86578c7772b2"
#       }
#     ],
#     "name": "terraform-local-k8s-api-lb",
#     "operating_status": "OFFLINE",
#     "pools": [
#       {
#         "id": "46cce6f8-5008-487f-8471-25a40bfa3093"
#       }
#     ],
#     "project_id": "91e057130eed4f8499d15741301511fd",
#     "provider": "amphora",
#     "provisioning_status": "ACTIVE",
#     "updated_at": "2026-04-09T12:36:16",
#     "vip_address": "192.168.0.133",
#     "vip_network_id": "5a86626f-63b5-48bb-a2cc-88b5f5842ca2",
#     "vip_port_id": "a867d3f9-0da9-4d10-8c1f-d0fbf51e1392",
#     "vip_qos_policy_id": null,
#     "vip_subnet_id": "ed21f47a-af93-44c2-8cc2-d49d8a64b9e0",
#     "vip_vnic_type": "normal",
#     "vip_sg_ids": "",
#     "tags": [],
#     "additional_vips": ""
#   }
#   

class LoadBalancer:
    def __init__(self, loadbalancer_id=None, name=None, cloud=Cloud()):
        self._cloud = cloud
        self._id = None
        self._name = None
        if loadbalancer_id:
            self._id = loadbalancer_id
        if name:
            self._name = name
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} loadbalancer show {self._name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} loadbalancer show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def name(self):
        """
        returns the name associated to this LoadBalancer
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the loadbalancer_id associated to this LoadBalancer
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def project(self):
        """
        returns the Project of this LoadBalancer
        """
        from myos.project import Project
        if not self._data_d:
            self._get_data()
        project_id = self._data_d['project_id']
        return Project(project_id=project_id)

    @property
    def amphoras(self):
        """
        example: 

        $ openstack --os-cloud admin loadbalancer amphora list --loadbalancer 42f4894e-ae68-4ff7-8b50-508be82ac52f -f json -c ID
        [
          {
            "id": "4049623f-61c7-4739-a12a-8da22a177b4e"
          },
          {
            "id": "7b757572-779e-4a98-9305-3f7267b7ced5"
          }
        ]
        """
        from myos.amphora import Amphora
        cmd = f'openstack --os-cloud {self._cloud.name} loadbalancer amphora list --loadbalancer {self.id} --format json -c ID'
        results = run(cmd)
        amphoras_l  = json.loads(results.out)
        out = EntityList()
        for amphora in amphoras_l:
            amphora_id = amphora['ID']
            out.append(Amphora(amphora_id=amphora_id))
        return out
