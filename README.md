# ReVanced Magisk Module (Fork)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/rvc_magisk)
[![Automated CI Build](https://github.com/Othmane-ElAlami/ReVanced-Magisk-Module/actions/workflows/ci.yml/badge.svg?event=schedule)](https://github.com/Othmane-ElAlami/ReVanced-Magisk-Module/actions/workflows/ci.yml)

Extensive ReVanced & Morphe builder.

> **Note:** This is a fork of [j-hc/revanced-magisk-module](https://github.com/j-hc/revanced-magisk-module).
> This fork is customized for advanced batch building with more resilient error handling and dynamic release title generation. By default, its configuration builds apps from the **ReVanced** and **Morphe** patch ecosystems, with additional ecosystems (like **Piko**) preconfigured for easy enablement.

Get the [latest CI release](https://github.com/Othmane-ElAlami/ReVanced-Magisk-Module/releases).

Use [**zygisk-detach**](https://github.com/j-hc/zygisk-detach) to detach YouTube and YT Music from the Play Store if you are using Magisk modules.

<details><summary><big>Features</big></summary>
<ul>
 <li> <b>Fork features:</b></li>
    <ul>
     <li> Robust batch building: A failure in one app's build does not stop the entire batch process.</li>
     <li> Dynamic GitHub Release titles and clean Markdown summaries based on detected patch ecosystems and generated artifacts.</li>
    </ul>
 <li> <b>Core builder features:</b></li>
    <ul>
     <li> Supports building from multiple patch ecosystems simultaneously (Morphe, ReVanced, Extended, Piko, etc.).</li>
     <li> Can build Magisk modules and non-root APKs.</li>
     <li> Optimizes APKs and modules for size.</li>
     <li> Modules:</li>
        <ul>
         <li> recompile invalidated odex for faster usage</li>
         <li> receive updates from Magisk app</li>
         <li> do not break safetynet or trigger root detections</li>
         <li> handle installation of the correct version of the stock app</li>
         <li> support Magisk and KernelSU</li>
        </ul>
    </ul>
</ul>
</details>

## Customizing Builds

* **Fork this repository** to build your own apps via GitHub Actions.
* Customize [`config.toml`](./config.toml) to specify which apps, patch ecosystems, and versions to build.
  *(Note: You can use the upstream [rvmm-config-gen](https://j-hc.github.io/rvmm-config-gen/) tool to help generate configs, but make sure to review the output against this fork's capabilities).*
* See [`CONFIG.md`](./CONFIG.md) for detailed configuration explanations.
* Run the manual build [workflow](https://github.com/Othmane-ElAlami/ReVanced-Magisk-Module/actions/workflows/build.yml) or wait for the scheduled CI.
* Grab your customized modules and APKs from [releases](https://github.com/Othmane-ElAlami/ReVanced-Magisk-Module/releases).

## Troubleshooting Modules

If you are having trouble with the classic mount method of the modules, such as:
- **"Reflash needed"** error after reboots
- **"Suspicious mount detected"** warnings from root detector apps

You can consider using [rvmm-zygisk-mount](https://github.com/j-hc/rvmm-zygisk-mount).

## Building Locally

### On Termux
```console
bash <(curl -sSf https://raw.githubusercontent.com/Othmane-ElAlami/ReVanced-Magisk-Module/master/build-termux.sh)
```

### On Linux
```console
$ git clone https://github.com/Othmane-ElAlami/ReVanced-Magisk-Module --depth 1
$ cd ReVanced-Magisk-Module
$ ./build.sh
```

## Credits
* Huge thanks to [j-hc](https://github.com/j-hc) for the original robust upstream repository and extensive build scripts.
