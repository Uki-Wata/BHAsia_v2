from create_diagram_code import generate_aws_service_description

input_text = "Simple Web Application"

# 関数の呼び出しと返り値の分割
description, json_result = generate_aws_service_description(input_text)

print("AWS Service Description:")
print(description)
print("\nJSON Result:")
print(json_result)
