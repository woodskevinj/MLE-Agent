from agent.agent import Agent


agent = Agent()

result = agent.executor.execute_steps({
    "type": "tool",
    "name": "generate_scaffold",
    "kwargs": {
        "base_path": ".",
        "project_name": "demo_ml_project"
    }
})

print(result)
