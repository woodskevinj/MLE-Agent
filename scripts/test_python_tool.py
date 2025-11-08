from agent.agent import Agent
import pandas as pd


agent = Agent()

code_snippet = """
x = 10
y = 32
print(x + y)
"""

df = pd.DataFrame({"a":[1,2,3],"b":[4,5,6]})

result = agent.executor.execute_steps({
    "type": "tool",
    "name": "run_python",
    "kwargs": { "code": code_snippet }
})

print("Tool Output")
print(result)

print("#####")
print("More Descriptive Stats")
print(df.describe)