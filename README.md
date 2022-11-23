# napari-mouse-gesture

[![License BSD-3](https://img.shields.io/pypi/l/napari-mouse-gesture.svg?color=green)](https://github.com/hanjinliu/napari-mouse-gesture/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-mouse-gesture.svg?color=green)](https://pypi.org/project/napari-mouse-gesture)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-mouse-gesture.svg?color=green)](https://python.org)
[![tests](https://github.com/hanjinliu/napari-mouse-gesture/workflows/tests/badge.svg)](https://github.com/hanjinliu/napari-mouse-gesture/actions)
[![codecov](https://codecov.io/gh/hanjinliu/napari-mouse-gesture/branch/main/graph/badge.svg)](https://codecov.io/gh/hanjinliu/napari-mouse-gesture)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-mouse-gesture)](https://napari-hub.org/plugins/napari-mouse-gesture)

Install mouse gesture functions into napari viewers

![](example.gif)

### Register callbacks

Use `register_gesture` to register custom callback functions.

```python
from napari_mouse_gesture import register_gesture

# use standard strings (up, left, down, right) split by "-"
@register_gesture("up-left")
def _callback(viewer):
    print("called")

# use triangles (^, <, v, >)
@register_gesture("^<")
def _callback(viewer):
    print("called")

# use arrows (↑, ←, ↓, →)
@register_gesture("↑←")
def _callback(viewer):
    print("called")
```

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/stable/plugins/index.html
-->

## Installation

You can install `napari-mouse-gesture` via [pip]:

    pip install napari-mouse-gesture



To install latest development version :

    pip install git+https://github.com/hanjinliu/napari-mouse-gesture.git


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-mouse-gesture" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/hanjinliu/napari-mouse-gesture/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
