udf_fields_mapping = {
    "udf_pick_5415": "datacenter",
    "udf_pick_5416": "cluster",
    "udf_pick_5417": "datastore",
    "udf_pick_5418": "network",
    "udf_sline_5419": "name",
    "udf_sline_1524": "cpu",
    "udf_long_5420": "num_cores_per_socket",
    "udf_sline_1525": "ram",
    "udf_sline_5425": "guest_os",
    "udf_pick_5422": "network_adapter_type",
    "udf_sline_5423": "disk_size",
    "udf_sline_5424": "disk_label",
}


class UDFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            udf_fields = request.data.get('content').get('request').get('udf_fields', {})
            mapped_data = {}
            for key, value in udf_fields.items():
                if key in udf_fields_mapping:
                    mapped_data[udf_fields_mapping[key]] = value
            request.udf_data = mapped_data
        response = self.get_response(request)
        return response
