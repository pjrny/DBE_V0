"""Reference checks for SDBES V3 core logical semantics.

This is not a production solver. It verifies the normative examples used by
V3: four-valued knowledge propagation, strong three-valued scenario logic,
k-of-n gates, route-local versus global necessity, minimal path/cut sets in a
small monotone model, and bootstrap fixed-point ambiguity.
"""

from itertools import combinations, product

# Belnap/Dunn-style information state: (support_true, support_false)
NEITHER = (0, 0)
TRUE_ONLY = (1, 0)
FALSE_ONLY = (0, 1)
BOTH = (1, 1)

NAMES = {
    NEITHER: "NEITHER",
    TRUE_ONLY: "TRUE_ONLY",
    FALSE_ONLY: "FALSE_ONLY",
    BOTH: "BOTH",
}


def knowledge_all(*values):
    return (
        int(all(value[0] for value in values)),
        int(any(value[1] for value in values)),
    )


def knowledge_any(*values):
    return (
        int(any(value[0] for value in values)),
        int(all(value[1] for value in values)),
    )


def knowledge_k_of_n(k, *values):
    n = len(values)
    return (
        int(sum(value[0] for value in values) >= k),
        int(sum(value[1] for value in values) >= n - k + 1),
    )


SCENARIO_TRUE = "TRUE"
SCENARIO_FALSE = "FALSE"
SCENARIO_UNKNOWN = "UNKNOWN"


def scenario_all(*values):
    if SCENARIO_FALSE in values:
        return SCENARIO_FALSE
    if all(value == SCENARIO_TRUE for value in values):
        return SCENARIO_TRUE
    return SCENARIO_UNKNOWN


def scenario_any(*values):
    if SCENARIO_TRUE in values:
        return SCENARIO_TRUE
    if all(value == SCENARIO_FALSE for value in values):
        return SCENARIO_FALSE
    return SCENARIO_UNKNOWN


def scenario_k_of_n(k, *values):
    true_count = sum(value == SCENARIO_TRUE for value in values)
    unknown_count = sum(value == SCENARIO_UNKNOWN for value in values)
    if true_count >= k:
        return SCENARIO_TRUE
    if true_count + unknown_count < k:
        return SCENARIO_FALSE
    return SCENARIO_UNKNOWN


def minimal_sets(items, property_fn):
    results = []
    for size in range(1, len(items) + 1):
        for candidate in combinations(items, size):
            candidate_set = set(candidate)
            if property_fn(candidate_set) and not any(
                set(existing).issubset(candidate_set) for existing in results
            ):
                results.append(candidate)
    return results


def run_checks():
    # Conflict is retained rather than collapsed to unknown.
    assert knowledge_all(BOTH, TRUE_ONLY) == BOTH
    assert knowledge_all(BOTH, FALSE_ONLY) == FALSE_ONLY
    assert knowledge_any(BOTH, TRUE_ONLY) == TRUE_ONLY
    assert knowledge_any(BOTH, FALSE_ONLY) == BOTH

    # k-of-n preserves conflict when there is qualifying support both ways.
    assert knowledge_k_of_n(2, TRUE_ONLY, NEITHER, FALSE_ONLY) == NEITHER
    assert knowledge_k_of_n(2, TRUE_ONLY, BOTH, FALSE_ONLY) == BOTH

    # Strong three-valued scenario logic.
    assert scenario_k_of_n(
        2, SCENARIO_TRUE, SCENARIO_UNKNOWN, SCENARIO_FALSE
    ) == SCENARIO_UNKNOWN
    assert scenario_k_of_n(
        2, SCENARIO_TRUE, SCENARIO_TRUE, SCENARIO_FALSE
    ) == SCENARIO_TRUE
    assert scenario_k_of_n(
        2, SCENARIO_FALSE, SCENARIO_FALSE, SCENARIO_UNKNOWN
    ) == SCENARIO_FALSE

    # Target = (A AND B) OR C.
    variables = ["A", "B", "C"]

    def target(satisfied):
        return ("A" in satisfied and "B" in satisfied) or "C" in satisfied

    path_sets = minimal_sets(variables, target)

    def blocks_target(failed):
        working = set(variables) - failed
        return not target(working)

    cut_sets = minimal_sets(variables, blocks_target)

    assert set(map(frozenset, path_sets)) == {
        frozenset({"A", "B"}),
        frozenset({"C"}),
    }
    assert set(map(frozenset, cut_sets)) == {
        frozenset({"A", "C"}),
        frozenset({"B", "C"}),
    }

    # A is route-local to {A,B}, but no predicate is globally necessary.
    global_necessary = set(path_sets[0]).intersection(
        *[set(path) for path in path_sets[1:]]
    )
    assert global_necessary == set()

    # Bootstrap equations A=B, B=A have two fixed points without a seed.
    fixed_points = []
    for a, b in product([False, True], repeat=2):
        if a == b and b == a:
            fixed_points.append((a, b))
    assert set(fixed_points) == {(False, False), (True, True)}

    # An external true seed yields one fixed point for A=(seed OR B), B=A.
    seeded_fixed_points = []
    for a, b in product([False, True], repeat=2):
        if a == (True or b) and b == a:
            seeded_fixed_points.append((a, b))
    assert seeded_fixed_points == [(True, True)]

    return {
        "knowledge_conflict_preserved": NAMES[knowledge_all(BOTH, TRUE_ONLY)],
        "k_of_n_conflict_preserved": NAMES[
            knowledge_k_of_n(2, TRUE_ONLY, BOTH, FALSE_ONLY)
        ],
        "scenario_k_of_n_partial": scenario_k_of_n(
            2, SCENARIO_TRUE, SCENARIO_UNKNOWN, SCENARIO_FALSE
        ),
        "minimal_path_sets": path_sets,
        "minimal_cut_sets": cut_sets,
        "global_necessary": sorted(global_necessary),
        "bootstrap_fixed_points_without_seed": fixed_points,
        "bootstrap_fixed_points_with_seed": seeded_fixed_points,
    }


if __name__ == "__main__":
    results = run_checks()
    for key, value in results.items():
        print(f"{key}: {value}")
    print("ALL_CHECKS_PASSED")