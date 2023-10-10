import logging
import math
from typing import Optional

import numpy as np
from scipy import signal

from qfmu.model.lti import LTI


class PID(LTI):
    def __init__(
        self,
        kp: float = 0.0,
        ki: float = 0.0,
        kd: float = 0.0,
        T: float = 0.0,
        x0: Optional[float] = None,
        u0: Optional[float] = None,
    ) -> None:
        has_P = not math.isclose(kp, 0.0)
        has_I = not math.isclose(ki, 0.0)
        has_D = not math.isclose(kd, 0.0)

        if math.isclose(T, 0.0) and has_D:
            raise ValueError("T must be greater than zero")

        P = signal.TransferFunction([kp], [1.0]) if has_P else None  # noqa: E741
        I = signal.TransferFunction([ki], [1.0, 0.0]) if has_I else None  # noqa: E741
        D = (  # noqa: E741
            signal.TransferFunction([kd, 0.0], [T, 1.0]) if has_D else None
        )

        if sum([has_P, has_I, has_D]) == 0:
            raise ValueError("At least one of kp, ki, kd must be non-zero")
        elif sum([has_P, has_I, has_D]) == 1:
            self.m = (
                P.to_ss()
                if P is not None
                else I.to_ss()
                if I is not None
                else D.to_ss()
            )
        elif sum([has_P, has_I, has_D]) == 2:
            if has_P and has_I:
                self.m = signal.TransferFunction([kp, ki], [1.0, 0.0]).to_ss()
            elif has_P and has_D:
                self.m = signal.TransferFunction([kp * T + kd, kd], [T, 1.0]).to_ss()
            else:
                self.m = I.to_ss() + D.to_ss()
        else:
            self.m = signal.TransferFunction([kp, ki], [1.0, 0.0]).to_ss() + D.to_ss()

        super().__init__(
            self.m.A.shape[0],
            1,
            1,
            np.array([x0]) if x0 is not None else None,
            np.array([u0]) if u0 is not None else None,
        )

        logging.info(f"P = {P}")
        logging.info(f"I = {I}")
        logging.info(f"D = {D}")

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
