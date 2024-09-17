import os
import ffmpeg
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, BooleanVar, StringVar
import threading
import subprocess

def detect_gpu_codec():
    try:
        subprocess.check_output("nvidia-smi", stderr=subprocess.STDOUT)
        return 'h264_nvenc'
    except subprocess.CalledProcessError:
        pass

    try:
        result = subprocess.check_output("clinfo", stderr=subprocess.STDOUT).decode()
        if 'AMD' in result:
            return 'h264_amf'
    except subprocess.CalledProcessError:
        pass

    return 'libx264'

def scan_files(folder, file_types):
    if file_types == 'All':
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    else:
        return [f for f in os.listdir(folder) if f.endswith(file_types) and os.path.isfile(os.path.join(folder, f))]

def update_file_list(folder, file_types, file_vars, file_frame):
    for widget in file_frame.winfo_children():
        widget.destroy()

    files = scan_files(folder, file_types)
    file_vars.clear()

    for file in files:
        var = BooleanVar()
        file_vars[file] = var
        check = tk.Checkbutton(file_frame, text=file, variable=var, bg='#2e2e2e', fg='white', selectcolor='#2e2e2e')
        check.pack(anchor='w', pady=2, padx=5)

    file_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def browse_folder(folder_var, file_types_var, file_vars, file_frame):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var.set(folder_selected)
        update_file_list(folder_selected, file_types_var.get(), file_vars, file_frame)

def filter_files(folder_var, file_types_var, file_vars, file_frame):
    update_file_list(folder_var.get(), file_types_var.get(), file_vars, file_frame)

def toggle_select_all(select_all_var, file_vars):
    select_all = select_all_var.get()
    for var in file_vars.values():
        var.set(select_all)

def convert_file(input_file, output_format, remove_original, progress_bar, status_var, stop_var, total_files, current_file_index):
    try:
        output_path = save_var.get() if not save_to_original_var.get() else os.path.dirname(input_file)
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_path, f"{base_name}.{output_format.strip('.')}")

        codec = detect_gpu_codec() if output_format in ["mp4", "mkv", "avi", "mov", "wmv"] else None
        stream = ffmpeg.input(input_file)
        if codec:
            stream = ffmpeg.output(stream, output_file, vcodec=codec)
        else:
            stream = ffmpeg.output(stream, output_file)  # For image formats

        process = ffmpeg.run_async(stream, overwrite_output=True)

        while True:
            if stop_var.get():
                process.terminate()
                status_var.set("Stopped")
                return False

            progress = process.poll()
            if progress is not None:
                progress_bar['value'] = (current_file_index + 1) * (100 / total_files)
                status_var.set(f"Converting {os.path.basename(input_file)}...")
                root.update_idletasks()
                break

        if remove_original:
            os.remove(input_file)

        return True

    except Exception as e:
        print(f"Failed to convert file {input_file}: {str(e)}")
        return False

def start_conversion(folder_var, file_vars, output_format_var, remove_original_var, save_to_original_var, save_var, stop_var, progress_bar, status_var):
    selected_files = [file for file, var in file_vars.items() if var.get()]
    total_files = len(selected_files)
    
    if total_files == 0:
        messagebox.showinfo("Info", "No files selected for conversion.")
        return
    
    progress_bar['maximum'] = 100
    progress_bar['value'] = 0
    stop_var.set(False)
    
    def conversion_task():
        converted_files = []
        status_var.set("Processing...")

        for index, file_name in enumerate(selected_files):
            if stop_var.get():
                break
            success = convert_file(os.path.join(folder_var.get(), file_name), output_format_var.get(), remove_original_var.get(), progress_bar, status_var, stop_var, total_files, index)
            if success:
                converted_files.append(file_name)

        summary = f"Converted files: {len(converted_files)} out of {total_files}\n"
        summary += "\n".join([f"{i+1}. {file}" for i, file in enumerate(converted_files)])

        if stop_var.get():
            status_var.set("Conversion Stopped")
            summary += "\n\nConversion process was stopped."
        else:
            status_var.set("Conversion Completed")
            progress_bar['value'] = 100

        messagebox.showinfo("Conversion Completed", summary)

    threading.Thread(target=conversion_task).start()

def stop_conversion(stop_var, status_var):
    stop_var.set(True)
    status_var.set("Stopping...")

def toggle_save_path():
    if save_to_original_var.get():
        save_var_entry.config(state='disabled', bg='#5e5e5e', fg='white')
        save_to_folder_button.config(bg='#5e5e5e', fg='white', state='disabled')
    else:
        save_var_entry.config(state='normal', bg='#444444', fg='white')
        save_to_folder_button.config(bg='#444444', fg='white', state='normal')

root = tk.Tk()
root.title("Media Convert Free")
root.geometry("700x600")

