import requests

from util import Util

start_url = 'https://raw.githubusercontent.com/epam-cross-platform-lab/swagger-dart-code-generator/master/example/input_folder/pet_service_json.json'

response = requests.get(start_url)

data = response.json()

# get all the paths
paths = data['paths']
# #print("paths:", paths)
# key is the path, value is the
for path, method in paths.items():
    # #print("path:", path)
    # #print("method:", method)
    # get tags
    for method_name, method_info in method.items():
        #print("method_name:", method_name)
        # #print("method_info:", method_info)
        # get tags
        tags = method_info.get('tags', [])
        #print("tags:", tags)
        # get summary
        summary = method_info.get('summary', '')
        #print("summary:", summary)
        # get operationId
        operationId = method_info.get('operationId', '')
        #print("operationId:", operationId)
        # get parameters
        parameters = method_info.get('parameters', [])
        #print("parameters:", parameters)
        # parameters: [{'in': 'body', 'name': 'input', 'description': 'input', 'required': True, 'schema': {'$ref': '#/definitions/TCustomerCodeReqVO'}}]
        # get TCustomerCodeReqVO from parameters
        class_name = ''
        for parameter in parameters:
            schema = parameter.get('schema', {})
            ref = schema.get('$ref', '')
            #print("ref:", ref)
            # get the class name from ref
            class_name = ref.split('/')[-1]
            #print("class_name:", class_name)
        # get responses
        responses = method_info.get('responses', {})
        #print("responses:", responses)
        # responses: {'200': {'description': 'OK', 'schema': {'$ref': '#/definitions/ReplyEntity«object»'}}, '201': {'description': 'Created'}, '401': {'description': 'Unauthorized'}, '403': {'description': 'Forbidden'}, '404': {'description': 'Not Found'}}
        # get the class name from responses
        for response_code, response_info in responses.items():
            # only handle the response response_name is 200
            #print('response_code:', response_code)
            if response_code != '200':
                continue
            #print('response_info:', response_info)
            schema = response_info.get('schema', {})
            ref = schema.get('$ref', '')
            ##print("ref:", ref)
            # get the class name from ref
            res_class_name = ref.split('/')[-1]
            #print("res_class_name:", res_class_name)
            # method_name, class_name, path, summary, operationId, parameters, res_class_name
            Util.generate_dart_service_function(method_name, class_name, path, summary, operationId, parameters, res_class_name)
        #print("==" * 80)

# get definitions
definitions = data['definitions']
#print("definitions:", definitions)
for definition_name, definition_info in definitions.items():
    # get the class name from definition_name
    class_name = definition_name
    class_str = f'''
    class {class_name} {{

    '''
    #print("definition_name:", definition_name)
    # #print("definition_info:", definition_info)
    properties = definition_info.get('properties', {})
    #print("properties:", properties)
    for property_name, property_info in properties.items():
        #print("property_name:", property_name)
        #print("property_info:", property_info)
        # get type
        type = property_info.get('type', '')
        #print("type:", type)
        # get format
        format = property_info.get('format', '')
        #print("format:", format)
        # get description
        description = property_info.get('description', '')
        #print("description:", description)
        # get ref
        ref = property_info.get('$ref', '')
        #print("ref:", ref)
        # get items
        items = property_info.get('items', {})
        #print("items:", items)
        # get $ref from items
        items_ref = items.get('$ref', '')
        #print("items_ref:", items_ref)
        #print("==" * 80)
    #print("==" * 80)
