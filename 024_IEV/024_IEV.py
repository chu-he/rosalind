import sys

couples = [int(x) for x in sys.argv[1:7]]

dom = 0.0
# children per couple
cpc = 2.0

# 1: AA-AA
dom += couples[0] * 1

# 2: AA-Aa
dom += couples[1] * 1

# 3: AA-aa
dom += couples[2] * 1

# 4: Aa-Aa
dom += couples[3] * 0.75

# 5: Aa-aa
dom += couples[4] * 0.50

# 6: aa-aa
# 0


print dom * cpc