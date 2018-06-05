import os
import time

import numpy as np
import xarray as xr
from numba import jit, prange
from xarray import Variable

from fiduceo.tool.radprop.algorithms.algorithm_factory import AlgorithmFactory
from fiduceo.tool.radprop.radiance_disturbances import RadianceDisturbances
from fiduceo.tool.radprop.sensitivity_calculator import SensitivityCalculator

CORRELATION_MATRIX_INDEPENDENT = "channel_correlation_matrix_independent"
CORRELATION_MATRIX_STRUCTURED = "channel_correlation_matrix_structured"
CORRELATION_MATRIX_COMMON = "channel_correlation_matrix_common"


class RadPropProcessor():

    def __init__(self):
        self._algorithm_factory = AlgorithmFactory()
        self._rad_disturbance_proc = RadianceDisturbances()
        self.sensitivity_calculator = SensitivityCalculator()
        self.input_file = None

    def run(self, cmd_line_args):
        dataset = xr.open_dataset(cmd_line_args.input_file, chunks=1024 * 1024)

        algorithm = self._algorithm_factory.get_algorithm(cmd_line_args.algorithm)

        # disturbances per channel
        variable_names = algorithm.get_variable_names()
        channel_indices = self._extract_channel_indices(dataset, variable_names)
        disturbances = self._rad_disturbance_proc.calculate(dataset, variable_names)

        # sensitivities per channel
        sensitivities = self.sensitivity_calculator.run(dataset, disturbances, algorithm)

        rci, rcs, rcu = self._subset_correlation_matrices(dataset, channel_indices)
        u_ind, u_str = self._extract_uncertainties(dataset, channel_indices)

        width = dataset.dims["x"]
        height = dataset.dims["y"]

        start_time = time.time()
        uncertainties = calculate_uncertainty_components(width, height, rci, rcs, u_ind, u_str, sensitivities)
        print("--- %s seconds ---" % (time.time() - start_time))

        target_variable = algorithm.process(dataset)

        target_dataset = xr.Dataset()
        target_dataset[cmd_line_args.algorithm] = target_variable
        target_dataset["u_total"] = Variable(["y", "x"], uncertainties[0, :, :])
        target_dataset["u_independent"] = Variable(["y", "x"], uncertainties[1, :, :])
        target_dataset["u_structured"] = Variable(["y", "x"], uncertainties[2, :, :])

        self._write_result(cmd_line_args, target_dataset)

        dataset.close()

    def get_algorithm_help_string(self):
        algorithm_names = self._algorithm_factory.get_names()
        help_string = "available algorithms are:\n"
        for name in algorithm_names:
            help_string += "- " + name + "\n"

        return help_string

    @staticmethod
    def _subset_correlation_matrices(dataset, channel_indices):
        # @todo read correlation matrices and subset
        # for now we have only algorithms with two channels and assume no correlation, just to get the code running
        size = len(channel_indices)
        indices = channel_indices.values()
        index_array = np.array(list(indices), dtype=np.int16)

        if CORRELATION_MATRIX_INDEPENDENT in dataset:
            full_correlation_matrix = dataset[CORRELATION_MATRIX_INDEPENDENT].values
            row_subset = full_correlation_matrix[index_array, :]
            rci = row_subset[:, index_array]
        else:
            rci = np.diag(np.ones(size, dtype=np.float64))

        if CORRELATION_MATRIX_STRUCTURED in dataset:
            full_correlation_matrix = dataset[CORRELATION_MATRIX_STRUCTURED].values
            row_subset = full_correlation_matrix[index_array, :]
            rcs = row_subset[:, index_array]
        else:
            rcs = np.diag(np.ones(size, dtype=np.float64))

        if CORRELATION_MATRIX_COMMON in dataset:
            full_correlation_matrix = dataset[CORRELATION_MATRIX_COMMON].values
            row_subset = full_correlation_matrix[index_array, :]
            rcu = row_subset[:, index_array]
        else:
            rcu = np.diag(np.ones(size, dtype=np.float64))

        return rci, rcs, rcu

    def _extract_uncertainties(self, dataset, channel_names):
        width = dataset.dims["x"]
        height = dataset.dims["y"]
        u_ind = np.full([len(channel_names), height, width], np.nan, np.float64)
        u_str = np.full([len(channel_names), height, width], np.nan, np.float64)

        index = 0
        for name, chanel_index in channel_names.items():
            u_ind_name = "u_independent_" + name
            u_ind[index, :, :] = dataset[u_ind_name].data

            u_str_name = "u_structured_" + name
            u_str[index, :, :] = dataset[u_str_name].data
            index += 1

        return u_ind, u_str

    @staticmethod
    def _extract_channel_indices(dataset, variable_names):
        # @todo 1 tb/tb read from channel coordinate and order by spectral index
        channel_names = dict()
        for name in variable_names:
            if name == "Ch1":
                channel_names.update({"Ch1": 0})
            if name == "Ch2":
                channel_names.update({"Ch2": 1})
            if name == "Ch3a":
                channel_names.update({"Ch3a": 2})
            if name == "Ch3b":
                channel_names.update({"Ch3b": 3})
            if name == "Ch4":
                channel_names.update({"Ch4": 4})
            if name == "Ch5":
                channel_names.update({"Ch5": 5})
            if name == "Ch1_BT":
                channel_names.update({"Ch1_BT": 0})
            if name == "Ch2_BT":
                channel_names.update({"Ch2_BT": 1})
            if name == "Ch3_BT":
                channel_names.update({"Ch3_BT": 2})
            if name == "Ch4_BT":
                channel_names.update({"Ch4_BT": 3})
            if name == "Ch5_BT":
                channel_names.update({"Ch5_BT": 4})

        return channel_names

    def _write_result(self, cmd_line_args, target_dataset):
        target_filename = self._create_target_filename(cmd_line_args.input_file, cmd_line_args.algorithm)
        target_path = os.path.join(cmd_line_args.out_dir, target_filename)

        comp = dict(zlib=True, complevel=5)
        encoding = dict()
        for var_name in target_dataset.data_vars:
            var_encoding = dict(comp)
            var_encoding.update(target_dataset[var_name].encoding)
            encoding.update({var_name: var_encoding})
        target_dataset.to_netcdf(target_path, format='netCDF4', engine='netcdf4', encoding=encoding)

    @staticmethod
    def _create_target_filename(source_file_name, algorithm_name):
        (head, file_name) = os.path.split(source_file_name)
        (prefix, extension) = os.path.splitext(file_name)

        return prefix + "_" + algorithm_name + extension


