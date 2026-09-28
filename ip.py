import json
from myos.tools import run
from myos.cloud import Cloud

class FloatingIP:
    def __init__(self, fip_id=None, name=None, cloud=Cloud()):
        self._id = None
        self._name = None
        if fip_id:
            self._id = fip_id
        if name:
            self._name = name
        self._cloud = cloud
        self._data_d = {}


    def _get_data(self):
        if self._name:
            cmd = f'openstack --os-cloud {self._cloud.name} floating ip show {self._name} -f json'
        if self._id:
            cmd = f'openstack --os-cloud {self._cloud.name} floating ip show {self._id} -f json'
        results = run(cmd)
        self._data_d = json.loads(results.out)

    @property
    def ip(self):
        """
        returns the Floating IP value
        """
        if not self._name:
            self._get_data()
            return self._data_d['floating_ip_address']
        else:
            return self._name

    @property
    def name(self):
        """
        returns the Floating IP value
        name and ip are the same thing for this class
        """
        return self.ip


    @property
    def id(self):
        """
        returns the FIP ID associated to this Floating IP
        """
        if not self._id:
            self._get_data()
            return self._data_d['id']
        else:
            return self._id

    @property
    def fixed_ip(self):
        """
        returns the Fixed IP associated to this Floating IP
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['fixed_ip_address']

    @property
    def port(self):
        """
        returns the port associated to this Floating IP
        """
        if not self._data_d:
            self._get_data()
        return self._data_d['port_id']

    @property
    def project(self):
        """
        returns the Project associated to this Floating IP
        """
        from myos.project import Project
        if not self._data_d:
            self._get_data()
        project_id = self._data_d['project_id']
        return Project(project_id=project_id)

