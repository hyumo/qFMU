from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import numpy as np
import numpy.typing as npt
from annotated_types import Ge
from typing_extensions import Annotated


@dataclass
class VR0:
    x: int
    der: int
    x0: int
    u: int
    u0: int
    y: int


@dataclass
class VR:
    x: np.ndarray
    der: np.ndarray
    x0: np.ndarray
    u: np.ndarray
    u0: np.ndarray
    y: np.ndarray


class LTI(ABC):
    def __init__(
        self,
        nx: Annotated[int, Ge(0)],
        nu: Annotated[int, Ge(0)],
        ny: Annotated[int, Ge(0)],
        x0: Optional[npt.NDArray[np.float64]] = None,
        u0: Optional[npt.NDArray[np.float64]] = None,
    ) -> None:
        self._nx = nx
        self._nu = nu
        self._ny = ny

        self._x0 = np.zeros(nx, dtype=float) if x0 is None else x0
        self._u0 = np.zeros(nu, dtype=float) if u0 is None else u0

        if self._x0.shape[0] != nx:
            raise ValueError("x0 has invalid shape")

        if self._u0.shape[0] != nu:
            raise ValueError("u0 has invalid shape")

    @property
    def nx(self) -> int:
        return self._nx

    @property
    def nu(self) -> int:
        return self._nu

    @property
    def ny(self) -> int:
        return self._ny

    @property
    def nr(self) -> int:
        return 3 * self.nx + 2 * self.nu + self.ny

    @property
    def vr0(self) -> VR0:
        return VR0(
            x=0,
            der=self.nx,
            x0=self.nx + self.nx,
            u=self.nx + self.nx + self.nx,
            u0=self.nx + self.nx + self.nx + self.nu,
            y=self.nx + self.nx + self.nx + self.nu + self.nu,
        )

    @property
    def vr(self) -> VR:
        return VR(
            x=np.array(range(self.vr0.x, self.vr0.der), dtype=int),
            der=np.array(range(self.vr0.der, self.vr0.x0), dtype=int),
            x0=np.array(range(self.vr0.x0, self.vr0.u), dtype=int),
            u=np.array(range(self.vr0.u, self.vr0.u0), dtype=int),
            u0=np.array(range(self.vr0.u0, self.vr0.y), dtype=int),
            y=np.array(range(self.vr0.y, self.nr), dtype=int),
        )

    def has_states(self) -> bool:
        return self.nx > 0

    def has_inputs(self) -> bool:
        return self.nu > 0

    def has_outputs(self) -> bool:
        return self.ny > 0

    @property
    def x0(self) -> np.ndarray:
        return self._x0

    @property
    def u0(self) -> np.ndarray:
        return self._u0

    @abstractmethod
    def A(self) -> np.ndarray:
        raise NotImplementedError("A not implemented")

    @abstractmethod
    def B(self) -> np.ndarray:
        raise NotImplementedError("B not implemented")

    @abstractmethod
    def C(self) -> np.ndarray:
        raise NotImplementedError("C not implemented")

    @abstractmethod
    def D(self) -> np.ndarray:
        raise NotImplementedError("D not implemented")