@jit('float64[:, :](float64[:], float64[:, :])', nopython=True)
def calculate_covariances(uncertainty_vector, correlation_matrix):
    unc_matrix = np.diag(uncertainty_vector)
    covariance_matrix = np.dot(unc_matrix, correlation_matrix)
    covariance_matrix = np.dot(covariance_matrix, unc_matrix)

    return covariance_matrix


@jit('float32(float64[:], float64[:, :], float64[:, :])', nopython=True)
def calculate_total_uncertainty(c, sci, scs):
    u_total_sq = np.dot(c, (sci + scs))
    u_total_sq = np.dot(u_total_sq, c)
    return np.sqrt(u_total_sq)


@jit('float32(float64[:], float64[:, :])', nopython=True)
def calculate_uncertainty(c, s):
    u_sq = np.dot(c, s)
    u_sq = np.dot(u_sq, c)
    return np.sqrt(u_sq)


@jit('float32[:, :](int32, int32)', nopython=True)
def create_float_array(width, height):
    he_64 = np.int64(height)
    wi_64 = np.int64(width)
    return np.zeros((he_64, wi_64), dtype=np.float32)


@jit('float32[:, :, :](int32, int32, int32)', nopython=True)
def create_float_array_3D(width, height, layers):
    he_64 = np.int64(height)
    wi_64 = np.int64(width)
    la_64 = np.int64(layers)
    return np.zeros((la_64, he_64, wi_64), dtype=np.float32)


@jit('float32[:, :, :](int32, int32, float64[:,:], float64[:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:])', nopython=True, parallel=True)
def calculate_uncertainty_components(width, height, rci, rcs, u_ind, u_str, sensitivities):
    u = create_float_array(width, height)
    u_i = create_float_array(width, height)
    u_s = create_float_array(width, height)

    for y in prange(0, height):
        for x in prange(0, width):
            u_ind_pixel = u_ind[:, y, x]

            sci = calculate_covariances(u_ind_pixel, rci)

            u_str_pixel = u_str[:, y, x]
            scs = calculate_covariances(u_str_pixel, rcs)

            # not for now tb 2018-04-11
            # @todo calculate Sch = Uch + UchT

            c = sensitivities[:, y, x]

            u[y, x] = calculate_total_uncertainty(c, sci, scs)
            u_i[y, x] = calculate_uncertainty(c, sci)
            u_s[y, x] = calculate_uncertainty(c, scs)

    result = create_float_array_3D(width, height, 3)
    result[0, :, :] = u
    result[1, :, :] = u_i
    result[2, :, :] = u_s
    return result
