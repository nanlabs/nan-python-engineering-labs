"""
Example: Visualization of GIL contention in different scenarios.

Demonstrates convoy effect, priority inversion, and other traditional GIL issues.
"""

import threading
import time
import sys
from dataclasses import dataclass
from typing import List
from collections import defaultdict

@dataclass
class GILEvent:
    """Record of a GIL acquire/release event."""
    timestamp: float
    thread_name: str
    event_type: str  # 'acquire' o 'release'
    wait_time: float = 0.0

class GILTracer:
    """
    Simulates and tracks GIL events to visualize contention.
    """
    
    def __init__(self):
        self.events: List[GILEvent] = []
        self.current_holder = None
        self.wait_start_times = {}
        self.lock = threading.Lock()
    
    def acquire(self, thread_name: str):
        """Simulate GIL acquisition."""
        wait_start = time.perf_counter()
        
        with self.lock:
            # If someone else has the GIL, we must wait
            while self.current_holder is not None:
                self.lock.release()
                time.sleep(0.001)  # Simulate waiting
                self.lock.acquire()
            
            wait_time = time.perf_counter() - wait_start
            self.current_holder = thread_name
            self.events.append(GILEvent(
                timestamp=time.perf_counter(),
                thread_name=thread_name,
                event_type='acquire',
                wait_time=wait_time
            ))
    
    def release(self, thread_name: str):
        """Simulate GIL release."""
        with self.lock:
            if self.current_holder == thread_name:
                self.current_holder = None
                self.events.append(GILEvent(
                    timestamp=time.perf_counter(),
                    thread_name=thread_name,
                    event_type='release'
                ))
    
    def generate_timeline_report(self) -> str:
        """Generate an ASCII report of the GIL timeline."""
        if not self.events:
            return "No events recorded"
        
        # Group by thread
        thread_events = defaultdict(list)
        for event in self.events:
            thread_events[event.thread_name].append(event)
        
        report = ["\nGIL TIMELINE"]
        report.append("="*70)
        report.append("Legend: [A]=Acquire, [R]=Release, [W]=Waiting\n")
        
        for thread_name in sorted(thread_events.keys()):
            events = thread_events[thread_name]
            report.append(f"{thread_name:15} ", end="")
            
            for event in events:
                if event.event_type == 'acquire':
                    if event.wait_time > 0.001:
                        report.append("[W]", end="")
                    report.append("[A]", end="")
                else:
                    report.append("[R] ", end="")
            
            report.append("")
        
        # Metrics
        report.append("\n" + "="*70)
        report.append("CONTENTION METRICS")
        report.append("="*70)
        
        for thread_name in sorted(thread_events.keys()):
            events = thread_events[thread_name]
            total_wait = sum(e.wait_time for e in events if e.event_type == 'acquire')
            acquisitions = sum(1 for e in events if e.event_type == 'acquire')
            
            report.append(f"{thread_name:15} Acquires: {acquisitions:3d}  "
                         f"Total wait: {total_wait*1000:6.2f}ms  "
                         f"Avg wait: {total_wait/acquisitions*1000:5.2f}ms")
        
        return "\n".join(report)


def demo_convoy_effect():
    """Demonstration of convoy effect with multiple CPU-bound threads."""
    print("\n🔴 CONVOY EFFECT DEMO")
    print("="*70)
    
    tracer = GILTracer()
    
    def cpu_worker(name: str, iterations: int):
        for _ in range(iterations):
            tracer.acquire(name)
            # Simulate CPU work
            _ = sum(range(1000))
            tracer.release(name)
    
    threads = []
    for i in range(6):
        t = threading.Thread(
            target=cpu_worker,
            args=(f"CPU-{i}", 10),
            daemon=True
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(tracer.generate_timeline_report())
    print("\n💡 Observe: Many [W] (waiting) markers indicate severe convoy effect")


def demo_priority_inversion():
    """Demonstration of priority inversion: I/O blocked by CPU work."""
    print("\n🟡 PRIORITY INVERSION DEMO")
    print("="*70)
    
    tracer = GILTracer()
    response_times = []
    
    def io_worker():
        """I/O worker that needs low latency."""
        for i in range(5):
            start = time.perf_counter()
            
            # Simulate I/O (releases the GIL)
            time.sleep(0.01)
            
            # Needs the GIL to process
            tracer.acquire("IO-Worker")
            _ = sum(range(100))
            tracer.release("IO-Worker")
            
            response_times.append(time.perf_counter() - start)
    
    def cpu_hog():
        """CPU worker that monopolizes the GIL."""
        for _ in range(20):
            tracer.acquire("CPU-Hog")
            _ = sum(range(5000))
            tracer.release("CPU-Hog")
    
    # Run simultaneously
    io_thread = threading.Thread(target=io_worker, daemon=True)
    cpu_thread = threading.Thread(target=cpu_hog, daemon=True)
    
    io_thread.start()
    time.sleep(0.005)  # Give I/O a head start
    cpu_thread.start()
    
    io_thread.join()
    cpu_thread.join()
    
    print(tracer.generate_timeline_report())
    print(f"\nI/O worker response times: {[f'{t*1000:.2f}ms' for t in response_times]}")
    print("💡 Observe: The I/O worker experiences delays while CPU-Hog holds the GIL")


def main():
    print("GIL CONTENTION VISUALIZATION")
    print("="*70)
    print(f"Python: {sys.version.split()[0]}")
    print(f"Switch interval: {sys.getswitchinterval()}s")
    
    demo_convoy_effect()
    time.sleep(1)
    demo_priority_inversion()


if __name__ == "__main__":
    main()
