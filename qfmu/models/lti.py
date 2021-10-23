import numpy as np
from qfmu.utils import str_to_1d_array, str_to_2d_array

class TransferFunction:
    pass

class StateSpace:
    '''
    State Space Models

    A, B, C,D should be 2d numpy arrays or strings "1,2,3;4,5,6"
    '''
    def __init__(self, A=None, B=None, C=None, D=None, x0=None, u0=None) -> None:
        
        if all(m is None for m in [A, B, C, D]):
            raise ValueError("A, B, C, D cannot be all empty")
        
        if isinstance(A, str):
            A = str_to_2d_array(A)
        if isinstance(B, str):
            B = str_to_2d_array(B)
        if isinstance(C, str):
            C = str_to_2d_array(C)
        if isinstance(D, str):
            D = str_to_2d_array(D)
        if isinstance(x0, str):
            x0 = str_to_1d_array(x0)
        if isinstance(u0, str):
            u0 = str_to_1d_array(u0)

        self.A = None if A is None else np.array(A, dtype=float)
        self.B = None if B is None else np.array(B, dtype=float)
        self.C = None if C is None else np.array(C, dtype=float)
        self.D = None if D is None else np.array(D, dtype=float)
        self.x0 = None if x0 is None else np.array(x0, dtype=float)
        self.u0 = None if u0 is None else np.array(u0, dtype=float)
        
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

        if self.x0 is None and self.nx > 0:
            self.x0 = np.zeros(self.nx, dtype=float)
        if self.x0 is not None:
            if self.nx != self.x0.size:
                raise ValueError("size mismatch. len(x0) != number of states")
        
        if self.u0 is None and self.nu > 0:
            self.u0 = np.zeros(self.nu, dtype=float)
        if self.u0 is not None:
            if self.nu != self.u0.size:
                raise ValueError("size mismatch. len(u0) != number of inputs")
        