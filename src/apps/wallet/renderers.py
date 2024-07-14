from rest_framework_json_api.renderers import JSONRenderer as JSONAPIRenderer
from rest_framework_json_api.parsers import JSONParser as JSONAPIParser


class CustomJSONAPIRenderer(JSONAPIRenderer):
    media_type = 'application/vnd.api+json'


class CustomJSONAPIParser(JSONAPIParser):
    media_type = 'application/vnd.api+json'
