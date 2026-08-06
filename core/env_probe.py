# -*- coding: utf-8 -*-
"""Environment probe: are this installation's data files really on this disk?

WHY THIS EXISTS. A file-sync client (OneDrive Files On-Demand, Dropbox Smart
Sync, iCloud, Google Drive) can keep a file ONLY in the cloud and leave a
placeholder on disk. Reading such a file blocks the process while the operating
system downloads it -- silently, with no error and no progress. Measured here on
2026-08-07: a gate that costs 0.3s stalled past a 300-second timeout because the
sync client was busy with files that had just been written.

WHY IT IS NOT THE USER'S JOB. Telling people "go tick Always keep on this
device" is the same delegate-to-the-consumer answer this project rejected in the
SNI round: an integration that occasionally freezes with no explanation gets
switched off, and no one reads the manual to discover why. So the system detects
the condition itself and says what is happening in one plain sentence, before the
wait rather than after it.

HOW IT IS CHEAP. Placeholder state is an ATTRIBUTE, not content: on Windows
GetFileAttributesW answers without opening the file, so the whole probe costs a
handful of syscalls and never triggers the very download it is warning about.
FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS (0x400000) means "reading this WILL fetch
from the network"; FILE_ATTRIBUTE_OFFLINE (0x1000) is the older equivalent. On
platforms without that API the probe reports UNSUPPORTED and stays silent -- an
unknown environment must not produce a scary message it cannot justify.

CONTRACT: report-only and side-effect-free. It reads no file contents, changes
no verdict, and is never consulted by any decision path.
"""
import ctypes
import os
import sys

_RECALL_ON_DATA_ACCESS = 0x00400000
_OFFLINE = 0x00001000
_RECALL_ON_OPEN = 0x00040000
_INVALID = 0xFFFFFFFF

# Files whose absence-from-disk would stall an analysis: the pinned Unicode
# tables every axis reads, the vendored domain registries, and the cards. Listed
# as directories so a new pinned table is covered without editing this list.
_DATA_DIRS = (
    os.path.join("data", "unicode"),
    os.path.join("data", "unicode", "conformance"),
    os.path.join("data", "net"),
    "cards",
)

_CACHED = None


def _win_getattrs():
    """GetFileAttributesW with its types declared. Without an explicit restype
    ctypes assumes a SIGNED int, so the documented failure value
    INVALID_FILE_ATTRIBUTES (0xFFFFFFFF) arrives as -1 -- and -1 has every bit
    set, so a missing file would answer yes to every attribute test. Caught by
    this module's gate, which asks whether a nonexistent path is a placeholder."""
    fn = ctypes.windll.kernel32.GetFileAttributesW
    fn.argtypes = [ctypes.c_wchar_p]
    fn.restype = ctypes.c_uint32
    return fn


def _attributes(path):
    """Windows file attributes, or None where the API is unavailable or the
    path cannot be queried (missing, denied, malformed)."""
    if not sys.platform.startswith("win"):
        return None
    try:
        attrs = _win_getattrs()(str(path))
    except (AttributeError, OSError, ValueError):
        return None
    if attrs == _INVALID:
        return None
    return attrs


def is_cloud_placeholder(path) -> bool:
    """True when reading `path` would fetch it from a sync service first.

    False for a normal local file AND wherever the question cannot be answered
    -- the probe never guesses, because a false alarm about the user's disk is
    worse than silence."""
    attrs = _attributes(path)
    if attrs is None:
        return False
    return bool(attrs & (_RECALL_ON_DATA_ACCESS | _OFFLINE | _RECALL_ON_OPEN))


def probe(base_dir=None) -> dict:
    """Check the installation's data files. Returns:

      status  -- OK / CLOUD_PLACEHOLDERS_PRESENT / UNSUPPORTED
      pending -- repo-relative paths whose first read would block
      checked -- how many files were examined
      message -- one plain sentence for a human, or "" when there is nothing
                 to say. Written for someone who has never heard of file
                 sync placeholders and should not have to learn.
    """
    base = base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not sys.platform.startswith("win"):
        return {"status": "UNSUPPORTED", "pending": [], "checked": 0,
                "message": "", "platform": sys.platform}
    pending, checked = [], 0
    for rel in _DATA_DIRS:
        directory = os.path.join(base, rel)
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            full = os.path.join(directory, name)
            if not os.path.isfile(full):
                continue
            checked += 1
            if is_cloud_placeholder(full):
                pending.append(os.path.join(rel, name).replace("\\", "/"))
    if not pending:
        return {"status": "OK", "pending": [], "checked": checked, "message": ""}
    return {
        "status": "CLOUD_PLACEHOLDERS_PRESENT",
        "pending": pending,
        "checked": checked,
        "message": (
            "%d of this installation's %d data files are stored online rather "
            "than on this disk (a file-sync service is managing this folder). "
            "The first analysis may pause while they download -- that pause is "
            "the download, not the analyzer. Results are unaffected."
            % (len(pending), checked)),
    }


def status(base_dir=None) -> dict:
    """Cached probe: the answer cannot change mid-process in a way that matters,
    and a per-analysis probe would add syscalls to every call."""
    global _CACHED
    if _CACHED is None:
        _CACHED = probe(base_dir)
    return _CACHED
