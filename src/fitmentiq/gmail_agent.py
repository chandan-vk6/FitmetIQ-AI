import os
from langchain_google_community import GmailToolkit
from langchain import hub
import streamlit as st
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials
from dotenv import load_dotenv
import groq
from langchain_core.prompts import ChatPromptTemplate
import openai
from langgraph.prebuilt import create_react_agent
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()
load_dotenv(".env")

class GmailAgent:
    def __init__(self, token_file="token.json", client_secrets_file="credentials.json", scopes=["https://mail.google.com/"], model_name="llama3-8b-8192", api_base="https://api.groq.com/openai/v1", api_key=os.getenv("OPENAI_API_KEY")):
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
        self.tools = self._get_tools()
        self.llm = ChatOpenAI(model=self.model_name, temperature=0)
        # self.agent = self._create_agent()
        self.agent_executor = create_react_agent(self.llm, self.tools)

    def _get_tools(self):
        tools = self.toolkit.get_tools()
        draft_tool = None
        for tool in tools:
            if "draft" in tool.name.lower():
                draft_tool = tool
                break

        if draft_tool is None:
            raise ValueError("Drafting tool not found in the toolkit.")

        return [draft_tool]
    
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

    # def _create_agent(self):
    #     instructions = """You are an assistant."""
    #     base_prompt = hub.pull("langchain-ai/openai-functions-template")
    #     prompt = base_prompt.partial(instructions=instructions)
    #     return create_openai_functions_agent(self.llm, self.tools, prompt)

    # def _create_agent_executor(self):
    #     return AgentExecutor(
    #         agent=self.agent,
    #         tools=self.tools,
    #         verbose=True,
    #         handle_parsing_errors=True
    #     )

    def create_draft(self, input_text):
        try:
            
            prompt = ChatPromptTemplate.from_messages([
                # ("system", """You are Expert Prompt Generator for Drafting Email to schedule screening Interview by analysing the given content like Human decison on candidate, position mad more, provide the complete Draft as well and keep it short.
                 
                # Follow the example.

                # Example: Draft an email to fake@fake.com thanking them for coffee."""),
                # ("user", "{input}")
                ("system", """You are an Expert Email Drafting Assistant specialized in scheduling screening interviews. Your role is to carefully analyze the given content, including candidate evaluations, position details, and any other relevant information, before drafting a concise and accurate email.

    Make sure to directly reference the provided content and avoid making assumptions not supported by the data.

    Example:
    Input: "Candidate John Doe has been shortlisted for the Software Engineer role. Please draft an email to john.doe@example.com to schedule a screening interview."

    Output: "Subject: Scheduling Your Screening Interview for Software Engineer Role

    Dear John Doe,

    We are pleased to inform you that you have been shortlisted for the Software Engineer position at [Company Name]. We would like to schedule a screening interview with you to discuss your qualifications further. Please let us know your availability for a 30-minute interview in the upcoming week.

    Thank you, and we look forward to speaking with you.

    Best regards,
    [Your Name]
    [Your Job Title]"""),
    ("user", "{input}")
            ])
            # chain = prompt | self.llm 
            chain = prompt | self.llm | output_parser
            prompt = chain.invoke({"input": input_text})
            print("prompt:", prompt)
            result = self.agent_executor.stream({"messages": [("user", prompt)]}, stream_mode="values")
            # print(result)
            found_first = False
            with st.chat_message("AI"):
                st.write(f"Agent Name: Email_craft")
                for event in result:
                    st.write(event["messages"][-1].content) 
                    
                # st.write("Email Drafted Succesfully, You can check in your Mail!")
            # return result
        except groq.BadRequestError as e:
            print("Ignore:An error occurred during the function call:")

        except openai.BadRequestError as e:
            print("Ignore:An error occurred during the function call:")
            print(e)

# if __name__ == "__main__":    
#     agent = GmailAgent(
#         token_file="token.json",
#         client_secrets_file="credentials.json",
#         scopes=["https://mail.google.com/"],
#         model_name="llama-3.1-8b-instant",
#         api_base="https://api.groq.com/openai/v1",
#         api_key="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"
#     )
#     input_text = ("Create a gmail draft for me to edit of a letter from the perspective of a sentient parrot"
#                   " who is looking to collaborate on some research with her estranged friend, a cat."
#                   " Under no circumstances may you send the message, however.")
#     agent.create_draft(input_text)
