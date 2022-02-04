import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import cache
from sys import platform


class AnimatedBaseGraph(tk.Frame):

    def __init__(self, parent, max_points, dtype):
        tk.Frame.__init__(self, parent)

        self.max_points = max_points
        self.dtype = dtype

        # mat plot lib figure
        self.figure = Figure(figsize=(3, 2), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # initial dummy 0 data
        date_time_points_ago = datetime.now() + timedelta(seconds=-max_points)
        self.data_x = [date_time_points_ago +
                       timedelta(seconds=i) for i in range(max_points)]
        self.data_y = [0 for _ in range(max_points)]
        self.figure.tight_layout(pad=1)
        # create the plot
        self.plot = self.ax.plot(self.data_x, self.data_y)[0]
        self.plot.title = self.dtype
        self.plot.axes.get_xaxis().set_visible(False)
        # all plots are PERCENT
        self.ax.set_ylim(0, 101)
        self.ax.set_xlim(self.data_x[0], self.data_x[-1])
        self.ax.set_ylabel("Percent")

        self.info_frame = tk.Frame(self)
        # add info to frame
        self.heading_label = tk.Label(self.info_frame, text=self.dtype)
        self.heading_label.pack(in_=self.info_frame, side=tk.LEFT)
        self.info_value = tk.StringVar()
        self.info_value.set("00.00%")
        self.info_value_label = tk.Label(
            self.info_frame, textvariable=self.info_value)
        self.info_value_label.pack(in_=self.info_frame, side=tk.RIGHT)

        self.info_frame.pack(side=tk.TOP, expand=1, fill="both")

        self.extra_info = tk.StringVar()
        self.extra_info.set("")
        self.extra_info_label = tk.Label(
            self.info_frame, textvariable=self.extra_info)
        self.extra_info_label.pack(side=tk.RIGHT)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=1)

    def animate(self):
        new_data = cache.get_cache()

        self.data_x = [d[0] for d in new_data]
        if self.dtype == "CPU":
            self.data_y = [d[1] for d in new_data]
        elif self.dtype == "MEMORY":
            self.data_y = [round((d[3]/d[2])*100, 2) for d in new_data]
        elif self.dtype == "DISK":
            self.data_y = [round((d[5]/d[4])*100, 2) for d in new_data]
        else:
            raise Exception("Unknown dtype")

        if len(self.data_x) < self.max_points:
            # generate 1 second intervals to prepend
            # 120 seconds ago...
            dt_120_second_ago = datetime.now() + timedelta(seconds=-self.max_points)
            self.data_x = [dt_120_second_ago + timedelta(seconds=i) for i in range(
                (self.max_points - len(self.data_x)) + 1)] + self.data_x

        if len(self.data_y) < self.max_points:
            self.data_y = [None for _ in range(
                (self.max_points - len(self.data_y)) + 1)] + self.data_y

        # update plot data
        self.plot.set_xdata(self.data_x)
        self.plot.set_ydata(self.data_y)
        self.ax.set_xlim(self.data_x[0], self.data_x[-1])
        self.canvas.draw_idle()  # redraw plot

        # update info
        self.info_value.set("{:.2f}".format(
            self.data_y[-1]).rjust(5, "0") + "%")

        if self.dtype == "MEMORY":
            self.extra_info.set(
                f"{round(new_data[-1][3]/1.049e+6, 2)}/{round(new_data[-1][2]/1.049e+6,2)} MB")
        elif self.dtype == "DISK":
            if platform == "win32":
                self.extra_info.set(
                    f"{round(new_data[-1][5]/1.074e+9,2)}/{round(new_data[-1][4]/1.074e+9,2)} GB")
            else:
                self.extra_info.set(
                    f"{round(new_data[-1][5]/1e+9,2)}/{round(new_data[-1][4]/1e+9,2)} GB")

        self.after(1000, self.animate)  # repeat after 1s
