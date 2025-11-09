from __future__ import annotations
from math import sqrt
from dataclasses import dataclass

@dataclass
class ProportionResult:
    lift: float
    p_value: float
    ci_low: float
    ci_high: float
    control_rate: float
    treatment_rate: float

def z_test_proportions(n1: int, x1: int, n2: int, x2: int, alpha: float = 0.05) -> ProportionResult:
    if n1 <= 0 or n2 <= 0:
        raise ValueError("Sample sizes must be positive.")
    p1, p2 = x1/n1, x2/n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = sqrt(max(p_pool*(1-p_pool)*(1/n1 + 1/n2), 1e-12))
    z = (p2 - p1)/se
    from math import erf, sqrt as _sqrt
    p_value = 2*(1 - 0.5*(1+erf(abs(z)/_sqrt(2))))
    zcrit = 1.96
    diff = p2 - p1
    ci_low, ci_high = diff - zcrit*se, diff + zcrit*se
    lift = (p2 - p1) / p1 if p1 > 0 else float('inf')
    return ProportionResult(lift=lift, p_value=p_value, ci_low=ci_low, ci_high=ci_high,
                            control_rate=p1, treatment_rate=p2)

def verdict_from_result(res: ProportionResult, alpha: float = 0.05) -> str:
    if res.p_value < alpha and res.lift > 0:
        return "Win"
    if res.p_value < alpha and res.lift < 0:
        return "Lose"
    return "Inconclusive"
