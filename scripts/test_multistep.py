from agent.agent import Agent

agent = Agent()

commands = [
    "Read file demo.txt and then run python: print(2+2) and then write this to file result.txt: done",
    "Create a new project called agent_test in . and then write this to file agent_test/README.md: This project was auto-generated",
    "Run python: import pandas as pd; print(pd.DataFrame({'a':[1,2]})) and then explain this"
]

for c in commands:
    print("\n--------------------------------------")
    print("USER:", c)

    # Print plan
    plan = agent.planner.create_plan(c)

    #Execute the plan
    result = agent.executor.execute_steps(plan)
    print("RESULT:", result)
