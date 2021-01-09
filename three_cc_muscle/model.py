from typing import List, Optional

import numpy as np


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

    def _update_compartments(self, target_intensity: float, control: float, dt: float) -> None:
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

        self._update_compartments(target_intensity, control, dt)

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


class CCrMuscleGroupModel:
    def __init__(self, n_muscles: int, recovery_rates: Optional[List[float]] = None,
                 fatigue_rates: Optional[List[float]] = None, rest_rates: Optional[List[float]] = None):

        assert fatigue_rates is None or len(fatigue_rates) == n_muscles
        assert recovery_rates is None or len(recovery_rates) == n_muscles
        assert rest_rates is None or len(rest_rates) == n_muscles

        self.models: List[CCrMuscleModel] = list()
        for i in range(n_muscles):
            kwargs = {}
            if recovery_rates is not None:
                kwargs["recovery_rate"] = recovery_rates[i]
            if fatigue_rates is not None:
                kwargs["fatigue_rate"] = fatigue_rates[i]
            if rest_rates is not None:
                kwargs["rest_rate"] = rest_rates[i]
            self.models.append(CCrMuscleModel(**kwargs))

    def reset(self) -> None:
        map(lambda model: model.reset(), self.models)

    def step(self, actions: np.ndarray, dt: float) -> np.ndarray:
        return np.array(list(map(lambda model, action: model.step(action, dt), self.models, actions)))

