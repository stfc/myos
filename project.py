import json
from myos.tools import run
from myos.cloud import Cloud
from myos.entitylist import EntityList


class Project:
    def __init__(self, project_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if project_id:
            self._id = project_id.strip()
        if name:
            self._name = name.strip()
        self._cloud = cloud
        self._data_d = {}

    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} project show "{self._name}" -f json'
        else:
            cmd = f'openstack --os-cloud {self._cloud.name} project show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def name(self):
        """
        returns the name associated to this Project
        """
        if not self._name:
            self._get_data()
            return self._data_d['name']
        else:
            return self._name

    @property
    def id(self):
        """
        returns the ID associated to this Project
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def parent(self):
        """
        returns the parent Project associated to this Project
        """
        if not self._id:
            self._get_data()
        parent_id = self._data_d['parent_id']
        if parent_id == None:
            return None
        else:
            return Project(project_id=parent_id)

    @property
    def tags(self):
        """
        returns the tags associated to this Project
        output is a list of strings
        """
        if not self._id:
            self._get_data()
        return self._data_d['tags']

    @property
    def servers(self):
        """
        get the list of Servers currently running on this Project
       
        $ openstack --os-cloud admin server list --project ncas-force-U
        +--------------------------------------+-----------------------------------+--------+-------------------------------+-------+----------+----------------------------------+
        | ID                                   | Name                              | Status | Networks                      | Image | Flavor   | Project ID                       |
        +--------------------------------------+-----------------------------------+--------+-------------------------------+-------+----------+----------------------------------+
        | 99333158-356a-41a5-9c64-84f9e8e881f9 | force-staging-control-plane-fb4sb | ACTIVE | portal-internal=192.168.3.77  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 3e447537-b525-4792-a277-e274963b02a2 | force-staging-control-plane-c5xnn | ACTIVE | portal-internal=192.168.3.254 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | dd928a49-ac65-484c-95af-14bafc67404e | force-staging-staging-pljbm-fv7k9 | ACTIVE | portal-internal=192.168.3.58  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 28a58a54-9ffe-490c-8a37-ad331d6055c7 | force-staging-staging-pljbm-lhndq | ACTIVE | portal-internal=192.168.3.60  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | fb231de3-2eee-4411-8cd6-8a404cf9476c | force-staging-staging-pljbm-rnxr9 | ACTIVE | portal-internal=192.168.3.180 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 27d111dc-1e2d-41b7-a19c-01ef0713c8c4 | force-staging-control-plane-kfcql | ACTIVE | portal-internal=192.168.3.26  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 2738bd95-50e0-40b1-80bc-5551a285507d | force-live-control-plane-mm5xz    | ACTIVE | portal-internal=192.168.3.43  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | e5dfbdc1-e993-4138-80b1-bb73e9d5b3f4 | force-live-control-plane-pszdt    | ACTIVE | portal-internal=192.168.3.242 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | e83b9437-1abd-4adb-a98b-43669594b187 | force-live-live-8wptz-dmfbh       | ACTIVE | portal-internal=192.168.3.84  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 5a915b61-2402-4463-9819-294c0a6d44e3 | force-live-live-8wptz-7qqr4       | ACTIVE | portal-internal=192.168.3.192 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | f21978e5-99a5-4456-a6e7-219ec6410f96 | force-live-live-8wptz-2gbqp       | ACTIVE | portal-internal=192.168.3.63  |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        | 23c7d1b6-ff4c-405b-b71c-42060ab22312 | force-live-control-plane-bk6dl    | ACTIVE | portal-internal=192.168.3.231 |       | l3.micro | 5b37be0037c94b69a35e72cb2da8b016 |
        +--------------------------------------+-----------------------------------+--------+-------------------------------+-------+----------+----------------------------------+

        $ openstack --os-cloud {self._cloud.name} server list --project Condor --format json
        [
          {
            "ID": "e2951a59-e290-430f-8f12-1fa4168c3024",
            "Name": "vwn-gpu-2025-12-17-07-17-16-0",
            "Status": "SHUTOFF",
            "Networks": {
              "Internal": [
                "172.16.112.122"
              ]
            },
            "Image": "rocky-8-aqml",
            "Flavor": "g-a100-80gb-2022.x1",
            "Project ID": "2d8252b430c2405da24d74df2004c24b"
          },
          ...
          ...
        """
        from myos.server import Server
        cmd = f'openstack --os-cloud {self._cloud.name} server list --project {self.name} --format json'
        results = run(cmd)
        servers_l = json.loads(results.out)
        out = EntityList()
        for server in servers_l:
            server_id = server["ID"]
            out.append(Server(server_id=server_id))
        return out

    @property
    def users(self):
        """
        returns the list of Users with access to this Project

        $ openstack --os-cloud admin role assignment list --project Condor  --names --format json
        [
          {
            "Role": "user",
            "User": "mfh49987@stfc",
            "Group": "",
            "Project": "Condor@default",
            "Domain": "",
            "System": "",
            "Inherited": false
          },
          ...
          ...
        ]
        """
        from myos.user import User
        cmd = f'openstack --os-cloud {self._cloud.name} role assignment list --project {self.id} --names --format json'
        results = run(cmd)
        users_l = json.loads(results.out)
        out = EntityList()
        for user in users_l:
            user_name = user['User']
            out.append(User(name=user_name))
        return out
       
    @property
    def fips(self):
        """
        returns the list of Floating IPs in this Project

        $ openstack --os-cloud admin floating ip list --project lsst-drp --format json
        [
          {
            "ID": "3b90998e-ab39-45b4-b56e-120e00d31fdb",
            "Floating IP Address": "130.246.83.113",
            "Fixed IP Address": null,
            "Port": null,
            "Floating Network": "5283f642-8bd8-48b6-8608-fa3006ff4539",
            "Project": "22547d0eef6445ff9febfedec9b4da4a"
          }
        ]        
        """
        from myos.ip import FloatingIP
        cmd = f'openstack --os-cloud {self._cloud.name} floating ip list --project {self.name} --format json'
        results = run(cmd)
        fip_l = json.loads(results.out)
        out = EntityList()
        for fip in fip_l:
            fip_id = fip['ID']
            out.append(FloatingIP(fip_id=fip_id))
        return out

    @property
    def volumes(self):
        """
        returns the list of Volumes in this Project

        $ openstack --os-cloud admin volume list --project 06ee7f8a3202436288b09a981d341b75  -f json -c ID
        [
          {
            "ID": "f341094e-d27c-4251-b801-5465df070af3"
          },
          {
            "ID": "6ea541dc-5173-4ce2-9fd9-ca29c9c129c6"
          }
        ]
        """
        from myos.volume import Volume
        cmd = f'openstack --os-cloud {self._cloud.name} volume list --project {self.name} --format json -c ID'
        results = run(cmd)
        volume_l = json.loads(results.out)
        out = EntityList()
        for volume in volume_l:
            volume_id = volume['ID']
            out.append(Volume(volume_id=volume_id))
        return out


    @property
    def images(self):
        """
        returns the list of Images in this Project

        $ openstack --os-cloud admin image list --project fa0f417fb4b5462791e4320e317eb2d2 -f json -c ID 
        [
          {
            "ID": "44d86835-03ba-4ce4-bd8f-649f52434815"
          },
          {
            "ID": "30f6e47f-3ec5-4fa4-a305-df06c56d00d6"
          },
          ...
          ...
        ]
        """
        from myos.image import Image
        cmd = f'openstack --os-cloud {self._cloud.name} image list --project {self.name} --format json -c ID'
        results = run(cmd)
        image_l = json.loads(results.out)
        out = EntityList()
        for image in image_l:
            image_id = image['ID']
            out.append(Image(image_id=image_id))
        return out

    @property
    def flavors(self):
        """
        returns the list of Flavors in this Project

        $ openstack --os-cloud J-C-Bejar-Scratch-Space flavor list --os-project-id f7c59f63597648caa654c3427f8d22d3 -f json -c ID 
        [
          {
            "ID": "0001e264-dc23-4029-a71e-3be4c70635c1"
          },
          {
            "ID": "0d2555d9-23dc-4b40-a2f4-d03281d58719"
          },
          ...
          ...
        ]
        """
        from myos.flavor import Flavor
        cmd = f'openstack --os-cloud {self._cloud.name} flavor list --os-project-id {self.id} --format json -c ID'
        results = run(cmd)
        flavor_l = json.loads(results.out)
        out = EntityList()
        for flavor in flavor_l:
            flavor_id = flavor['ID']
            out.append(Flavor(flavor_id=flavor_id))
        return out


    @property
    def quotas(self):
        from myos.quota import Quota
        cmd = f'openstack --os-cloud {self._cloud.name} quota show {self.name} --format json'
        results = run(cmd)
        return Quota(json.loads(results.out))

    @property
    def shared_quotas(self):
        from myos.quota import SharedQuota
        cmd = f'openstack --os-cloud {self._cloud.name} share quota show {self.name} --format json'
        results = run(cmd)
        return SharedQuota(json.loads(results.out))



    ####################################
    # BEGIN DEV
    ####################################

    def add(self, entity):
        from myos.user import User, UserGroup
        from myos.flavor import Flavor
        if type(entity) is User:
            self._add_user(entity)
        elif type(entity) is UserGroup:
            self._add_user_group(entity)
        elif type(entity) is Flavor:
            self._add_flavor(entity)

    def remove(self, entity):
        from myos.user import User
        if type(entity) is User:
            self._remove_user(entity)
        elif type(entity) is Flavor:
            self._remove_flavor(entity)

    def set_quota_cores(self, cores):
        self._set_quota("cores", cores)

    def set_quota_ram(self, ram):
        self._set_quota("ram", ram)

    def set_quota_gigabytes(self, gigabytes):
        self._set_quota("gigabytes", gigabytes)

    def set_quota_floaiting_ips(self, floating_ips):
        self._set_quota("floating_ips", floating_ips)


    def _add_user(self, user):
        # example: 
        #    openstack role add user 
        #    --user 69669657eb53642a96b6a03cf27fb47b9fef0f863da0e5ca285c724c91c50e47 
        #    --project f2ae44b03b3742d0808c6197b76b0e5e 
        #    --user-domain stfc
        cmd = f'openstack --os-cloud {self._cloud.name} role add --user {user.id} --project {self.name} --user-domain {user.domain.name} user'
        results = run(cmd)

    def _add_user_group(self, group):
        # example:
        # openstack role add 
        # --project b23574609dd44a219b1dbf5d69a8f6d1 
        # --group 43eba3ef7244a53f90f5d114fbf3f3ce0578a08f430aca380ff597d6a40381b3 
        # --group-domain jasmin 
        # user
        cmd = f'openstack --os-cloud {self._cloud.name} role add --project {self.id} --group {group.id} --group-domain {group.domain.id} user'
        results = run(cmd)

    def _add_flavor(self, flavor):
        # command:
        #  openstack flavor set --project <project_name_or_UID> <flavor_name>
        cmd = f'openstack --os-cloud {self._cloud.name} flavor set --project {self.name} {flavor.name}'
        results = run(cmd)

    def _remove_user(self, user):
        cmd = f'openstack --os-cloud {self._cloud.name} role remove --user {user.id} --project {self.name} --user-domain {user.domain.name} user'
        results = run(cmd)

    def _remove_flavor(self, flavor):
        # command:
        #  openstack flavor unset --project <project_name_or_UID> <flavor_name>
        cmd = f'openstack --os-cloud {self._cloud.name} flavor unset --project {self.name} {flavor.name}'
        results = run(cmd)

    def _set_quota(self, resource, value):
        cmd = f'openstack --os-cloud {self._cloud.name} quota set --{resource} {value} {self.id}'
        results = run(cmd)


    ####################################
    # END DEV
    ####################################



if __name__ == '__main__':
    p = Project(name="lsst-drp")
    print(p.name)
    print(p.id)
    #ss = p.servers
    #for s in ss:
    #    print(s.id)
    #    print(s.name)
    #uu = p.users
    #for u in uu:
    #    print(u.name)
    #fips = p.fips
    #print(fips[0].ip)
    quotas = p.quotas
    print(quotas.cores)
    print(quotas.ram)

