import sys

(k, m, n) = [float(x) for x in sys.argv[1:4]]
pop = k+m+n

prob = 0
# Calculate total probability of selecting
#  k + any
prob += k/pop

#  m + k
prob += m/pop * k/(pop-1)

#  m + m (3/4)
prob += 0.75 * m/pop * (m-1)/(pop-1)

#  m + n (1/2)
prob += 0.5 * m/pop * n/(pop-1)

#  n + k
prob += n/pop * k/(pop-1)

#  n + m (1/2)
prob += 0.5 * n/pop * m/(pop-1)

print prob
print round(prob, 5)