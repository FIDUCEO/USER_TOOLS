import numpy as np
from numba import jit


class RadianceDisturbances:

    def calculate(self, dataset, variable_names):
        disturbances = dict()

        y = dataset.dims["y"]
        x = dataset.dims["x"]
        for variable_name in variable_names:
            u_ind_name = "u_independent_" + variable_name

            u_ind_data = None
            if u_ind_name in dataset:
                u_ind_data = dataset[u_ind_name].values

            u_str_name = "u_structured_" + variable_name
            u_str_data = None
            if u_str_name in dataset:
                u_str_data = dataset[u_str_name].values

            u_com_name = "u_common_" + variable_name
            u_com_data = None
            if u_com_name in dataset:
                u_com_data = dataset[u_com_name].values

            if u_str_data is None and u_ind_data is None and u_com_data is None:
                continue  # if no uncertainty can be found we skip this variable from calculation tb 2018-04-04

            if u_ind_data is None:
                u_ind_data = np.zeros([y, x])

            if u_str_data is None:
                u_str_data = np.zeros([y, x])

            if u_com_data is None:
                u_com_data = np.zeros([y, x])

            rad_delta = calculate_radiance_delta(u_ind_data, u_str_data, u_com_data)
            disturbances.update({variable_name: rad_delta})

        return disturbances


@jit(nopython=True)
def calculate_radiance_delta(u_ind, u_str, u_com):
    return np.sqrt(u_ind * u_ind + u_str * u_str + u_com * u_com)
