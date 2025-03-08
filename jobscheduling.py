import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

# Round Robin Scheduling
def round_robin(processes, quantum):
    n = len(processes)
    remaining_time = [p['burst_time'] for p in processes]
    time = 0
    complete = 0
    waiting_time = [0] * n
    turn_around_time = [0] * n
    process_queue = []

    for i, p in enumerate(processes):
        process_queue.append(i)
    
    while complete != n:
        for i in list(process_queue):
            if remaining_time[i] > quantum:
                time += quantum
                remaining_time[i] -= quantum
            else:
                time += remaining_time[i]
                waiting_time[i] = time - processes[i]['burst_time']
                remaining_time[i] = 0
                complete += 1
                process_queue.remove(i)
            turn_around_time[i] = waiting_time[i] + processes[i]['burst_time']

    return waiting_time, turn_around_time

# Shortest Job First (Non-Preemptive)
def shortest_job_first(processes):
    processes.sort(key=lambda p: p['burst_time'])
    waiting_time = [0] * len(processes)
    turn_around_time = [0] * len(processes)
    total_time = 0

    for i, process in enumerate(processes):
        waiting_time[i] = total_time - process['arrival_time']
        total_time += process['burst_time']
        turn_around_time[i] = total_time - process['arrival_time']

    return waiting_time, turn_around_time

# Priority Scheduling
def priority_scheduling(processes):
    processes.sort(key=lambda p: p['priority'])
    waiting_time = [0] * len(processes)
    turn_around_time = [0] * len(processes)
    total_time = 0

    for i, process in enumerate(processes):
        waiting_time[i] = total_time - process['arrival_time']
        total_time += process['burst_time']
        turn_around_time[i] = total_time - process['arrival_time']

    return waiting_time, turn_around_time

# Helper to calculate average waiting and turnaround time
def average_times(waiting_time, turn_around_time, n):
    avg_waiting_time = sum(waiting_time) / n
    avg_turn_around_time = sum(turn_around_time) / n
    return avg_waiting_time, avg_turn_around_time

# Suggest the best method based on the characteristics of the processes
def suggest_best_method(processes):
    max_burst_time = max([p['burst_time'] for p in processes])
    min_burst_time = min([p['burst_time'] for p in processes])
    has_priority = any(p['priority'] != processes[0]['priority'] for p in processes)
    
    if has_priority:
        return "Priority Scheduling"
    elif max_burst_time - min_burst_time > 5:  # Large difference in burst times
        return "Shortest Job First"
    else:
        return "Round Robin"

