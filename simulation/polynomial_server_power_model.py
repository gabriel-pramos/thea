import numpy as np
""" Contains a server power model definition."""


class PolynomialServerPowerModel:
    """Server power model proposed in [1], which assumes a linear correlation between a server's power consumption and demand.

    [1] Anton Beloglazov, and Rajkumar Buyya, "Optimal Online Deterministic Algorithms and Adaptive Heuristics for Energy and
    Performance Efficient Dynamic Consolidation of Virtual Machines in Cloud Data Centers", Concurrency and Computation: Practice
    and Experience (CCPE), Volume 24, Issue 13, Pages: 1397-1420, John Wiley & Sons, Ltd, New York, USA, 2012
    """

    @classmethod
    def get_power_consumption(cls, device: object) -> float:
        """Gets the power consumption of a server.

        Args:
            device (object): Server whose power consumption will be computed.

        Returns:
            power_consumption (float): Server's power consumption.
        """
        if "utilization" not in device.power_model_parameters:
            raise Exception("The power model parameters must contain the utilization parameter.")
        if "power_consumption" not in device.power_model_parameters:
            raise Exception("The power model parameters must contain the power_consumption parameter.")

        if device.active:
            utilization = np.array(device.power_model_parameters["utilization"])
            power = np.array(device.power_model_parameters["power_consumption"])
            fit_func = np.poly1d(np.polyfit(utilization, power, 7))

            demand = device.cpu_demand
            capacity = device.cpu
            utilization = demand / capacity

            power_consumption = fit_func(utilization)
        else:
            power_consumption = 0

        return power_consumption
