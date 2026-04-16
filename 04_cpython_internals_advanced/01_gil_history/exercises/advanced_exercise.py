"""
ADVANCED EXERCISE: Custom GIL Implementation

Objective:
Implement a cooperative multitasking system that mimics GIL behavior
while providing fine-grained control over scheduling policies. Create a
CustomGIL class that supports multiple interchangeable policies.

Tasks:
1. Implement the CustomGIL class with acquire/release
2. Implement scheduling policies:
   - FIFO (First In First Out)
   - Priority-based (higher-priority threads acquire first)
   - Fair-share (distributes time equitably)
   - Lottery scheduling (ticket-based probabilistic selection)
3. Simulate 10+ competing threads with different priorities
4. Collect metrics: fairness, throughput, latency, starvation
5. Detect and prevent deadlocks
6. Compare it with CPython's real GIL
7. Document the tradeoffs of each policy

Required policies:
- FIFOScheduler: Arrival order
- PriorityScheduler: Highest priority first (with aging to prevent starvation)
- FairShareScheduler: Distributes time proportionally
- LotteryScheduler: Ticket-based probabilistic selection

Metrics:
- Fairness index (Jain's fairness)
- Throughput (tasks completed per second)
- Average waiting time
- Maximum waiting time (starvation detection)
- Context switches per second

Success criteria:
✅ CustomGIL works correctly with all policies
✅ No deadlocks or race conditions
✅ FIFOScheduler is deterministic
✅ PriorityScheduler respects priorities while preventing starvation
✅ FairShareScheduler achieves a fairness index > 0.9
✅ LotteryScheduler converges toward the expected distribution
✅ Exhaustive pytest tests
✅ Complete tradeoff documentation

Estimated time: 4-6 hours
"""

import threading
import time
import queue
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from dataclasses import dataclass
from enum import Enum
import random


class SchedulerPolicy(Enum):
    """Available scheduling policies."""
    FIFO = "fifo"
    PRIORITY = "priority"
    FAIR_SHARE = "fair_share"
    LOTTERY = "lottery"


@dataclass
class ThreadRequest:
    """Represents a thread request to acquire the GIL."""
    thread_id: int
    thread_name: str
    priority: int = 5  # 1 (lowest) - 10 (highest)
    tickets: int = 100  # For lottery scheduling
    arrival_time: float = 0.0
    wait_time: float = 0.0


class Scheduler(ABC):
    """Abstract interface for scheduling policies."""
    
    @abstractmethod
    def enqueue(self, request: ThreadRequest):
        """Add a request to the queue."""
        pass
    
    @abstractmethod
    def dequeue(self) -> Optional[ThreadRequest]:
        """Get the next request according to the policy."""
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        """Check whether there are pending requests."""
        pass


class FIFOScheduler(Scheduler):
    """
    TODO: Implement a FIFO (First In First Out) scheduler.
    
    Characteristics:
    - Strict arrival order
    - Ignores priorities
    - Deterministic and predictable
    - Can lead to starvation if there are many requests
    """
    
    def __init__(self):
        """TODO: Initialize the FIFO queue."""
        pass  # YOUR CODE HERE
    
    def enqueue(self, request: ThreadRequest):
        """TODO: Add to the end of the queue."""
        pass  # YOUR CODE HERE
    
    def dequeue(self) -> Optional[ThreadRequest]:
        """TODO: Remove from the start of the queue."""
        pass  # YOUR CODE HERE
    
    def is_empty(self) -> bool:
        """TODO: Check whether the queue is empty."""
        pass  # YOUR CODE HERE


class PriorityScheduler(Scheduler):
    """
    TODO: Implement a priority-based scheduler with aging.
    
    Characteristics:
    - Higher-priority threads go first
    - Aging: increase the priority of threads that wait too long
    - Prevents starvation
    - Tradeoff: may be unfair to low-priority threads
    """
    
    def __init__(self, aging_factor: float = 0.1):
        """
        TODO: Initialize the priority queue.
        
        Args:
            aging_factor: How much to increase priority per second of waiting
        """
        pass  # YOUR CODE HERE
    
    def enqueue(self, request: ThreadRequest):
        """TODO: Add with priority."""
        pass  # YOUR CODE HERE
    
    def dequeue(self) -> Optional[ThreadRequest]:
        """
        TODO: Remove the highest-priority request.
        
        Apply aging before selecting.
        """
        pass  # YOUR CODE HERE
    
    def is_empty(self) -> bool:
        pass  # YOUR CODE HERE


class FairShareScheduler(Scheduler):
    """
    TODO: Implement a scheduler that distributes time fairly.
    
    Characteristics:
    - Tracks how much time each thread has executed
    - Prioritizes threads that have executed less
    - Achieves high fairness
    - Tracking overhead
    """
    
    def __init__(self):
        """TODO: Initialize tracking structures."""
        pass  # YOUR CODE HERE
    
    def enqueue(self, request: ThreadRequest):
        """TODO: Add a request."""
        pass  # YOUR CODE HERE
    
    def dequeue(self) -> Optional[ThreadRequest]:
        """TODO: Select the thread that has executed for the least time."""
        pass  # YOUR CODE HERE
    
    def is_empty(self) -> bool:
        pass  # YOUR CODE HERE
    
    def record_execution(self, thread_id: int, duration: float):
        """TODO: Record a thread's execution time."""
        pass  # YOUR CODE HERE


