from rest_framework import serializers


class ManageEngineSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_null=False)


class CreateVMSerializer(serializers.Serializer):
    datacenter = serializers.CharField()
    cluster = serializers.CharField()
    datastore = serializers.CharField()
    network = serializers.CharField()
    name = serializers.CharField()
    cpu = serializers.IntegerField()
    num_cores_per_socket = serializers.IntegerField()
    ram = serializers.IntegerField()
    guest_os = serializers.CharField()
    network_adapter_type = serializers.CharField()
    disk_size = serializers.IntegerField()
    disk_label = serializers.CharField()


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
