import time
import json # tool for packaging and send the internet

# --- DATABASE CONFIGURATION ---

# 1 ROSTER
student_roster = {
    "12345": "Riley",
    "54321": "Momy",
    "99999": "Dady"
}

# 2. The Route
# We use a Dictionary here to give each stop a type (Stop vs Barn)
route_map = [
    {"name": "Stop A: Main St", "type": "STOP"},
    {"name": "Stop B: Maple Ave", "type": "STOP"},
    {"name": "BUS BARN", "type": "WIFI_ZONE"}
]

print("--- PROJECT ALICORN SYSTEM ONLINE ---")
print("Connecting to Cellular Network... Connected.")


#-------PRETRIP INSPECTION(phase 1)--------

print("Pre-Trip Inspection Required.")
driver_id = input("Enter Driver ID: ")

# Driver input
tires = input("Check Tires (pass/fail): ")
lights = input("Check Lights (pass/fail): ")
brakes = input("Check Brakes (pass/fail): ")    

if tires == "pass" and lights == "pass" and brakes == "pass":
    print("INSPECTION PASSED")
    # Send a packet to the Barn
    startup_packet = {
        "bus_id": 222,
        "driver": driver_id,
        "status": "Bus inspection Passed"
    }
    #simulates sending email/text to busBarn
    print(f" SENDING DATA TO BUSBARN: {json.dumps(startup_packet)}")
    time.sleep(2) 
else:
    print("INSPECTION FAILED. ALERT SENT TO MECHANICS. FIND A BETTER BUS.")
    exit() #stops the program if inspection fails




#--------ADD THE ROUTE (phase 2)----------    

print("--- ROUTE STARTED ---")

for location in route_map:
    # Simulate driving time
    print("\n🚍 DRIVING...")
    time.sleep(2)
    print(f"📍 ARRIVED AT: {location['name']}")
    
    # CHECK: Is this a Stop or the Barn?
    if location['type'] == "STOP":
        # We are at a stop. Allow scanning.
        action = input("Press 'Enter' to open doors (or type 'skip'): ")
        
        if action != "skip":
            scanned_id = input("Scan Student ID: ")
            
            # Identify Student
            if scanned_id in student_roster:
                student_name = student_roster[scanned_id]
                print(f"✅ WELCOME, {student_name}")
                
                # --- LIVE DATA PACKET (Requirements #1 & #4) ---
                # We send this INSTANTLY over cellular
                live_packet = {
                    "bus_id": 101,
                    "gps_location": location['name'],
                    "event": "BOARDING",
                    "student": student_name,
                    "timestamp": "08:00 AM"
                }
                # json.dumps turns our data into a text string the internet can read
                print(f"📡 SENDING LIVE PUSH NOTIFICATION TO PARENT: {json.dumps(live_packet)}")
            
            else:
                print("❌ UNKNOWN ID.")

    elif location['type'] == "WIFI_ZONE":
        # --- THE DATA DUMP (Requirement #3) ---
        print("\n📶 SECURE WIFI DETECTED.")
        print("Initiating End-of-Day Protocols...")
        time.sleep(1)
        print("1. Uploading 4K Camera Footage... [||||||||||] 100%")
        print("2. Uploading Engine Telemetry Logs... [||||||||||] 100%")
        print("✅ DATA DUMP COMPLETE.")
        print("System Shutting Down. Goodnight.")
