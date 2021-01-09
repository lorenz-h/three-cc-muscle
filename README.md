# three-cc-muscle
Python implementation of the 3CC-r muscle model as proposed in 
[Modification of a three-compartment muscle fatigue model to predict peak torque decline during intermittent tasks](https://doi.org/10.1016/j.jbiomech.2012.04.018).
The model is adapted for use with direct torque control on hinge joints and takes actions on the interval (-1, 1) as input.

## Installation
```shell
git clone https://github.com/lorenz-h/three-cc-muscle.git
pip install -e ./three-cc-muscle
```

## Usage
The optimal rates for specific joints can be found in the [original paper](https://doi.org/10.1016/j.jbiomech.2012.04.018). 
By default the model uses the optimal parameters for general joints as described in the paper.
```python
from three_cc_muscle import CCrMuscleModel
model = CCrMuscleModel()
```

## Note
I have no affiliation with the original authors and cannot guarantee the correctness of my implementation.