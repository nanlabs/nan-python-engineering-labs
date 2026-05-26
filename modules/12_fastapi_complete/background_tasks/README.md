# Background Tasks

Estimated time: 60 minutes

## 1. Definition

FastAPI's **`BackgroundTasks`** allows you to queue functions to be called *after* the HTTP response has been sent. The client receives the response immediately while the background work runs in the same process.

### Key Characteristics

- **`background_tasks.add_task(fn, *args, **kwargs)`**: queues a callable with its arguments.
- **Post-response execution**: the function runs after `return`, not during request handling.
- **In-process**: no broker, no worker process — same Python interpreter.
- **Multiple tasks**: multiple `add_task()` calls queue multiple functions per request.
- **Not for heavy work**: CPU-bound or long tasks (> seconds) should use Celery/ARQ instead.

## 2. Practical Application

### Use Cases

- Sending confirmation emails after a successful registration.
- Writing audit logs asynchronously to avoid slowing the response.
- Triggering webhooks or external API calls post-response.
- Generating thumbnails after an image upload.

### Code Example

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_email(to: str, subject: str):
    # Runs after the response is sent
    print(f"Email sent to {to}: {subject}")

@app.post("/register", status_code=201)
def register(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Registered"}
```

## 3. Why Is It Important?

### Problem It Solves

Calling slow operations (email, webhooks) inline with the request handler adds latency that the client must wait for, even though the client doesn't need the result of that operation.

### Solution and Benefits

`BackgroundTasks` decouples fast, client-visible work (create DB record) from slow, non-critical work (send email). Response time drops and client experience improves without adding infrastructure.

## 4. References

- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Starlette BackgroundTasks](https://www.starlette.io/background/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create `POST /send-notification` that returns `202 Accepted` immediately and prints a log message in the background task.

### Intermediate Level

Track background tasks in an in-memory `task_registry` dict. Return a `task_id` in the response. Expose `GET /tasks/{task_id}` to check whether the task has completed.

### Advanced Level

Add three background tasks to a single `POST /orders` request: process order, send confirmation email, write audit log. Use `asyncio.sleep()` to simulate work durations.

### Success Criteria

- `POST /orders` returns within milliseconds, not seconds.
- Task status transitions from `pending` to `completed` after the background work finishes.
- All three tasks are queued and executed after the response.

## 6. Summary

`BackgroundTasks` is FastAPI's lightweight post-response task mechanism. It requires no external broker and is ideal for short, non-critical operations like email sending and logging. For distributed, persistent, or retryable tasks, use Celery or ARQ.

## 7. Reflection Prompt

What happens to a background task if the server crashes immediately after sending the response? How would you redesign the system to guarantee the task is eventually executed even through server restarts?
