class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = can_teach_subjects
        self.assigned_subjects = set()


def create_schedule(subjects, teachers):
    remaining = set(subjects)
    selected = []
    available = list(teachers)

    for t in teachers:
        t.assigned_subjects = set()

    while remaining:
        # Pick teacher covering the most uncovered subjects; break ties by youngest age
        best = max(
            available,
            key=lambda t: (len(t.can_teach_subjects & remaining), -t.age),
            default=None,
        )
        if best is None or not (best.can_teach_subjects & remaining):
            return None
        best.assigned_subjects = best.can_teach_subjects & remaining
        remaining -= best.assigned_subjects
        available.remove(best)
        selected.append(best)

    return selected


if __name__ == "__main__":
    subjects = {"Математика", "Фізика", "Хімія", "Інформатика", "Біологія"}

    teachers = [
        Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", {"Математика", "Фізика"}),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", {"Хімія"}),
        Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", {"Інформатика", "Математика"}),
        Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", {"Біологія", "Хімія"}),
        Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", {"Фізика", "Інформатика"}),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", {"Біологія"}),
    ]

    schedule = create_schedule(subjects, teachers)

    if schedule:
        print("Schedule:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} years old, email: {teacher.email}")
            print(f"   Teaches: {', '.join(sorted(teacher.assigned_subjects))}\n")
        assert set().union(*(t.assigned_subjects for t in schedule)) == subjects
    else:
        print("Cannot cover all subjects with available teachers.")
