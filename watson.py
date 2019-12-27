import yaml

creds = {}
with open( "creds.yaml" , "r" )  as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
