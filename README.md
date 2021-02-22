# three-cc-muscle
Python implementation of the 3CC-r muscle model as proposed in 
[Modification of a three-compartment muscle fatigue model to predict peak torque decline during intermittent tasks](https://doi.org/10.1016/j.jbiomech.2018.06.005).
As expressed in the original paper, this implementation may also be used as a 3CC model, by setting the rest parameter equal to 1.
The model is adapted for use with direct torque control on hinge joints and takes actions on the interval (-1, 1) as input.

## Installation
```shell
git clone https://github.com/lorenz-h/three-cc-muscle.git
pip install -e ./three-cc-muscle
```

## Usage
The optimal rates for specific joints can be found in the [original paper](https://doi.org/10.1016/j.jbiomech.2018.06.005). 
By default the model uses the optimal parameters for general joints as described in the paper.
```python
from three_cc_muscle import CCrMuscleModel

muscle = CCrMuscleModel()
action = muscle.step(0.95, 0.01)
```
Additionally, the package offers a simple wrapper to handle multiple muscles concurrently. 
Internally it uses the builtin map() function. 
To reduce the risk for implementation errors there is no truly vector based implementation for now.
```python
from three_cc_muscle import CCrMuscleGroupModel
import numpy as np

n_muscles = 7
muscle = CCrMuscleGroupModel(n_muscles=n_muscles)
action = muscle.step(np.ones((n_muscles, )), 0.01)
```
## Note
I have no affiliation with the original authors and cannot guarantee the correctness of my implementation.