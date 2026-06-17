from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimizes 3D print queue by priority and printer constraints.

    Args:
        print_jobs: List of print job dicts
        constraints: Printer constraint dict

    Returns:
        Dict with print_order and total_time
    """
    jobs = [PrintJob(**j) for j in print_jobs]
    c = PrinterConstraints(**constraints)

    jobs.sort(key=lambda j: j.priority)

    print_order = []
    total_time = 0
    i = 0

    while i < len(jobs):
        batch = [jobs[i]]
        batch_volume = jobs[i].volume
        i += 1

        while (
            i < len(jobs)
            and len(batch) < c.max_items
            and batch_volume + jobs[i].volume <= c.max_volume
        ):
            batch.append(jobs[i])
            batch_volume += jobs[i].volume
            i += 1

        print_order.extend(j.id for j in batch)
        total_time += max(j.print_time for j in batch)

    return {"print_order": print_order, "total_time": total_time}


def test_printing_optimization():
    # Test 1: Same priority
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    # Test 2: Different priorities
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},
    ]

    # Test 3: Volume constraint exceeded
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("Test 1 (same priority):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} minutes")

    print("\nTest 2 (different priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} minutes")

    print("\nTest 3 (volume exceeded):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} minutes")

    assert result1 == {"print_order": ["M1", "M2", "M3"], "total_time": 270}
    assert result2 == {"print_order": ["M2", "M1", "M3"], "total_time": 270}
    assert result3 == {"print_order": ["M1", "M2", "M3"], "total_time": 450}
    print("\nAll assertions passed.")


if __name__ == "__main__":
    test_printing_optimization()
