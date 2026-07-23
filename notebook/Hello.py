# Demo Python Program

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

students = {
    "Alice": [85, 90, 88],
    "Bob": [78, 82, 80],
    "Charlie": [92, 95, 91]
}

print("Student Average Scores")
print("-" * 25)

for name, scores in students.items():
    avg = calculate_average(scores)
    print(f"{name}: {avg:.2f}")

highest_student = max(
    students,
    key=lambda s: calculate_average(students[s])
)

print("-" * 25)
print(f"Top Performer: {highest_student}")

print("Program Completed Successfully")
