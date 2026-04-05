import tkinter as tk
from tkinter import messagebox
import json

# --- DATA SETUP ---
student_roster = {"12345": "Riley", "54321": "Dad", "99999": "Mom"}

# The Route Map (auto demo)!!!!!
route_stops = [
    "Depot (Start)", 
    "Stop 1: Main St", 
    "Stop 2: Maple Ave", 
    "Stop 3: High School", 
    "BUS BARN (WIFI ZONE)"
]
current_stop_index = 0

# --- LOGIC FUNCTIONS ---
def drive_bus():
    """ This function moves the bus to the next stop automatically """
    global current_stop_index
    
    # Check if we are at the end of the route
    if current_stop_index < len(route_stops):
        location = route_stops[current_stop_index]
        
        # Update the Screen
        location_label.config(text=f"📍 LOCATION: {location}", fg="cyan")
        print(f"DEBUG: Bus moved to {location}")
        
        # Check for Wifi Dump
        if "WIFI ZONE" in location:
            status_label.config(text="📶 UPLOADING VIDEO...", fg="orange")
            root.after(2000, finish_upload) # Wait 2 seconds, then run finish_upload
        else:
            # Keep driving! Run this function again in 4 seconds (4000ms)
            current_stop_index += 1
            root.after(4000, drive_bus) 
            
    else:
        status_label.config(text="🛑 ROUTE COMPLETE", fg="red")

def finish_upload():
    status_label.config(text="✅ UPLOAD COMPLETE", fg="#2ecc71")
    messagebox.showinfo("System", "4K Video Uploaded to Server via Wi-Fi.")

def scan_card():
    """ Runs when you click SCAN """
    card_id = scan_entry.get()
    current_loc = route_stops[current_stop_index] # Get current bus location
    
    if card_id in student_roster:
        name = student_roster[card_id]
        display_label.config(text=f"WELCOME, {name}", fg="#2ecc71")
        
        # Create the JSON Packet (The "Live" Data)
        packet = {
            "type": "BOARDING_EVENT",
            "student": name,
            "location": current_loc, # Sends the LIVE location
            "status": "SAFE"
        }
        # Print it to console so you can see what is being "sent"
        print(f"📡 SENDING DATA: {json.dumps(packet)}")
        
    else:
        display_label.config(text="⛔ UNKNOWN ID", fg="red")
        
    scan_entry.delete(0, tk.END)

def start_route():
    # Triggered by the PASS button
    status_label.config(text="🚌 EN ROUTE", fg="#2ecc71")
    scan_entry.config(state="normal")
    scan_btn.config(state="normal")
    drive_bus() # <--- Kicks off the automatic driving loop

# --- GUI SETUP ---
root = tk.Tk()
root.title("Project Alicorn - MASTER SYSTEM")
root.geometry("500x600")
root.configure(bg="#2c3e50")

# Header
tk.Label(root, text="PROJECT ALICORN", font=("Arial", 20, "bold"), bg="#2c3e50", fg="white").pack(pady=10)

# Location Display (Changes automatically)
location_label = tk.Label(root, text="📍 LOCATION: PARKED", font=("Arial", 16), bg="black", fg="cyan", width=30)
location_label.pack(pady=10)

# Status Display
status_label = tk.Label(root, text="WAITING FOR INSPECTION...", font=("Arial", 12), bg="#2c3e50", fg="yellow")
status_label.pack(pady=10)

# Inspection Buttons
btn_frame = tk.Frame(root, bg="#2c3e50")
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="✅ START ROUTE", bg="#2ecc71", command=start_route).pack(side=tk.LEFT, padx=10)

# Scanner Section
tk.Label(root, text="-------------------------------", bg="#2c3e50", fg="gray").pack(pady=10)
display_label = tk.Label(root, text="READY", font=("Arial", 24, "bold"), bg="black", fg="gray", width=15)
display_label.pack(pady=10)

scan_entry = tk.Entry(root, font=("Arial", 18), justify='center')
scan_entry.pack(pady=5)
scan_entry.config(state="disabled")

scan_btn = tk.Button(root, text="SCAN ID", font=("Arial", 14), bg="orange", command=scan_card)
scan_btn.pack(pady=10)
scan_btn.config(state="disabled")

root.mainloop()
