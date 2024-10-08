# Fitmentiq Crew

Welcome to the Fitmentiq Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```
### Customizing
I am using groq through openai ,if you want you can use openai 

Make sure you place your `credentials.json` file which you got from your google Auth in root folder.

**Add your `OPENAI_API_KEY`  `GOOGLE_API_KEY`  `OPENAI_API_BASE` into the `.env` file**


- Modify `src/fitmentiq/config/agents.yaml` to define your agents
- Modify `src/fitmentiq/config/tasks.yaml` to define your tasks
- Modify `src/fitmentiq/crew.py` to add your own logic, tools and specific args
- Modify `src/fitmentiq/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run fitmentiq
```
To watch the Agent outputs on Terminal you can run:

```bash
streamlit run src/fitmentiq/app.py
```
This command initializes the FitmentIQ Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The FitmentIQ Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Fitmentiq Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
