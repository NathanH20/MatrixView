import ttkbootstrap as ttk
from Matrix import Matrix
from style import MainStyle
from fractions import Fraction

class App:
    def __init__(self, window: ttk.Window):
        self.window = window

        self.matrix: Matrix = Matrix(3, 3, mode='identity')
        self.determinant: ttk.IntVar = ttk.IntVar(value=self.matrix.get_determinant())
        self.type: ttk.StringVar = ttk.StringVar(value=self.matrix.get_type()[0])
        self.cells: dict[tuple, Cell] = {}
        self.infos: list[Info] = []
        self.main_style = MainStyle()

        #window configuring
        self.configure_window()

        #tool bar frame
        self.configure_toolbar_frame()
        self.layout_toolbar_frame()

        #info frame
        self.configure_info_frame()
        self.layout_info_frame()

        #action frame
        self.configure_action_frame()
        self.layout_action_frame()

        #matrix frame
        self.update_matrix()
        self.refresh_matrix()

        def resize(n, m):

            if not 1 <= n <= 10: return
            elif not 1 <= m <= 10: return

            self.matrix.resize(n, m)

            self.update_matrix()
            self.refresh_matrix()

        window.bind("<Up>", lambda _: resize(self.matrix.n-1, self.matrix.m))
        window.bind("<Down>", lambda _: resize(self.matrix.n+1, self.matrix.m))
        window.bind("<Left>", lambda _: resize(self.matrix.n, self.matrix.m-1))
        window.bind("<Right>", lambda _: resize(self.matrix.n, self.matrix.m+1))

    def configure_window(self):
        self.window.title("Matrix View")

        width, height = 800, 800

        x_offset = int((self.window.winfo_screenwidth() / 2) - (width / 2))
        y_offset = int((self.window.winfo_screenheight() / 2) - (height / 2))

        self.window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
        self.window.resizable(False, False)



    # TOOL BAR FRAME CONFIG
    def configure_toolbar_frame(self):
        self.toolbar_FR = ttk.Frame(
            self.window,
            borderwidth=10
        )

        self.sub_toolbar_FR = ttk.Frame(
            self.toolbar_FR,
            style="Toolbar.TFrame"
        )

        self.order_LB = ttk.Label(
            self.sub_toolbar_FR,
            text=f"{self.matrix.n}x{self.matrix.m}",
            font="calibri 30 bold",
            anchor="e",
            style="Toolbar.TLabel"
        )

        self.calculate_BT = ttk.Button(
            self.sub_toolbar_FR,
            text="Calculate",
            style="Toolbar.TButton",
            command=self.calculate
        )

    # TOOL BAR FRAME LAYOUT
    def layout_toolbar_frame(self):
        self.toolbar_FR.place(
            relx=0,
            rely=0.6,
            relwidth=0.6,
            relheight=0.1
        )

        self.sub_toolbar_FR.place(
            relwidth=1,
            relheight=1
        )

        self.order_LB.place(
            relx=0.98,
            rely=0,
            relwidth=0.3,
            relheight=1,
            anchor="ne",
        )

        self.calculate_BT.place(
            relheight=1,
            relwidth=0.4,
            anchor="nw"
        )



    # INFO FRAME CONFIG
    def configure_info_frame(self):
        self.info_FR = ttk.Frame(
            self.window,
            borderwidth=10
        )

        #infos to display in info frame
        infos: dict = {
            "determinant": self.determinant,
            "type": self.type
        }

        #make info sub frames for all info and add to infos list
        for i, (name, value) in enumerate(infos.items()):
            if i % 2 == 0: style_name: str = "Even_Info"
            else: style_name: str = "Odd_Info"

            info = Info(self.info_FR, name, value, style_name)
            self.infos.append(info)

    # INFO FRAME LAYOUT
    def layout_info_frame(self):
        self.info_FR.place(
            relx=1,
            rely=0,
            relwidth=0.4,
            relheight=1,
            anchor="ne"
        )

        #display all infos in info frame
        for i, info in enumerate(self.infos):
            info.frame.place(
                rely=(i*0.08),
                relwidth=1,
                relheight=0.08
            )

    # ACTION FRAME CONFIG
    def configure_action_frame(self):
        self.action_FR = ttk.Frame(
            self.window,
            borderwidth=10
        )

        self.transpose_BT = ttk.Button(
            self.action_FR,
            text="Transpose",
            command=self.transpose,
            style="Action.TButton"
        )

        self.inverse_BT = ttk.Button(
            self.action_FR,
            text="Inverse",
            command=self.inverse,
            style="Action.TButton"
        )

    # ACTION FRAME LAYOUT
    def layout_action_frame(self):
        self.action_FR.place(
            rely=0.7,
            relwidth=0.6,
            relheight=0.3
        )

        self.transpose_BT.place(
            relwidth=0.4,
            relheight=0.28,
            rely=.4
        )

        self.inverse_BT.place(
            relwidth=0.4,
            relheight=0.28
        )

    def calculate(self):
        """calculate infos of the matrix"""
        #update matrix
        self.update_matrix()

        #set matrix determinant
        determinant: int = self.matrix.get_determinant()
        self.determinant.set(determinant)

        #set matrix mode
        modes: list[str] = self.matrix.get_type()
        self.type.set(modes[0])

    def transpose(self):
        """transposes the matrix"""
        #update matrix
        self.update_matrix()

        #transpose matrix
        self.matrix.transpose()

        #update matrix
        self.refresh_matrix()

    def inverse(self):
        """inverse the matrix"""

        self.update_matrix()

        self.matrix.inverse()

        self.refresh_matrix()
        
    def update_matrix(self):
        """updates the matrix's data"""
        data = {(i, j): cell.value.get() for (i, j), cell in self.cells.items()}
        self.matrix.replace(data=data)
        
    def refresh_matrix(self):
        """refresh the matrix grid to current data"""
        #destroy old frame
        try: self.matrix_frame.destroy()
        except: pass

        #make new frame
        self.matrix_frame = ttk.Frame(
            self.window,
            borderwidth=10
        )
        self.matrix_frame.place(
            relx=0,
            rely=0,
            relwidth=0.6,
            relheight=0.6
        )
        
        #clear grid
        for widget in self.matrix_frame.grid_slaves():
            widget.grid_remove()

        #set matrix rows and columns
        for i in range(self.matrix.n): self.matrix_frame.rowconfigure(i, weight=1)
        for j in range(self.matrix.m): self.matrix_frame.columnconfigure(j, weight=1)

        #clear previous cells
        self.cells.clear()

        #make all cells
        for i in range(1, self.matrix.n+1):
            for j in range(1, self.matrix.m+1):
                cell = Cell(self.matrix_frame, self.matrix[i, j], i, j, self.matrix.n, self.matrix.m)
                self.cells[(i, j)] = cell   

        self.order_LB.configure(text=f"{self.matrix.n}x{self.matrix.m}")



