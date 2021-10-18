import numpy as np
from numpy.core.fromnumeric import shape
from .utils import convert_from_string

class StateSpace:
    '''
    State Space Models

    A, B, C,D should be 2d numpy arrays or strings "1,2,3;4,5,6"
    '''
    def __init__(self, A=None, B=None, C=None, D=None) -> None:
        
        if all(m is None for m in [A, B, C, D]):
            raise ValueError("A, B, C, D cannot be all empty")
        
        if isinstance(A, str):
            A = convert_from_string(A)
        if isinstance(B, str):
            B = convert_from_string(B)
        if isinstance(C, str):
            C = convert_from_string(C)
        if isinstance(D, str):
            D = convert_from_string(D)

        self.A = None if A is None else np.array(A, dtype=float)
        self.B = None if B is None else np.array(B, dtype=float)
        self.C = None if C is None else np.array(C, dtype=float)
        self.D = None if D is None else np.array(D, dtype=float)

        # Create A if it is None
        if self.A is None:
            self.A = np.zeros((0, 0))

        if self.A.ndim != 2:
            raise ValueError("size mismatch. A must be 2D")
        if self.A.shape[0] != self.A.shape[1]:
            raise ValueError("size mismatch. A must be square")

        self.nx = self.A.shape[0]

        # Create C if it is None
        if self.C is None and self.D is None:
            self.C = np.identity(self.nx)
        elif self.C is None:
            self.C = np.zeros((self.D.shape[0], self.nx))
        
        if self.C.ndim != 2:
            raise ValueError("size mismatch. C must be 2D")
        if self.C.shape[1] != self.nx:
            raise ValueError("size mismatch. C must have the same number of columns as A")

        self.ny=self.C.shape[0]

        # Create B and D if any of them is None
        if self.B is None and self.D is None is None:
            self.B=np.zeros((self.nx, 0))
            self.D=np.zeros((self.ny, 0))
        elif self.B is None:
            self.B=np.zeros((self.nx, self.D.shape[1]))
        elif self.D is None:
            self.D=np.zeros((self.ny, self.B.shape[1]))

        if self.B.ndim != 2:
            raise ValueError("size mismatch. B must be 2D")
        if self.D.ndim != 2:
            raise ValueError("size mismatch. B must be 2D")

        if self.nx != self.B.shape[0]:
            raise ValueError("size mismatch. A must have the same number of rows as B")
        if self.C.shape[0] != self.D.shape[0]:
            raise ValueError("size mismatch. C must have the same number of rows as D")
        if self.B.shape[1] != self.D.shape[1]:
            raise ValueError("size mismatch. B must have the same number of columns as D")
        
        self.nu = self.B.shape[1]
                
    def toFMI2(self, x0, u0, identifier: str="foo", version: str="v0.1"):
        print("not implemented")
