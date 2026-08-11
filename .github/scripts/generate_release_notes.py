
import re
import glob
import os
import datetime

def generate_release_notes(build_dir="build", build_md_path="build.md", date_str=None):
    if date_str is None:
        date_str = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
        
    patch_lines = []
    skipped = []
    
    if os.path.exists(build_md_path):
        with open(build_md_path, 'r', encoding='utf-8') as f:
            lines = f.read().strip().splitlines()
            
        in_skipped = False
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.startswith("Skipped:"):
                in_skipped = True
                continue
            if in_skipped:
                skipped.append(line)
                continue
                
            if line.startswith("Patches:"):
                patch_lines.append(line.split(":", 1)[1].strip())
                
    ecosystems = {}
    for p in patch_lines:
        brand = None
        if re.search(r"morphe", p, re.IGNORECASE): brand = "Morphe"
        elif re.search(r"crimera|piko", p, re.IGNORECASE): brand = "Piko"
        elif re.search(r"extended", p, re.IGNORECASE): brand = "Extended"
        elif re.search(r"revanced", p, re.IGNORECASE): brand = "ReVanced"
        
        if brand:
            ver_match = re.search(r"-v?([0-9]+(?:\.[0-9]+)+(?:-[a-zA-Z0-9.-]+)?)", p)
            ver = ver_match.group(1) if ver_match else None
            
            if brand not in ecosystems:
                ecosystems[brand] = set()
            if ver:
                ecosystems[brand].add(ver)
                
    brands = list(ecosystems.keys())
    # Deterministic sorting
    priority = ["Morphe", "ReVanced", "Piko", "Extended"]
    brands.sort(key=lambda x: priority.index(x) if x in priority else len(priority) + brands.index(x))
    
    if not brands:
        title = f"Modules Release ({date_str})"
    elif len(brands) == 1:
        brand = brands[0]
        vers = list(ecosystems[brand])
        if len(vers) == 1 and re.match(r"^[0-9]", vers[0]):
            title = f"{brand} {vers[0]} ({date_str})"
        else:
            title = f"{brand} Release ({date_str})"
    else:
        joined = " & ".join(brands)
        title = f"{joined} Release ({date_str})"
        
    artifacts = glob.glob(f"{build_dir}/*")
    apps = {}
    for a in artifacts:
        name = os.path.basename(a)
        if name == 'dummy': continue
        
        # Ext
        if not (name.endswith('.apk') or name.endswith('.zip')):
            continue
            
        name_no_ext = name.rsplit(".", 1)[0]
        ext = name.rsplit(".", 1)[1]
        
        # Check architecture explicitly
        arch = "unknown"
        for possible_arch in ["-all", "-arm64-v8a", "-arm-v7a", "-x86_64", "-x86"]:
            if name_no_ext.endswith(possible_arch):
                arch = possible_arch[1:]
                name_no_ext = name_no_ext[:-len(possible_arch)]
                break
                
        # Now name_no_ext should be something like youtube-morphe-module-v21.04.223
        if "-v" in name_no_ext:
            parts = name_no_ext.rsplit("-v", 1)
            app_name = parts[0]
            if app_name.endswith("-module"): app_name = app_name[:-7]
            version = parts[1]
            
            key = f"{app_name}_{version}_{arch}"
            if key not in apps:
                apps[key] = {
                    "name": app_name.replace("-", " ").title(),
                    "version": version,
                    "arch": arch,
                    "outputs": []
                }
                
            if ext == "apk" and "APK" not in apps[key]["outputs"]:
                apps[key]["outputs"].append("APK")
            if ext == "zip" and "Module" not in apps[key]["outputs"]:
                apps[key]["outputs"].append("Module")
                
    successful_apps = sorted(list(apps.values()), key=lambda x: (x["name"], x["arch"]))
    
    body_lines = ["## Build Summary"]
    if successful_apps:
        body_lines.append(f"Successfully generated **{len(successful_apps)}** build variants.\n")
        body_lines.append("| App | Version | Architecture | Outputs |")
        body_lines.append("|---|---|---|---|")
        for app in successful_apps:
            outs = ", ".join(sorted(app["outputs"]))
            body_lines.append(f"| {app['name']} | {app['version']} | {app['arch']} | {outs} |")
    else:
        body_lines.append("No apps were successfully generated.\n")
        
    if patch_lines:
        body_lines.append("\n## Patch Sets")
        for p in patch_lines:
            if "/" in p:
                parts = p.split("/", 1)
                body_lines.append(f"- **{parts[0]}**: `{parts[1]}`")
            else:
                body_lines.append(f"- `{p}`")
                
    if skipped:
        body_lines.append("\n## Skipped / Failed")
        for s in skipped:
            body_lines.append(f"- {s}")
            
    body_lines.append(f"\n*Build Date: {date_str}*")
    
    return title, "\n".join(body_lines)

if __name__ == "__main__":
    title, body = generate_release_notes()
    
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        import secrets
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"RELEASE_TITLE={title}\n")
            delim = secrets.token_hex(8)
            f.write(f"BUILD_LOG<<{delim}\n")
            f.write(body + "\n")
            f.write(f"{delim}\n")
    else:
        # Fallback for manual testing
        print("RELEASE_TITLE=" + title)
        print("BUILD_LOG:\n" + body)
