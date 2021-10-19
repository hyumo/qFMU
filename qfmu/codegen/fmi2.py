import os
from dataclasses import dataclass, field
from typing import List
import uuid
import datetime
from jinja2.environment import Template

from ..models.lti import StateSpace, TransferFunction

#DIR = os.path.dirname(os.path.abspath(__file__))
#TEMPLATE_DIR = os.path.join(DIR, "templates", "fmi2")
#FMI2ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape())

class Fmi2:
    def __init__(self, identifier: str = "fmi2model", version: str = "v0.0") -> None:
        self.identifier = identifier
        self.version = version
        self.guid = str(uuid.uuid1())
        self.datetime = str(datetime.datetime.now())


class Lti(Fmi2):

    @dataclass
    class VR0:
        x: int = 0
        der: int = 0
        u: int = 0
        y: int = 0
        x0: int = 0
        u0: int = 0

    @dataclass
    class VRs:
        x: List[str] = field(default_factory=lambda: [])
        der: List[str] = field(default_factory=lambda: [])
        u: List[str] = field(default_factory=lambda: [])
        y: List[str] = field(default_factory=lambda: [])
        x0: List[str] = field(default_factory=lambda: [])
        u0: List[str] = field(default_factory=lambda: [])

    def __init__(self, model, identifier: str = "fmi2model", version: str = "v0.0") -> None:
        super().__init__(identifier=identifier, version=version)

        # Convert all model forms to state space
        if isinstance(model, TransferFunction):
            model = model.toStateSpace()

        # Make sure model is always in state-space form
        if isinstance(model, StateSpace) == False:
            raise ValueError("model is not in state space form")

        self._load_ss(model)

    def _load_ss(self, model: StateSpace):
        self.nx = model.nx
        self.nu = model.nu
        self.ny = model.ny
        self.nr = 3*self.nx + 2*self.nu + self.ny

        self.A = [",".join(list(map(str, row))) for row in model.A.tolist()] if model.A is not None else None
        self.B = [",".join(list(map(str, row))) for row in model.B.tolist()] if model.B is not None else None
        self.C = [",".join(list(map(str, row))) for row in model.C.tolist()] if model.C is not None else None
        self.D = [",".join(list(map(str, row))) for row in model.D.tolist()] if model.D is not None else None
        self.x0 = list(map(str, model.x0)) if model.x0 is not None else None
        self.u0 = list(map(str, model.u0)) if model.u0 is not None else None

        self.vr0 = Lti.VR0(
            x=0,
            der=self.nx,
            u=2*self.nx,
            y=2*self.nx+self.nu,
            x0=2*self.nx+self.nu+self.ny,
            u0=3*self.nx+self.nu+self.ny)

        self.vrs = Lti.VRs(
            x=list(map(str, range(self.vr0.x, self.vr0.der))),
            der=list(map(str, range(self.vr0.der, self.vr0.u))),
            u=list(map(str, range(self.vr0.u, self.vr0.y))),
            y=list(map(str, range(self.vr0.y, self.vr0.x0))),
            x0=list(map(str, range(self.vr0.x0, self.vr0.u0))),
            u0=list(map(str, range(self.vr0.u0, self.vr0.u0 + self.nu))),
        )

    def render_c(self):
        from .fmi2tmpl import lti_c_tmpl
        tmpl = Template(lti_c_tmpl)
        return tmpl.render(self.__dict__)

    def render_xml(self):
        from .fmi2tmpl import lti_md_xml_tmpl
        tmpl = Template(lti_md_xml_tmpl)
        return tmpl.render(self.__dict__)

    def render_doc(self):
        return r"## qFMU model"

def generate_code(model, fmudir: str = None):
    """Create an unzipped fmuoutput folder structure that represents an fmu

    Args:
        model ([type]): [description]
        fmudir (str, optional): [description]. Defaults to None.

    Raises:
        ValueError: [description]
    """
    if not os.path.isdir(fmudir):
        raise ValueError("Target path does not exist. {}".format(fmudir))

    root = fmudir
    binaries = os.mkdir(os.path.join(fmudir, "binaries"))
    sources = os.mkdir(os.path.join(fmudir, "sources"))
    documentation = os.mkdir(os.path.join(fmudir, "documentation"))

    with open(os.path.join(sources, "fmi2model.c"), "w") as file:
        file.write(model.render_c())
    with open(os.path.join(root, "modelDescripion.xml"), "w") as file:
        file.write(model.render_xml())
    with open(os.path.join(documentation, "README.md"), "w") as file:
        file.write(model.render_doc())
    
    from .fmi2src import fmi2Template_h, fmi2Template_c, fmi2TypesPlatform_h, fmi2FunctionTypes_h, fmi2Functions_h
    with open(os.path.join(sources, "fmi2Template.h"), "w") as file:
        file.write(fmi2Template_h)
    with open(os.path.join(sources, "fmi2Template.c"), "w") as file:
        file.write(fmi2Template_c)
    with open(os.path.join(sources, "fmi2Functions.h"), "w") as file:
        file.write(fmi2Functions_h)
    with open(os.path.join(sources, "fmi2FunctionTypes.h"), "w") as file:
        file.write(fmi2FunctionTypes_h)
    with open(os.path.join(sources, "fmi2TypesPlatform.h"), "w") as file:
        file.write(fmi2TypesPlatform_h)

def compile_dll(fmudir: str = None, compiler=None, target_platform=None):
    if not os.path.isdir(os.path.join(fmudir, "sources")):
        raise ValueError("Sources path does not exist. Please generate source code.")
        
    




if __name__ == "__main__":
    from .fmi2src import fmi2Template_h, fmi2Template_c, fmi2Functions_h, fmi2FunctionTypes_h, fmi2TypesPlatform_h

    s = Lti(StateSpace(A="1,2;3,4"), identifier="fooooooo")
    with open("/home/hyu/sw/qFMU/tmp/fmi2model.c", "w") as file:
        file.write(s.render_c())
    with open("/home/hyu/sw/qFMU/tmp/modelDescripion.xml", "w") as file:
        file.write(s.render_xml())

    with open("/home/hyu/sw/qFMU/tmp/fmi2Template.h", "w") as file:
        file.write(fmi2Template_h)
    with open("/home/hyu/sw/qFMU/tmp/fmi2Template.c", "w") as file:
        file.write(fmi2Template_c)
    with open("/home/hyu/sw/qFMU/tmp/fmi2Functions.h", "w") as file:
        file.write(fmi2Functions_h)
    with open("/home/hyu/sw/qFMU/tmp/fmi2FunctionTypes.h", "w") as file:
        file.write(fmi2FunctionTypes_h)
    with open("/home/hyu/sw/qFMU/tmp/fmi2TypesPlatform.h", "w") as file:
        file.write(fmi2TypesPlatform_h)
