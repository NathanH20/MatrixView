from fractions import Fraction

class Matrix:
    def __init__(self, n:int, m:int, mode:str="null", data:dict[tuple, int]=None):
        self.n: int = n
        self.m: int = m

        self.grid: dict[tuple, int] = {}

        if data: # if data was passed as arg
            for (i, j), num in data.items():
                self[i, j] = num
        else: # else fill with given mode
            for i in range(1, n+1):
                for j in range(1, m+1):
                    if n != m: # if not square
                        self[i, j] = 0
                        continue

                    match mode:
                        case "null":
                            self[i, j] = 0
                        
                        case "identity":
                            if i == j: self[i, j] = 1
                            else: self[i, j] = 0

                        case "upper":
                            if i <= j: self[i, j] = 1
                            else: self[i, j] = 0

                        case "lower":
                            if i >= j: self[i, j] = 1
                            else: self[i, j] = 0
            

    def __setitem__(self, pos, value):
        i, j = pos
        if i > self.n or j > self.m:
            raise IndexError("Index out of range")
        self.grid[(i, j)] = value

    def __getitem__(self, key):
        i, j = key
        return self.grid[(i, j)]
    
    def __add__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ValueError("Matrices need to be of the same size")
        
        new_data: dict[tuple, int] = {}
        for i in range(1, self.n+1):
            for j in range(1, self.m+1):
                new_data[(i, j)] = self[i, j] + other[i, j]
        return Matrix(self.n, self.m, data=new_data)
    
    def __sub__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ValueError("Matrices need to be of the same size")
        
        new_data: list[int] = []
        for i in range(1, self.n+1):
            for j in range(1, self.m+1):
                new_data.append(self[i, j] - other[i, j])
        return Matrix(self.n, self.m, data=new_data)
    
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_data: dict[tuple, int] = {}
            for i in range(1, self.n+1):
                for j in range(1, self.m+1):
                    new_data[(i, j)] = self[i, j] * other
            return Matrix(self.n, self.m, data=new_data)
        
        if isinstance(other, Matrix):
            return Matrix(1, 1)

    def __rmul__(self, other):
        return self.__mul__(other)

    def resize(self, n: int, m: int):
        """resizes the matrix to a new nxm, cutting waste and filling expands with 0s"""
        new_grid: dict = {}
        for i in range(1, n+1):
            for j in range(1, m+1):
                data: int = 0
                if self.get(i, j) != None: data = self[i, j]
                new_grid[(i, j)] = data

        #update n, m
        self.n, self.m = n, m

        #assign new grid to grid
        self.grid = new_grid

    def get(self, i: int, j: int) -> int:
        """returns given value if exists, None if not"""
        if (i, j) in self.grid.keys():
            return self[i, j]
        else: return None

    def replace(self, data: dict[tuple, int]):
        """replaces value(s) at given position(s) if exists"""
        for (i, j), num in data.items():
            if self.get(i, j) != None: self[i, j] = num
    
    def show(self):
        """prints the matrix"""
        m_str: str = ""
        for (i, j), num in self.grid.items():
            if(isinstance(num, int)): m_str += f"{num} "
            else: m_str += f"{Fraction(num).limit_denominator()} "
            if j % self.m == 0 and i + j != self.m + self.n:
                m_str += "\n"
        print(m_str)

    def get_determinant(self, absi: int = 1, absj: int = 1) -> int:
        """returns the determinant of the matrix of order n"""
        if self.n != self.m: return 0

        match self.n:
            case 1:
                #if matrix is of order 1

                return self[1, 1] * pow(-1, absi + absj)
            case 2:
                #if matrix is of order 2

                s1: int = self[1, 1] * self[2, 2]
                s2: int = self[1, 2] * self[2, 1]
                det: int = s1 - s2
                return det * pow(-1, absi + absj)
            case _:
                #if matrix is of order >= 3

                #final determinant
                det: int = 0

                for i in range(1, self.n + 1):
                    matrix = self.get_sub_matrix(i, 1)
                    d: int = matrix.get_determinant()

                    del matrix

                    partial_det: int = self[i, 1] * pow(-1, i + 1) * d
                    det += partial_det

                #return final det
                return det
            
    def get_sub_matrix(self, n: int, m: int):

            #sub data to pass to sub matrix
            sub_data: dict[tuple, int] = {}
            data: list = []

            #for each num that is not on the row or column or current num
            for (i, j), num in self.grid.items():
                if i == n or j == m: continue

                data.append(num)
                
            ii: int = 1
            jj: int = 1
            for d in data:
                
                if jj == self.m:
                    ii += 1
                    jj = 1

                sub_data[ii, jj] = d

                jj += 1

            #make new matrix with sub data to run again for determinant
            matrix = Matrix(self.n - 1, self.m - 1, data=sub_data)
            
            return matrix


        
    def get_type(self) -> list[str]:
        """returns the matrix's mode"""
        types: list[str] = [
            "Null",
            "Identity",
            "Upper",
            "Lower",
            "Row",
            "Column",
            "Square",
            #"Scalar",
            "Diagonal",
            #"Symetric",
            #"Antisymetric"
        ]

        for (i, j), num in self.grid.items():
            if num != 0 and "Null" in types: types.remove("Null")

            if (i == j and num != 1) or (i != j and num != 0):
                if "Identity" in types: types.remove("Identity")

            if i > j and num != 0 and "Upper" in types: types.remove("Upper")

            if i < j and num != 0 and "Lower" in types: types.remove("Lower")

        if self.n != self.m: 
            if "Square" in types: types.remove("Square")
            if "Identity" in types: types.remove("Identity")
            if "Upper" in types: types.remove("Upper")
            if "Lower" in types: types.remove("Lower")


        if self.n >= self.m: types.remove("Row")
        if self.n <= self.m: types.remove("Column")

        if "Lower" not in types or "Upper" not in types:
            types.remove("Diagonal")

        if len(types) == 0: types.append("Any")
        print(types)
        return types
    
    def transpose(self):
        """transposes the matrix, such that: (i, j) -> (j, i)"""
        transposed: Matrix = Matrix(self.m, self.n)

        for (i, j), num in self.grid.items():
            transposed[j, i] = num

        self.grid = transposed.grid
        self.n = transposed.n
        self.m = transposed.m

    def inverse(self):
        """inverse the matrix"""

        determinant: int = self.get_determinant()
        if(determinant == 0): return

        inverse: Matrix = Matrix(self.n, self.m)
        
        # get the cofactor
        for i in range(1, inverse.n + 1):
            for j in range(1, inverse.m + 1):
                inverse[i, j] = (self.get_sub_matrix(i, j)).get_determinant(i, j)
        
        # get the adjoint
        inverse.transpose()

        # get the inverse
        inverse *= 1/determinant

        # modify self for inverse
        self.grid = inverse.grid