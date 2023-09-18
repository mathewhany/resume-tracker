from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse

from .config import ConfigProvider, EnvironmentConfigProvider, Config
from .metrics import MetricsManager, JSONMetricsManager


def get_metrics_manager():
    try:
        file = open("metrics.json", "r+")
        yield JSONMetricsManager(file)
    finally:
        file.close()


def get_config_provider():
    return EnvironmentConfigProvider()


def get_config(config_provider: ConfigProvider = Depends(get_config_provider)):
    return config_provider.get_config()


app = FastAPI()


@app.get("/resume")
async def root(
    metrics_manager: Annotated[MetricsManager, Depends(get_metrics_manager)],
    config: Annotated[Config, Depends(get_config)],
    source: str = "",
):
    metrics_manager.record_visit("resume", source)
    return RedirectResponse(url=config.resume_url)


@app.get("/metrics")
async def metrics(
    metrics_manager: Annotated[MetricsManager, Depends(get_metrics_manager)],
):
    return metrics_manager.get_all_counts()
