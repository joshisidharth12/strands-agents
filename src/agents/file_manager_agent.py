
from strands import Agent
from config.llm_model import groq_model
from harness.delete_interrupt_hook import DeleteApprovalHook
from tools.file_manager_tools import list_dir, create_file
from tools.file_manager_tools.operations import delete_file

def file_manager_agent():
    agent = Agent(
        model=groq_model,
        system_prompt="You are file manager to lists and creates file on behalf of the user when prompted to.",
        tools=[list_dir, create_file, delete_file],
        hooks=[DeleteApprovalHook()]
    )
    # agent("Create a new file at 'new-1.txt' content: 'this is a new file'");
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        print()
        result = agent(user_input)

        while result.stop_reason == "interrupt":
            for interrupt in result.interrupts:
                approval = input(f"\n⚠️  Delete '{interrupt.reason['file_name']}'? (y/N): ")
                result = agent([
                    {
                        "interruptResponse": {
                            "interruptId": interrupt.id,
                            "response": approval,
                        }
                    }
                ])

if __name__ == "__main__":
    file_manager_agent()


