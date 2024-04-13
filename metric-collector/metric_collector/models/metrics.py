from prometheus_api_client import PrometheusConnect


class Metrics:
    def __init__(self, targets) -> None:
        self.set_targets(targets)
        self.__queries = [
            [
                "sum(irate(container_cpu_usage_seconds_total{%s}[1m])) by (pod)",
                "cpu",
            ],
        ]

        prom_url = "http://10.106.152.99:9090/"
        self.__prom = PrometheusConnect(url=prom_url)

    def set_targets(self, targets) -> None:
        self.__targets = targets

    def get_all(self) -> dict:
        metrics = dict()
        for ns in self.__targets.keys():
            metrics[ns] = self.__query_prom(ns)
        return metrics

    def __query_prom(self, ns) -> dict:
        metrics = dict()
        for q, name in self.__queries:
            deploys = self.__targets[ns]
            pod_label = Metrics.__to_pod_label(deploys)

            query = q % f'namespace="{ns}", pod=~"{pod_label}"'
            res = self.__prom.custom_query(query)
            values = Metrics.__get_values(res, deploys)

            for deploy in values.keys():
                if deploy not in metrics.keys():
                    metrics[deploy] = dict()
                metrics[deploy][name] = values[deploy]
        return metrics

    def __get_values(data, deploys):
        values = dict()
        for item in data:
            pod = item["metric"]["pod"]
            deploy = Metrics.__find_deploy(pod, deploys)
            value = float(item["value"][1])
            values[deploy] = value
        return values

    def __find_deploy(pod, deploys):
        for deploy in deploys:
            if pod.startswith(deploy):
                return deploy
        return ""

    def __to_pod_label(deploys):
        pods = [f"{deploy}-.*" for deploy in deploys]
        return "|".join(pods)
