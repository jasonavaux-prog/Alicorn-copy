import tkinter as tk
from tkinter import messagebox

# --- DATABASE ---
student_roster = {
    "12345": "Riley",
    "54321": "Alex",
    "99999": "Sam"
}

# --- FUNCTIONS ---
def mark_safe():
    status_label.config(text="✅ SYSTEM: ACTIVE", fg="#2ecc71")
    # Enable the scanner (normal apps disable features until you are ready)
    scan_entry.config(state="normal") 
    scan_btn.config(state="normal")

def mark_unsafe():
    status_label.config(text="❌ SYSTEM: MAINTENANCE", fg="#e74c3c")
    messagebox.showwarning("Dispatch", "CRITICAL ERROR: Mechanic Alerted.")

def scan_card():
    # 1. Get the text from the white box
    card_id = scan_entry.get()
    
    # 2. Check the database
    if card_id in student_roster:
        name = student_roster[card_id]
        # Update the Big Screen
        display_label.config(text=f"WELCOME, {name}", fg="#2ecc71") # Green Text
        
        # Simulate sending the text message
        print(f"📡 UPLOAD: Student {name} boarded at GPS 40.7128")
        
    else:
        display_label.config(text="⛔ UNKNOWN ID", fg="red")
        messagebox.showerror("Security", "Card not recognized!")

    # 3. Clear the box for the next student
    scan_entry.delete(0, tk.END)

# --- GUI SETUP ---
root = tk.Tk()
root.title("Project Alicorn - Driver Terminal")
root.geometry("400x600")
root.configure(bg="#2c3e50")

# -- SECTION 1: INSPECTION --
tk.Label(root, text="STEP 1: INSPECTION", font=("Arial", 12, "bold"), bg="#2c3e50", fg="white").pack(pady=10)

status_label = tk.Label(root, text="WAITING...", font=("Arial", 10), bg="#2c3e50", fg="yellow")
status_label.pack()

btn_frame = tk.Frame(root, bg="#2c3e50") # A container to hold buttons side-by-side
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="✅ PASS", bg="#2ecc71", command=mark_safe).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="❌ FAIL", bg="#e74c3c", command=mark_unsafe).pack(side=tk.LEFT, padx=10)

# -- SECTION 2: SCANNER --
tk.Label(root, text="-------------------------------", bg="#2c3e50", fg="gray").pack(pady=10)
tk.Label(root, text="STEP 2: STUDENT SCANNER", font=("Arial", 12, "bold"), bg="#2c3e50", fg="white").pack(pady=5)

# The Big Display Screen
display_label = tk.Label(root, text="READY TO SCAN", font=("Arial", 20, "bold"), bg="black", fg="#2ecc71", width=20, height=2)
display_label.pack(pady=10)

# The Input Box (Entry)
scan_entry = tk.Entry(root, font=("Arial", 14), justify='center')
scan_entry.pack(pady=5)
# Disable it initially so they MUST do inspection first
scan_entry.config(state="disabled") 

# The Scan Button
scan_btn = tk.Button(root, text="SCAN CARD", font=("Arial", 12), bg="orange", command=scan_card)
scan_btn.pack(pady=10)
scan_btn.config(state="disabled")

root.mainloop()