import sys

threshold = float(sys.argv[1])
score = float(input())

print("PASS" if score >= threshold else "FAIL: %f" % score)
