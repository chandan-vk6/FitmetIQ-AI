from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool
from typing import Union, List, Tuple, Dict
from langchain_core.agents import AgentFinish
import streamlit as st
from datetime import datetime
import json
import os
# Uncomment the following line to use an example of a custom tool
# from fitmentiq.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool
os.environ['GOOGLE_API_KEY']="AIzaSyBz34fG4xflXfY1iFnTr0fsLykgJ-5bnYo"
os.environ['OPENAI_API_BASE'] = "https://api.groq.com/openai/v1"
os.environ['OPENAI_MODEL_NAME'] = "llama3-groq-70b-8192-tool-use-preview"
os.environ['OPENAI_API_KEY'] = "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"


@CrewBase
class FitmentiqCrew():
	"""Fitmentiq crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	pdf_tool = PDFSearchTool(
    config=dict(
        llm=dict(
            provider="openai",
            config=dict(
                model=os.getenv("OPENAI_MODEL_NAME"),
            ),
        ),
        embedder=dict(
            provider="google",
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
				# api_key='AIzaSyBz34fG4xflXfY1iFnTr0fsLykgJ-5bnYo'
            ),
        ),
    )
)
	
	def step_callback(
        self,
        agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish],
        agent_name,
        *args,):

		
		# Try to parse the output if it is a JSON string
		if isinstance(agent_output, str):
			with st.chat_message("AI"):
				try:
					agent_output = json.loads(agent_output)
				except json.JSONDecodeError:
					pass

		# if isinstance(agent_output, list) and all(
		# 	isinstance(item, tuple) for item in agent_output
		# ):

		# 	for action, description in agent_output:
		# 		# Print attributes based on assumed structure
		# 		st.write(f"Agent Name: {agent_name}")
		# 		st.write(f"Tool used: {getattr(action, 'tool', 'Unknown')}")
		# 		st.write(f"Tool input: {getattr(action, 'tool_input', 'Unknown')}")
		# 		st.write(f"{getattr(action, 'log', 'Unknown')}")
		# 		with st.expander("Show observation"):
		# 			st.markdown(f"Observation\n\n{description}")

		# Check if the output is a dictionary as in the second case
		elif isinstance(agent_output, AgentFinish):
			with st.chat_message("AI"):
				st.write(f"Agent Name: {agent_name}")
				output = agent_output.return_values
				st.markdown(f"{output['output']}")

		# Handle unexpected formats
		# else:
		# 	st.write(type(agent_output))
		# 	st.write(agent_output)

	@agent
	def job_description_parser(self) -> Agent:
		return Agent(
			config=self.agents_config['job_description_parser'],
			tools=[self.pdf_tool], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			memory=False,
			allow_delegation=True,
			step_callback=lambda step: self.step_callback(step, "Job_description_parser"),
		)

	@agent
	def resume_parser(self) -> Agent:
		return Agent(
			config=self.agents_config['resume_parser'],
			tools=[self.pdf_tool], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			memory=False,
			allow_delegation=True,
			step_callback=lambda step: self.step_callback(step, "Resume_parser"),
		)
	
	@agent
	def summarizer(self) -> Agent:
		return Agent(
			config=self.agents_config['summarizer'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			memory=False,
			allow_delegation=False,
			step_callback=lambda step: self.step_callback(step, "Summarizer"),
		)
	
	@agent
	def fitment_analysis(self) -> Agent:
		return Agent(
			config=self.agents_config['fitment_analysis'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			memory=False,
			allow_delegation=False,
			step_callback=lambda step: self.step_callback(step, "Fitment_analysis"),
		)
	
	@agent
	def human_interaction(self) -> Agent:
		return Agent(
			config=self.agents_config['human_interaction'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			memory=False,
			allow_delegation=False,
			step_callback=lambda step: self.step_callback(step, "Human_interaction"),
		)
	

	@agent
	def email_crafting(self) -> Agent:
		return Agent(
			config=self.agents_config['email_crafting'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			memory=False,
			allow_delegation=False,
			step_callback=lambda step: self.step_callback(step, "Email_crafting"),
		)

	@task
	def parse_job_description_task(self) -> Task:
		return Task(
			config=self.tasks_config['parse_job_description_task'],
			agent=self.job_description_parser(),
			output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_parse_job_description_task.md",
		)

	@task
	def parse_resume_task(self) -> Task:
		return Task(
			config=self.tasks_config['parse_resume_task'],
			agent=self.resume_parser(),
			output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_parse_resume_task.md",
		)
	
	@task
	def summarize_information_task(self) -> Task:
		return Task(
			config=self.tasks_config['summarize_information_task'],
			agent=self.summarizer(),
			context=[self.parse_resume_task()],
			output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_summarize_information_task.md",
		)
	

	@task
	def perform_fitment_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['perform_fitment_analysis_task'],
			agent=self.fitment_analysis(),
			context=[self.parse_job_description_task(), self.summarize_information_task()],
			output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_perform_fitment_analysis_task.md",
		)
	
	@task
	def prompt_human_input_task(self) -> Task:
		return Task(
			config=self.tasks_config['prompt_human_input_task'],
			agent=self.human_interaction(),
			human_input=True,
			output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_prompt_human_input_task.md",
		)
	
	@task
	def craft_email_task(self) -> Task:
		return Task(
			config=self.tasks_config['craft_email_task'],
			agent=self.email_crafting(),
			context=[self.parse_job_description_task(), self.prompt_human_input_task()],
			output_file=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_craft_email_task.md",

		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Fitmentiq crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)