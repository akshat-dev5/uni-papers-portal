import subprocess
import time
import sys


def run_stage(script_name, description):
    """Runs a Python script as a separate process and checks for success."""

    print("\n" + "=" * 60)
    print(f"STARTING: {description}")
    print(f"Executing: {script_name}")
    print("=" * 60 + "\n")

    start_time = time.time()

    try:
        subprocess.run(
            [sys.executable, script_name],
            check=True
        )

        elapsed = time.time() - start_time

        print(f"\nSUCCESS: {description} completed in {elapsed:.2f} seconds.")
        return True

    except subprocess.CalledProcessError as e:

        print(f"\nFATAL ERROR: {script_name} failed with exit code {e.returncode}.")
        print("Pipeline halted.")
        return False

    except FileNotFoundError:

        print(f"\nERROR: Could not find script '{script_name}'.")
        return False


def main():

    print("=" * 60)
    print("AI DOCUMENT PROCESSING PIPELINE")
    print("Version 1.0")
    print("=" * 60)

    overall_start = time.time()

    stages = [
        ("stage2_decompose.py", "Stage 2: PDF Decomposition"),
        ("stage3_margin_wipe.py", "Stage 3: Configurable Margin Wipe"),
        ("stage4_ocr.py", "Stage 4: OCR Text Extraction"),
        ("stage5_watermark.py", "Stage 5: Heuristic Candidate Generation"),
        ("stage6_verify.py", "Stage 6: Geometric Verification"),
        ("stage7_fallback.py", "Stage 7: YOLOv8 ML Fallback"),
        ("stage8_fusion.py", "Stage 8: Detection Fusion"),
        ("stage9_restoration.py", "Stage 9: Adaptive Visual Restoration"),
        ("stage10_qa.py", "Stage 10: Automated QA Audit"),
        ("stage11_recovery.py", "Stage 11: Auto-Recovery System"),
        ("stage12_reconstruct.py", "Stage 12: PDF Reconstruction"),
        ("stage13_feedback.py", "Stage 13: MLOps Telemetry Sync")
    ]

    for script, description in stages:

        success = run_stage(script, description)

        if not success:
            sys.exit(1)

    total_time = time.time() - overall_start

    print("\n" + "=" * 60)
    print("PIPELINE EXECUTION COMPLETE")
    print(f"Total Runtime: {total_time:.2f} seconds")
    print(f"Total Runtime: {total_time/60:.2f} minutes")
    print("Check the final_outputs folder.")
    print("=" * 60)


if __name__ == "__main__":
    main()