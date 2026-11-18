# /// script
# requires-python = "==3.14.*"
# dependencies = ["pip==26.3"]
# ///
"""Build the npm packages of djLint.

The djlint package runs djLint on the Python of a package for its platform,
which npm picks out of its optional dependencies by their os, cpu and libc.
Each of those holds a CPython from python-build-standalone, cut down to what
djLint can use, with djLint and its dependencies installed into it.

    npm ci --include=dev
    uv run npm/build.py WHEELS [PLATFORM ...]

WHEELS is a folder with the djLint wheels of this version. When it has
compiled ones, as for a release, each platform that djLint is compiled for
has to find its own there; the others, and all of them when there is only the
pure one, as for a test, take the pure one. With no PLATFORM, all of them are
built. The packages are packed into npm/dist. npm ci, on the Node in .nvmrc,
installs esbuild, which builds the launcher, even with NODE_ENV=production.

The Python of a package runs this one's bytecode, so this script runs on the
same Python version. A package for Linux or macOS has to be built on one of
them, as Windows can't keep the files' modes.
"""

from __future__ import annotations

import compileall
import hashlib
import io
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from typing import Final

# Renovate updates it. Each release has every Python version, and the package
# takes the newest one of PYTHON.
PYTHON_BUILD_STANDALONE: Final = "20261110"
# The newest Python that every dependency has wheels for: PyYAML has none for 3.15.
PYTHON: Final = "3.14"


@dataclass(frozen=True)
class Platform:
    # python-build-standalone's name for it.
    python: str
    # The wheel tag pip takes the packages for it by. It caps the glibc or macOS
    # a wheel may need at what the Python needs: pip passes over a wheel that
    # needs a newer one, and the build stops instead of quietly asking for more.
    tag: str
    # Whether djLint has compiled wheels for it.
    mypyc: bool = True
    # Whether PyYAML has wheels for it. Where it has none, PyYAML goes without
    # its C extension, as it does where pip builds it without LibYAML.
    libyaml: bool = True


# The npm name of each platform, after Node's process.platform and
# process.arch, with one for each libc on Linux: every one python-build-standalone
# builds this Python for, but Linux on 32-bit Arm, which regex has no wheels for.
PLATFORMS: Final = {
    "darwin-arm64": Platform("aarch64-apple-darwin", "macosx_11_0_arm64"),
    "darwin-x64": Platform("x86_64-apple-darwin", "macosx_10_15_x86_64"),
    "linux-arm64-gnu": Platform("aarch64-unknown-linux-gnu", "manylinux_2_17_aarch64"),
    "linux-arm64-musl": Platform("aarch64-unknown-linux-musl", "musllinux_1_2_aarch64"),
    "linux-ppc64-gnu": Platform(
        "ppc64le-unknown-linux-gnu", "manylinux_2_17_ppc64le", mypyc=False, libyaml=False
    ),
    "linux-riscv64-gnu": Platform(
        "riscv64-unknown-linux-gnu", "manylinux_2_31_riscv64", mypyc=False, libyaml=False
    ),
    "linux-s390x-gnu": Platform("s390x-unknown-linux-gnu", "manylinux_2_17_s390x", mypyc=False),
    "linux-x64-gnu": Platform("x86_64-unknown-linux-gnu", "manylinux_2_17_x86_64"),
    "linux-x64-musl": Platform("x86_64-unknown-linux-musl", "musllinux_1_2_x86_64"),
    "win32-arm64": Platform("aarch64-pc-windows-msvc", "win_arm64"),
    "win32-ia32": Platform("i686-pc-windows-msvc", "win32", libyaml=False),
    "win32-x64": Platform("x86_64-pc-windows-msvc", "win_amd64"),
}
# Where PyYAML without its C extension comes from: its Python is the same in
# every wheel.
_PYYAML_TAG: Final = PLATFORMS["linux-x64-gnu"].tag

