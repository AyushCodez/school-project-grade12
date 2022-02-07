# use tkinter to create gui with 3 tabs - current, historical and read csv

# import libraries
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import matplotlib.pyplot as plt
import numpy as np
from utils import data_util, database_util, graph_util
import threading
import time
import platform
import cache
from tkcalendar import Calendar
from datetime import datetime, timedelta
import csv
from sys import platform

if platform == "win32":
    import warnings
    warnings.filterwarnings(
        "ignore", message="tight_layout : falling back to Agg renderer")


def graph():
    # generate random data
    a = np.random.normal(0, 1, 100)
    plt.hist(a, bins=20, color='#3B3C6E')
    plt.show()


def setup_window():
    # make button on tab1
    # make window
    if platform == "win32":
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    window = tk.Tk()
    window.title("Your Computer At A Glance (YCAAG)")
    if platform == "win32":
        window.geometry("300x650")
    else:
        window.geometry("400x750")
    window.resizable(0, 0)

    photo = tk.PhotoImage(file="images/icon.png")
    window.iconphoto(False, photo)

    s = ttk.Style(window)

    if platform != "win32":
        s.theme_use('clam')

    s.layout("Tab",
             [('Notebook.tab', {'sticky': 'nswe', 'children':
                                [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                                                       # [('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
                                                       [('Notebook.label', {
                                                        'side': 'top', 'sticky': ''})],
                                                       # })],
                                                       })],
                                })]
             )
    s.configure("TNotebook", tabposition='n')
    # make tabs
    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab4 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Current")
    tab_control.add(tab2, text="Historical")
    tab_control.add(tab3, text="Export CSV")
    tab_control.add(tab4, text="Import CSV")
    tab_control.pack(expand=1, fill="both")

    cpu_graph = graph_util.AnimatedBaseGraph(tab1, 60, "CPU")
    mem_graph = graph_util.AnimatedBaseGraph(tab1, 60, "MEMORY")
    disk_graph = graph_util.AnimatedBaseGraph(tab1, 60, "DISK")

    # frame1 = ttk.Frame(tab1)
    # frame2 = ttk.Frame(tab1)
    # frame3 = ttk.Frame(tab1)
    # new_data = cache.get_cache()[-1]
    cpu_graph.pack(fill="both", expand=1)
    # T = tk.Label(tab1, text = "MEMORY")
    # T.pack()
    mem_graph.pack(fill="both", expand=1)
    # T = tk.Label(tab1, text = "DISK")
    # T.pack()
    disk_graph.pack(fill="both", expand=1)

    ######
    '''TAB 2'''
    ######

    # Add Calendar
    top = tk.Frame(tab2)
    bottom = tk.Frame(tab2)

    T = tk.Label(tab2, text="From:")
    T.pack(pady=10)

    cal_tab2_var = tk.StringVar()
    cal_tab2_var.set(datetime.now().strftime("%d/%m/%y"))
    cal_tab2 = Calendar(tab2, textvariable=cal_tab2_var, selectmode='day', date_pattern='y-mm-dd', mindate=datetime.now() - timedelta(days=31),
                        maxdate=datetime.now(), weekendbackground='#FFFFFF', othermonthbackground='#FFFFFF', othermonthwebackground='#FFFFFF', showweeknumbers=False)
    cal_tab2_var.set(datetime.now().strftime("%Y-%m-%d"))

    cal_tab2.pack()
    top.pack()

    clicked_tab2 = tk.StringVar()
    clicked_tab2.set("Hour")
    options = ['Hour'] + [str(i) for i in range(24)]
    drop = tk.OptionMenu(tab2, clicked_tab2, *options)
    drop.pack(in_=top, side=tk.LEFT)

    clicked1_tab2 = tk.StringVar()
    clicked1_tab2.set("Minutes")
    options = ['Minutes'] + [str(i) for i in range(60)]
    drop1 = tk.OptionMenu(tab2, clicked1_tab2, *options)
    drop1.pack(in_=top, side=tk.RIGHT)

    T = tk.Label(tab2, text="To:")
    T.pack(pady=10)

    cal1_tab2_var = tk.StringVar()
    cal1_tab2_var.set(datetime.now().strftime("%d/%m/%y"))
    cal1_tab2 = Calendar(tab2, textvariable=cal1_tab2_var, selectmode='day', date_pattern='y-mm-dd', mindate=datetime.now() - timedelta(days=31),
                         maxdate=datetime.now(), weekendbackground='#FFFFFF', othermonthbackground='#FFFFFF', othermonthwebackground='#FFFFFF', showweeknumbers=False)
    cal1_tab2_var.set(datetime.now().strftime("%Y-%m-%d"))

    cal1_tab2.pack()
    bottom.pack()

    clicked2_tab2 = tk.StringVar()
    clicked2_tab2.set("Hour")
    options = ['Hour'] + [str(i) for i in range(24)]
    drop2 = tk.OptionMenu(tab2, clicked2_tab2, *options)
    drop2.pack(in_=bottom, side=tk.LEFT)

    clicked3_tab2 = tk.StringVar()
    clicked3_tab2.set("Minutes")
    options = ['Minutes'] + [str(i) for i in range(60)]
    drop3 = tk.OptionMenu(tab2, clicked3_tab2, *options)
    drop3.pack(in_=bottom, side=tk.RIGHT)

    def grad_date():
        a = clicked_tab2.get()
        if a == "Hour":
            a = "0"
        b = clicked1_tab2.get()
        if b == "Minutes":
            b = "0"
        a1 = clicked2_tab2.get()
        if a1 == "Hour":
            a1 = "23"
        b1 = clicked3_tab2.get()
        if b1 == "Minutes":
            b1 = "59"

        date1 = datetime.strptime(
            cal_tab2.get_date() + f' {a}:{b}:00', '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(
            cal1_tab2.get_date() + f' {a1}:{b1}:59', '%Y-%m-%d %H:%M:%S')
        data = database_util.get_data_from_date(date1, date2)

        # create 3 subplots for cpu, memory, disk
        fig, axs = plt.subplots(3, dpi=100, figsize=(6, 5))
        fig.tight_layout(pad=4)
        axs[0].set_title("CPU")
        axs[1].set_title("MEMORY")
        axs[2].set_title("DISK")
        axs[0].set_ylabel("Percent")
        axs[1].set_ylabel("Percent")
        axs[2].set_ylabel("Percent")
        axs[0].set_xlabel("Time")

        x_data = [date1 + timedelta(minutes=i)
                  for i in range((date2-date1).seconds//60 + 1)]
        x_from_the_dataa = [datetime.strptime(
            i[0], "%Y-%m-%d %H:%M") for i in data]
        yhaha = [float(ts[1]) for ts in data]
        y_data_cpu = []
        c = 0
        for i in x_data:
            if i not in x_from_the_dataa:
                y_data_cpu.append(None)
            else:
                y_data_cpu.append(yhaha[c])
                c += 1
        yhaha = [(float(ts[3])/float(ts[2]))*100 for ts in data]
        y_data_mem = []
        c = 0
        for i in x_data:
            if i not in x_from_the_dataa:
                y_data_mem.append(None)
            else:
                y_data_mem.append(yhaha[c])
                c += 1
        yhaha = [(float(ts[5])/float(ts[4]))*100 for ts in data]
        y_data_disk = []
        c = 0
        for i in x_data:
            if i not in x_from_the_dataa:
                y_data_disk.append(None)
            else:
                y_data_disk.append(yhaha[c])
                c += 1

        axs[0].set_ylim(0, 101)
        axs[1].set_ylim(0, 101)
        axs[2].set_ylim(0, 101)

        axs[0].set_xlim(date1, date2)
        axs[1].set_xlim(date1, date2)
        axs[2].set_xlim(date1, date2)

        axs[0].plot(x_data, y_data_cpu)
        axs[1].plot(x_data, y_data_mem)
        axs[2].plot(x_data, y_data_disk)
        plt.show()

    def switch_tab2(*args):
        a = clicked_tab2.get()
        if a == "Hour":
            a = "0"
        b = clicked1_tab2.get()
        if b == "Minutes":
            b = "0"
        a1 = clicked2_tab2.get()
        if a1 == "Hour":
            a1 = "23"
        b1 = clicked3_tab2.get()
        if b1 == "Minutes":
            b1 = "59"
        date1 = datetime.strptime(
            cal_tab2.get_date() + f' {a}:{b}:00', '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(
            cal1_tab2.get_date() + f' {a1}:{b1}:59', '%Y-%m-%d %H:%M:%S')
        if date1 > date2:
            button2.config(state='disabled')
        else:
            button2.config(state='normal')

    clicked_tab2.trace("w", switch_tab2)
    clicked1_tab2.trace("w", switch_tab2)
    clicked2_tab2.trace("w", switch_tab2)
    clicked3_tab2.trace("w", switch_tab2)
    cal_tab2_var.trace("w", switch_tab2)
    cal1_tab2_var.trace("w", switch_tab2)
    # Add Button and Label
    button2 = tk.Button(tab2, text="Get Data",
                        command=grad_date)
    button2.pack(pady=20)

    ######
    '''TAB 3'''
    ######
    top = tk.Frame(tab3)
    bottom = tk.Frame(tab3)

    T = tk.Label(tab3, text="From:")
    T.pack(pady=10)
    cal_var = tk.StringVar()
    cal_var.set(datetime.now().strftime("%d/%m/%y"))
    cal = Calendar(tab3, textvariable=cal_var, selectmode='day', date_pattern='y-mm-dd', mindate=datetime.now() - timedelta(days=31),
                   maxdate=datetime.now(), weekendbackground='#FFFFFF', othermonthbackground='#FFFFFF', othermonthwebackground='#FFFFFF', showweeknumbers=False)
    cal_var.set(datetime.now().strftime("%Y-%m-%d"))
    cal.pack()
    top.pack()

    clicked = tk.StringVar()
    clicked.set("Hour")
    options = ['Hour'] + [str(i) for i in range(24)]
    drop = tk.OptionMenu(tab3, clicked, *options)
    drop.pack(in_=top, side=tk.LEFT)

    clicked1 = tk.StringVar()
    clicked1.set("Minutes")
    options = ['Minutes'] + [str(i) for i in range(60)]
    drop1 = tk.OptionMenu(tab3, clicked1, *options)
    drop1.pack(in_=top, side=tk.RIGHT)

    T = tk.Label(tab3, text="To:")
    T.pack(pady=10)

    cal1_var = tk.StringVar()
    cal1_var.set(datetime.now().strftime("%d/%m/%y"))
    cal1 = Calendar(tab3, textvariable=cal1_var, selectmode='day', date_pattern='y-mm-dd', mindate=datetime.now() - timedelta(days=31),
                    maxdate=datetime.now(), weekendbackground='#FFFFFF', othermonthbackground='#FFFFFF', othermonthwebackground='#FFFFFF', showweeknumbers=False)
    cal1_var.set(datetime.now().strftime("%Y-%m-%d"))

    cal1.pack()

    bottom.pack()

    clicked2 = tk.StringVar()
    clicked2.set("Hour")
    options = ['Hour'] + [str(i) for i in range(24)]
    drop2 = tk.OptionMenu(tab3, clicked2, *options)
    drop2.pack(in_=bottom, side=tk.LEFT)

    clicked3 = tk.StringVar()
    clicked3.set("Minutes")
    options = ['Minutes'] + [str(i) for i in range(60)]
    drop3 = tk.OptionMenu(tab3, clicked3, *options)
    drop3.pack(in_=bottom, side=tk.RIGHT)

    def save_file_date():
        a = clicked.get()
        if a == "Hour":
            a = "0"
        b = clicked1.get()
        if b == "Minutes":
            b = "0"
        a1 = clicked2.get()
        if a1 == "Hour":
            a1 = "23"
        b1 = clicked3.get()
        if b1 == "Minutes":
            b1 = "59"
        date1 = datetime.strptime(
            cal.get_date() + f' {a}:{b}:00', '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(
            cal1.get_date() + f' {a1}:{b1}:59', '%Y-%m-%d %H:%M:%S')
        data = database_util.get_data_from_date(date1, date2)
        files = [('', '*.csv')]
        f = filedialog.asksaveasfile(filetypes=files, defaultextension=files)
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        a = f.name
        f.close()
        with open(a, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["TIME", "CPU", "MEMORY_TOTAL_BYTES",
                            "MEMORY_USED_BYTES", "DISK_TOTAL_BYTES", "DISK_USED_BYTES"])
            writer.writerows(data)

    def save_file_all():
        files = [('', '*.csv')]
        f = filedialog.asksaveasfile(filetypes=files, defaultextension=files)
        if f is None:
            return
        a = f.name
        f.close()
        with open(a, 'w', newline='') as f:

            with open('data1.csv', 'r+', newline='') as f1:
                reader = csv.reader(f1)
                writer = csv.writer(f)
                writer.writerow(["TIME", "CPU", "MEMORY_TOTAL_BYTES",
                                "MEMORY_USED_BYTES", "DISK_TOTAL_BYTES", "DISK_USED_BYTES"])
                writer.writerows(list(reader))

    def switch(*args):
        a = clicked.get()
        if a == "Hour":
            a = "0"
        b = clicked1.get()
        if b == "Minutes":
            b = "0"
        a1 = clicked2.get()
        if a1 == "Hour":
            a1 = "23"
        b1 = clicked3.get()
        if b1 == "Minutes":
            b1 = "59"
        date1 = datetime.strptime(
            cal_var.get() + f' {a}:{b}:00', '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(
            cal1.get_date() + f' {a1}:{b1}:59', '%Y-%m-%d %H:%M:%S')
        if date1 > date2:
            button1.config(state='disabled')
        else:
            button1.config(state='normal')

    clicked.trace("w", switch)
    clicked1.trace("w", switch)
    clicked2.trace("w", switch)
    clicked3.trace("w", switch)
    cal_var.trace("w", switch)
    cal1_var.trace("w", switch)

    # Add Button and Label
    button1 = tk.Button(tab3, text="Get data between dates",
                        command=save_file_date)
    button1.pack(pady=10)

    tk.Button(tab3, text="Get all data", command=save_file_all).pack()

    ######
    '''TAB 4'''
    ######
    def upload_data():
        window.update()
        filename = filedialog.askopenfile(title="Select a File",
                                          filetypes=[("CSV files",
                                                      "*.csv")])
        if filename is None:
            return
        f = filename.name
        filename.close()
        with open(f, 'r', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)[1:]
            fig, axs = plt.subplots(3, dpi=100, figsize=(6, 5))
            fig.tight_layout(pad=4)
            axs[0].set_title("CPU")
            axs[1].set_title("MEMORY")
            axs[2].set_title("DISK")
            axs[0].set_ylabel("Percent")
            axs[1].set_ylabel("Percent")
            axs[2].set_ylabel("Percent")
            axs[0].set_xlabel("Time")
            date_list = [i[0] for i in data]
            for i in range(len(date_list)):
                date_list[i] = datetime.strptime(
                    date_list[i], '%Y-%m-%d %H:%M')
            date1 = min(date_list)
            date2 = max(date_list)

            x_data = [date1 + timedelta(minutes=i)
                      for i in range((date2-date1).seconds//60 + 1)]
            x_from_the_dataa = [datetime.strptime(
                i[0], "%Y-%m-%d %H:%M") for i in data]
            yhaha = [float(ts[1]) for ts in data]
            y_data_cpu = []
            c = 0
            for i in x_data:
                if i not in x_from_the_dataa:
                    y_data_cpu.append(None)
                else:
                    y_data_cpu.append(yhaha[c])
                    c += 1
            yhaha = [(float(ts[3])/float(ts[2]))*100 for ts in data]
            y_data_mem = []
            c = 0
            for i in x_data:
                if i not in x_from_the_dataa:
                    y_data_mem.append(None)
                else:
                    y_data_mem.append(yhaha[c])
                    c += 1
            yhaha = [(float(ts[5])/float(ts[4]))*100 for ts in data]
            y_data_disk = []
            c = 0
            for i in x_data:
                if i not in x_from_the_dataa:
                    y_data_disk.append(None)
                else:
                    y_data_disk.append(yhaha[c])
                    c += 1

            axs[0].set_ylim(0, 101)
            axs[1].set_ylim(0, 101)
            axs[2].set_ylim(0, 101)

            axs[0].set_xlim(date1, date2)
            axs[1].set_xlim(date1, date2)
            axs[2].set_xlim(date1, date2)

            axs[0].plot(x_data, y_data_cpu)
            axs[1].plot(x_data, y_data_mem)
            axs[2].plot(x_data, y_data_disk)
            plt.show()

    def change_state(*args):
        with open("bg_run.txt", 'w') as f:
            f.write(str(Checkbutton1.get()))

    Checkbutton1 = tk.IntVar()
    with open('bg_run.txt', 'r') as f:
        Checkbutton1.set(int(f.read()))
    Checkbutton1.trace("w", change_state)

    Import = tk.LabelFrame(tab4, relief='flat')
    Settings = tk.LabelFrame(tab4, relief='flat')
    tk.Label(tab4, text="Upload data from file", font=(
        'Arial', 18)).pack(in_=Import, pady=10)
    tk.Button(tab4, text="Upload data", command=upload_data).pack(
        in_=Import, pady=10)
    tk.Label(tab4, text="Settings", font=(
        'Arial', 18)).pack(in_=Settings, pady=10)
    tk.Checkbutton(tab4, text="Keep running in Background?",
                   variable=Checkbutton1,
                   onvalue=1,
                   offvalue=0,
                   height=1,
                   width=25).pack(in_=Settings, pady=10)
    Import.grid(row=0, column=0, sticky="nsew", pady=10)
    Settings.grid(row=1, column=0, sticky="nsew", pady=10)
    tab4.grid_rowconfigure(0, minsize=tab1.winfo_height()//2)
    tab4.grid_columnconfigure(0, minsize=tab1.winfo_width())
    return window, cpu_graph, mem_graph, disk_graph


def poll():
    global thread_death, run_in_bg
    while True:
        with open("bg_run.txt", 'r') as f:
            bg_run = int(f.read())
        if (thread_death and not(bg_run)) or not(run_in_bg):
            print("\nShutting down...")
            break
        # update graphs with new data
        new_data = data_util.get_all_parsed_data()
        cache.update_data(new_data)
        time.sleep(0.9)
    return


thread_death = False
run_in_bg = True


def main():
    try:
        t1 = threading.Thread(target=poll)
        t1.start()
        window, cpu_graph, mem_graph, disk_graph = setup_window()
        cpu_graph.animate()
        mem_graph.animate()
        disk_graph.animate()

        def on_closing():
            global thread_death, run_in_bg
            thread_death = True
            window.destroy()
            with open("bg_run.txt", 'r') as f:
                bg_run = int(f.read())
            if bg_run == 1:
                nu = input("Press enter to exit")
                run_in_bg = False
            
            
            
        window.protocol("WM_DELETE_WINDOW", on_closing)
        window.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down...")
        exit()


if __name__ == "__main__":
    main()
