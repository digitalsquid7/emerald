import os


class EnvironmentVariableRetriever:
    @staticmethod
    def retrieve(name: str):
        env_var = os.getenv(name)

        if env_var is None:
            raise Exception(f"required environment variable not set: {name}")

        return env_var
