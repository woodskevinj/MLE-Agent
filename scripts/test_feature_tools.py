from agent.agent import Agent


if __name__ == "__main__":
    agent = Agent()

    print("\n--- Load CSV ---")
    print(agent.run("load csv file data/telco/WA_Fn-UseC_-Telco-Customer-Churn.csv"))

    print("\n--- Encode Categoricals ---")
    print(agent.run("encode categoricals"))

    print("\n--- Scale Numerical ---")
    print(agent.run("scale numerical"))

    print("\n--- Split Data ---")
    print(agent.run("split data"))

    print("\n--- Save DataFrame")
    print(agent.run("save dataframe to data/telco/transformed_telco.csv"))