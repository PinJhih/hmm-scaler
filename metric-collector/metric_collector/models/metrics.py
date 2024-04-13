from prometheus_api_client import PrometheusConnect


class Metrics:
    def __init__(self, targets) -> None:
        self.set_targets(targets)
        self.__queries = [
            'sum(irate(container_cpu_usage_seconds_total{%s, container!=""}[1m])) by (pod)',
        ]

        prom_url = "http://10.106.152.99:9090/"
        self.__prom = PrometheusConnect(url=prom_url)

    def set_targets(self, targets) -> None:
        self.__targets = targets

    def get_all(self) -> dict:
        metrics = self.__query_prom()
        return metrics

    def __query_prom(self):
        res = {}
        for ns in self.__targets.keys():
            res[ns] = []
            metrics = []
            for query in self.__queries:
                q = Metrics.__fill_parameters(query, ns)
                data = self.__prom.custom_query(query=q)
                metrics.extend(data)
            res[ns].append(metrics)
        return res

    def __fill_parameters(query, ns):
        return query % f'namespace="{ns}"'
