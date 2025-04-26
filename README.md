# ReVanced Magisk Module

> **Note:** This fork’s primary goal is to **add most popular apps** that aren’t in the original repo, providing an even wider range of ReVanced/Extended patches out of the box.  
> **Additionally**, all apps are built as **APKs and Magisk modules**, but this project focuses **only on the armv8** architecture.

## Extensive ReVanced Builder

Utilize [**zygisk-detach**](https://github.com/j-hc/zygisk-detach) to detach YouTube and YouTube Music from the Play Store if you are using Magisk modules.

### Features

- Support all current and future [ReVanced](https://github.com/revanced/revanced-patches) and [ReVanced Extended](https://github.com/inotia00/revanced-patches) apps
- Build Magisk modules and non-root APKs
- Daily updates with the latest versions of apps and patches
- Optimize APKs and modules for size
- Modules:
  - Recompile invalidated odex for faster usage
  - Receive updates from the Magisk app
  - Do not break SafetyNet or trigger root detections
  - Handle the installation of the correct version of the stock app
  - Support Magisk and KernelSU

Note that the [CI workflow](../../actions/workflows/ci.yml) is scheduled to build the modules and APKs daily using GitHub Actions if there is a change in ReVanced patches. You may want to disable it.

## To Include/Exclude Patches or Patch Other Apps

[**View the List of Patches**](https://j-hc.github.io/rvmm-config-gen/)

- Star the repo :eyes:
- [Fork the repo](https://github.com/j-hc/revanced-magisk-module/fork) or use it as a template
- Customize [`config.toml`](./config.toml) using [rvmm-config-gen](https://j-hc.github.io/rvmm-config-gen/)
- Run the build [workflow](../../actions/workflows/build.yml)
- Grab your modules and APKs from [releases](../../releases)

Also, see [`CONFIG.md`](./CONFIG.md) for more details.

## Building Locally

### On Termux

```bash
bash <(curl -sSf https://raw.githubusercontent.com/j-hc/revanced-magisk-module/main/build-termux.sh)
```

### On Desktop

```bash
git clone https://github.com/j-hc/revanced-magisk-module
cd revanced-magisk-module
./build.sh
```

## Contributions

We welcome contributions to improve this project. Please feel free to submit pull requests, open issues, or contact the maintainers for any suggestions or questions.

Happy building!
