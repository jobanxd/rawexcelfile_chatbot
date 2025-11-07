from google.adk.agents import Agent, LlmAgent
from google.adk.planners import PlanReActPlanner
from google.adk.tools import AgentTool
from .agents.agentprofiles import AgentProfile

query_agent_profile = AgentProfile(agent_name="query_agent")
query_agent = LlmAgent(
    name=query_agent_profile.name,
    model=query_agent_profile.model_id,
    description=query_agent_profile.description,
    instruction=query_agent_profile.instruction,
)

root_agent_profile = AgentProfile(agent_name="root_agent")
root_agent = Agent(
    name=root_agent_profile.name,
    model=root_agent_profile.model_id,
    description=root_agent_profile.description,
    instruction=root_agent_profile.instruction,
    planner=PlanReActPlanner(),
    tools=[
        AgentTool(agent=query_agent),
    ],
)