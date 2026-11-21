Dataset preparation notes
=========================
Source: StudentsPerformance.csv (from the uploaded ZIP archive).
Original rows: 1000
Messy CSV rows: 1000
Rows assigned repeated admission numbers: 100
Added columns: admission_no and student_name.
The cleaning script normalizes admission numbers and keeps the first row
for each admission number. This is a demonstration rule; if repeated
admission numbers represent valid multiple records, review them instead
of automatically deleting them.
