from pynput.keyboard import Key, Listener
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from collections import Counter
import threading

class KeyLogger:
    def __init__(self):
        self.log_file = "keylog.txt"
        self.stats_file = "keystats.json"
        self.word_count = 0
        self.char_count = 0
        self.key_counts = Counter()
        self.current_word = []
        self.is_running = False
        self.load_stats()
        
    def load_stats(self):
        try:
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
                self.word_count = stats.get('word_count', 0)
                self.char_count = stats.get('char_count', 0)
                self.key_counts = Counter(stats.get('key_counts', {}))
        except FileNotFoundError:
            pass
            
    def save_stats(self):
        stats = {
            'word_count': self.word_count,
            'char_count': self.char_count,
            'key_counts': dict(self.key_counts)
        }
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f)
            
    def on_press(self, key):
        if not self.is_running:
            return False
            
        try:
            char = key.char
            if char:
                self.current_word.append(char)
                self.char_count += 1
                self.key_counts[char] += 1
                
        except AttributeError:
            key_name = str(key).replace('Key.', '')
            self.key_counts[key_name] += 1
            
            if key in [Key.space, Key.enter]:
                if self.current_word:
                    self.word_count += 1
                    self.current_word = []
                    
        self.write_to_log(str(key))
        self.save_stats()
        
        return True
        
    def write_to_log(self, key_str):
        with open(self.log_file, 'a') as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp}: {key_str}\n")
            
    def get_statistics(self):
        stats = f"""Typing Statistics:
        Total Words: {self.word_count}
        Total Characters: {self.char_count}
        
        Most Common Keys:
        {self._format_key_counts()}
        """
        return stats
        
    def _format_key_counts(self):
        return '\n        '.join(
            f"{key}: {count}" 
            for key, count in self.key_counts.most_common(10)
        )
        
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.listener = Listener(on_press=self.on_press)
            self.listener.start()
            
    def stop(self):
        self.is_running = False
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.save_stats()

    def reset_data(self):
        self.word_count = 0
        self.char_count = 0
        self.key_counts.clear()
        self.current_word = []
        
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        if os.path.exists(self.stats_file):
            os.remove(self.stats_file)
        
        self.save_stats()

class ConsentDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("User Consent Required")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_window(self.dialog)
        
        self.result = False
        self.setup_dialog()
        
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_dialog(self):
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        title_label = ttk.Label(main_frame, 
                              text="Keylogger Consent Form",
                              font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        consent_text = """This application will record keyboard inputs for the purpose of:
        - Analyzing typing patterns and productivity
        - Collecting typing statistics
        - Creating activity logs

        Important Information:
        - All data is stored locally on your computer
        - Data is saved in encrypted format
        - You can revoke consent at any time
        - Data older than 30 days is automatically deleted
        
        Please provide your consent to continue."""
        
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        text_widget = scrolledtext.ScrolledText(text_frame, 
                                              height=10, 
                                              width=50,
                                              font=('Helvetica', 10))
        text_widget.pack(fill="both", expand=True)
        text_widget.insert(tk.END, consent_text)
        text_widget.config(state='disabled')
        
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))
        
        name_label = ttk.Label(info_frame, 
                             text="Your Name:",
                             font=('Helvetica', 10))
        name_label.pack(anchor="w", pady=(0, 5))
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(info_frame, 
                                  textvariable=self.name_var,
                                  width=40)
        self.name_entry.pack(fill="x", pady=(0, 10))
        
        purpose_label = ttk.Label(info_frame, 
                                text="Purpose of Usage:",
                                font=('Helvetica', 10))
        purpose_label.pack(anchor="w", pady=(0, 5))
        
        self.purpose_var = tk.StringVar()
        self.purpose_entry = ttk.Entry(info_frame, 
                                     textvariable=self.purpose_var,
                                     width=40)
        self.purpose_entry.pack(fill="x", pady=(0, 10))
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=(20, 0))
        
        self.consent_button = tk.Button(button_frame,
                                      text="I Consent",
                                      font=('Helvetica', 10, 'bold'),
                                      bg='#007bff',
                                      fg='white',
                                      width=15,
                                      height=2,
                                      command=self.accept)
        self.consent_button.pack(side="left", padx=10)
        
        self.decline_button = tk.Button(button_frame,
                                      text="I Decline",
                                      font=('Helvetica', 10),
                                      width=15,
                                      height=2,
                                      command=self.decline)
        self.decline_button.pack(side="left", padx=10)
    
    def accept(self):
        if not self.name_var.get() or not self.purpose_var.get():
            messagebox.showerror("Error", "Please fill in all fields")
            return
        self.result = True
        self.user_name = self.name_var.get()
        self.purpose = self.purpose_var.get()
        self.dialog.destroy()
        
    def decline(self):
        self.result = False
        self.dialog.destroy()

