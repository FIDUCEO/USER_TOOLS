import xarray as xr


class SensitivityCalculator():

    def run(self, dataset, disturbances, algorithm):
        sensitivities = dict()

        for channel_name, channel_disturbance in disturbances.items():
            positive_disturbance = dataset[channel_name].data + channel_disturbance
            negative_disturbance = dataset[channel_name].data - channel_disturbance

            names = algorithm.get_variable_names()

            subset = self._create_subset(dataset, names)
            subset[channel_name].data = positive_disturbance
            z2 = algorithm.process(subset)

            # subset = self._create_subset(dataset, names)
            subset[channel_name].data = negative_disturbance
            z1 = algorithm.process(subset)

            sensitivity = (z2.data - z1.data) * 0.5

            sensitivities.update({channel_name: sensitivity})

        return sensitivities

    def _create_subset(self, dataset, variable_names):
        subset = xr.Dataset()

        for variable_name in variable_names:
            subset[variable_name] = dataset[variable_name]

        return subset
