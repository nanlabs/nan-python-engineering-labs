"""
EJERCICIO AVANZADO: Custom GIL Implementation

Objetivo:
Implementar un sistema de "cooperative multitasking" que imite el comportamiento
del GIL pero con control fino sobre políticas de scheduling. Crear una clase
CustomGIL que soporte múltiples políticas intercambiables.

Tareas:
1. Implementar CustomGIL class con acquire/release
2. Implementar políticas de scheduling:
   - FIFO (First In First Out)
   - Priority-based (hilos con mayor prioridad adquieren primero)
   - Fair-share (distribuye tiempo equitativamente)
   - Lottery scheduling (probabilístico basado en tickets)
3. Simular 10+ hilos con diferentes prioridades compitiendo
4. Recolectar métricas: fairness, throughput, latency, starvation
5. Detectar y prevenir deadlocks
6. Comparar con GIL real de CPython
7. Documentar tradeoffs de cada política

Políticas requeridas:
- FIFOScheduler: Orden de llegada
- PriorityScheduler: Mayor prioridad primero (con aging para prevenir starvation)
- FairShareScheduler: Distribuye tiempo proporcionalmente
- LotteryScheduler: Selección probabilística basada en tickets

Métricas:
- Fairness index (Jain's fairness)
- Throughput (tareas completadas por segundo)
- Average waiting time
- Maximum waiting time (detección de starvation)
- Context switches por segundo

Criterios de éxito:
✅ CustomGIL funciona correctamente con todas las políticas
✅ No hay deadlocks ni race conditions
✅ FIFOScheduler es determinístico
✅ PriorityScheduler respeta prioridades pero previene starvation
✅ FairShareScheduler logra fairness index > 0.9
✅ LotteryScheduler converge a distribución esperada
✅ Tests exhaustivos con pytest
✅ Documentación completa de tradeoffs

Tiempo estimado: 4-6 horas
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
    """Políticas de scheduling disponibles."""
    FIFO = "fifo"
    PRIORITY = "priority"
    FAIR_SHARE = "fair_share"
    LOTTERY = "lottery"


@dataclass
class ThreadRequest:
    """Representa una solicitud de un hilo para adquirir el GIL."""
    thread_id: int
    thread_name: str
    priority: int = 5  # 1 (lowest) - 10 (highest)
    tickets: int = 100  # Para lottery scheduling
    arrival_time: float = 0.0
    wait_time: float = 0.0


class Scheduler(ABC):
    """Interfaz abstracta para políticas de scheduling."""
    
    @abstractmethod
    def enqueue(self, request: ThreadRequest):
        """Agregar solicitud a la cola."""
        pass
    
    @abstractmethod
    def dequeue(self) -> Optional[ThreadRequest]:
        """Obtener siguiente solicitud según la política."""
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        """Verificar si hay solicitudes pendientes."""
        pass


class FIFOScheduler(Scheduler):
    """
    TODO: Implementar scheduler FIFO (First In First Out).
    
    Características:
    - Orden de llegada estricto
    - No considera prioridades
    - Determinístico y predecible
    - Puede llevar a starvation si hay muchas solicitudes
    """
    
    def __init__(self):
        """TODO: Inicializar cola FIFO."""
        pass  # TU CÓDIGO AQUÍ
    
    def enqueue(self, request: ThreadRequest):
        """TODO: Agregar al final de la cola."""
        pass  # TU CÓDIGO AQUÍ
    
    def dequeue(self) -> Optional[ThreadRequest]:
        """TODO: Remover del inicio de la cola."""
        pass  # TU CÓDIGO AQUÍ
    
    def is_empty(self) -> bool:
        """TODO: Verificar si cola está vacía."""
        pass  # TU CÓDIGO AQUÍ


class PriorityScheduler(Scheduler):
    """
    TODO: Implementar scheduler basado en prioridades con aging.
    
    Características:
    - Hilos con mayor prioridad van primero
    - Aging: incrementar prioridad de hilos esperando mucho tiempo
    - Previene starvation
    - Tradeoff: puede ser injusto con hilos de baja prioridad
    """
    
    def __init__(self, aging_factor: float = 0.1):
        """
        TODO: Inicializar priority queue.
        
        Args:
            aging_factor: Cuánto incrementar prioridad por segundo de espera
        """
        pass  # TU CÓDIGO AQUÍ
    
    def enqueue(self, request: ThreadRequest):
        """TODO: Agregar con prioridad."""
        pass  # TU CÓDIGO AQUÍ
    
    def dequeue(self) -> Optional[ThreadRequest]:
        """
        TODO: Remover solicitud de mayor prioridad.
        
        Aplicar aging antes de seleccionar.
        """
        pass  # TU CÓDIGO AQUÍ
    
    def is_empty(self) -> bool:
        pass  # TU CÓDIGO AQUÍ


class FairShareScheduler(Scheduler):
    """
    TODO: Implementar scheduler que distribuye tiempo equitativamente.
    
    Características:
    - Rastrea cuánto tiempo ha ejecutado cada hilo
    - Prioriza hilos que han ejecutado menos
    - Logra alta fairness
    - Overhead de tracking
    """
    
    def __init__(self):
        """TODO: Inicializar estructuras de tracking."""
        pass  # TU CÓDIGO AQUÍ
    
    def enqueue(self, request: ThreadRequest):
        """TODO: Agregar solicitud."""
        pass  # TU CÓDIGO AQUÍ
    
    def dequeue(self) -> Optional[ThreadRequest]:
        """TODO: Seleccionar hilo que ha ejecutado menos tiempo."""
        pass  # TU CÓDIGO AQUÍ
    
    def is_empty(self) -> bool:
        pass  # TU CÓDIGO AQUÍ
    
    def record_execution(self, thread_id: int, duration: float):
        """TODO: Registrar tiempo de ejecución de un hilo."""
        pass  # TU CÓDIGO AQUÍ


class LotteryScheduler(Scheduler):
    """
    TODO: Implementar lottery scheduling.
    
    Características:
    - Selección probabilística basada en tickets
    - Hilos con más tickets tienen mayor probabilidad
    - Converge a fair share en el largo plazo
    - No determinístico (aleatorio)
    """
    
    def __init__(self):
        """TODO: Inicializar estructuras."""
        pass  # TU CÓDIGO AQUÍ
    
    def enqueue(self, request: ThreadRequest):
        """TODO: Agregar solicitud con tickets."""
        pass  # TU CÓDIGO AQUÍ
    
    def dequeue(self) -> Optional[ThreadRequest]:
        """
        TODO: Seleccionar ganador de lotería.
        
        Algoritmo:
        1. Sumar todos los tickets
        2. Generar número aleatorio [0, total_tickets)
        3. Seleccionar hilo correspondiente
        """
        pass  # TU CÓDIGO AQUÍ
    
    def is_empty(self) -> bool:
        pass  # TU CÓDIGO AQUÍ


class CustomGIL:
    """
    TODO: Implementar Custom GIL con políticas intercambiables.
    
    El GIL debe:
    - Permitir solo un hilo ejecutar a la vez
    - Usar el scheduler para decidir qué hilo sigue
    - Rastrear métricas (waiting time, context switches, etc.)
    - Detectar deadlocks (timeout en acquire)
    - Thread-safe (usar locks reales de Python)
    """
    
    def __init__(self, policy: SchedulerPolicy = SchedulerPolicy.FIFO):
        """
        TODO: Inicializar CustomGIL.
        
        Args:
            policy: Política de scheduling a usar
        """
        pass  # TU CÓDIGO AQUÍ
    
    def acquire(
        self,
        thread_id: int,
        thread_name: str,
        priority: int = 5,
        tickets: int = 100,
        timeout: Optional[float] = None
    ) -> bool:
        """
        TODO: Adquirir el GIL.
        
        Args:
            thread_id: ID del hilo
            thread_name: Nombre del hilo
            priority: Prioridad (1-10)
            tickets: Tickets para lottery scheduling
            timeout: Máximo tiempo de espera (None = infinito)
            
        Returns:
            True si se adquirió, False si timeout
        """
        pass  # TU CÓDIGO AQUÍ
    
    def release(self, thread_id: int):
        """
        TODO: Liberar el GIL.
        
        Args:
            thread_id: ID del hilo que libera
        """
        pass  # TU CÓDIGO AQUÍ
    
    def get_metrics(self) -> Dict:
        """
        TODO: Retornar métricas recopiladas.
        
        Métricas:
        - fairness_index
        - average_wait_time
        - max_wait_time
        - context_switches
        - throughput (releases por segundo)
        """
        pass  # TU CÓDIGO AQUÍ


# Funciones de prueba

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
    TODO: Implementar tarea de worker que usa CustomGIL.
    
    La tarea debe:
    1. Adquirir GIL
    2. Simular trabajo (time.sleep)
    3. Liberar GIL
    4. Repetir 'iterations' veces
    """
    pass  # TU CÓDIGO AQUÍ


