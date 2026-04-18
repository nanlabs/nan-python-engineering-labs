"""
Human-in-the-loop workflows.
"""

class HumanApprovalWorkflow:
    """Workflow requiring human approval."""
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.status = "pending_approval"
        self.approved_by = None
    
    def request_approval(self) -> dict:
        return {
            "task_id": self.task_id,
            "action": "waiting_for_approval",
        }
    
    def approve(self, reviewer: str):
        self.status = "approved"
        self.approved_by = reviewer

if __name__ == "__main__":
    workflow = HumanApprovalWorkflow("task_123")
    print(f"Approval request: {workflow.request_approval()}")
    workflow.approve("reviewer_1")
    print(f"Status: {workflow.status}")
