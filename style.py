import ttkbootstrap as ttk

class MainStyle():
    def __init__(self):
        self.style: ttk.Style = ttk.Style()

        # Odd Info Frame
        self.style.configure('Odd_Info.TFrame', background="#222222")
        self.style.configure('Odd_Info.TLabel', background="#222222")

        # Even Info Frame
        self.style.configure('Even_Info.TFrame', background="#262626")
        self.style.configure('Even_Info.TLabel', background="#262626")

        # Tool Bar Frame
        self.style.configure('Toolbar.TFrame', background="#262626")
        self.style.configure('Toolbar.TLabel', background="#262626")
        self.style.configure('Toolbar.TButton', font=("calibri", 24))

        # Action Frame
        self.style.configure('Action.TButton', font=("calibri", 24))