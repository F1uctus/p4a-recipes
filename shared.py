from __future__ import annotations

from typing import Iterable

from pythonforandroid.recipe import Recipe


def extend_env_with_recipe_build_dirs(
    env: dict,
    *,
    ctx,
    arch,
    recipe_names: Iterable[str],
    keys: tuple[str, ...] = ("CYTHON_INCLUDE_PATH", "PYTHONPATH"),
) -> dict:
    """
    Prepend each recipe build dir to selected env vars.

    This is mainly used to help Cython resolve `.pxd` files when cythonizing
    under hostpython (where dependency sources are otherwise not on sys.path).
    """
    if arch is None:
        return env

    dep_build_dirs = [
        Recipe.get_recipe(name, ctx).get_build_dir(arch.arch) for name in recipe_names
    ]
    # deduplicate
    dep_build_dirs = list(dict.fromkeys(dep_build_dirs))

    for key in keys:
        existing = env.get(key)
        env[key] = ":".join(dep_build_dirs + ([existing] if existing else []))

    return env