root.configure(bg='#2e2e2e')
style = ttk.Style(root)
style.theme_use('clam')
style.configure("TButton", background='#444444', foreground='white')
style.configure("TLabel", background='#2e2e2e', foreground='white')
style.configure("TCheckbutton", background='#2e2e2e', foreground='white')
style.configure("TEntry", background='#444444', foreground='white')

folder_var = StringVar()
output_format_var = StringVar(value="mp4")
remove_original_var = BooleanVar(value=False)
save_to_original_var = BooleanVar(value=False)
file_types = sorted(["All", ".ts", ".mp4", ".mkv", ".mp3", ".flac", ".avi", ".mov", ".wmv", ".aac", ".wav", ".jpg", ".png", ".webp"])
file_types_var = StringVar(value="All")
file_vars = {}
stop_var = BooleanVar(value=False)
status_var = StringVar(value="Idle")

folder_frame = tk.Frame(root, bg='#2e2e2e')
folder_frame.pack(pady=10, fill=tk.X, padx=10)

tk.Label(folder_frame, text="Select Folder:", bg='#2e2e2e', fg='white').grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
tk.Entry(folder_frame, textvariable=folder_var, width=50, bg='#444444', fg='white').grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
tk.Button(folder_frame, text="Browse", command=lambda: browse_folder(folder_var, file_types_var, file_vars, file_frame), width=10, bg='#5e5e5e', fg='white').grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

save_frame = tk.Frame(root, bg='#2e2e2e')
save_frame.pack(pady=10, fill=tk.X, padx=10)

save_to_folder_label = tk.Label(save_frame, text="Save to Folder", bg='#2e2e2e', fg='white')
save_to_folder_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

save_var = StringVar()
save_var_entry = tk.Entry(save_frame, textvariable=save_var, width=50, bg='#444444', fg='white')
save_var_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

save_to_folder_button = tk.Button(save_frame, text="Browse", command=lambda: save_var.set(filedialog.askdirectory()), width=10, bg='#5e5e5e', fg='white')
save_to_folder_button.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

save_to_original_path_button = tk.Checkbutton(save_frame, text="Save to Original Path", variable=save_to_original_var, bg='#2e2e2e', fg='white', selectcolor='#2e2e2e', command=toggle_save_path)
save_to_original_path_button.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)

format_frame = tk.Frame(root, bg='#2e2e2e')
format_frame.pack(pady=10, fill=tk.X, padx=10)

tk.Label(format_frame, text="Convert to Format:", bg='#2e2e2e', fg='white').grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
output_format_menu = ttk.Combobox(format_frame, values=file_types, state='readonly', textvariable=output_format_var)
output_format_menu.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

filter_menu = ttk.Combobox(format_frame, values=file_types, state='readonly', textvariable=file_types_var)
filter_menu.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)
tk.Button(format_frame, text="Apply Filter", command=lambda: filter_files(folder_var, file_types_var, file_vars, file_frame)).grid(row=0, column=4, padx=10, pady=5, sticky=tk.W)

control_frame = tk.Frame(root, bg='#2e2e2e')
control_frame.pack(pady=10, fill=tk.X, padx=10)

tk.Button(control_frame, text="Start Conversion", command=lambda: start_conversion(folder_var, file_vars, output_format_var, remove_original_var, save_to_original_var, save_var, stop_var, progress_bar, status_var)).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
tk.Button(control_frame, text="Stop", command=lambda: stop_conversion(stop_var, status_var)).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
status_label = tk.Label(control_frame, textvariable=status_var, bg='#2e2e2e', fg='white')
status_label.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", troughcolor='#2e2e2e', background='white')

progress_bar = ttk.Progressbar(root, style="TProgressbar", length=100)
progress_bar.pack(fill=tk.X, padx=10, pady=5)

options_frame = tk.Frame(root, bg='#2e2e2e')
options_frame.pack(pady=10, fill=tk.X, padx=10)

select_all_var = BooleanVar()
tk.Checkbutton(options_frame, text="Select All", variable=select_all_var, bg='#2e2e2e', fg='white', selectcolor='#2e2e2e', command=lambda: toggle_select_all(select_all_var, file_vars)).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
tk.Checkbutton(options_frame, text="Delete original file after conversion", variable=remove_original_var, bg='#2e2e2e', fg='white', selectcolor='#2e2e2e').grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

file_canvas_frame = tk.Frame(root, bg='#2e2e2e', bd=2, relief=tk.SOLID)
file_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(file_canvas_frame, bg='#2e2e2e', bd=0, highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(file_canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
file_frame = tk.Frame(canvas, bg='#2e2e2e')
canvas.create_window((0, 0), window=file_frame, anchor='nw')

root.mainloop()
