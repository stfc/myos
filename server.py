import json
from datetime import datetime, timezone
from myos.tools import run
from myos.cloud import Cloud
from myos.entitylist import EntityList

class Server:
    def __init__(self, server_id=None, name=None, cloud=Cloud()):
        self._cloud = cloud
        self._id = None
        self._name = None
        if server_id:
            self._id = server_id
        if name:
            self._name = name.strip()
        self._data_d = {}

    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} server show {self._name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} server show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def name(self):
        """
        returns the name associated to this Server
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the server_id associated to this Server
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def status(self):
        """
        returns the status of this Server
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['status']

    @property
    def flavor(self):
        """
        returns the Flavor of this Server
        """
        from myos.flavor import Flavor
        if not self._data_d:
            self._get_data()
        flavor_name = self._data_d['flavor']['name']
        return Flavor(name=flavor_name)

    @property
    def image(self):
        """
        returns the Image of this Server
        """
        from myos.image import Image
        if not self._data_d:
            self._get_data()
        image_name = self._data_d['image'].split('(')[0].strip()
        return Image(name=image_name)

    @property
    def user(self):
        """
        returns the User who created this Server
        """
        from myos.user import User
        if not self._data_d:
            self._get_data()
        user_id = self._data_d['user_id']
        return User(user_id=user_id)

    @property
    def hypervisor(self):
        """
        returns the Hypervisor where this Server is running
        """
        from myos.hypervisor import Hypervisor
        if not self._data_d:
            self._get_data()
        hostname = self._data_d['OS-EXT-SRV-ATTR:hypervisor_hostname']
        return Hypervisor(name=hostname)

    @property
    def project(self):
        """
        returns the Project this Server belongs to 
        """
        from myos.project import Project 
        if not self._data_d:
            self._get_data()
        project_id = self._data_d['project_id']
        return Project(project_id=project_id)

    @property
    def volumes(self):
        """
        returns the list of Volumes attached to this Server

        they look like this:

              "volumes_attached": [
                {
                  "id": "1dae81a0-946c-43d1-93d7-f1e300a3331b",
                  "delete_on_termination": false
                },
                {
                  "id": "9d9b94b7-0ebd-439c-a15e-4bcd55b84c00",
                  "delete_on_termination": false
                },
                {
                  "id": "733b63ad-098f-492c-bd87-debe2ec24760",
                  "delete_on_termination": false
                },
                {
                  "id": "e6a81cd7-c055-40fa-9e71-3d913b070c91",
                  "delete_on_termination": false
                }
              ]
        """
        from myos.volume import Volume
        if not self._data_d:
            self._get_data()
        out = EntityList()
        for volume in self._data_d['volumes_attached']:
            volume_id = volume["id"]
            out.append(Volume(volume_id=volume_id))
        return out


    @property
    def snapshots(self):
        """
        returns the list of Images created as Snapshots from this Server
        It looks like this

            laptop : ~ $ openstack --os-cloud admin image list --property instance_uuid='e1564001-33e4-4a9a-8625-b49b84fbee3b' --property image_type='snapshot'
            +--------------------------------------+-----------------------------------------------------------------+--------+
            | ID                                   | Name                                                            | Status |
            +--------------------------------------+-----------------------------------------------------------------+--------+
            | ea4d373f-d50c-442b-a8d7-d2a9e2d5bd0f | stackstorm-e1564001-33e4-4a9a-8625-b49b84fbee3b-06-07-2026-0802 | active |
            | 1753fb61-0a07-4c73-a60f-7ec1cec251bb | stackstorm-e1564001-33e4-4a9a-8625-b49b84fbee3b-06-07-2026-0830 | active |
            | 60ccd485-7019-476f-8c70-6a90baf7f27c | stackstorm-e1564001-33e4-4a9a-8625-b49b84fbee3b-06-07-2026-0906 | active |
            | c0b36b18-efbc-4e10-9e9c-5bdb7cd9c40d | stackstorm-e1564001-33e4-4a9a-8625-b49b84fbee3b-06-07-2026-1130 | active |
            | 9b3eb2cc-9034-4dfe-9459-5b91c8b2124c | stackstorm-e1564001-33e4-4a9a-8625-b49b84fbee3b-06-07-2026-1500 | active |
            +--------------------------------------+-----------------------------------------------------------------+--------+
        """
        from myos.image import Image
        cmd = f'openstack --os-cloud {self._cloud.name} image list --property instance_uuid="{self.id}" --property image_type="snapshot" -f value -c ID'
        results = run(cmd)
        out = EntityList()
        for image_id in results.out.split():
            image_id = image_id.strip()
            out.append( Image(image_id=image_id) )
        return out


    # FIXME 
    # this is a draft. It needs a proper class EventList
    @property
    def seconds_in_current_state(self):
        import openstack
        conn = openstack.connect(cloud=self._cloud.name)
        events = list(conn.compute.server_actions(self.id))
        last_event = events[0]
        last_event_t = last_event.start_time
        # last_event_t looks like this
        # 2024-07-25T12:08:40.000000
        last_event_dt = datetime.fromisoformat(last_event_t).replace(
            tzinfo=timezone.utc
        )
        time_delta = datetime.now(timezone.utc) - last_event_dt
        seconds = int(time_delta.total_seconds())
        return seconds


    def start(self):
        """
        restarts this Server when it is in status SHUTOFF
        """
        cmd = f'openstack --os-cloud {self._cloud.name} server start {self.id}'
        results = run(cmd)
        return results.out

    def stop(self):
        """
        stops this Server when it is in status ACTIVE
        """
        cmd = f'openstack --os-cloud {self._cloud.name} server stop {self.id}'
        results = run(cmd)
        return results.out


if __name__ == '__main__':
    s = Server(server_id="79b3b46d-c7d8-47d2-a59d-ce5ded79b63b")
    print(s.id)
    print(s.name)
    #print(s.flavor.name)
    #print(s.flavor.id)
    #print(s.image.name)
    #print(s.image.id)
