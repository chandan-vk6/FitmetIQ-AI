import os
from langchain_google_community import GmailToolkit
from langchain import hub
import streamlit as st
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials
from dotenv import load_dotenv
load_dotenv()

class GmailAgent:
    def __init__(self, token_file="token.json", client_secrets_file="credentials.json", scopes=["https://mail.google.com/"], model_name="llama3-groq-70b-8192-tool-use-preview", api_base="https://api.groq.com/openai/v1", api_key=os.getenv("OPENAI_API_KEY")):
        self.token_file = token_file
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.model_name = model_name
        self.api_base = api_base
        self.api_key = api_key
        self._setup_environment()
        self.credentials = self._get_gmail_credentials()
        self.api_resource = self._build_resource_service()
        self.toolkit = GmailToolkit(api_resource=self.api_resource)
        self.tools = self.toolkit.get_tools()
        self.llm = ChatOpenAI(model=self.model_name, temperature=0)
        self.agent = self._create_agent()
        self.agent_executor = self._create_agent_executor()

    def _setup_environment(self):
        os.environ['OPENAI_API_BASE'] = self.api_base
        os.environ['OPENAI_MODEL_NAME'] = self.model_name
        os.environ['OPENAI_API_KEY'] = self.api_key

    def _get_gmail_credentials(self):
        return get_gmail_credentials(
            token_file=self.token_file,
            scopes=self.scopes,
            client_secrets_file=self.client_secrets_file,
        )

    def _build_resource_service(self):
        return build_resource_service(credentials=self.credentials)

    def _create_agent(self):
        instructions = """You are an assistant."""
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        prompt = base_prompt.partial(instructions=instructions)
        return create_openai_functions_agent(self.llm, self.tools, prompt)

    def _create_agent_executor(self):
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
        )

    def create_draft(self, input_text):
        result = self.agent_executor.invoke({"input": input_text})
        with st.chat_message("AI"):
            st.write(f"Agent Name: Email_craft")
            st.write(result.get("output"))
        # return result

# if __name__ == "__main__":
#     agent = GmailAgent(
#         token_file="token.json",
#         client_secrets_file="credentials.json",
#         scopes=["https://mail.google.com/"],
#         model_name="llama3-groq-70b-8192-tool-use-preview",
#         api_base="https://api.groq.com/openai/v1",
#         api_key="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"
#     )
#     input_text = ("Create a gmail draft for me to edit of a letter from the perspective of a sentient parrot"
#                   " who is looking to collaborate on some research with her estranged friend, a cat."
#                   " Under no circumstances may you send the message, however.")
#     agent.create_draft(input_text)
