from rest_framework import serializers


class CreateVMSerializer(serializers.Serializer):

    vsphere_datacenter = serializers.CharField()
    vsphere_cluster = serializers.CharField()
    vm_datastore = serializers.CharField()
    vm_network = serializers.CharField()
    vm_name = serializers.CharField()
    vm_cpu = serializers.IntegerField()
    vm_num_cores_per_socket = serializers.IntegerField()
    vm_ram = serializers.IntegerField()
    vm_guest = serializers.CharField()
    vm_network_adapter_type = serializers.CharField()
    vm_disk_size = serializers.IntegerField()
    vm_disk_label = serializers.CharField()


class UpdateVMSerializer(serializers.Serializer):

    vsphere_datacenter = serializers.CharField(required=False)
    vsphere_cluster = serializers.CharField(required=False)
    vm_datastore = serializers.CharField(required=False)
    vm_network = serializers.CharField(required=False)
    vm_cpu = serializers.IntegerField(required=False)
    vm_num_cores_per_socket = serializers.IntegerField(required=False)
    vm_ram = serializers.IntegerField(required=False)
    vm_guest = serializers.CharField(required=False)
    vm_network_adapter_type = serializers.CharField(required=False)
    vm_disk_size = serializers.IntegerField(required=False)
    vm_disk_label = serializers.CharField(required=False)
