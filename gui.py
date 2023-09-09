import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import threading
import csv
import logging
from file_revision import FileRevisionManager

LOG_FILE = "file_revision.log"
MAX_LOG_LINES = 100


class TextHandler(logging.Handler):
    """Handler class for logging messages to a tkinter text widget."""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_entry = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, log_entry + '\n')
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)


class FileRevisionTracker(tk.Tk):
    """Main Application Class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("File Revision Tracker")
        self.geometry("900x700")

        self.manager = FileRevisionManager()
        self._after_id = None

        self.init_ui()

        self.thread = threading.Thread(target=self.monitor_files)
        self.thread.daemon = True
        self.thread.start()

    def init_ui(self):
        """Initialize the user interface."""
        self.create_file_config_panel()
        self.create_status_panel()
        self.create_log_panel()

    def create_file_config_panel(self):
        """Panel for file configuration."""
        panel = self._create_panel("File Configuration")
        panel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self._setup_search_bar(panel)
        self._setup_file_table(panel)
        self._setup_config_buttons(panel)

        self.load_file_config_data()

    def _create_panel(self, title):
        return ttk.LabelFrame(self, text=title, padding=(10, 5))

    def _setup_search_bar(self, parent):
        search_frame = ttk.Frame(parent)
        search_frame.pack(pady=10, fill=tk.X, expand=True)

        self.search_var = tk.StringVar()
        self.search_entry = self._create_search_entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(search_frame, text="Reset", command=self.reset_search).pack(side=tk.RIGHT, padx=5)

    def _create_search_entry(self, parent):
        entry = tk.Entry(parent, textvariable=self.search_var, fg='grey')
        entry.insert(0, 'Search for files...')
        entry.bind('<Key>', self.on_key_press)
        entry.bind('<FocusIn>', self.on_entry_click)
        entry.bind('<FocusOut>', self.on_focusout)
        self.search_var.trace_add("write", lambda *args: self.delayed_search())
        return entry

    def _setup_file_table(self, parent):
        self.table = ttk.Treeview(parent, columns=('File Path', 'Revision Directory'), show="headings")
        self.table.heading('File Path', text='File Path')
        self.table.heading('Revision Directory', text='Revision Directory')
        self.table.pack(fill=tk.BOTH, expand=True)

    def _setup_config_buttons(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, expand=True)

        ttk.Button(btn_frame, text="Add", command=self.add_file_config).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Edit", command=self.edit_file_config).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Delete", command=self.delete_file_config).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Reload Config", command=self.reload_config).pack(side=tk.RIGHT, padx=10)

    def load_file_config_data(self):
        for item in self.table.get_children():
            self.table.delete(item)

        for path, revision_dir in self.manager.FILE_PATHS.items():
            self.table.insert("", tk.END, values=(path, revision_dir))

    def monitor_files(self):
        self.manager.start_monitoring()

    def create_status_panel(self):
        panel = self._create_panel("Status")
        panel.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.status_label = ttk.Label(panel, text="Monitoring")
        self.status_label.grid(row=0, column=0, sticky="w")

        ttk.Button(panel, text="Start Monitoring", command=self.start_monitoring).grid(row=1, column=0)
        ttk.Button(panel, text="Stop Monitoring", command=self.stop_monitoring).grid(row=1, column=1)

    def create_log_panel(self):
        panel = self._create_panel("Log Panel")
        panel.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self._setup_log_text(panel)

    def _setup_log_text(self, parent):
        self.log_text = tk.Text(parent, wrap=tk.WORD, height=15, width=100)
        self.log_text.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        scroll = ttk.Scrollbar(parent, command=self.log_text.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        self.log_text.config(yscrollcommand=scroll.set)

        self._load_initial_log_data()
        self._configure_log_handler()

        self.log_text.config(state=tk.DISABLED)

    def _load_initial_log_data(self):
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines[-MAX_LOG_LINES:]:
                self.log_text.insert(tk.END, line)
            self.log_text.see(tk.END)

    def _configure_log_handler(self):
        text_handler = TextHandler(self.log_text)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
        text_handler.setFormatter(formatter)
        logging.getLogger().addHandler(text_handler)

    def start_monitoring(self):
        self.manager.start_monitoring()
        self.status_label.config(text="Monitoring")

    def stop_monitoring(self):
        self.manager.stop_monitoring()
        self.status_label.config(text="Stopped")

    def add_file_config(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            revision_dir = simpledialog.askstring("Input", "Enter Revision Directory Name")
            if revision_dir:
                self.manager.FILE_PATHS[file_path] = revision_dir
                self.write_to_csv()
                self.load_file_config_data()

    def edit_file_config(self):
        selected_item = self.table.selection()
        if not selected_item:
            return

        selected_item = selected_item[0]
        file_path, revision_dir = self.table.item(selected_item, "values")
        new_revision_dir = simpledialog.askstring("Input", "Edit Revision Directory Name", initialvalue=revision_dir)

        if new_revision_dir:
            self.manager.FILE_PATHS[file_path] = new_revision_dir
            self.write_to_csv()
            self.load_file_config_data()

    def delete_file_config(self):
        selected_item = self.table.selection()
        if not selected_item:
            return

        selected_item = selected_item[0]
        file_path, revision_dir = self.table.item(selected_item, "values")
        del self.manager.FILE_PATHS[file_path]
        self.write_to_csv()
        self.load_file_config_data()

    def on_entry_click(self, event):
        if self.search_entry.get().strip() == 'Search for files...':
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg='black')

    def on_key_press(self, event):
        current_text = self.search_entry.get()
        if self.search_entry.get().strip() == 'Search for files...':
            self.search_entry.delete(0, "end")
            self.search_entry.config(fg='black')

    def on_focusout(self, event):
        current_text = self.search_entry.get()
        if current_text == '':
            self.search_entry.insert(0, 'Search for files...')
            self.search_entry.config(fg='grey')

    def reset_search(self):
        self.search_var.set("")
        self.load_file_config_data()

    def reload_config(self):
        self.manager.reload_configuration()
        self.load_file_config_data()

    def write_to_csv(self):
        config_file = 'file_config.csv'
        with open(config_file, mode='w', newline='') as file:
            fieldnames = ['file_path', 'revision_dir']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for path, revision_dir in self.manager.FILE_PATHS.items():
                writer.writerow({'file_path': path, 'revision_dir': revision_dir})

    def search_files(self):
        search_term = self.search_var.get().lower()

        # Clear all items from the table
        for item in self.table.get_children():
            self.table.delete(item)

        # Insert items that match the search term
        for path, revision_dir in self.manager.FILE_PATHS.items():
            if search_term in str(path).lower() or search_term in revision_dir.lower():
                self.table.insert("", tk.END, values=(path, revision_dir))

    def delayed_search(self):
        """Initiate the search after a delay."""
        # If there's an existing scheduled search, cancel it
        if self._after_id:
            self.after_cancel(self._after_id)

        # Schedule a new search in 300 milliseconds
        self._after_id = self.after(300, self.search_files)

if __name__ == "__main__":
    app = FileRevisionTracker()
    app.mainloop()
