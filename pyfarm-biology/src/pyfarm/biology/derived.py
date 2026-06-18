"""Pure-math biology metric functions for pyfarm-biology."""

from __future__ import annotations

import math


def _linear_regression(xs: list[float], ys: list[float]) -> tuple[float, float]:
    n = len(xs)
    if n < 2:
        raise ValueError("Need at least 2 data points for linear regression")
    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_xx = sum(x * x for x in xs)
    sum_xy = sum(x * y for x, y in zip(xs, ys))
    denom = n * sum_xx - sum_x * sum_x
    if denom == 0:
        raise ValueError("All x values are identical")
    slope = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y - slope * sum_x) / n
    return slope, intercept


def ph_drift_rate(readings: list[tuple[float, float]]) -> float:
    """pH drift per hour (negative = acidification)."""
    if len(readings) < 2:
        raise ValueError("Need at least 2 pH readings")
    xs = [t / 3600.0 for t, _ in readings]
    ys = [ph for _, ph in readings]
    slope, _ = _linear_regression(xs, ys)
    return slope


def doubling_time_hours(od_readings: list[tuple[float, float]]) -> float | None:
    """Cell doubling time from OD600 readings via log-linear regression."""
    if len(od_readings) < 2:
        return None
    valid = [(t, od) for t, od in od_readings if od > 0]
    if len(valid) < 2:
        return None
    xs = [t / 3600.0 for t, _ in valid]
    ys = [math.log(od) for _, od in valid]
    slope, _ = _linear_regression(xs, ys)
    if slope <= 0:
        return None
    return math.log(2) / slope


def fermentation_efficiency(initial_gravity: float, final_gravity: float) -> float:
    """Apparent attenuation % = (OG - FG) / (OG - 1.0) * 100."""
    og_points = initial_gravity - 1.0
    if og_points == 0:
        raise ValueError("Initial gravity must be greater than 1.0")
    return (og_points - (final_gravity - 1.0)) / og_points * 100.0


def co2_production_rate(gravity_readings: list[tuple[float, float]]) -> float:
    """CO2 production rate in g/L/hr from gravity drop."""
    if len(gravity_readings) < 2:
        raise ValueError("Need at least 2 gravity readings")
    xs = [t / 3600.0 for t, _ in gravity_readings]
    ys = [sg for _, sg in gravity_readings]
    slope, _ = _linear_regression(xs, ys)
    return -slope * 2042.5
