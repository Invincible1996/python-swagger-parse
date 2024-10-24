class Util:
    # generate the dart service function by method_name, class_name, path, summary, operationId, parameters, res_class_name
    # eg: Future<ReplyEntity<object>> getCustomerCode(TCustomerCodeReqVO input) async {
    #     final response = await http.get(Uri.parse('/v1/api/login'));
    #    if (response.statusCode == 200) {
    #     return ReplyEntity<object>.fromJson(jsonDecode(response.body));
    #  } else {
    #    throw Exception('Failed to load customer code');
    # }
    # }
    @staticmethod
    def generate_dart_service_function(method_name, class_name, path, summary, operationId, parameters, res_class_name):
        # Util.generate_dart_request_parameter(parameters)
        request=Util.generate_dart_params(parameters)
        print('result:',request)
        dart_service_function = f'''
        /// {summary}
        Future<{res_class_name}> {operationId}({request}) async {{
            final response = await http.{method_name}(Uri.parse('{path}'));
            if (response.statusCode == 200) {{
                return {res_class_name}.fromJson(jsonDecode(response.body));
            }} else {{
                throw Exception('Failed to load {operationId}');
            }}
        }}
        '''
        print(dart_service_function)
        return dart_service_function

    # generate the dart variable by properties. eg: String? name; int? age; List<String>? hobbies;
    @staticmethod
    def generate_dart_variable(properties):
        dart_variable = ''
        for property_name, property_info in properties.items():
            type = property_info.get('type', '')
            format = property_info.get('format', '')
            if type == 'array':
                items = property_info.get('items', {})
                items_ref = items.get('$ref', '')
                if items_ref:
                    dart_variable += f'List<{items_ref.split("/")[-1]}>? {property_name};\n'
                else:
                    dart_variable += f'List<{format}>? {property_name};\n'
            else:
                dart_variable += f'{format}? {property_name};\n'
        return dart_variable

    # generate the dart class by class_name and properties eg: class Person { String? name; int? age; List<String>? hobbies; }
    @staticmethod
    def generate_dart_class(class_name, properties):
        dart_class = f'''
        class {class_name} {{

        '''
        dart_class += Util.generate_dart_variable(properties)
        dart_class += '}\n'
        return dart_class

    # generate request parameter by parameters.
    # "parameters": [
    # {
    # "in": "body",
    # "name": "body",
    # "description": "List of user object",
    # "required": true,
    # "schema": {
    # "type": "array",
    # "items": {
    # "$ref": "#/definitions/User"
    # }
    # }
    # }
    # ],
    @staticmethod
    def generate_dart_request_parameter(parameters):
        dart_request_parameter = ''
        for parameter in parameters:
            in_type = parameter.get('in', '')
            name = parameter.get('name', '')
            description = parameter.get('description', '')
            required = parameter.get('required', False)
            schema = parameter.get('schema', {})
            type = schema.get('type', '')
            items = schema.get('items', {})
            items_ref = items.get('$ref', '')
            if in_type == 'body':
                if type == 'array':
                    dart_request_parameter += f'List<{items_ref.split("/")[-1]}> {name};\n'
                else:
                    dart_request_parameter += f'{items_ref.split("/")[-1]} {name};\n'
        print(dart_request_parameter)
        return dart_request_parameter

    @staticmethod
    def parse_parameter(parameter: dict) -> str:
        """解析单个参数定义，返回 Dart 参数字符串"""
        param_type = ""
        param_name = parameter.get("name", "")
        is_required = parameter.get("required", False)

        # 处理 schema
        schema = parameter.get("schema", {})
        if schema:
            if schema.get("type") == "array":
                items = schema.get("items", {})
                if "$ref" in items:
                    # 从 $ref 中提取类名
                    class_name = items["$ref"].split("/")[-1]
                    param_type = f"List<{class_name}>"
                else:
                    param_type = f"List<{items.get('type', 'dynamic')}>"
            elif "$ref" in schema:
                param_type = schema["$ref"].split("/")[-1]
            else:
                param_type = schema.get("type", "dynamic")
        # "type": "array",
        # "items": {
        # "type": "string",
        # "enum": [
        # "available",
        # "pending",
        # "sold"
        # ],
        # "default": "available"
        # }
        elif parameter["type"] == "array":
            items = parameter.get("items", {})
            if items.get("type") == "string":
                param_type = "List<String>"
            elif items.get("type") == "integer":
                param_type = "List<int>"
            elif items.get("type") == "number":
                param_type = "List<double>"
            elif items.get("type") == "boolean":
                param_type = "List<bool>"
            else:
                param_type = "List<dynamic>"
        else:
            param_type = parameter.get("type", "dynamic")

        # 转换类型名称
        type_mapping = {
            "string": "String",
            "integer": "int",
            "number": "double",
            "boolean": "bool",
            "array": "List",
            "object": "Map<String, dynamic>"
        }
        param_type = type_mapping.get(param_type, param_type)

        # 构建参数字符串
        if is_required:
            return f"required {param_type} {param_name}"
        else:
            return f"{param_type}? {param_name}"

    @staticmethod
    def generate_dart_params(params: list) -> str:
        """生成 Dart 函数的参数列表"""
        param_strings = []

        # 处理每个参数
        for param in params:
            param_str = Util.parse_parameter(param)
            if param_str:
                param_strings.append(param_str)

        # 组合参数列表
        if param_strings:
            return "{" + ", ".join(param_strings) + "}"
        return "()"
