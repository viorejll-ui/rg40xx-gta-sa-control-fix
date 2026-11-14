#!/usr/bin/env python3
"""Experimental GTA SA muOS-Keys -> virtual RG34XXSP compatible controller.
Requires root, /dev/input/event3 and /dev/uinput. No third-party modules.
Run only from GTA launcher; SIGTERM restores device.
"""
import os
import sys
import time
import fcntl
import struct
import signal
import select

SRC = '/dev/input/event3'
UINPUT = '/dev/uinput'
EV_SYN, EV_KEY, EV_ABS = 0, 1, 3
SYN_REPORT = 0
UI_SET_EVBIT = 0x40045564
UI_SET_KEYBIT = 0x40045565
UI_SET_ABSBIT = 0x40045567
UI_DEV_CREATE = 0x5501
UI_DEV_DESTROY = 0x5502
EVIOCGRAB = 0x40044590
# The binary identifies the virtual-pad special case by its input-device name.
# This candidate name is deliberately reported in logs for verification.
VIRTUAL_NAME = b'GTASA-Remap'

# RG40XX H muOS-Keys button codes -> old RG34XXSP profile button codes.
KEY_MAP = {
    304: 304, 305: 305, 307: 306, 308: 307,
    310: 308, 311: 309, 312: 314, 313: 315,
    314: 310, 315: 311, 316: 312, 317: 313, 318: 316,
}
# Original axes X/Y/RX/RY -> the RG34XXSP layout expected by the binary.
AXIS_MAP = {0: 2, 1: 3, 3: 4, 4: 5, 16: 16, 17: 17}
DEADZONE = 1024
FMT = 'llHHi' # native 64-bit Linux input_event
EVENT_SIZE = struct.calcsize(FMT)
sfd = None
ufd = None
created = False
grabbed = False
running = True


def log(message):
    print('[axis_remap] ' + message, flush=True)


def on_signal(_sig, _frame):
    global running
    running = False


def write_event(kind, code, value):
    # Time fields can be zero for uinput events.
    os.write(ufd, struct.pack(FMT, 0, 0, kind, code, value))


def cleanup():
    global created, grabbed
    if grabbed and sfd is not None:
        try: fcntl.ioctl(sfd, EVIOCGRAB, 0)
        except OSError: pass
        grabbed = False
    if created and ufd is not None:
        try: fcntl.ioctl(ufd, UI_DEV_DESTROY)
        except OSError: pass
        created = False
    for fd in (sfd, ufd):
        if fd is not None:
            try: os.close(fd)
            except OSError: pass


def main():
    global sfd, ufd, created, grabbed
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    sfd = os.open(SRC, os.O_RDONLY | os.O_NONBLOCK)
    ufd = os.open(UINPUT, os.O_WRONLY | os.O_NONBLOCK)
    for et in (EV_KEY, EV_ABS):
        fcntl.ioctl(ufd, UI_SET_EVBIT, et)
    for key in sorted(set(KEY_MAP.values()) | {114, 115}):
        fcntl.ioctl(ufd, UI_SET_KEYBIT, key)
    for axis in sorted(set(AXIS_MAP.values())):
        fcntl.ioctl(ufd, UI_SET_ABSBIT, axis)

    # legacy struct uinput_user_dev: name[80], input_id 4x u16, ff_effects_max u32,
    # absmax/min/fuzz/flat arrays of 64 signed ints each.
    name = VIRTUAL_NAME.ljust(80, b'\0')
    ids = struct.pack('HHHHI', 0x03, 0x756d, 0x7079, 0x0001, 0)
    maxs = [0]*64; mins=[0]*64; fuzz=[0]*64; flat=[0]*64
    for axis in (2,3,4,5):
        mins[axis] = -32767; maxs[axis] = 32767; flat[axis] = DEADZONE
    for axis in (16,17):
        mins[axis] = -1; maxs[axis] = 1
    payload = name + ids + struct.pack('256i', *(maxs + mins + fuzz + flat))
    os.write(ufd, payload)
    fcntl.ioctl(ufd, UI_DEV_CREATE)
    created = True
    time.sleep(0.25)
    # Exclusive grab prevents double input from the real node while GTA runs.
    fcntl.ioctl(sfd, EVIOCGRAB, 1)
    grabbed = True
    log('READY virtual=' + VIRTUAL_NAME.decode() + ' source=' + SRC)
    pending = b''
    last = {axis: 0 for axis in AXIS_MAP if axis not in (16,17)}
    while running:
        readable, _, _ = select.select([sfd], [], [], 0.2)
        if not readable: continue
        try:
            chunk = os.read(sfd, EVENT_SIZE * 64)
        except BlockingIOError:
            continue
        if not chunk: continue
        pending += chunk
        while len(pending) >= EVENT_SIZE:
            block, pending = pending[:EVENT_SIZE], pending[EVENT_SIZE:]
            sec, usec, kind, code, value = struct.unpack(FMT, block)
            if kind == EV_KEY:
                if code in KEY_MAP:
                    write_event(EV_KEY, KEY_MAP[code], value)
                elif code in (114,115):
                    write_event(EV_KEY, code, value)
            elif kind == EV_ABS and code in AXIS_MAP:
                if code not in (16,17):
                    value = 0 if -DEADZONE < value < DEADZONE else value
                    if value == last[code]: continue
                    last[code] = value
                write_event(EV_ABS, AXIS_MAP[code], value)
            elif kind == EV_SYN and code == SYN_REPORT:
                write_event(EV_SYN, SYN_REPORT, 0)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        log('ERROR: ' + repr(exc))
        sys.exit(1)
    finally:
        cleanup()