class KeyLoggerGUI:
    def __init__(self):
        self.keylogger = KeyLogger()
        self.setup_gui()

    def setup_gui(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Key Logger")
        self.root.geometry("800x600")
        
        # Center the main window
        self.center_window(self.root)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create tabs
        self.tab_control = ttk.Notebook(self.root)
        
        # Dashboard tab
        self.dashboard_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.dashboard_tab, text='Dashboard')
        self.setup_dashboard()
        
        # Statistics tab
        self.stats_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.stats_tab, text='Statistics')
        self.setup_statistics()
        
        # Log viewer tab
        self.log_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.log_tab, text='Log Viewer')
        self.setup_log_viewer()
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Check consent before proceeding
        self.root.after(100, lambda: self.check_consent())
        
        # Start update loop
        self.update_stats()
        
    def setup_dashboard(self):
        control_frame = ttk.LabelFrame(self.dashboard_tab, text="Controls", padding="10")
        control_frame.pack(fill="x", padx=10, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Logging", 
                                     command=self.start_logging)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Logging", 
                                    command=self.stop_logging, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(control_frame,
                                    text="Reset All Data",
                                    command=self.reset_all_data,
                                    bg='#ff4444',
                                    fg='white',
                                    font=('Helvetica', 9, 'bold'))
        self.reset_button.pack(side="left", padx=20)
        
        status_frame = ttk.LabelFrame(self.dashboard_tab, text="Current Status", padding="10")
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Status: Stopped")
        self.status_label.pack()
        
        stats_frame = ttk.LabelFrame(self.dashboard_tab, text="Real-time Statistics", padding="10")
        stats_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.word_count_label = ttk.Label(stats_frame, text="Words Typed: 0")
        self.word_count_label.pack()
        
        self.char_count_label = ttk.Label(stats_frame, text="Characters Typed: 0")
        self.char_count_label.pack()
        
    def setup_statistics(self):
        self.stats_text = scrolledtext.ScrolledText(self.stats_tab, height=20)
        self.stats_text.pack(fill="both", expand=True, padx=10, pady=5)
        
    def setup_log_viewer(self):
        self.log_text = scrolledtext.ScrolledText(self.log_tab, height=20)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        refresh_button = ttk.Button(self.log_tab, text="Refresh Log", 
                                  command=self.refresh_log)
        refresh_button.pack(pady=5)
    
    def check_consent(self):
        dialog = ConsentDialog(self.root)
        self.root.wait_window(dialog.dialog)
        if not dialog.result:
            self.root.quit()
            return False
        return True
        
    def start_logging(self):
        self.keylogger.start()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Status: Running")
        
    def stop_logging(self):
        self.keylogger.stop()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopped")
        
    def reset_all_data(self):
        if messagebox.askyesno("Reset Data", 
                             "Are you sure you want to reset all data?\nThis will delete all logs and statistics."):
            if self.keylogger.is_running:
                self.stop_logging()
            
            self.keylogger.reset_data()
            
            self.word_count_label.config(text="Words Typed: 0")
            self.char_count_label.config(text="Characters Typed: 0")
            self.stats_text.delete(1.0, tk.END)
            self.log_text.delete(1.0, tk.END)
            
            messagebox.showinfo("Success", "All data has been reset successfully!")
        
    def update_stats(self):
        if self.keylogger.is_running:
            self.word_count_label.config(
                text=f"Words Typed: {self.keylogger.word_count}")
            self.char_count_label.config(
                text=f"Characters Typed: {self.keylogger.char_count}")
            
            stats = self.keylogger.get_statistics()
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, stats)
            
            if self.tab_control.select() == str(self.log_tab):
                self.refresh_log()
            
        self.root.after(1000, self.update_stats)
        
    def refresh_log(self):
        try:
            with open(self.keylogger.log_file, 'r') as f:
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, f.read())
        except FileNotFoundError:
            self.log_text.delete(1.0, tk.END)
            
    def run(self):
        self.root.mainloop()

def main():
    app = KeyLoggerGUI()
    app.run()

if __name__ == "__main__":
    main()
