# This is our Digital Roster(Dictionary) of students
# Format is "ID_NUMBER": "Student Name"
student_roster = {
    "12345": "Riley",
    "54321": "Alex",
    "99999": "Sam",
    "11111": "Taylor"
}
#keep track of number students on roster
print("Roster contains", len(student_roster), "students.")




#simulate scanning student ID, manual input to sim scanner
print("Ready to scan student IDs")

#loop for student scan
while True:
    print("\n--- READY TO SCAN ---")
    scanned_id = input("Scan Card (or type 'exit'): ")

    #  Exit condition for the loop
    if scanned_id == "exit":
        print("Shutting down scanner...")
        break

    # pulls up name from dictionary (student_roster)
    # if on your roster
    if scanned_id in student_roster:
        student_name = student_roster[scanned_id]
        print("BEEP! (Green Light)")
        print("Welcome aboard, " + student_name)
        print("Student is on the bus: " + scanned_id + " - " + student_name)
    #if not on your roster
    else:
        print("BUZZ! (Red Light)")
        print("ERROR: Unknown Student ID.")
        print("Try again or get off my bus.")