def run_simulation(
    policy: SchedulerPolicy,
    num_threads: int,
    work_duration: float,
    iterations: int
):
    """
    TODO: Ejecutar simulación con política específica.
    
    Args:
        policy: Política de scheduling
        num_threads: Número de hilos
        work_duration: Duración de cada "trabajo"
        iterations: Iteraciones por hilo
    """
    pass  # TU CÓDIGO AQUÍ


def compare_policies():
    """
    TODO: Comparar todas las políticas con la misma configuración.
    
    Mostrar:
    - Fairness index de cada política
    - Average/max waiting time
    - Throughput
    - Tabla comparativa
    """
    pass  # TU CÓDIGO AQUÍ


def main():
    """
    TODO: Función principal que ejecuta todas las simulaciones.
    
    Debe:
    1. Ejecutar cada política con diferentes configuraciones
    2. Mostrar métricas y análisis
    3. Generar conclusiones sobre tradeoffs
    4. Comparar con GIL real de CPython (conceptualmente)
    """
    pass  # TU CÓDIGO AQUÍ


if __name__ == "__main__":
    main()


# TESTS UNITARIOS (ver test_advanced.py para implementación completa)

def test_fifo_scheduler():
    """TODO: Verificar comportamiento FIFO."""
    pass

def test_priority_scheduler():
    """TODO: Verificar prioridades y aging."""
    pass

def test_fair_share_scheduler():
    """TODO: Verificar fairness."""
    pass

def test_lottery_scheduler():
    """TODO: Verificar distribución probabilística."""
    pass

def test_custom_gil_no_deadlock():
    """TODO: Verificar que no hay deadlocks."""
    pass

def test_custom_gil_mutual_exclusion():
    """TODO: Verificar mutual exclusion (solo 1 hilo a la vez)."""
    pass
