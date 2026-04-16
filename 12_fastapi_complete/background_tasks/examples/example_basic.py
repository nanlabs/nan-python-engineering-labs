"""
Basic example: Background Tasks
==================================

FastAPI's BackgroundTasks allows you to run slow operations (sending emails,
writing logs, calling external APIs) AFTER returning the HTTP response,
without making the client wait.

This example demonstrates:
1. Adding a single background task to a route
2. Adding multiple background tasks
3. Background tasks with dependencies
4. Tracking task status via an in-memory log
5. Differentiating from async endpoints (background ≠ concurrent)

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs
"""

import time
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel, EmailStr


# =============================================================================
# MODELS
# =============================================================================


class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str


class OrderRequest(BaseModel):
    customer_email: str
    items: List[str]
    total: float


class TaskLog(BaseModel):
    task_id: str
    task_type: str
    status: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    result: Optional[str] = None


# =============================================================================
# IN-MEMORY TASK TRACKER
# =============================================================================

task_registry: dict[str, TaskLog] = {}


def register_task(task_type: str) -> str:
    task_id = str(uuid.uuid4())[:8]
    task_registry[task_id] = TaskLog(
        task_id=task_id,
        task_type=task_type,
        status="pending",
        started_at=datetime.now(),
    )
    return task_id


def complete_task(task_id: str, result: str):
    if task_id in task_registry:
        task_registry[task_id].status = "completed"
        task_registry[task_id].finished_at = datetime.now()
        task_registry[task_id].result = result


def fail_task(task_id: str, error: str):
    if task_id in task_registry:
        task_registry[task_id].status = "failed"
        task_registry[task_id].finished_at = datetime.now()
        task_registry[task_id].result = f"ERROR: {error}"


# =============================================================================
# BACKGROUND FUNCTIONS (run after response is sent)
# =============================================================================


def send_email(to: str, subject: str, body: str, task_id: str):
    """
    Simulate sending an email.

    In production this would call an SMTP server or email API.
    The client does NOT wait for this — it runs after the response.
    """
    time.sleep(2)  # Simulate slow network call
    print(f"[BG] Email sent to {to} | subject: {subject}")
    complete_task(task_id, f"Email delivered to {to}")


def process_order(order: OrderRequest, task_id: str):
    """
    Simulate order processing: inventory check + receipt generation.

    Both steps run sequentially in the background.
    """
    time.sleep(1)
    print(f"[BG] Checking inventory for {len(order.items)} items...")
    time.sleep(1)
    print(f"[BG] Generating receipt for {order.customer_email}")
    complete_task(task_id, f"Order processed: {len(order.items)} items, total ${order.total}")


def write_audit_log(action: str, user: str, resource: str, task_id: str):
    """Write an audit log entry asynchronously."""
    time.sleep(0.1)
    entry = f"{datetime.now().isoformat()} | {user} | {action} | {resource}"
    print(f"[BG] Audit log: {entry}")
    complete_task(task_id, entry)


def send_welcome_email_sequence(email: str, task_id: str):
    """Send a multi-step welcome email sequence."""
    steps = ["Welcome email", "Getting started guide", "Feature highlights"]
    for step in steps:
        time.sleep(0.5)
        print(f"[BG] Sending: {step} → {email}")
    complete_task(task_id, f"Welcome sequence complete for {email}")


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="Background Tasks Example", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Background Tasks Demo", "docs": "/docs"}


@app.post("/send-email", status_code=202)
async def schedule_email(
    email_req: EmailRequest,
    background_tasks: BackgroundTasks,
):
    """
    Schedule an email to be sent in the background.

    Returns 202 Accepted immediately — the email is sent after the response.
    The `background_tasks.add_task(fn, *args)` call queues the function.
    """
    task_id = register_task("send_email")
    background_tasks.add_task(
        send_email,
        email_req.to,
        email_req.subject,
        email_req.body,
        task_id,
    )
    return {
        "message": "Email scheduled",
        "task_id": task_id,
        "check_status": f"/tasks/{task_id}",
    }


@app.post("/orders", status_code=202)
async def place_order(
    order: OrderRequest,
    background_tasks: BackgroundTasks,
):
    """
    Place an order and schedule multiple background tasks.

    Three independent tasks are queued after a single POST request:
    1. Process the order (inventory + receipt)
    2. Send order confirmation email
    3. Write audit log
    """
    order_task_id = register_task("process_order")
    email_task_id = register_task("send_email")
    audit_task_id = register_task("audit_log")

    background_tasks.add_task(process_order, order, order_task_id)
    background_tasks.add_task(
        send_email,
        order.customer_email,
        "Order Confirmation",
        f"Your order of {len(order.items)} items (${order.total}) was received.",
        email_task_id,
    )
    background_tasks.add_task(
        write_audit_log,
        "order_placed",
        order.customer_email,
        f"order:{order.items}",
        audit_task_id,
    )

    return {
        "message": "Order placed — processing in background",
        "task_ids": {
            "order_processing": order_task_id,
            "confirmation_email": email_task_id,
            "audit_log": audit_task_id,
        },
    }


@app.post("/users/register", status_code=201)
async def register_user(email: str, background_tasks: BackgroundTasks):
    """
    Register a user and immediately trigger the welcome email sequence.

    The registration response is instant; the email sequence runs in background.
    """
    task_id = register_task("welcome_sequence")
    background_tasks.add_task(send_welcome_email_sequence, email, task_id)
    return {
        "message": f"User {email} registered",
        "welcome_sequence_task": task_id,
    }


@app.get("/tasks/{task_id}", response_model=TaskLog)
async def get_task_status(task_id: str):
    """Check the status of a background task."""
    if task_id not in task_registry:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_registry[task_id]


@app.get("/tasks", response_model=List[TaskLog])
async def list_tasks():
    """List all tracked background tasks."""
    return list(task_registry.values())


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 60)
    print("BACKGROUND TASKS — DEMO")
    print("=" * 60)
    print()
    print("Key concept:")
    print("  BackgroundTasks.add_task(fn, *args)")
    print("  → fn runs AFTER the HTTP response is sent")
    print("  → Client does NOT wait for the background work")
    print()
    print("Endpoints:")
    print("  POST /send-email         — 202 immediately, email sent async")
    print("  POST /orders             — 3 background tasks per order")
    print("  POST /users/register     — triggers welcome email sequence")
    print("  GET  /tasks/{id}         — check task status")
    print("  GET  /tasks              — list all tasks")
    print()
    print("When to use BackgroundTasks vs Celery:")
    print("  BackgroundTasks: simple, in-process, no broker needed")
    print("  Celery/ARQ: persistent, distributed, retryable")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 60)


if __name__ == "__main__":
    demo()
