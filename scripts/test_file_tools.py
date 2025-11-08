from agent.agent import Agent


agent = Agent()

# Test write
result = agent.executor.execute_steps({
    "type": "tool",
    "name": "write_file",
    "kwargs": { "path": "test-output.txt", "content": "Hello from MLE-Agent!" }
})
print(result)

# Test read
result = agent.executor.execute_steps({
    "type": "tool",
    "name": "read_file",
    "kwargs": { "path": "test-output.txt" }
})
print(result)