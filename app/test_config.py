import os

from .config import EnvironmentConfigProvider, Config


def test_env_config_provider():
    os.environ["RESUME_URL"] = "https://example.com/resume.pdf"
    config_provider = EnvironmentConfigProvider()
    config = config_provider.get_config()
    assert config == Config(resume_url="https://example.com/resume.pdf")


def test_validate_config():
    config = Config(resume_url="https://example.com/resume.pdf")
    assert not config.validate()

    config = Config(resume_url="")
    assert "resume_url" in config.validate()
