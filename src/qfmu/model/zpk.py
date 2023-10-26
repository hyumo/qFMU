import logging
from typing import Optional

import numpy as np
import numpy.typing as npt
from scipy import signal

from qfmu.model.lti import LTI


class ZerosPolesGain(LTI):
    def __init__(
        self,
        z: npt.NDArray[np.float64],
        p: npt.NDArray[np.float64],
        k: float,
        x0: Optional[npt.NDArray[np.float64]] = None,
        u0: Optional[float] = None,
    ):
        self._A, self._B, self._C, self._D = signal.zpk2ss(z=z, p=p, k=k)
        super().__init__(
            nx=self._A.shape[0],
            nu=1,
            ny=1,
            x0=np.array(x0) if x0 is not None else np.zeros(self._A.shape[0]),
            u0=np.array([u0]) if u0 is not None else np.zeros(1),
        )

        logging.info(f"{signal.TransferFunction(*signal.zpk2tf(z, p, k))}")

    @property
    def A(self) -> np.ndarray:
        return self._A

    @property
    def B(self) -> np.ndarray:
        return self._B

    @property
    def C(self) -> np.ndarray:
        return self._C

    @property
    def D(self) -> np.ndarray:
        return self._D
