# Architecture

Status: draft, derived from the Surma chats of 2026-11-07..11 and the
decision log. Nothing here is implemented yet.

## One layer, five foundations

Surma is not five operating systems. It is one over-layer made once and
carried over five bases, so that only the foundation differs:

```
        surma-shell / surma-apps / surma-sensord
                          |
     +---------+----------+----------+---------+
     |         |          |          |         |
   [1]       [2]        [3]        [4]        [5]
   linux    linux+bsd    bsd      bsd+linux   windows
```

| # | Branch    | Foundation                                          | Phone realism            |
|---|-----------|-----------------------------------------------------|--------------------------|
| 1 | linux     | mainline Linux, postmarketOS-style base             | primary target           |
| 2 | linux+bsd | Linux kernel, BSD userland (Chimera Linux pattern)  | cheap variation of [1]   |
| 3 | bsd       | FreeBSD / NetBSD / OpenBSD                          | laptops, servers, x86 tablets first |
| 4 | bsd+linux | FreeBSD + Linuxulator + LinuxKPI                    | apps solved, phone hardware not |
| 5 | windows   | Renegade UEFI, user-supplied Windows ARM64 image    | last; device-dependent   |

Precedents noted in the chats: Debian GNU/kFreeBSD (dormant for lack of
maintainers), Chimera Linux (Linux kernel, BSD userland), FreeBSD
Linuxulator and LinuxKPI, Renegade Project (UEFI on phones: Lumia 950/950
XL, Surface Duo, POCO F1 and other Snapdragon devices).

## Shared layer

- `surma-shell` — the interface. Wayland compositor on wlroots (C) or
  Smithay (Rust); light toolkit; the recognisable part of Surma.
  Ubuntu Touch is remembered for Lomiri but survives on Halium; Surma
  wants the shell to define the project the way the basement defines
  whether it boots at all.
- `surma-apps` — minimal set: launcher, settings, phone/tablet basics.
- `surma-sensord` — kernel-independent sensor daemon, one API (D-Bus or
  socket), pluggable backends. This is the project's signature piece:

| Backend       | Kernel   | Covers                                           |
|---------------|----------|--------------------------------------------------|
| iio           | mainline | plain IIO sensors through iio-sensor-proxy or direct |
| qcom-ssc      | mainline | modern Qualcomm: Sensor Core DSP via libssc + hexagonrpcd, data files under /usr/share/qcom |
| halium        | android  | vendor HALs through libhybris (transitional)     |
| bsd-hwsensors | BSD      | OpenBSD hw.sensors, NetBSD envsys                |

On modern Qualcomm chips sensors are not plain IIO devices: they sit
behind the Snapdragon Sensor Core DSP. Any Linux backend must therefore
speak to libssc, with iio-sensor-proxy as a facade where it helps.
On BSD there is no equivalent known to the project; bsd-hwsensors covers
what the kernels expose and no more.

## Own Halium replacement (direction, not yet design)

Halium runs an Android kernel and vendor HALs and exposes them to glibc
userland through libhybris — a working crutch on hundreds of devices, not
a clean design. The stated direction is to replace it over time:

1. Talk to vendor services over binder directly (binderfs), with own
   clean code, no libhybris.
2. Mainline where mainline works, own HAL layer where it does not —
   the realistic hybrid the project is expected to land on.

Not replaceable by anyone: the kernel stays Linux on phones; modem,
camera ISP, DSP and bootloader firmware run on separate signed cores.

## Android application compatibility

Waydroid-class approach: full Android in an LXC container on the same
kernel, windows in the Wayland compositor. Requirements: binder/binderfs,
memfd/ashmem, cgroups, namespaces, a working GPU driver. Costs: roughly
1 GB or more of RAM — so it runs lazily, started on demand, unloaded
after. Google apps are never bundled; microG or user-installed GApps.

The far-future direction is an own runtime without a container; for now
the container is the accepted compatibility module. AOSP is Apache-2.0,
so the pattern is free to embed.

## Light stack

- musl, busybox; runit or OpenRC, not systemd
- wlroots-based compositor (C) or Smithay (Rust)
- toolkits from the light end: LVGL, EFL, Slint, GTK without baggage;
  heavy Qt/QML, Electron, JVM, Python avoided in the basement
- zram, zswap, few resident processes, lazy loading of heavy things
- measured from day one: smem, ps_mem, per-build graphs. Lightness that
  is not measured is a feeling, not a property

Budget: a working interface in 1 GB of RAM or less.
