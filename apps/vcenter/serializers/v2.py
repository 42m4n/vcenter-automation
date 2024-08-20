from rest_framework import serializers


class ManageEngineSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_null=False)


class CreateVMSerializer(serializers.Serializer):
    datacenter = serializers.CharField()
    cluster = serializers.CharField()
    datastore = serializers.CharField()
    network = serializers.CharField(required=False)
    name = serializers.CharField()
    cpu = serializers.IntegerField()
    num_cores_per_socket = serializers.IntegerField(required=False)
    ram = serializers.IntegerField()
    guest_os = serializers.CharField(required=False)
    network_adapter_type = serializers.CharField(required=False)
    disk_size = serializers.IntegerField(required=False)
    disk_label = serializers.CharField(required=False)
    ticket_id = serializers.CharField()
    hostname = serializers.CharField(required=False)
    ip_addr = serializers.CharField()
    cidr = serializers.IntegerField()
    defaultGW = serializers.CharField()
    dns_server1 = serializers.CharField(required=False)
    dns_server2 = serializers.CharField(required=False)
    vlan_id = serializers.IntegerField()


class UpdateVMSerializer(serializers.Serializer):
    datacenter = serializers.CharField(required=False)
    cluster = serializers.CharField(required=False)
    datastore = serializers.CharField(required=False)
    network = serializers.CharField(required=False)
    cpu = serializers.IntegerField(required=False)
    num_cores_per_socket = serializers.IntegerField(required=False)
    ram = serializers.IntegerField(required=False)
    guest_os = serializers.CharField(required=False)
    network_adapter_type = serializers.CharField(required=False)
    disk_size = serializers.IntegerField(required=False)
    disk_label = serializers.CharField(required=False)
    ticket_id = serializers.CharField()
    ip_addr = serializers.CharField(required=False)
    cidr = serializers.IntegerField(required=False)
    defaultGW = serializers.CharField(required=False)
    dns_server1 = serializers.CharField(required=False)
    dns_server2 = serializers.CharField(required=False)
    vlan_id = serializers.IntegerField(required=False)
