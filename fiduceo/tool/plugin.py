import pkg_resources
import sys
import traceback

ENTRY_POINTS_GROUP = "fiduceo_user_tools_plugins"


def get_plugins():
    return dict(_PLUGIN_REGISTRY)


def _load_plugins():
    plugins = dict()

    for entry_point in pkg_resources.iter_entry_points(group=ENTRY_POINTS_GROUP, name=None):

        problem = None

        # noinspection PyBroadException
        try:
            plugin = entry_point.load()
            if callable(plugin):
                # noinspection PyBroadException
                try:
                    plugin()
                except Exception as e:
                    problem = _get_problem(entry_point, e,
                                           'error executing plugin loaded from '
                                           'entry point "{name}" of group "{group}"')
            else:
                problem = _get_problem(entry_point, None,
                                       'plugin must be a function or callable object: '
                                       'entry point "{name}" of group "{group}"')
        except Exception as e:
            problem = _get_problem(entry_point, e,
                                   'error loading plugin from '
                                   'entry point "{name}" of group "{group}"')

        # Here: generate a JSON-serializable plugin entry
        plugins[entry_point.name] = dict(name=entry_point.name,
                                         module_name=entry_point.module_name,
                                         attrs=entry_point.attrs,
                                         dist=entry_point.dist,
                                         extras=entry_point.extras,
                                         problem=problem)

    # import pprint
    # pprint.pprint(plugins)

    return plugins


def _get_problem(entry_point, error, message_pattern):
    message = message_pattern.format(name=entry_point.name, group=ENTRY_POINTS_GROUP)
    traceback_lines = None
    detail = None
    if error is not None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_lines = traceback.format_tb(exc_traceback)
        detail = str(error)
    return dict(message=message, traceback=traceback_lines, detail=detail)


def test_plugin_1():
    # Used to test a plugin that loads successfully (but does nothing)
    pass


def test_plugin_2():
    # Used to test a plugin that raises an error
    raise IOError('intentional failure')


#: Mapping of entry point names to JSON-serializable plugin meta-information.
_PLUGIN_REGISTRY = _load_plugins()
