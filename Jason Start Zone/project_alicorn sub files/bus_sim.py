print("--- PRE-TRIP INSPECTION ---")
driver_name = input("Enter Driver Name: ")

print("Checking Bus Safety...")
# driver saftey check questions and save the answers
tires = input("Are TIRES good? (pass/fail): ")
lights = input("Are LIGHTS good? (pass/fail): ")
brakes = input("Are BRAKES good? (pass/fail): ")



#inspection results to send out
print("----------------------------")
print("Processing Report...")

if tires == "pass" and lights == "pass" and brakes == "pass":
    print("----------------------------")
    print("INSPECTION PASSED.")
    print("Sending 'Green' Signal to Dispatch.")
    print("Starting Engine...")
else:
    print("----------------------------")
    print("INSPECTION FAILED!")
    print("Sending 'RED FLAG' to Mechanics.")
    print("DO NOT DRIVE.")