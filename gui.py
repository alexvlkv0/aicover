import os
import tkinter as tk
from tkinter import ttk
import download
import requests

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
        
        self.model_menu_list = ["Models", "1", "2", "3"]
        #self.truncate_menu_list = ["", "Male to male", "Male to female", "Female to male", "Female to female"]
        
        self.model = tk.StringVar(value=self.model_menu_list[0])
        self.truncval = tk.IntVar(value=0)
        self.truncaccuracy = tk.IntVar(value=3)
        self.feature = tk.DoubleVar(value=0.75)
        self.var_2 = tk.BooleanVar(value=False)
        self.youtube_link = tk.StringVar(value="youtube link")
        self.output_path = tk.StringVar(value=os.getcwd())
        
        self.setup_widgets()
        
    def download_youtube(self):
        path = download.downloadYT(self.youtube_link.get())
        self.switch.invoke()
        self.switch.configure(state='disabled')
        self.youtube_entry.configure(foreground='grey',state='disabled')
        self.youtube_link.set(path)
        print(path, path[path.rfind('\\')+1:])
    
    def change_input_type(self):
        if self.var_2:
            self.youtube_link.set('enter path')
        else:
            self.youtube_link.set('youtube link')
        self.var_2 = not self.var_2
        
    def convert(self):
        path = self.youtube_link.get()
        files={'file': (path[path.rfind('\\'):], open(path, 'rb'))}
        r = requests.post('http://127.0.0.1:5000/upload?dora-7-4-0.75', files=files)

        # mp3file = urllib2.urlopen("http://gaana99.com/fileDownload/Songs/0/28768.mp3")
        # output = open('test.mp3','wb')
        # output.write(mp3file.read())
        # output.close()
        print(r.status_code)
        print(r.text)
    
    def setup_widgets(self):
        
        #INPUTS
        self.audio_frame = ttk.LabelFrame(self,text="Audio", padding=(0, 0, 0, 10))
        self.audio_frame.grid(
            row=0, column=0, padx=10, pady=(30, 10), sticky="nsew"
        )
        self.audio_frame.columnconfigure(index=0, weight=1)
        
        #entry for a youtube link
        self.youtube_entry = ttk.Entry(self.audio_frame, width=20,textvariable=self.youtube_link)
        self.youtube_entry.grid(row=0, columnspan=2, padx=5, pady=(10, 5), sticky="nsew")
        
        #toggle to switch from link to path
        self.switch = ttk.Checkbutton(
            self.audio_frame, text="switch to path", command=self.change_input_type, style="Switch.TCheckbutton"
        )
        self.switch.grid(row=1, column=0, padx=5, pady=(5, 15), sticky="nsew")
        self.checkbutton_value = True
        
        self.download_button = ttk.Button(self.audio_frame, text="Download", command=self.download_youtube)
        self.download_button.grid(row=1, column=1, padx=5, pady=(5, 15), sticky="nsew")
        
        #entry for an output folder
        self.feature_label = ttk.Label(
            self.audio_frame,
            text="Output folder",
            font=("-size", 11, "-weight", "bold"),
            padding=(10,0,0,5)
        )
        self.feature_label.grid(row=2,sticky="w")
        
        self.output_entry = ttk.Entry(self.audio_frame, width=20,textvariable=self.output_path)
        self.output_entry.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="nsew",columnspan=2)
        
        # Separator
        self.separator = ttk.Separator(self)
        self.separator.grid(row=4, column=0, padx=(20, 10), pady=(15, 10), sticky="nsew")
        
        self.model_frame = ttk.LabelFrame(self,text="Model options", padding=(0, 0, 0, 10))
        self.model_frame.grid(
            row=5, column=0, padx=10, pady=(10, 10), sticky="nsew"
        )
        self.model_frame.columnconfigure(index=0, weight=1)
        
        self.modelmenu = ttk.OptionMenu(
            self.model_frame, self.model, *self.model_menu_list
        )
        self.modelmenu.grid(row=6, column=0, padx=5, pady=10, sticky="nsew",columnspan=3)
        
        #truncate value
        self.label = ttk.Label(
            self.model_frame,
            text="Truncate",
            font=("-size", 12, "-weight", "bold"),
        )
        self.label.grid(row=7, columnspan=3)
        
        self.trunc_scale = ttk.Scale(
            self.model_frame,
            from_=-15,
            to=15,
            variable=self.truncval,
            command=lambda event: self.trunc_spin.set(int(self.trunc_scale.get())//1)
        )
        self.trunc_scale.grid(row=8, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew",columnspan=3)
        
        self.trunc_spin = ttk.Spinbox(self.model_frame, from_=-15, to=15, increment=1, width=6, textvariable = self.truncval)
        self.trunc_spin.grid(row=9, column=0, padx=5, pady=10, sticky="nw")
        
        self.plusminus = ttk.Label(self.model_frame,text="±",font=("-size", 15),justify="center")
        self.plusminus.grid(row=9, column=1, padx=5,pady=(5,5), sticky="nsew")
        
        self.trunc_accuracy = ttk.Spinbox(self.model_frame, from_=0, to=8, increment=1, width=5, textvariable = self.truncaccuracy)
        self.trunc_accuracy.grid(row=9, column=2, padx=5, pady=10, sticky="nw")
        
        #feature value
        self.feature_label = ttk.Label(
            self.model_frame,
            text="Feature",
            font=("-size", 12, "-weight", "bold"),
        )
        self.feature_label.grid(row=10, columnspan=3)
        
        self.feature_scale = ttk.Scale(
            self.model_frame,
            from_=0,
            to=1.01,
            variable=self.feature,
            command=lambda event: self.feature.set(self.feature_scale.get()//0.01/100)
        )
        self.feature_scale.grid(row=11, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew",columnspan=3)
        
        self.feature_spin = ttk.Spinbox(self.model_frame, from_=0, to=1, increment=0.1, width=7, textvariable = self.feature)
        self.feature_spin.grid(row=12, column=0, padx=5, pady=10, sticky="nw")
        
        
        #OUTPUT
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=4, pady=(25, 5), sticky="nsew")
        
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)
        
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")
        
        self.treeview = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=1,
            height=10,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)
        
        self.treeview.column("#0", anchor="w", width=120)
        self.treeview.column(1, anchor="w",width=360)
        self.treeview.heading("#0", text="Column 1", anchor="center")
        self.treeview.heading(1, text="Column 2", anchor="center")
        
        self.run_frame = ttk.LabelFrame(self,text="Run", padding=(0, 0, 0, 10))
        self.run_frame.grid(
            row=5, column=4, padx=10, pady=(30, 10), sticky="wse"
        )
        self.proceed_button = ttk.Button(self.run_frame, text="Convert", command=self.convert)
        self.proceed_button.grid(row=1, column=4, padx=20, pady=(20, 15), sticky="wse")
        
        self.merge_button = ttk.Button(self.run_frame, text="Merge", state='disabled')
        self.merge_button.grid(row=1, column=5, padx=20, pady=(20, 15), sticky="e")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("")

    # Simply set the theme
    root.tk.call("source", "theme\\azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()