# What djLint has no use for: headers and libraries to build against, Tk and
# IDLE, pip, and the tests of Python itself. Relative to the python folder, on
# Linux and macOS, where the interpreter has libpython built in.
_REMOVED_POSIX: Final = (
    "include",
    "lib/itcl*",
    "lib/libpython*",
    "lib/libtcl*",
    "lib/pkgconfig",
    "lib/tcl*",
    "lib/thread*",
    "lib/tk*",
    "share",
)
# The same on Windows, kept apart: where case does not matter, lib/thread*
# would take Lib/threading.py.
_REMOVED_WINDOWS: Final = (
    "DLLs/_ctypes_test*",
    "DLLs/_test*",
    "DLLs/_tkinter*",
    "DLLs/tcl*",
    "DLLs/xxlimited*",
    "Scripts",
    "include",
    "libs",
    "pythonw.exe",
    "tcl",
)
# The same, relative to the standard library.
_REMOVED_FROM_STDLIB: Final = (
    "config-*",
    "ensurepip",
    "idlelib",
    "lib-dynload/_ctypes_test*",
    "lib-dynload/_test*",
    "lib-dynload/_tkinter*",
    "lib-dynload/_xxtestfuzz*",
    "lib-dynload/xxlimited*",
    "pydoc_data",
    "site-packages/*",
    "test",
    "tkinter",
    "turtle.py",
    "turtledemo",
)

_ROOT: Final = Path(__file__).resolve().parent.parent
_DIST: Final = _ROOT / "npm" / "dist"
_DOWNLOADS: Final = _DIST / "downloads"
_RELEASE_URL: Final = f"https://github.com/astral-sh/python-build-standalone/releases/download/{PYTHON_BUILD_STANDALONE}"
_REPOSITORY: Final = {"type": "git", "url": "git+https://github.com/djlint/djLint.git"}


def _run(*args: str | Path, cwd: Path = _ROOT) -> str:
    result = subprocess.run(  # noqa: S603
        [str(arg) for arg in args], cwd=cwd, check=False, capture_output=True, text=True
    )
    if result.returncode:
        msg = f"{' '.join(map(str, args))} failed:\n{result.stdout}{result.stderr}"
        raise RuntimeError(msg)
    return result.stdout


def _fetch(url: str) -> bytes:
    with urllib.request.urlopen(url) as response:  # noqa: S310
        data: bytes = response.read()
    return data


def _download(name: str, url: str) -> Path:
    """Download a file once, and keep it for later builds.

    Only what is checked against a hash fetched anew is kept, so a file in
    the downloads can't stand in for another one.
    """
    path = _DOWNLOADS / name
    if not path.exists():
        _DOWNLOADS.mkdir(parents=True, exist_ok=True)
        partial = path.with_name(f"{name}.part")
        with urllib.request.urlopen(url) as response, partial.open("wb") as file:  # noqa: S310
            shutil.copyfileobj(response, file)
        partial.replace(path)
    return path


def _python_archives() -> tuple[str, dict[str, str]]:
    """Return the Python version, and the sha256 of each of its archives."""
    sums = _fetch(f"{_RELEASE_URL}/SHA256SUMS").decode()
    hashes = {name: digest for digest, name in (line.split() for line in sums.splitlines())}
    versions = {
        name.removeprefix("cpython-").partition("+")[0]
        for name in hashes
        if name.startswith(f"cpython-{PYTHON}.")
    }
    version = max(versions, key=lambda version: tuple(map(int, version.split("."))))
    return version, hashes


def _licenses() -> dict[str, bytes]:
    """Return the licenses of what python-build-standalone builds into Python."""
    archive = _fetch(
        "https://github.com/astral-sh/python-build-standalone/archive/refs/tags/"
        f"{PYTHON_BUILD_STANDALONE}.tar.gz"
    )
    licenses: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        for member in tar:
            name = member.name.partition("/")[2]
            # extractfile() gives nothing for what isn't a file.
            if name.startswith("LICENSE.") and (file := tar.extractfile(member)):
                licenses[name] = file.read()
    if not licenses:
        msg = "found no licenses in python-build-standalone's source"
        raise RuntimeError(msg)
    return licenses


def _extract_python(folder: Path, triple: str, version: str, hashes: dict[str, str]) -> None:
    name = f"cpython-{version}+{PYTHON_BUILD_STANDALONE}-{triple}-install_only_stripped.tar.gz"
    archive = _download(name, f"{_RELEASE_URL}/{urllib.parse.quote(name)}")
    if hashlib.sha256(archive.read_bytes()).hexdigest() != hashes[name]:
        archive.unlink()
        msg = f"{name} does not match its sha256"
        raise RuntimeError(msg)
    with tarfile.open(archive) as tar:
        tar.extractall(folder, filter="data")


