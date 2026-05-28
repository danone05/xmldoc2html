from pathlib import Path
import subprocess


def main():
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    txt_report = reports_dir / "report.txt"
    print("Running tests")
    html_report = reports_dir / "report.html"

    with open(txt_report, "w", encoding="utf-8") as report_file:
        result = subprocess.run(
            [
                "pytest",
                "-v",
                f"--html={html_report}",
            ],
            stdout=report_file,
            stderr=subprocess.STDOUT,
            text=True,
        )

    print(f"TXT report saved: {txt_report}")

    if result.returncode == 0:
        print("All tests passed")
    else:
        print("Some tests failed")

if __name__ == "__main__":
    main()
