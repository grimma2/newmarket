from django.urls import URLPattern


class ParseUrlPatterns:

    def __init__(self, project_urls):
        self.global_conf = __import__(project_urls, {}, {}, [''])
        self.parse_url_patterns()

    @staticmethod
    def _get_app_patterns(local_conf):
        app_patterns = {}

        for route_pattern in local_conf.url_patterns:
            if isinstance(route_pattern, URLPattern):
                app_patterns[route_pattern.name] = f'{local_conf.pattern}{route_pattern.pattern}'

        return app_patterns

    def parse_url_patterns(self):
        parsed_patterns = {}
        for local_conf in self.global_conf.urlpatterns:
            parsed_patterns[local_conf.namespace] = self._get_app_patterns(local_conf)

        return parsed_patterns
