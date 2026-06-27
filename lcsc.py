import argparse
import os
import subprocess
import sys
import shutil


def run(input_file, output_dir, python_exec="python"):
    input_file = os.path.abspath(input_file)
    output_prefix = os.path.join(os.path.abspath(output_dir), "lcsc")

    if not os.path.isfile(input_file):
        print(f"❌ File not found: {input_file}")
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        ids = [l.strip() for l in f if l.strip() and not l.lstrip().startswith("#")]

    if not ids:
        print("No LCSC IDs found.")
        return

    print(f"Found {len(ids)} component(s)\n")
    ok, fail = 0, 0

    for i, lcsc_id in enumerate(ids, 1):
        print(f"[{i}/{len(ids)}] {lcsc_id} ", end="", flush=True)
        cmd = [
            python_exec, "-m", "easyeda2kicad",
            "--full",
            f"--lcsc_id={lcsc_id}",
            f"--output={output_prefix}",
            "--overwrite"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅")
            ok += 1
        else:
            print("❌")
            if result.stderr:
                for line in result.stderr.strip().splitlines():
                    print(f"   {line}")
            fail += 1

    print(f"\n{'='*40}")
    print(f"✅ {ok} succeeded   ❌ {fail} failed")
    print(f"Output: {os.path.abspath(output_dir)}")
    print(f"  sym:  lcsc.kicad_sym")
    print(f"  fp:   lcsc.pretty/")
    print(f"  3d:   lcsc.3dshapes/")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = "F:/POWERBANKV1.0"

    parser = argparse.ArgumentParser(description="Batch LCSC → KiCad converter")
    parser.add_argument("input_file", nargs="?", default=f"{project_dir}/lcsc.txt")
    parser.add_argument("output_dir", nargs="?", default=f"{project_dir}/lib/lcsc")
    parser.add_argument("--python", dest="python_exec", default="python")
    args = parser.parse_args()
    run(args.input_file, args.output_dir, args.python_exec)


if __name__ == "__main__":
    main()