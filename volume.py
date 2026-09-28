import json
from myos.tools import run
from myos.cloud import Cloud
from myos.entitylist import EntityList

# 
# $ openstack --os-cloud admin volume show 6ea541dc-5173-4ce2-9fd9-ca29c9c129c6 -f json
# {
#   "attachments": [
#     {
#       "id": "6ea541dc-5173-4ce2-9fd9-ca29c9c129c6",
#       "attachment_id": "228b39fb-63d7-48bf-9bb7-12bc8967b2eb",
#       "volume_id": "6ea541dc-5173-4ce2-9fd9-ca29c9c129c6",
#       "server_id": "f09b4d3b-0ed6-4241-b6b5-ede3475a4ec1",
#       "host_name": "hv644.nubes.rl.ac.uk",
#       "device": "/dev/vdb",
#       "attached_at": "2026-03-03T21:07:37.000000"
#     }
#   ],
#   "availability_zone": "ceph",
#   "bootable": "false",
#   "consistencygroup_id": null,
#   "created_at": "2026-03-03T21:05:53.000000",
#   "description": null,
#   "encrypted": false,
#   "id": "6ea541dc-5173-4ce2-9fd9-ca29c9c129c6",
#   "migration_status": null,
#   "multiattach": false,
#   "name": "aurora-cloud-workstation-ssh-data",
#   "os-vol-host-attr:host": "service12.nubes.rl.ac.uk@rbd#ceph",
#   "os-vol-mig-status-attr:migstat": null,
#   "os-vol-mig-status-attr:name_id": null,
#   "os-vol-tenant-attr:tenant_id": "06ee7f8a3202436288b09a981d341b75",
#   "properties": {},
#   "replication_status": null,
#   "size": 999,
#   "snapshot_id": null,
#   "source_volid": null,
#   "status": "in-use",
#   "type": "__DEFAULT__",
#   "updated_at": "2026-03-03T21:07:37.000000",
#   "user_id": "345ee13320a644fcb3960055cb79f96c19ff7fe36c5e7e1e4fface366de20582"
# }
# 

class Volume:
    def __init__(self, volume_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if volume_id:
            self._id = volume_id.strip()
        if name:
            self._name = name.strip()
        self._cloud = cloud
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} volume show {self._name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} volume show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)


    @property
    def name(self):
        """
        returns the name associated to this Volume
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the volume_id associated to this Volume
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def zone(self):
        """
        returns the availability_zone associated to this Volume
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['availability_zone']

    @property
    def bootable(self):
        """
        returns is this Volume is bootable
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['bootable']

    @property
    def encrypted(self):
        """
        returns is this Volume is encrypted
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['encrypted']

    @property
    def multiattach(self):
        """
        returns is this Volume is multiattach
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['multiattach']

    @property
    def migration_status(self):
        """
        returns the migration sttatus of this Volume
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['migration_status']

    @property
    def replication_status(self):
        """
        returns the replication sttatus of this Volume
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['replication_status']

    @property
    def size(self):
        """
        returns the size of this Volume
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['size']

    @property
    def status(self):
        """
        returns the status of this Volume
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['status']

    @property
    def type(self):
        """
        returns the type of this Volume
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['type']

    @property
    def user(self):
        """
        returns the User of this Volume
        """
        from myos.user import User
        if not self._data_d:
            self._get_data()
        user_id = self._data_d['user_id']
        return User(user_id=user_id)

    @property
    def servers(self):
        """
        returns the list of Servers attached to this Volume

        Attachements look like this

              "attachments": [
                {
                  "id": "e6a81cd7-c055-40fa-9e71-3d913b070c91",
                  "attachment_id": "1a6b211a-01c8-4d6c-a4a8-aa157c27d2bd",
                  "volume_id": "e6a81cd7-c055-40fa-9e71-3d913b070c91",
                  "server_id": "4d5a25dd-816a-4154-a5f3-710be37945d1",
                  "host_name": "hv983.nubes.rl.ac.uk",
                  "device": "/dev/sde",
                  "attached_at": "2026-06-17T09:06:42.000000"
                }
              ],
        """
        from myos.server import Server
        if not self._data_d:
            self._get_data()
        out = EntityList()
        for attachment in self._data_d['attachments']:
            server_id = attachment['server_id']
            server = Server(server_id=server_id)
            out.append(server)
        return out

