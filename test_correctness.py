import csv

from common import generate_keypair, load_module, safe_verify


PARAM_NAME = "SLH-DSA-SHA2-128s"
MODULE_NAME = "pyspx.sha2_128s"

message = b"software-release-file-v1.0"
spx = load_module(MODULE_NAME)

pk, sk = generate_keypair(spx)
sig = spx.sign(message, sk)

wrong_pk, _ = generate_keypair(spx)

tampered_message = bytearray(message)
tampered_message[0] ^= 1

tampered_sig = bytearray(sig)
tampered_sig[0] ^= 1

results = [
    ["original file", "success", safe_verify(spx, message, sig, pk)],
    ["tampered file", "failure", safe_verify(spx, bytes(tampered_message), sig, pk)],
    ["tampered signature", "failure", safe_verify(spx, message, bytes(tampered_sig), pk)],
    ["wrong public key", "failure", safe_verify(spx, message, sig, wrong_pk)],
]

with open("results/correctness_results.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["test_case", "expected_result", "actual_verify_result", "pass_or_fail"])
    for case, expected, actual in results:
        passed = (expected == "success" and actual) or (expected == "failure" and not actual)
        writer.writerow([case, expected, actual, "PASS" if passed else "FAIL"])

print("Experiment 1 finished: results/correctness_results.csv")
for row in results:
    print(row)
