# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""Factorio Legendary Item Probability Calculator
This script calculates the probability of obtaining a legendary item in
Factorio, given various factory setups, and presents the information via
generated plots. Along the way, I reproduced a few tables from the Factorio
wiki:
https://wiki.factorio.com/Quality#Optimal_module_usage

Usage:
uv run factorio-legendary.py
"""
import matplotlib.pyplot as plt
import numpy as np


def get_unit_vector(n, k):
    a = np.zeros(n)
    a[k - 1] = 1
    return a


def get_transition_matrix(n_p, n_q, base_p, zero_rows=None):
    if zero_rows is None:
        zero_rows = []

    p = base_p + n_p * 0.25
    q = n_q * 0.062

    # Define the transition vectors
    a1 = (1 + p) * np.array([(1 - q), q * (1 - 1e-1), q * (1e-1 - 1e-2), q * (1e-2 - 1e-3), q * 1e-3])
    a2 = (1 + p) * np.array([0, (1 - q), q * (1 - 1e-1), q * (1e-1 - 1e-2), q * 1e-2])
    a3 = (1 + p) * np.array([0, 0, (1 - q), q * (1 - 1e-1), q * 1e-1])
    a4 = (1 + p) * np.array([0, 0, 0, (1 - q), q])
    a5 = (1 + base_p + (n_q + n_p) * 0.25) * get_unit_vector(5, 5)

    # Recycler q
    rq = 4 * 0.062
    a6 = (1 - 0.75) * np.array([(1 - rq), rq * (1 - 1e-1), rq * (1e-1 - 1e-2), rq * (1e-2 - 1e-3), rq * 1e-3])
    a7 = (1 - 0.75) * np.array([0, (1 - rq), rq * (1 - 1e-1), rq * (1e-1 - 1e-2), rq * 1e-2])
    a8 = (1 - 0.75) * np.array([0, 0, (1 - rq), rq * (1 - 1e-1), rq * 1e-1])
    a9 = (1 - 0.75) * np.array([0, 0, 0, (1 - rq), rq])

    a10 = get_unit_vector(10, 10)

    # Create the transition matrix
    T = np.zeros((10, 10))

    for i in range(1, 11):  # Matlab-like indexing
        if i in zero_rows:
            T[i - 1] = np.zeros(10)
        else:
            if i == 1:
                T[i - 1] = np.concatenate([np.zeros(5), a1])
            elif i == 2:
                T[i - 1] = np.concatenate([np.zeros(5), a2])
            elif i == 3:
                T[i - 1] = np.concatenate([np.zeros(5), a3])
            elif i == 4:
                T[i - 1] = np.concatenate([np.zeros(5), a4])
            elif i == 5:
                T[i - 1] = np.concatenate([np.zeros(5), a5])
            elif i == 6:
                T[i - 1] = np.concatenate([a6, np.zeros(5)])
            elif i == 7:
                T[i - 1] = np.concatenate([a7, np.zeros(5)])
            elif i == 8:
                T[i - 1] = np.concatenate([a8, np.zeros(5)])
            elif i == 9:
                T[i - 1] = np.concatenate([a9, np.zeros(5)])
            elif i == 10:
                T[i - 1] = a10

    return T


def get_legendary_fraction(n_p, n_q, base_p, zero_rows=None):
    if zero_rows is None:
        zero_rows = []

    T = get_transition_matrix(n_p, n_q, base_p, zero_rows)
    # Transpose so we can multiply it on the right
    T = np.linalg.matrix_transpose(T)

    # Create unit vector [1,0,0,...,0]
    initial_state = get_unit_vector(10, 1)

    # Calculate the state after 100 iterations
    final_state = np.linalg.matrix_power(T, 1000) @ initial_state

    # Return the 10th element (equivalent to Mathematica indexing)
    return final_state[9]


# Analysis of optimal allocation between p and q
def analyze_slot_allocation(total_slots=8, base_p=0):
    # Define the trade-off parameters
    p_increment = 0.25  # Each slot gives +0.25 to p
    q_increment = 0.062  # Each slot gives +0.062 to q

    # Initialize results arrays
    slot_allocations = []
    yields = []

    # Try different allocations
    for p_slots in range(total_slots + 1):
        q_slots = total_slots - p_slots

        p_value = base_p + p_slots * p_increment
        q_value = q_slots * q_increment

        # Calculate yield for this allocation
        yield_value = get_legendary_fraction(p_slots, q_slots, base_p)

        slot_allocations.append(p_slots)
        yields.append(yield_value)

        print(
            f"Slots for p: {p_slots}, Slots for q: {q_slots}, p={p_value:.3f}, q={q_value:.3f}, Yield={yield_value:.6f}"
        )

    # Find the optimal allocation
    optimal_index = np.argmax(yields)
    optimal_p_slots = slot_allocations[optimal_index]
    optimal_q_slots = total_slots - optimal_p_slots
    optimal_yield = yields[optimal_index]

    print(f"\nOptimal allocation: {optimal_p_slots} slots for p, {optimal_q_slots} slots for q")
    print(
        f"Optimal p value: {base_p + optimal_p_slots * p_increment:.3f}, Optimal q value: {optimal_q_slots * q_increment:.3f}"
    )
    print(f"Maximum yield: {optimal_yield:.6f}")
    print(f"Number of crafts: {int(np.ceil(1 / optimal_yield))}")

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(slot_allocations, yields, "o-", linewidth=2)
    plt.scatter([optimal_p_slots], [optimal_yield], color="red", s=100, zorder=5)

    plt.xlabel("Number of Slots Allocated to p")
    plt.ylabel("Yield (Legendary Fraction)")
    plt.title(
        f"Yield vs. Allocation of Slots Between p and q Parameters (Total Slots: {total_slots}, Start p: {base_p})"
    )
    plt.grid(True)

    # Add text annotations
    plt.annotate(
        f"Optimal: {optimal_p_slots} slots for p, {optimal_q_slots} slots for q\nYield: {optimal_yield:.6f} (Number of crafts: {int(np.ceil(1 / optimal_yield))})",
        xy=(optimal_p_slots, optimal_yield),
        xytext=(optimal_p_slots + 0.5, optimal_yield),
        arrowprops=dict(facecolor="black", shrink=0.05, width=1.5),
    )

    # Add secondary x-axis for q slots
    ax2 = plt.gca().twiny()
    ax2.set_xlabel("Number of Slots Allocated to q")
    ax2.set_xlim(plt.gca().get_xlim())
    ax2.set_xticks(range(total_slots + 1))
    ax2.set_xticklabels([total_slots - i for i in range(total_slots + 1)])

    plt.tight_layout()
    plt.savefig(f"slot_allocation_analysis_{total_slots}_slots_start_p_{base_p}.png")
    plt.show()

    return slot_allocations, yields, optimal_p_slots, optimal_q_slots, optimal_yield


def main():
    print("Hello from factorio-legendary-calc!")

    # Run the analysis for different scenarios
    scenarios = [
        (2, 0),  # total_slots 2, start_p 0
        (3, 0),  # total_slots 3, start_p 0
        (4, 0),  # total_slots 4, start_p 0
        (4, 0.5),  # total_slots 4, start_p 0.5
        (5, 0.5),  # total_slots 5, start_p 0.5
        (8, 0),  # total_slots 8, start_p 0 (current)
    ]

    for total_slots, start_p in scenarios:
        print(f"\n\n=== Analysis for {total_slots} total slots with start_p={start_p} ===")
        slot_allocations, yields, optimal_p_slots, optimal_q_slots, optimal_yield = analyze_slot_allocation(
            total_slots, start_p
        )

        # Print example matrix, printing with precision of 2
    T = get_transition_matrix(2, 2, 0)
    print(np.array2string(T, precision=8, max_line_width=150, suppress_small=True))


if __name__ == "__main__":
    main()