class Cell:
    """class of single matrix cell"""
    def __init__(self, master, num: int, i: int, j: int, n: int, m: int):
        self.value = ttk.DoubleVar(value=num)

        if isinstance(num, float):
            self.strvalue = ttk.StringVar(value=str(Fraction(num).limit_denominator()))
        else:
            self.strvalue = ttk.StringVar(value=str(num))

        #TEMP
        modif: int = max(n, m)
        font_size: int = 100 // (modif - (modif // 4))

        self.entry = ttk.Entry(
            master,
            textvariable=self.strvalue,
            justify="center",
            font=("calibri", font_size)
        )
        self.entry.grid(
            row=i-1,
            column=j-1,
            sticky="news"
        )

        def focus_in(_):
            if self.strvalue.get() != '0': return
            self.entry.delete(0, "end")

        def focus_out(_):
            if self.strvalue.get() != '': 
                try:
                    num: float = float(self.strvalue.get())
                    self.value.set(num)
                    return
                except:
                    pass

            self.strvalue.set('0')

        def next(_):
            focus_out(None)
            self.entry.tk_focusNext().focus()

        self.entry.bind("<FocusIn>", focus_in)
        self.entry.bind("<FocusOut>", focus_out)
        self.entry.bind("<Return>", next)



class Info:
    """class of single info bar"""
    def __init__(self, master, name: str, value: int, style_name: str):
        self.value: int = value

        # WIDGETS
        self.frame = ttk.Frame(
            master,
            style=f"{style_name}.TFrame"
        )
        self.name_label = ttk.Label(
            self.frame,
            text=f"{name.title()}:",
            font="calibri 16 bold",
            style=f"{style_name}.TLabel"
        )
        self.value_label = ttk.Label(
            self.frame,
            textvariable=value,
            anchor="e",
            font="calibri 16 bold",
            style=f"{style_name}.TLabel"
        )

        # LAYOUT
        self.name_label.place(
            relx=0.02,
            relwidth=0.5,
            relheight=1
        )
        self.value_label.place(
            relx=0.98,
            rely=0,
            relwidth=0.5,
            relheight=1,
            anchor="ne"
        )



if __name__ == "__main__":
    window = ttk.Window(themename="darkly")
    app = App(window)
    window.mainloop()