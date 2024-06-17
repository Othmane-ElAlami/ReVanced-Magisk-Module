# ReVanced Magisk Module

## Extensive ReVanced Builder

Utilize [**zygisk-detach**](https://github.com/j-hc/zygisk-detach) to detach YouTube and YouTube Music from the Play Store if you are using Magisk modules.

<details>
<summary><big>Features</big></summary>
<ul>
  <li>Support all current and future ReVanced and <a href="https://github.com/inotia00/revanced-patches">ReVanced Extended</a> apps</li>
  <li>Build Magisk modules and non-root APKs</li>
  <li>Daily updates with the latest versions of apps and patches</li>
  <li>Optimize APKs and modules for size</li>
  <li>Modules</li>
  <ul>
    <li>Recompile invalidated odex for faster usage</li>
    <li>Receive updates from the Magisk app</li>
    <li>Do not break SafetyNet or trigger root detections</li>
    <li>Handle the installation of the correct version of the stock app</li>
    <li>Support Magisk and KernelSU</li>
  </ul>
</ul>
Note that the <a href="../../actions/workflows/ci.yml">CI workflow</a> is scheduled to build the modules and APKs daily using GitHub Actions if there is a change in ReVanced patches. You may want to disable it.
</details>

## To Include/Exclude Patches or Patch Other Apps

[**View the List of Patches**](https://j-hc.github.io/rvmm-config-gen/)

- Star the repo :eyes:
- [Fork the repo](https://github.com/j-hc/revanced-magisk-module/fork) or use it as a template
- Customize [`config.toml`](./config.toml) using [rvmm-config-gen](https://j-hc.github.io/rvmm-config-gen/)
- Run the build [workflow](../../actions/workflows/build.yml)
- Grab your modules and APKs from [releases](../../releases)

Also see [`CONFIG.md`](./CONFIG.md) for more details.

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
