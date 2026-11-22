
from strands.hooks import BeforeToolCallEvent, HookProvider, HookRegistry

class DeleteApprovalHook(HookProvider):
    """Only interrupt delete operations"""
    
    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolCallEvent, self.check_delete)


    def check_delete(self, event: BeforeToolCallEvent)-> None:
        if(event.tool_use['name']!="delete_file"):
            return

        approval = event.interrupt(
            "delete-approval",
            reason={"file_name": event.tool_use["input"]["file_name"]}
        )

        if approval.lower() != "y":
            event.cancel_tool = "User Cancelled the deletion operations"
    
