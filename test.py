from three_cc_muscle import CCrMuscleModel

if __name__ == '__main__':
    model = CCrMuscleModel()

    print(model.step(1.0, 0.01))
    for i in range(1000):
        action = model.step(1.0, 0.01)
        assert -1.0 < action <= 1.0
        assert model.m_r < 10.1

    for i in range(1000):
        action = model.step(-1.0, 0.01)

    print(model.step(1.0, 0.01))

    for i in range(10000):
        action = model.step(0.0, 0.01)
        assert -1.0 < action <= 1.0
        assert model.m_r <= model.tracking_factor

    print(model.step(-1.0, 0.01))