def _remove(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def _trim(python: Path, stdlib: Path, *, windows: bool) -> None:
    removed = _REMOVED_WINDOWS if windows else _REMOVED_POSIX
    for base, patterns in ((python, removed), (stdlib, _REMOVED_FROM_STDLIB)):
        for pattern in patterns:
            for path in base.glob(pattern):
                _remove(path)
    for cache in list(python.rglob("__pycache__")):
        shutil.rmtree(cache)
    binaries = python / "bin"
    if binaries.is_dir():
        # npm packs no symbolic links, so the interpreter is kept under the
        # name of the link the launcher calls.
        for path in binaries.iterdir():
            if path.name != f"python{PYTHON}":
                _remove(path)
        (binaries / f"python{PYTHON}").rename(binaries / "python3")
    links = [path for path in python.rglob("*") if path.is_symlink()]
    if links:
        msg = f"npm would leave out these symbolic links: {links}"
        raise RuntimeError(msg)


def _install(site: Path, tag: str, *requirements: str | Path) -> None:
    # pip, as uv knows no wheel tags for ppc64le or s390x.
    _run(
        sys.executable,
        "-m",
        "pip",
        "install",
        "--isolated",
        "--quiet",
        "--disable-pip-version-check",
        # With the downloads, which CI keeps from one run to the next.
        "--cache-dir",
        _DOWNLOADS / "pip",
        "--target",
        site,
        "--platform",
        tag,
        "--python-version",
        PYTHON,
        "--implementation",
        "cp",
        "--only-binary",
        ":all:",
        "--no-deps",
        "--no-compile",
        *requirements,
    )


def _requirements() -> dict[str, str]:
    """Return what uv.lock pins djLint's dependencies to, with their hashes, by name."""
    exported = _run(
        os.environ.get("UV", "uv"),
        "export",
        "--frozen",
        "--no-default-groups",
        "--no-emit-project",
        "--no-header",
        "--no-annotate",
    )
    # A requirement takes its first line and the --hash lines under it.
    entries = exported.replace(" \\\n    ", " ").splitlines()
    for entry in entries:
        marker = entry.partition(";")[2].partition("--hash")[0]
        # pip, which installs them, reads a marker for the Python it runs on.
        if any(word in marker for word in ("sys_platform", "platform_", "os_name")):
            msg = f"a requirement only some platforms have: {entry}"
            raise RuntimeError(msg)
    return {entry.partition("==")[0]: entry for entry in entries}


def _install_locked(site: Path, tag: str, requirements: Iterable[str]) -> None:
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "requirements.txt"
        path.write_text("".join(f"{line}\n" for line in requirements), encoding="utf-8")
        _install(site, tag, "--require-hashes", "--requirement", path)


def _npm() -> str:
    npm = shutil.which("npm")
    if npm is None:
        msg = "npm is not on PATH"
        raise RuntimeError(msg)
    return npm


def _write_manifest(folder: Path, manifest: Mapping[str, object]) -> None:
    # Without spaces, as no one reads it in the package.
    (folder / "package.json").write_text(
        json.dumps(manifest, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )


def _pack(folder: Path) -> Path:
    [packed] = json.loads(_run(_npm(), "pack", "--json", "--pack-destination", _DIST, cwd=folder))
    files = {path for path in folder.rglob("*") if path.is_file()}
    if packed["entryCount"] != len(files):
        msg = f"npm packed {packed['entryCount']} of the {len(files)} files in {folder}"
        raise RuntimeError(msg)
    filename: str = packed["filename"]
    return _DIST / filename


def _build_platform(
    name: str,
    *,
    wheels: Path,
    requirements: dict[str, str],
    version: str,
    python_version: str,
    hashes: dict[str, str],
    licenses: dict[str, bytes],
) -> Path:
    platform = PLATFORMS[name]
    system, cpu, *libc = name.split("-")
    folder = _DIST / name
    python = folder / "python"
    windows = system == "win32"
    stdlib = python / ("Lib" if windows else f"lib/python{PYTHON}")

    _extract_python(folder, platform.python, python_version, hashes)
    _trim(python, stdlib, windows=windows)
    site = stdlib / "site-packages"
    if platform.libyaml:
        _install_locked(site, platform.tag, requirements.values())
    else:
        others = [line for package, line in requirements.items() if package != "pyyaml"]
        _install_locked(site, platform.tag, others)
        _install_locked(site, _PYYAML_TAG, [requirements["pyyaml"]])
        for extension in (site / "yaml").glob("_yaml.*"):
            extension.unlink()
    _install(site, platform.tag, "--no-index", "--find-links", wheels, f"djlint=={version}")
    # The commands of the packages, made for a Python that is not this one.
    shutil.rmtree(site / "bin", ignore_errors=True)
    # An unchecked hash lets Python take the bytecode as is: npm gives every
    # file the same date, and may install them where they can't be rewritten.
    if not compileall.compile_dir(
        python, quiet=1, invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH
    ):
        msg = f"some of Python's modules for {name} did not compile"
        raise RuntimeError(msg)
    (python / "licenses").mkdir()
    for license_name, text in licenses.items():
        (python / "licenses" / license_name).write_bytes(text)
    shutil.copy(_ROOT / "LICENSE", folder)

    compiled = any(site.glob("*__mypyc*"))
    if platform.mypyc and not compiled and any(wheels.glob("djlint-*-cp*.whl")):
        msg = f"none of the compiled djLint wheels is for {name}"
        raise RuntimeError(msg)
    (folder / "README.md").write_text(
        f"# @djlint/{name}\n\n"
        f"[djLint](https://djlint.com) {version} for {name}, with CPython {python_version}"
        " from [python-build-standalone](https://github.com/astral-sh/python-build-standalone)."
        f" djLint here is {'compiled with mypyc' if compiled else 'pure Python'}.\n\n"
        "Install [djlint](https://www.npmjs.com/package/djlint) rather than this package:"
        " it runs djLint with the package for your platform.\n",
        encoding="utf-8",
        newline="\n",
    )
    manifest = {
        "name": f"@djlint/{name}",
        "version": version,
        "description": f"djLint for {name}, which the djlint package runs",
        "homepage": "https://djlint.com",
        "bugs": {"url": "https://github.com/djlint/djLint/issues"},
        "license": "GPL-3.0-or-later",
        "repository": _REPOSITORY,
        "os": [system],
        "cpu": [cpu],
        **({"libc": ["glibc" if libc == ["gnu"] else "musl"]} if libc else {}),
        # Yarn's Plug'n'Play can't run Python out of a zip archive.
        "preferUnplugged": True,
        # The interpreter, which the launcher and the VS Code extension run
        # djLint with.
        "python": "python/python.exe" if windows else "python/bin/python3",
    }
    _write_manifest(folder, manifest)
    return _pack(folder)


def _build_launcher(version: str) -> Path:
    folder = _DIST / "djlint"
    folder.mkdir(parents=True)
    manifest = json.loads((_ROOT / "package.json").read_text(encoding="utf-8"))
    if manifest["version"] != version:
        msg = f"package.json has {manifest['version']} and pyproject.toml {version}"
        raise RuntimeError(msg)
    # The oldest Node the launcher runs on is the one esbuild builds it for, the first with
    # Object.hasOwn.
    target = re.search(
        r"--target=node(\d+(?:\.\d+){0,2})\b", manifest["scripts"]["esbuild-launcher"]
    )
    if target is None:
        msg = "the esbuild-launcher script in package.json has no --target=node"
        raise RuntimeError(msg)
    for field in ("devDependencies", "private", "scripts", "type"):
        manifest.pop(field, None)
    manifest |= {
        "bin": {"djlint": "djlint.mjs"},
        "files": ["djlint.mjs"],
        "optionalDependencies": {f"@djlint/{name}": version for name in PLATFORMS},
        "engines": {"node": f">={target[1]}"},
    }
    _write_manifest(folder, manifest)
    _run(_npm(), "run", "esbuild-launcher", "--", "--minify")
    for file in (_ROOT / "README.md", _ROOT / "LICENSE"):
        shutil.copy(file, folder)
    return _pack(folder)


def main(wheels: Path, platforms: list[str]) -> None:
    unknown = set(platforms) - PLATFORMS.keys()
    if unknown:
        msg = f"unknown platforms: {', '.join(sorted(unknown))}"
        raise SystemExit(msg)
    platforms = platforms or list(PLATFORMS)
    if os.name == "nt" and any(not name.startswith("win32-") for name in platforms):
        msg = "build the packages for Linux and macOS on Linux or macOS"
        raise SystemExit(msg)

    with (_ROOT / "pyproject.toml").open("rb") as file:
        version = tomllib.load(file)["project"]["version"]
    for path in _DIST.glob("*"):
        if path != _DOWNLOADS:
            _remove(path)
    python_version, hashes = _python_archives()
    licenses = _licenses()
    requirements = _requirements()
    packed = [_build_launcher(version)]
    packed.extend(
        _build_platform(
            name,
            wheels=wheels.resolve(),
            requirements=requirements,
            version=version,
            python_version=python_version,
            hashes=hashes,
            licenses=licenses,
        )
        for name in platforms
    )
    for path in packed:
        print(f"{path.name}: {path.stat().st_size / 2**20:.1f} MiB")


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if not arguments:
        raise SystemExit(__doc__)
    main(Path(arguments[0]), arguments[1:])
