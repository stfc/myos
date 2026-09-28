import json
from myos.tools import run
from myos.entitylist import EntityList

class Cloud:
    def __init__(self, name="admin"):
        self.name = name 

    @property
    def hypervisors(self):
        """
        returns the entire list of Hypervisor objects for this cloud instance
        """
        from myos.hypervisor import Hypervisor
        cmd = f'openstack --os-cloud {self.name} hypervisor list --format json'
        results = run(cmd)
        hv_l = json.loads(results.out)
        out = EntityList() 
        for hv in hv_l:
            hostname = hv['Hypervisor Hostname']
            out.append( Hypervisor(name=hostname, cloud=self) )
        return out

    @property
    def users(self):
        """
        returns the entire list of Users for this cloud instance
        """
        from myos.user import User
        cmd = f'openstack --os-cloud {self.name} user list --format json'
        results = run(cmd)
        user_l = json.loads(results.out)
        out = EntityList() 
        for user in user_l:
            user_id = user['ID']
            out.append( User(user_id=user_id, cloud=self) )
        return out


    @property
    def flavors(self):
        """
        returns the entire list of Flavor objects for this cloud instance
        """
        from myos.flavor import Flavor
        cmd = f'openstack --os-cloud {self.name} flavor list --all --format json'
        results = run(cmd)
        flavor_l = json.loads(results.out)
        out = EntityList()
        for flavor in flavor_l:
            flavor_id = flavor['ID']
            out.append( Flavor(flavor_id=flavor_id, cloud=self) )
        return out

    @property
    def images(self):
        """
        returns the entire list of Image objects for this cloud instance
        """
        from myos.image import Image
        cmd = f'openstack --os-cloud {self.name} image list --all --format json'
        results = run(cmd)
        image_l = json.loads(results.out)
        out = EntityList()
        for image in image_l:
            image_id = image['ID']
            out.append( Image(image_id=image_id, cloud=self) )
        return out
    
    @property
    def projects(self):
        """
        returns the entire list of Project objects for this cloud instance
        """
        from myos.project import Project
        cmd = f'openstack --os-cloud {self.name} project list --format json'
        results = run(cmd)
        project_l = json.loads(results.out)
        out = EntityList()
        for project in project_l:
            project_id = project['ID']
            out.append( Project(project_id=project_id, cloud=self) )
        return out

    @property
    def fips(self):
        """
        returns the entire list of FloatingIP objects for this cloud instance
        """
        from myos.ip import FloatingIP
        cmd = f'openstack --os-cloud {self.name} floating ip list --format json'
        results = run(cmd)
        fip_l = json.loads(results.out)
        out = EntityList()
        for fip in fip_l:
            fip_id = fip['ID']
            out.append( FloatingIP(fip_id=fip_id, cloud=self) )
        return out

    @property
    def volumes(self):
        """
        returns the entire list of Volume objects for this cloud instance
        """
        from myos.volume import Volume
        cmd = f'openstack --os-cloud {self.name} volume list --all-projects --format json'
        results = run(cmd)
        volume_l = json.loads(results.out)
        out = EntityList()
        for volume in volume_l:
            volume_id = volume['ID']
            out.append( Volume(volume_id=volume_id, cloud=self) )
        return out

    def get_servers_from_ip(self, ip):
        """
        get all Servers behind a given IP
        """
        from myos.server import Server
        cmd = f'openstack --os-cloud {self.name} server list --all-projects --ip {ip} -f json -c ID'
        results = run(cmd)
        id_l = json.loads(results.out)
        out = EntityList()
        for section in id_l:
            ID = section['ID']
            out.append( Server(server_id=ID, cloud=self) )
        return out


if __name__ == '__main__':
    cloud = Cloud("admin")
    #hv_l = cloud.hypervisors
    #print(len(hv_l))
    #flavor_l = cloud.flavors
    #print(len(flavor_l))
    #image_l = cloud.images
    #print(len(image_l))
    fip_l = cloud.fips
    print(len(fip_l))

