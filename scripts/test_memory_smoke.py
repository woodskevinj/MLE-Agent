from agent.memory.module import MemoryModule

mm = MemoryModule("agent_memory.db")
mm.remember("User Kevin prefers step-by-step, code-heavy answers.", kind="semantic",
            tags=["user_pref","pinned"], importance=0.9, summary="User preference")
mm.remember("Docker push failed with large layers; fixed with multi-stage.", kind="episodic",
            tags=["docker","ecr","lesson"], importance=0.7)
print("Recall 'docker?':")
for m in mm.recall("What about docker?", k=5):
    print("-", m.text)

print("\nContext for 'Fix ECR push':")
print(mm.context("Fix ECR push"))