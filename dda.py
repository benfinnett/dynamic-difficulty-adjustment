from typing import Callable

class GameMetricController:
    """
    The DDA system uses a quantifiable metric to assess the difference
    between current performance and the desired performance (setpoint).
    
    A PID controller then uses the provided modifiers to adjust gameplay
    aspects aiming to push the player closer to the desired performance.
    """
    def __init__(self, 
                 metric: Callable[[], float],
                 modifiers: list,
                 setpoint: float, 
                 kp: float = .1, 
                 ki: float = .1, 
                 kd: float = 1):
        self.metric = metric
        self.modifiers = modifiers
        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_error = 0
        self.integral_sum = 0
        self.last_output = 0

        self.evaluation_cache: dict[float, float] = {}

    def evaluate_performance(self) -> float:
        error = self.setpoint - self.metric()

        # Check if error has previously been calculated
        if error in self.evaluation_cache:
            return self.evaluation_cache[error]

        # Proportional term
        proportional = self.kp * error

        # Integral term
        self.integral_sum += self.ki * error

        # Derivative term
        derivative = self.kd * (error - self.last_error)
        self.last_error = error

        # Summate terms
        self.last_output = proportional + self.integral_sum + derivative

        # Add to cache and return value
        self.evaluation_cache[error] = self.last_output
        return self.last_output
    
    def update_modifiers(self) -> None:     
        for modifier in self.modifiers:
            # modifier = [update_function, weight]
            modifier[0](self.last_output * modifier[1])