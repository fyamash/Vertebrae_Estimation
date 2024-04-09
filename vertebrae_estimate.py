import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import csv

# Add new races to list if user wants them to show on GUI
race_list=['White', 'Black', 'South Indian'] 

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Estimate T12, S1 Locations")
        # set size of window
        self.geometry('400x230')

        menubar = tk.Menu()
        # Create the first menu.
        menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(menu=menu, label="Help")
        menu.add_command(label="About", command=self.show_about)
        menu.add_command(label="Export as exe", command=self.show_exe)
        self.config(menu=menubar)

        self.gender = tk.StringVar(self,'')
        self.race = tk.StringVar(self,'')
        self.height = tk.StringVar(self,'')
        self.new_race = tk.StringVar(self,'')
        self.check = tk.IntVar()
        self.t12_est = 0
        self.s1_est = 0

        tk.Label(self, text='Select gender:').grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(self, text='Male', variable=self.gender, value='M').grid(row=1, column=0, sticky=tk.W, padx=5)
        ttk.Radiobutton(self, text='Female', variable=self.gender, value='F').grid(row=2, column=0, sticky=tk.W, padx=5)
        
        tk.Label(self, text='Select race:').grid(row=0, column=1, sticky=tk.W, padx=15)
        for i, race in enumerate(race_list):
            ttk.Radiobutton(self, text=race, variable=self.race, value=race).grid(row=i+1, column=1, sticky=tk.W, padx=20)
        
        row_idx = len(race_list)+1
        ttk.Radiobutton(self, text='New race to record', variable=self.race, value='New').grid(row=row_idx, column=1,columnspan=2, sticky=tk.W, padx=20)
        tk.Entry(self, textvariable=self.new_race, width=10).grid(row=row_idx, column=1, columnspan=2, padx=150)

        tk.Label(self, text='Input height (cm):').grid(row=0, column=2, sticky=tk.W)
        tk.Entry(self, textvariable=self.height, width=10).grid(row=1, column=2, sticky=tk.W, padx=15)
        
        tk.Button(self, text='Estimate', command=self.calculate).grid(row=row_idx+1, pady=10, sticky=tk.W, padx=15)
        tk.Button(self, text='Record Data', command=self.write_to_csv).grid(row=row_idx+1, column=1, columnspan=2, pady=10, sticky=tk.W, padx=15)
        ttk.Checkbutton(self, text='Record Estimations', variable=self.check, onvalue=1, offvalue=0).grid(row=row_idx+1, column=1, columnspan=2, pady=10)
        # set record estimations to be 'on' by default:
        # self.check.set('1')

        tk.Label(self, text="Result: ").grid(row=row_idx+2, sticky=tk.W, padx=20)
        self.result = tk.Label(self, text="")
        self.result.grid(row=row_idx+3, columnspan=3, sticky=tk.W, padx=20)

    def show_about(self):
        text = '''
        GUI written in Python that estimates positions of T12 and S1 relative to C7.
        Code written by Francis Yamashita.
        Source code: https://github.com/fyamash/Vertebrae_Estimation.git
        Papers Used to estimate vertebrae positions: 
            1. Frostell Arvid , Hakim Ramil , Thelin Eric Peter , Mattsson Per , Svensson Mikael 
               A Review of the Segmental Diameter of the Healthy Human Spinal Cord
               Frontiers in Neurology
               https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2016.00238/full
            2. Milani, Chantal & Panattoni, G.L.. (2013). 
                Estimation of stature from the vertebral column in physical and forensic anthropology. 
            Journal of Biological Research
            https://www.researchgate.net/publication/276226479_Estimation_of_stature_from_the_vertebra
            l_column_in_physical_and_forensic_anthropology 
        '''
        window = tk.Toplevel(self)
        window.title('About')
        window.geometry('550x300')
        label = tk.Label(window, text=text, justify="left")
        label.pack()
        close_button = tk.Button(window, text="Close", command=window.destroy)
        close_button.pack(pady=10)

    def show_exe(self):
        text = '''
        To export the GUI as an .exe file: 
        1. Install pyinstaller with: pip install pyinstaller
        2. Run command: pyinstaller --onefile vertebrae_estimate.py
        '''
        messagebox.showinfo("EXE", text)

    def valid_input(self):
        if self.gender.get() == '' or self.race.get() == '':
            self.result.config(text="Please select a gender and race.")
            return False
        elif self.height.get() == '':
            self.result.configure(text='')
            self.result.config(text="Please input the height.")
            return False
        else:
            return True

    def calculate(self):
        self.result.configure(text='')
        c7_t12 = 0.5035
        c7_s1 = 0.827
        if not self.valid_input():
            return
        gender = self.gender.get()
        race = self.race.get()
        height = self.height.get()
        try:
            height = float(height)
        except:
            self.result.config(text="Please input the height in cm.")
            return
        match race:
            case 'White':
                # White Americans
                if gender == 'M':
                    cl = (height - 47.26)/2.07
                else:
                    cl = (height - 29.74)/2.33
            case 'Black':
                # Black Americans
                if gender == 'M':
                    cl = (height - 29.4)/2.42
                else:
                    cl = (height - 70.34)/1.66
            case 'South Indian':
                # South Indian
                if gender == 'M':
                    cl = (height - 60.7)/1.88
                else:
                    cl = (height - 55.36)/1.9
            case 'New':
                self.result.config(text="Unable to estimate on new race.")
                return

        self.t12_est = round(c7_t12*cl, 2)
        self.s1_est = round(c7_s1*cl, 2)
        self.result.config(text="Distance from C7 to T12: {:.2f}cm\nDistance from C7 to S1: {:.2f}cm".format(self.t12_est, self.s1_est))

    def write_to_csv(self):
        if not self.valid_input():
            return
        elif self.race.get() == 'New' and self.new_race.get() == '':
            self.result.config(text="Please input the new race to record to file.")
            return
        try:
            filename = askopenfilename()
            with open(filename, "a", newline='') as file:  # Open file in append mode
                writer = csv.writer(file)
                if self.check.get():
                    self.calculate()
                    data = [self.gender.get(), self.race.get(), self.height.get(), self.t12_est, self.s1_est]
                else:
                    data = [self.gender.get(), self.race.get(), self.height.get()]
                writer.writerow(data)
            self.result.config(text=f"{data} has been recorded in {filename}")
        except Exception as e:
            self.result.config(text=f"Export error: {str(e)}")

if __name__=='__main__':
    root = Root()
    root.mainloop()
