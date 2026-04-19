import time # This tool allows us to pause the program

# made up bus route
#barn -> stop 1 -> stop 2 -> stop 3 -> barn
gps_route = [
    "Stop 1: Main St",
    "Stop 2: Maple Ave",
    "Stop 3: High School",
    "Bus Barn (WiFi Zone)"
]    
    
print("--- LETS GO!!!! ---")

for current_stop in gps_route:
    # 1. Announce the location
    print("--------------------------------")
    print("DRIVING...")
    time.sleep(2) # Pauses for 2 seconds (simulates driving)
    print("ARRIVED AT: " + current_stop)
    
    # 2. Simulate BusBarn auto upload
    if current_stop == "Bus Barn (WiFi Zone)":
        print(">> WIFI SIGNAL <<")
        print("ACTION: Uploading Camera Footage...")
        time.sleep(3) # Simulate upload time
        print("SUCCESS: Data Uploaded via WiFi.")
        #cost of upload:$0.00
        
    else:
        # We are out on the road (Cellular)
        print("STATUS: Sending Live GPS Ping (Data Saver Mode)")
        print("ACTION: Student Scan System Active")
