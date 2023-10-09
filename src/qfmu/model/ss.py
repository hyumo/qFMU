import logging
from typing import Optional

import numpy as np
import numpy.typing as npt
from scipy import signal

from qfmu.model.lti import LTI


class StateSpace(LTI):
    """Continuous-time state space system"""

    def __init__(
        self,
        A: Optional[npt.NDArray[np.float64]] = None,
        B: Optional[npt.NDArray[np.float64]] = None,
        C: Optional[npt.NDArray[np.float64]] = None,
        D: Optional[npt.NDArray[np.float64]] = None,
        x0: Optional[npt.NDArray[np.float64]] = None,
        u0: Optional[npt.NDArray[np.float64]] = None,
    ) -> None:
        """
        State space system constructor
        """
        if all([A is None, B is None, C is None, D is None]):
            raise ValueError("A, B, C, D matrices cannot all be None")
        elif all([A is not None, C is None, B is None, D is None]):
            C = np.eye(A.shape[0])
            B = np.zeros((A.shape[0], 0))
        elif all([B is not None, A is None, C is None, D is None]):
            A = np.zeros((B.shape[0], B.shape[0]))
            C = np.eye(A.shape[0])
        elif all([C is not None, A is None, B is None, D is None]):
            raise ValueError("C matrix provided without A matrix or D matrix")
        elif all([D is not None, A is None, B is None, C is None]):
            A = np.zeros((0, 0))
            C = np.zeros((D.shape[0], 0))
            B = np.zeros((0, D.shape[1]))
        elif all([A is not None, B is not None, C is None, D is None]):
            C = np.eye(A.shape[0])
        elif all([A is not None, C is not None, B is None, D is None]):
            B = np.zeros((A.shape[0], 0))

        self.m = signal.StateSpace(A, B, C, D)
        nx, nu, ny = self.m.A.shape[0], self.m.inputs, self.m.outputs
        super().__init__(nx=nx, nu=nu, ny=ny, x0=x0, u0=u0)

        logging.info(f"A[{self.A.shape[0]}, {self.A.shape[1]}] = {self.A.tolist()}")
        logging.info(f"B[{self.B.shape[0]}, {self.B.shape[1]}] = {self.B.tolist()}")
        logging.info(f"C[{self.C.shape[0]}, {self.C.shape[1]}] = {self.C.tolist()}")
        logging.info(f"D[{self.D.shape[0]}, {self.D.shape[1]}] = {self.D.tolist()}")

    @property
    def A(self) -> np.ndarray:
        return self.m.A

    @property
    def B(self) -> np.ndarray:
        return self.m.B

    @property
    def C(self) -> np.ndarray:
        return self.m.C

    @property
    def D(self) -> np.ndarray:
        return self.m.D
