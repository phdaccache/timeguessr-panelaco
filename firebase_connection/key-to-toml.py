import toml

output_file = ".streamlit/secrets.toml"

with open("firebase_connection/firebase-api-key.json") as json_file:
    json_text1 = json_file.read()

config1 = {"text-api-key": json_text1}
toml_config1 = toml.dumps(config1)

with open("firebase_connection/credentials.json") as json_file:
    json_text2 = json_file.read()

config2 = {"text-credentials": json_text2}
toml_config2 = toml.dumps(config2)

with open(output_file, "w") as target:
    target.write(toml_config1)
    target.write(toml_config2)