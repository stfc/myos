import json
from myos.tools import run
from myos.cloud import Cloud

#
# example:
#
#   $ openstack --os-cloud admin loadbalancer amphora show 4049623f-61c7-4739-a12a-8da22a177b4e -f json
#   {
#     "id": "4049623f-61c7-4739-a12a-8da22a177b4e",
#     "loadbalancer_id": "42f4894e-ae68-4ff7-8b50-508be82ac52f",
#     "compute_id": "0a0dde9d-7bd7-4808-8acf-365e64898685",
#     "lb_network_ip": "10.10.243.155",
#     "vrrp_ip": "192.168.0.101",
#     "ha_ip": "192.168.0.133",
#     "vrrp_port_id": "53a33d7c-8dd2-4404-ab5d-5fec9a6d7c7e",
#     "ha_port_id": "a867d3f9-0da9-4d10-8c1f-d0fbf51e1392",
#     "cert_expiration": "2026-05-09T12:34:58",
#     "cert_busy": false,
#     "role": "BACKUP",
#     "status": "ALLOCATED",
#     "vrrp_interface": "eth1",
#     "vrrp_id": 1,
#     "vrrp_priority": 90,
#     "cached_zone": "ceph",
#     "created_at": "2026-04-09T12:34:58",
#     "updated_at": "2026-04-09T12:35:43",
#     "image_id": "5c6d3874-f747-42ed-9bcd-b2dbb37c3abe",
#     "compute_flavor": "31c9bac0-f63a-4210-ae6c-f569f65124e8"
#   }
#   

class Amphora:
    def __init__(self, loadbalancer_id, cloud=Cloud()):
        """
        NOTE: we do not really need to use self._id
              and then a property method for id
              That's because amphoras don't have name,
              only IDs.
              However, we keep it for consistency, as
              this is how we do for every other class
        """
        self._cloud = cloud
        self._id = loadbalancer_id
        self._data_d = {}

    def _get_data(self):
        cmd = f'openstack --os-cloud {self._cloud.name} loadbalancer amphora show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def id(self):
        """
        returns the loadbalancer amphora ID 
        """
        return self._id

    @property
    def loadbalancer(self):
        """
        returns the LB of this Amphora
        """
        from myos.loadbalancer import LoadBalancer
        loadbalancer_id = self._data_d["loadbalancer_id"]
        return LoadBalancer(loadbalancer_id=loadbalancer_id)

