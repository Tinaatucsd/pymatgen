# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.
from __future__ import annotations

import os

from pymatgen.core.structure import Structure
from pymatgen.io.lammps.data import LammpsData
from pymatgen.io.lammps.generators import LammpsMinimization
from pymatgen.util.testing import PymatgenTest

test_dir = os.path.join(PymatgenTest.TEST_FILES_DIR, "lammps")


class LammpsMinimizationTest(PymatgenTest):
    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.join(test_dir, "lgps.in")
        cls.cif = os.path.join(test_dir, "lgps.cif")
        cls.structure = Structure.from_file(cls.cif)

    def test_get_input_set(self):
        lmp_min = LammpsMinimization(keep_stages=False).get_input_set(self.structure)
        assert list(lmp_min.data.as_dict().keys()) == list(LammpsData.from_structure(self.structure).as_dict().keys())
        assert (
            lmp_min.data.as_dict()["atoms"].values
            == LammpsData.from_structure(self.structure).as_dict()["atoms"].values
        ).all()
        assert lmp_min.inputfile.stages == [
            {
                "stage_name": "Stage 1",
                "commands": [
                    ("units", "metal"),
                    ("atom_style", "full"),
                    ("dimension", "3"),
                    ("boundary", "p p p"),
                    ("#", "2) System definition"),
                    ("read_data", "system.data"),
                    ("neigh_modify", "every 1 delay 5 check yes"),
                    ("#", "3) Simulation settings"),
                    ("Unspecified", "force field!"),
                    ("#", "4) Energy minimization"),
                    ("thermo", "5"),
                    ("thermo_style", "custom step lx ly lz press pxx pyy pzz pe"),
                    ("dump", "dmp all atom 5 run.dump"),
                    ("min_style", "cg"),
                    ("fix", "1 all box/relax iso 0.0 vmax 0.001"),
                    ("minimize", "1.0e-16 1.0e-16 5000 100000"),
                    ("#", "5) Write output data"),
                    ("write_data", "run.data"),
                    ("write_restart", "run.restart"),
                ],
            }
        ]

        lmp_min = LammpsMinimization(units="atomic", dimension=2, keep_stages=False).get_input_set(self.structure)
        assert list(lmp_min.data.as_dict().keys()) == list(LammpsData.from_structure(self.structure).as_dict().keys())
        assert (
            lmp_min.data.as_dict()["atoms"].values
            == LammpsData.from_structure(self.structure).as_dict()["atoms"].values
        ).all()
        assert lmp_min.inputfile.stages == [
            {
                "stage_name": "Stage 1",
                "commands": [
                    ("units", "atomic"),
                    ("atom_style", "full"),
                    ("dimension", "2"),
                    ("boundary", "p p p"),
                    ("#", "2) System definition"),
                    ("read_data", "system.data"),
                    ("neigh_modify", "every 1 delay 5 check yes"),
                    ("#", "3) Simulation settings"),
                    ("Unspecified", "force field!"),
                    ("#", "4) Energy minimization"),
                    ("thermo", "5"),
                    ("thermo_style", "custom step lx ly lz press pxx pyy pzz pe"),
                    ("dump", "dmp all atom 5 run.dump"),
                    ("min_style", "cg"),
                    ("fix", "1 all box/relax iso 0.0 vmax 0.001"),
                    ("minimize", "1.0e-16 1.0e-16 5000 100000"),
                    ("#", "5) Write output data"),
                    ("write_data", "run.data"),
                    ("write_restart", "run.restart"),
                ],
            }
        ]

        lmp_min = LammpsMinimization(keep_stages=True).get_input_set(self.structure)
        assert lmp_min.inputfile.stages == [
            {
                "stage_name": "1) Initialization",
                "commands": [("units", "metal"), ("atom_style", "full"), ("dimension", "3"), ("boundary", "p p p")],
            },
            {
                "stage_name": "2) System definition",
                "commands": [("read_data", "system.data"), ("neigh_modify", "every 1 delay 5 check yes")],
            },
            {"stage_name": "3) Simulation settings", "commands": [("Unspecified", "force field!")]},
            {
                "stage_name": "4) Energy minimization",
                "commands": [
                    ("thermo", "5"),
                    ("thermo_style", "custom step lx ly lz press pxx pyy pzz pe"),
                    ("dump", "dmp all atom 5 run.dump"),
                ],
            },
            {
                "stage_name": "Stage 5",
                "commands": [
                    ("min_style", "cg"),
                    ("fix", "1 all box/relax iso 0.0 vmax 0.001"),
                    ("minimize", "1.0e-16 1.0e-16 5000 100000"),
                ],
            },
            {
                "stage_name": "5) Write output data",
                "commands": [("write_data", "run.data"), ("write_restart", "run.restart")],
            },
        ]

        assert lmp_min.inputfile.nstages == 6
        assert lmp_min.inputfile.ncomments == 0
