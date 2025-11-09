from agent.agent import Agent

agent = Agent()

tests = [
    "Read file test-output.txt",
    "Write this to file demo.txt: Hello from the planner!",
    "Run python: print(3*7)",
    "Create a new project called churn_model in .",
    "What is cross validation?"
]

for t in tests:
    print("\nUSER:", t)
    print("AGENT:", agent.run(t))
    