from typing import List


class CCrMuscleModel:
    def __init__(self, recovery_rate: float = 0.00091, fatigue_rate: float = 0.00970, rest_rate: float = 15.0):
        # defaults for recovery, fatigue and rest rate are optimal parameters for general muscles
        # taken from https://doi.org/10.1016/j.jbiomech.2012.04.018
        self.tracking_factor = 10.
        self.m_r = 1.0
        self.m_a = 0.0
        self.m_f = 0.0

        self.recovery_rate = recovery_rate
        self.fatigue_rate = fatigue_rate
        self.rest_rate = rest_rate

    def update_compartments(self, target_intensity: float, control: float, dt: float) -> None:
        if target_intensity == 0:
            self.m_r += dt * (-control + self.recovery_rate * self.rest_rate * self.m_f)
        else:
            self.m_r += dt * (-control + self.recovery_rate * self.rest_rate * self.m_f)
        self.m_a += dt * (control - self.fatigue_rate * self.m_a)
        self.m_f += dt * (self.fatigue_rate * self.m_a - self.recovery_rate * self.m_f)

    def _forward(self, target_intensity: float, dt: float) -> float:
        control: float
        if self.m_a < target_intensity and self.m_r >= (target_intensity - self.m_a):
            # In conflict with paper I added >= instead of > to second condition here to cover all cases.
            control = self.tracking_factor * (target_intensity - self.m_a)
        elif self.m_a < target_intensity and self.m_r < (target_intensity - self.m_a):
            control = self.tracking_factor * self.m_r
        elif self.m_a >= target_intensity:
            control = self.tracking_factor * (target_intensity - self.m_a)
        else:
            raise RuntimeError(f"Condition occurred in muscle model not covered by the original authors.")

        self.update_compartments(target_intensity, control, dt)

        return control

    def step(self, action: float, dt: float) -> float:
        assert -1.0 <= action <= 1.0
        action_sign: float = 1 - ((action <= 0.0) * 2)  # get the sign (-1 or 1) of the action
        target_intensity = abs(action)
        control = self._forward(target_intensity, dt)
        return (control / self.tracking_factor) * action_sign

    def reset(self):
        self.m_r = 1.0
        self.m_a = 0.0
        self.m_f = 0.0