class LotteryScheduler(Scheduler):
    """
    TODO: Implement lottery scheduling.
    
    Characteristics:
    - Ticket-based probabilistic selection
    - Threads with more tickets have a higher probability
    - Converges toward fair share over time
    - Non-deterministic (random)
    """
    
    def __init__(self):
        """TODO: Initialize data structures."""
        pass  # YOUR CODE HERE
    
    def enqueue(self, request: ThreadRequest):
        """TODO: Add a request with tickets."""
        pass  # YOUR CODE HERE
    
    def dequeue(self) -> Optional[ThreadRequest]:
        """
        TODO: Select the lottery winner.
        
        Algorithm:
        1. Sum all tickets
        2. Generate a random number in [0, total_tickets)
        3. Select the corresponding thread
        """
        pass  # YOUR CODE HERE
    
    def is_empty(self) -> bool:
        pass  # YOUR CODE HERE


class CustomGIL:
    """
    TODO: Implement a Custom GIL with interchangeable policies.
    
    The GIL must:
    - Allow only one thread to execute at a time
    - Use the scheduler to decide which thread goes next
    - Track metrics (waiting time, context switches, etc.)
    - Detect deadlocks (timeout in acquire)
    - Be thread-safe (use real Python locks)
    """
    
    def __init__(self, policy: SchedulerPolicy = SchedulerPolicy.FIFO):
        """
        TODO: Initialize CustomGIL.
        
        Args:
            policy: Scheduling policy to use
        """
        pass  # YOUR CODE HERE
    
    def acquire(
        self,
        thread_id: int,
        thread_name: str,
        priority: int = 5,
        tickets: int = 100,
        timeout: Optional[float] = None
    ) -> bool:
        """
        TODO: Acquire the GIL.
        
        Args:
            thread_id: Thread ID
            thread_name: Thread name
            priority: Priority (1-10)
            tickets: Tickets for lottery scheduling
            timeout: Maximum wait time (None = infinite)
            
        Returns:
            True if acquired, False on timeout
        """
        pass  # YOUR CODE HERE
    
    def release(self, thread_id: int):
        """
        TODO: Release the GIL.
        
        Args:
            thread_id: ID of the thread releasing it
        """
        pass  # YOUR CODE HERE
    
    def get_metrics(self) -> Dict:
        """
        TODO: Return collected metrics.
        
        Metrics:
        - fairness_index
        - average_wait_time
        - max_wait_time
        - context_switches
        - throughput (releases per second)
        """
        pass  # YOUR CODE HERE


# Test helper functions

def worker_task(
    gil: CustomGIL,
    thread_id: int,
    thread_name: str,
    work_duration: float,
    iterations: int,
    priority: int = 5,
    tickets: int = 100
):
    """
    TODO: Implement a worker task that uses CustomGIL.
    
    The task must:
    1. Acquire the GIL
    2. Simulate work (time.sleep)
    3. Release the GIL
    4. Repeat 'iterations' times
    """
    pass  # YOUR CODE HERE


def run_simulation(
    policy: SchedulerPolicy,
    num_threads: int,
    work_duration: float,
    iterations: int
):
    """
    TODO: Run a simulation with a specific policy.
    
    Args:
        policy: Scheduling policy
        num_threads: Number of threads
        work_duration: Duration of each unit of work
        iterations: Iterations per thread
    """
    pass  # YOUR CODE HERE


def compare_policies():
    """
    TODO: Compare all policies with the same configuration.
    
    Show:
    - Fairness index for each policy
    - Average/max waiting time
    - Throughput
    - Comparison table
    """
    pass  # YOUR CODE HERE


def main():
    """
    TODO: Main function that runs all simulations.
    
    It must:
    1. Run each policy with different configurations
    2. Show metrics and analysis
    3. Generate conclusions about tradeoffs
    4. Compare conceptually with CPython's real GIL
    """
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    main()


# UNIT TESTS (see test_advanced.py for the full implementation)

def test_fifo_scheduler():
    """TODO: Verify FIFO behavior."""
    pass

def test_priority_scheduler():
    """TODO: Verify priorities and aging."""
    pass

def test_fair_share_scheduler():
    """TODO: Verify fairness."""
    pass

def test_lottery_scheduler():
    """TODO: Verify probabilistic distribution."""
    pass

def test_custom_gil_no_deadlock():
    """TODO: Verify that there are no deadlocks."""
    pass

def test_custom_gil_mutual_exclusion():
    """TODO: Verify mutual exclusion (only 1 thread at a time)."""
    pass
