#!/usr/bin/python3
import logging
import os
import sys
from dataclasses import dataclass
import requests
import json
import click

AVAILABLE_MODELS = [
    "sonar-reasoning-pro",
    "sonar-reasoning",
    "sonar-pro",
    "sonar"
]

logger = logging.getLogger(__name__)


class ApiKeyNotFoundException(Exception):
    pass


class InvalidSelectedModelException(Exception):
    pass


def display(
    message: str,
    color: str = "white",
    bold: bool = False,
    bg_color: str = "black",
):
    colors = {
        "red": "91m",
        "green": "92m",
        "yellow": "93m",
        "blue": "94m",
        "white": "97m",
    }
    bg_colors = {
        "black": "40",
        "red": "41",
        "green": "42",
        "yellow": "43",
        "blue": "44",
        "white": "47",
    }
    if bold:
        print(f"\033[1;{bg_colors[bg_color]};{colors[color]} {message}\033[0m")
    else:
        print(f"\033[{bg_colors[bg_color]};{colors[color]} {message}\033[0m")


@dataclass(frozen=True)
class ApiConfig:
    api_url: str = "https://api.perplexity.ai/chat/completions"
    api_key: str | None = None
    usage: bool = False
    citations: bool = False
    model: str | None = None


class ModelValidator:
    @staticmethod
    def validate(model: str) -> bool:
        return model in AVAILABLE_MODELS

    @staticmethod
    def get_AVAILABLE_MODELS() -> list[str]:
        return AVAILABLE_MODELS


class ApiKeyValidator:
    @staticmethod
    def get_api_key_from_system() -> str | None:
        return os.environ.get("PERPLEXITY_API_KEY")


class Perplexity:
    def __init__(self, args) -> None:
        self.setup = ApiConfig
        if not ModelValidator.validate(args["model"]):
            raise InvalidSelectedModelException(
                f"Invalid model: {args['model']}\n"
                f"Available models: {ModelValidator.get_AVAILABLE_MODELS()}"
            )
        self.setup.model = args["model"]
        self.setup.usage = args["usage"]
        self.setup.citations = args["citations"]
        self.use_glow = args["glow"]
        if not args["api_key"]:
            api_key = ApiKeyValidator.get_api_key_from_system()
            if api_key is None:
                display("Api key not found on system! ", "red")
                logger.debug("Api key not found on system!")
                raise ApiKeyNotFoundException
            else:
                logger.debug(f"Api key found on system: {api_key}")
                self.setup.api_key = api_key
        else:
            self.setup.api_key = args["api_key"]

    def get_response(self, message) -> None:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.setup.api_key}",
        }
        logger.debug(f"Headers: {headers}")
        query_data = {
            "model": self.setup.model,
            "messages": [
                {"role": "system", "content": "Be precise and concise."},
                {"role": "user", "content": message},
            ],
        }
        logger.debug(f"Query data: {query_data}")

        response = requests.post(
            self.setup.api_url, headers=headers, data=json.dumps(query_data)
        )

        if response.status_code == 200:
            result = response.json()
            if self.setup.citations:
                self._show_citations(result["citations"], self.use_glow)
            if self.setup.usage:
                self._show_usage(result["usage"], self.use_glow)
            self._show_content(result["choices"][0]["message"]["content"])
        elif response.status_code == 401:
            display("Invalid api key! ", "red")
        else:
            logger.error(f"Error: {response.status_code}")

    @staticmethod
    def _show_usage(result: dict, use_glow: bool) -> None:
        if use_glow:
            print("# Tokens")
        else:
            display("Tokens \n", "yellow", True, "blue")
        for token in result:
            print(f"- {token}: {result[token]}")
        print("\n")

    @staticmethod
    def _show_citations(result: list, use_glow: bool) -> None:
        if use_glow:
            print("# Citations")
        else:
            display("Citations \n", "yellow", True, "blue")
        for element in result:
            print(f"- {element}")
        print("\n")

    def _show_content(self, result: str) -> None:
        if self.use_glow:
            print("# Content")
        else:
            display("Content \n", "yellow", True, "blue")
        print(result)


@click.command()
@click.argument("query")
@click.option("-v", "--verbose", is_flag=True, help="Debug mode")
@click.option("-u", "--usage", is_flag=True, help="Show usage")
@click.option("-c", "--citations", is_flag=True, help="Show citations")
@click.option("-g", "--glow", is_flag=True, help="Show citations")
@click.option(
    "-a", "--api-key", type=str, required=False, help="Description for api_key argument"
)
@click.option(
    "-m",
    "--model",
    type=str,
    default="sonar-pro",
    help="Description for model argument (default: sonar-pro) "
         f"Available models: {AVAILABLE_MODELS}",
    show_default=True,
)
def main(query, verbose, usage, citations, glow, api_key, model):
    # Set up logging
    log_level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.debug("Inside main click command")
    args_dict = {
        "usage": usage,
        "citations": citations,
        "glow": glow,
        "api_key": api_key,
        "model": model,
    }
    try:
        perplexity = Perplexity(args_dict)
        perplexity.get_response(query)
    except Exception as e:
        logger.debug(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
