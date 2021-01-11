import copy
import matplotlib.pyplot as plt
from three_cc_muscle import CCrMuscleModel, CCrMuscleGroupModel
import numpy as np


if __name__ == '__main__':
    model = CCrMuscleModel()
    m_rs = list()
    m_fs = list()
    m_as = list()
    actions = list()
    dt = 0.01
    for i in range(20000):
        action = model.step(0.5, dt)
        assert -1.0 < action <= 1.0
        assert model.m_r < 10.1
        m_rs.append(copy.copy((i*dt, model.m_r)))
        m_fs.append(copy.copy((i*dt, model.m_f)))
        m_as.append(copy.copy((i*dt, model.m_a)))
        actions.append((i*dt, action))

    plt.scatter([m[0] for m in m_rs], [m[1] for m in m_rs], c="g")
    plt.scatter([m[0] for m in m_fs], [m[1] for m in m_fs], c="r")
    plt.scatter([m[0] for m in m_as], [m[1] for m in m_as], c="y")
    plt.scatter([m[0] for m in actions], [m[1] for m in actions], c="b")
    plt.savefig("test.png")