# Tkinter GUI
class SchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Algorithms")
        self.root.geometry("600x600")  # Set the window dimensions
        self.root.config(bg="#f0f0f0")  # Background color
        
        self.processes = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Font and colors
        label_font = ("Arial", 12, "bold")  # Changed font style
        entry_font = ("Arial", 14)  # Changed font size for larger input
        result_font = ("Arial", 14, "bold")  # Changed font style
        
        label_fg = "#333"
        entry_bg = "#fff"
        entry_fg = "#000"
        button_bg = "#4CAF50"
        button_fg = "#fff"
        
        # Process input frame
        self.input_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.input_frame.pack(pady=20, fill=tk.X)
        
        # Labels
        tk.Label(self.input_frame, text="Process ID", font=label_font, fg=label_fg, bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.input_frame, text="Arrival Time", font=label_font, fg=label_fg, bg="#f0f0f0").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.input_frame, text="Burst Time", font=label_font, fg=label_fg, bg="#f0f0f0").grid(row=0, column=2, padx=10, pady=5)
        tk.Label(self.input_frame, text="Priority", font=label_font, fg=label_fg, bg="#f0f0f0").grid(row=0, column=3, padx=10, pady=5)
        
        # Entry fields with increased width and centered
        self.process_id = tk.Entry(self.input_frame, font=entry_font, bg=entry_bg, fg=entry_fg, width=10)
        self.arrival_time = tk.Entry(self.input_frame, font=entry_font, bg=entry_bg, fg=entry_fg, width=10)
        self.burst_time = tk.Entry(self.input_frame, font=entry_font, bg=entry_bg, fg=entry_fg, width=10)
        self.priority = tk.Entry(self.input_frame, font=entry_font, bg=entry_bg, fg=entry_fg, width=10)
        
        self.process_id.grid(row=1, column=0, padx=10, pady=5)
        self.arrival_time.grid(row=1, column=1, padx=10, pady=5)
        self.burst_time.grid(row=1, column=2, padx=10, pady=5)
        self.priority.grid(row=1, column=3, padx=10, pady=5)
        
        # Add Process button
        tk.Button(self.input_frame, text="Add Process", command=self.add_process, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="raised", padx=10, pady=5).grid(row=1, column=4, padx=10)

        # Algorithm selection
        self.algorithm = tk.StringVar(value="Round Robin")
        self.algorithm_menu = ttk.Combobox(self.root, textvariable=self.algorithm, values=["Round Robin", "Shortest Job First", "Priority Scheduling"], font=entry_font, width=25)  # Decreased width
        self.algorithm_menu.pack(pady=10, fill=tk.X)

        # Output frame
        self.output_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.output_frame.pack(pady=10, fill=tk.X)
        
        # Calculate button
        tk.Button(self.root, text="Calculate", command=self.calculate, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="raised", padx=10, pady=5).pack(pady=10)
        
        self.result_label = tk.Label(self.root, text="", font=result_font, fg="#FF5722", bg="#f0f0f0")
        self.result_label.pack(pady=10)
        
        # Suggest Best Method button
        tk.Button(self.root, text="Suggest Best Method", command=self.suggest_method, bg=button_bg, fg=button_fg, font=("Arial", 10, "bold"), relief="raised", padx=10, pady=5).pack(pady=10)
        
        self.suggestion_label = tk.Label(self.root, text="", font=result_font, fg="#FF5722", bg="#f0f0f0")
        self.suggestion_label.pack(pady=10)
    
    def add_process(self):
        process = {
            'id': int(self.process_id.get()),
            'arrival_time': int(self.arrival_time.get()),
            'burst_time': int(self.burst_time.get()),
            'priority': int(self.priority.get())
        }
        self.processes.append(process)
        self.process_id.delete(0, tk.END)
        self.arrival_time.delete(0, tk.END)
        self.burst_time.delete(0, tk.END)
        self.priority.delete(0, tk.END)
        self.update_process_list()

    def update_process_list(self):
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        
        for i, process in enumerate(self.processes):
            tk.Label(self.output_frame, text=f"Process {i + 1}: {process}", font=("Arial", 10), fg="#333", bg="#f0f0f0").pack()
    
    def calculate(self):
        selected_algorithm = self.algorithm.get()
        
        # Show a pop-up dialog for the quantum value if Round Robin is selected
        quantum = None
        if selected_algorithm == "Round Robin":
            quantum = simpledialog.askinteger("Input", "Enter Quantum Value:", parent=self.root)
            if quantum is None:
                return  # User cancelled the dialog
        
        if selected_algorithm == "Round Robin":
            waiting_time, turn_around_time = round_robin(self.processes, quantum)
        elif selected_algorithm == "Shortest Job First":
            waiting_time, turn_around_time = shortest_job_first(self.processes)
        elif selected_algorithm == "Priority Scheduling":
            waiting_time, turn_around_time = priority_scheduling(self.processes)
        
        avg_waiting, avg_turnaround = average_times(waiting_time, turn_around_time, len(self.processes))
        self.result_label.config(text=f"Average Waiting Time: {avg_waiting:.2f}, Average Turnaround Time: {avg_turnaround:.2f}")

    def suggest_method(self):
        suggestion = suggest_best_method(self.processes)
        self.suggestion_label.config(text=f"Suggested Method: {suggestion}")

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulingApp(root)
    root.mainloop()
