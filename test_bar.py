from matplotlib import pyplot as plt

fig, ax = plt.subplots()

model = ["a", "b", "c", "d"]
err_rate = [0.2, 0.5, 0.1, 0.8]

for i in range(len(model)):
    ax.bar()
    ax.bar([model[i]], [err_rate[i]], weight, color="b")
a
plt.show()