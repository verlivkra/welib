[![Build status](https://github.com/ebranlard/welib/workflows/Tests/badge.svg)](https://github.com/ebranlard/welib/actions?query=workflow%3A%22Tests%22)
<a href="https://www.buymeacoffee.com/hTpOQGl" rel="nofollow"><img alt="Donate just a small amount, buy me a coffee!" src="https://warehouse-camo.cmh1.psfhosted.org/1c939ba1227996b87bb03cf029c14821eab9ad91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4275792532306d6525323061253230636f666665652d79656c6c6f77677265656e2e737667"></a>

# Wind Energy Library - welib

Wind energy library: suite of python and matlab tools for aero-servo-hydro-elasticity (aerodynanmics, controls, hydrodynamics, structure/elasticity) and wind energy.

# Installation and testing
Installing the latest release:
```bash
pip install --upgrade welib
```
Installing the latest dev version and running the unittests:
```bash
git clone http://github.com/ebranlard/welib -b dev
cd welib
python -m pip install -r requirements.txt
python -m pip install -e .
pytest
```

# Gallery of example scripts

A sample of the figures generated by the examples in this repository are given below.
Additional examples can be found in the `examples` and `tests` folders of the different subpackages.

Click on the links to access the corresponding scripts. 
Click on the figures to enlarge the figures.

| | | | |  |
| :-------------------------: | :-------------------------: | :-------------------------: | :-------------------------: | :-------------------------:  |
| [MGH dynamic stall model](/welib/airfoils/examples/dynamic_stall_mhh.py) | [Oye dynamic stall model](/welib/airfoils/examples/dynamic_stall_oye.py) | [Beam - Analytical mode shapes of a beam](/welib/beams/examples/Ex1_BeamModes.py) | [Beam - Analytical mode shapes different BC](/welib/beams/examples/Ex2_BeamModesAllBC.py) | [BEM Steady - High thrust correction](/welib/BEM/examples/Example_AxialInduction.py) |
| ![MGH dynamic stall model](/../figs/_figs/MGHDynamicStallModel.png) | ![Oye dynamic stall model](/../figs/_figs/OyeDynamicStallModel.png) | ![Beam - Analytical mode shapes of a beam](/../figs/_figs/Beam-AnalyticalModeShapesOfABeam.png) | ![Beam - Analytical mode shapes different BC](/../figs/_figs/Beam-AnalyticalModeShapesDifferentBC.png) | ![BEM Steady - High thrust correction](/../figs/_figs/BEMSteady-HighThrustCorrection.png) |
| [BEM Steady - Performance curve](/welib/BEM/examples/Example_BEM_2.py) | [BEM Steady - CP-lambda-pitch ](/welib/BEM/examples/Example_BEM_CPLambdaPitch.py) | [BEM Unsteady - Prescribed surge motion](/welib/BEM/examples/Example_UnsteadyBEM_2_PrescribedMotion.py) | [Dynamic Inflow (Oye) - induction step](/welib/dyninflow/examples/Ex1_StepUp.py) | [FAST - interpolate radial time series](/welib/fast/examples/Example_RadialInterp.py) |
| ![BEM Steady - Performance curve](/../figs/_figs/BEMSteady-PerformanceCurve.png) | ![BEM Steady - CP-lambda-pitch ](/../figs/_figs/BEMSteady-CP-lambda-pitch.png) | ![BEM Unsteady - Prescribed surge motion](/../figs/_figs/BEMUnsteady-PrescribedSurgeMotion.png) | ![Dynamic Inflow (Oye) - induction step](/../figs/_figs/DynamicInflow(Oye)-InductionStep.png) | ![FAST - interpolate radial time series](/../figs/_figs/FAST-InterpolateRadialTimeSeries.png) |
| [FAST - Average radial outputs](/welib/fast/examples/Example_RadialPostPro.py) | [FEM - mode shapes of a beam](/welib/FEM/examples/Beam_ModeShapes_UniformBeamFrame3d.py) | [Hydro - Wave kinematics](/welib/hydro/examples/Ex1_WaveKinematics.py) | [Hydro - Jonswap spectrum](/welib/hydro/examples/Ex2_Jonswap_spectrum.py) | [Hydro - wave generation](/welib/hydro/examples/Ex3_WaveTimeSeries.py) |
| ![FAST - Average radial outputs](/../figs/_figs/FAST-AverageRadialOutputs.png) | ![FEM - mode shapes of a beam](/../figs/_figs/FEM-ModeShapesOfABeam.png) | ![Hydro - Wave kinematics](/../figs/_figs/Hydro-WaveKinematics.png) | ![Hydro - Jonswap spectrum](/../figs/_figs/Hydro-JonswapSpectrum.png) | ![Hydro - wave generation](/../figs/_figs/Hydro-WaveGeneration.png) |
| [Hydro - Morison loads on monopile](/welib/hydro/examples/Ex4_WaveLoads.py) | [Plot - 3D blades](/welib/plot/examples/Plot_3D_blades.py) | [IEC Standards - Turbulence classes](/welib/standards/examples/Ex1_TurbulenceClasses.py) | [IEC Standards - Extreme operating gusts](/welib/standards/examples/Ex2_EOG.py) | [System - 2nd order - forced vibrations](/welib/system/examples/MassSpringDamper_ForcedVibrations.py) |
| ![Hydro - Morison loads on monopile](/../figs/_figs/Hydro-MorisonLoadsOnMonopile.png) | ![Plot - 3D blades](/../figs/_figs/Plot-3DBlades.png) | ![IEC Standards - Turbulence classes](/../figs/_figs/IECStandards-TurbulenceClasses.png) | ![IEC Standards - Extreme operating gusts](/../figs/_figs/IECStandards-ExtremeOperatingGusts.png) | ![System - 2nd order - forced vibrations](/../figs/_figs/System-2ndOrder-ForcedVibrations.png) |
| [3D pendulum - motion](/welib/system/examples/pendulum_3d.py) | [Signal - Correlation coefficient](/welib/tools/examples/ExampleCorrelation.py) | [Signal - FFT](/welib/tools/examples/Example_FFT.py) | [Wind - wind generation at point](/welib/wind/examples/WindGenerationAtPoint.py) |  |
| ![3D pendulum - motion](/../figs/_figs/3DPendulum-Motion.png) | ![Signal - Correlation coefficient](/../figs/_figs/Signal-CorrelationCoefficient.png) | ![Signal - FFT](/../figs/_figs/Signal-FFT.png) | ![Wind - wind generation at point](/../figs/_figs/Wind-WindGenerationAtPoint.png) |  |

# Examples of application


You can have a look at the example gallery below for direct links to examples and associated plots.

- Aerodynamic applications (package `airfoils`, `BEM`):
    - Manipulation of airfoil curves, find slopes, interpolate (see [airfoils](welib/airfoils/examples/))
    - Run different dynamic stall models (e.g Oye or MHH/HGM model) (see [airfoils/DS](welib/airfoils/examples/))

- Hydrodynamics applications (package `hydro`):
    - Wave kinematics for linear waves (see [hydro/Ex1](welib/hydro/examples/Ex1_WaveKinematics.py))
    - Generation of wave time series from a given spectrum (see [hydro/Ex3](welib/hydro/examples/Ex3_WaveTimeSeries.py))
    - Computation of wave loads on a monopile (see [hydro/Ex4](welib/hydro/examples/Ex4_WaveLoads.py))

- Structural dynamics and system dynamics applications (packages `FEM`, `system`, `yams`):
    - Setup the equation of motions for a multibody system with flexible members analytically or numerically (see [yams](welib/yams/tests))
    - Linearize a non-linear system defined by a state and output equation (implicit or explicit) (see [system](welib/system/tests))
    - Perform 2d/3d FEM analyses using beam/frame elements (see [FEM](welib/FEM/examples))
    - Craig-Bampton / Guyan reduction of a structure (see [FEM](welib/FEM/examples))
    - Perform time integration of mechanical systems (see [system](welib/system/examples))

- Controls applications (packages `ctrl`, `kalman`):
    - Run a kalman filter to estimate states of a system (see [kalman](welib/kalman/))

- Wind energy applications:
    - Run steady state BEM simulations (see [BEM/steady 1-2](welib/BEM/examples)
    - Run unsteady BEM simulations (see [BEM/unsteady 1-2](welib/BEM/examples/)
    - Read and write common wind energy file formats (see [weio](welib/weio), a clone of [weio](http://github.com/ebranlard/weio/))
    - Generate stochastic wind and [waves](welib/hydro/examples/Ex3_WaveTimeSeries.py) times series
    - Estimate wind speed (see 'welib\ws\_estimator`))
    - Theory of optimal circulation
    - Standards

- Other (packages `tools`, `ode`):
    -  Spectral analyses, signal processing, time integration, vector analyses

See also:

- [pyDatView](http://github.com/ebranlard/pyDatView/): GUI to visualize files (supported by weio) and perform analyses on the data




# Libraries

The repository contains a set of small packages, for aerodynamics, structure, control and more:

- airfoils: polar manipulations, dynamic stall models
- beams: analytical results for beams
- BEM: steady and unsteady bem code
- ctrl: control tools
- dyninflow: dynamic inflow models
- fastlib: tools to handle OpenFAST models (run simulations, postprocess, linear model)
- FEM: Finite Element Method tools (beams)
- hydro: hydrodynamic tools
- kalman: kalman filter
- mesh: meshing tools
- ode: tools for time integration of ODE
- standards: some formulae and scripts useful for the IEC standards
- system: tools for dynamic systems (e.g. LTI, state space) and mechanical systems (M,C,K matrices), eigenvalue analysis, time integration
- tools: mathematical tools, signal processing
- weio: library to read and write files used in wind energy, clone of [weio](http://github.com/ebranlard/weio/) 
- wt\_theory: scripts implementing some wind turbine aerodynamic theory 
- ws\_estimator: wind speed estimator for wind energy based on tabulated Cp Ct
- yams: multibody analyses


# References and how to cite
If you find some of this repository useful and use it in your research, thank you for using the following citations.

 - General wind turbine scripts and aerodynamics:
```bibtex
@book{Branlard:book,
    author = {E. Branlard},
    title = {Wind Turbine Aerodynamics and Vorticity-Based Methods: Fundamentals and Recent Applications},
    year = {2017},
    publisher= {Springer International Publishing},
    doi={10.1007/978-3-319-55164-7},
    isbn={ 978-3-319-55163-0}
}
```
 - Structural dynamics:
```bibtex
@article{Branlard:2019,
    title    = {{Flexible multibody dynamics using joint coordinates and the Rayleigh-Ritz approximation: The general framework behind and beyond Flex}},
    author   = {E. Branlard},
    journal  = {Wind Energy},
    volume   = {22},
    number   = {7},
    pages    = {877-893},
    year     = {2019},
    doi      = {10.1002/we.2327}
}
```





# Contributing
Any contributions to this project are welcome! If you find this project useful, you can also buy me a coffee (donate a small amount) with the link below:


<a href="https://www.buymeacoffee.com/hTpOQGl" rel="nofollow"><img alt="Donate just a small amount, buy me a coffee!" src="https://warehouse-camo.cmh1.psfhosted.org/1c939ba1227996b87bb03cf029c14821eab9ad91/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4275792532306d6525323061253230636f666665652d79656c6c6f77677265656e2e737667"></a>
