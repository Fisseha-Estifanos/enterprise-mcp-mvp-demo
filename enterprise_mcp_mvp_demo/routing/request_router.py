"""
Description: This module contains the RequestRouter class that routes incoming requests
to the appropriate server based on the user's role and the category of the request.
"""

import os
import json
import sqlite3

from openai import OpenAI

from db.db_manager import DatabaseManager
from mcp_client.mcp_client import EnterpriseMCPClient


class RequestResponse:
    """
    Class to define the response message for incoming requests.
    """

    def __init__(self, status, message):
        """
        Initializes the RequestResponse class with the status and message.

        Args:
            status (str): The status of the response message.
            message (str): The message of the response.
        """
        self.status = status
        self.message = message

    def to_dict(self):
        """
        Converts the response message to a dictionary.

        Returns:
            dict: The response message dictionary.
        """
        return {
            "status": self.status,
            "message": self.message,
        }


class RequestRouter:
    """
    Class to route incoming requests to the appropriate server based on the user's role
    and the category of the request.
    """

    def __init__(
        self,
        config_file="configurations.json",
    ):
        """
        Initializes the RequestRouter class with the OpenAI API client and
        configuration.

        Args:
            config_file (str, optional): The file path to the configuration file.
            Defaults to "configurations.json".
        """
        self.llm_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.configuration = self.load_configuration(config_file)

    def load_configuration(self, config_file: str) -> dict:
        """
        Loads the configuration from a JSON file.

        Args:
            config_file (str): Path to the JSON configuration file.

        Returns:
            dict: Configuration dictionary.
        """
        try:
            with open(config_file, "r", encoding="utf-8") as file:
                config = json.load(file)
            return config
        except FileNotFoundError:
            print(f"Configuration file '{config_file}' not found.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON configuration: {e}")
            return {}

    def check_user_role(self, username: str, server_name: str) -> bool:
        """
        Checks if the user passes or fails based on role criteria in the database.

        Args:
            username (str): User's username.
            server_name (str): Name of the server.

        Returns:
            bool: True if the user passes the role criteria, False otherwise.
        """
        try:
            crud = DatabaseManager()

            user = crud.get_user_by_name(username)
            server = crud.get_server_by_name(server_name)
            print(f"User: {user.username}, Role: {user.role}")
            print(
                f"Server: {server.name}, Required Role: {server.required_role}")
            user_have_access = crud.can_access_server(user.id, server.id)
            print(f"User have access : {user_have_access}")
            return user_have_access
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def categorize_question(self, question: str) -> str:
        """
        Categorizes the question into one of three groups using the class's LLM.

        Args:
            question (str): The incoming request.

        Returns:
            str: The category of the incoming request.

        Raises:
            Exception: If an error occurs during the LLM completion.
        """
        try:
            prompt = self.configuration.get("categorize_question_prompt", None)
            if prompt is None:
                print("categorize question prompt could not be found.")
                return
            prompt = prompt.format(question=question)
            response = self.llm_client.chat.completions.create(
                model=self.configuration.get("llm_model", "gpt-3.5-turbo"),
                messages=[
                    {
                        "role": "assistant",
                        "content": "You are an assistant that groups incoming requests into categories. You will only return the category and nothing else.",  # noqa: E501
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
            category = response.choices[0].message.content.strip()
            print(f"Incoming request's category: {category}")
            return category
        except KeyError as e:
            print(f"Configuration key error: {e}")
            return "Unknown"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Unknown"

    async def route_request(self, username: str, question: str) -> dict:
        """
        Routes the request upstream based on user role check and question category.

        Args:
            username (str): User's username.
            question (str): The incoming request.

        Returns:
            RequestResponse: A dictionary containing the status and message of the
            request.
        """
        category = self.categorize_question(question)
        # TODO : check this logic here
        if category == "Unknown_":
            # TODO : Call default stuff
            return RequestResponse("error", "Failed to categorize question").to_dict()

        if not self.check_user_role(
            username,
            server_name=category.lower(),
        ):
            return RequestResponse(
                "success",
                f"User {username} does not meet criteria to access the {category} server.",  # noqa: E501
            ).to_dict()

        # Get the answer based on the category of the request
        if "weather" in category.lower():
            rb_mcp_client = EnterpriseMCPClient()
            await rb_mcp_client.connect_to_server(
                self.configuration.get("weather_server_path", None),
                "",
            )
            response = await rb_mcp_client.process_query(question)
            return RequestResponse("success", response).to_dict()
        elif "filesystem" in category.lower():
            rb_mcp_client = EnterpriseMCPClient()
            await rb_mcp_client.connect_to_server(
                self.configuration.get("filesystem_server_path", None),
                self.configuration.get("allowed_directories", "."),
            )
            response = await rb_mcp_client.process_query(question)
            return RequestResponse("success", response).to_dict()
        else:
            response = "A server that corresponds to your question can not be found."
            return RequestResponse("success", response).to_dict()
