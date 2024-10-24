# def parse_parameter(parameter: dict) -> str:
#     """解析单个参数定义，返回 Dart 参数字符串"""
#     param_type = ""
#     param_name = parameter.get("name", "")
#     is_required = parameter.get("required", False)

#     # 处理 schema
#     schema = parameter.get("schema", {})
#     if schema:
#         if schema.get("type") == "array":
#             items = schema.get("items", {})
#             if "$ref" in items:
#                 # 从 $ref 中提取类名
#                 class_name = items["$ref"].split("/")[-1]
#                 param_type = f"List<{class_name}>"
#             else:
#                 param_type = f"List<{items.get('type', 'dynamic')}>"
#         elif "$ref" in schema:
#             param_type = schema["$ref"].split("/")[-1]
#         else:
#             param_type = schema.get("type", "dynamic")
#     else:
#         param_type = parameter.get("type", "dynamic")

#     # 转换类型名称
#     type_mapping = {
#         "string": "String",
#         "integer": "int",
#         "number": "double",
#         "boolean": "bool",
#         "array": "List",
#         "object": "Map<String, dynamic>"
#     }
#     param_type = type_mapping.get(param_type, param_type)

#     # 构建参数字符串
#     if is_required:
#         return f"required {param_type} {param_name}"
#     else:
#         return f"{param_type}? {param_name}"

# def generate_dart_params(params: list) -> str:
#     """生成 Dart 函数的参数列表"""
#     param_strings = []

#     # 处理每个参数
#     for param in params:
#         param_str = parse_parameter(param)
#         if param_str:
#             param_strings.append(param_str)

#     # 组合参数列表
#     if param_strings:
#         return "{" + ", ".join(param_strings) + "}"
#     return "()"

# 使用示例
# if __name__ == "__main__":
#     # 示例参数定义（已经是 Python 对象）
#     test_params = [{
#         "in": "body",
#         "name": "body",
#         "description": "List of user object",
#         "required": True,
#         "schema": {
#             "type": "array",
#             "items": {
#                 "$ref": "#/definitions/User"
#             }
#         }
#     }]

#     # 生成参数
#     result = generate_dart_params(test_params)
#     print(f"Generated Dart parameters: {result}")

#     # 更多测试用例
#     more_test_params = [
#         {
#             "in": "query",
#             "name": "userId",
#             "type": "integer",
#             "required": True
#         },
#         {
#             "in": "body",
#             "name": "user",
#             "schema": {
#                 "$ref": "#/definitions/User"
#             },
#             "required": False
#         }
#     ]

#     print("\nMore test cases:")
#     print(f"Generated Dart parameters: {generate_dart_params(more_test_params)}")
