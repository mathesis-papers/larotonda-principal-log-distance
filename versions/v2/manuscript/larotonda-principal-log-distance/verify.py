import json
from fractions import Fraction
from itertools import product


def quadratic(angles, coefficient):
    return sum(angle * angle for angle in angles) + coefficient * sum(angles) ** 2


def winding(angles, index=0):
    shifted = list(angles)
    shifted[index] -= 2
    return tuple(shifted)


def same_endpoint(angles, shifted):
    return all(((angle - other) / 2).denominator == 1
               for angle, other in zip(angles, shifted, strict=True))


def verify():
    first = (Fraction(4, 5), Fraction(1, 2))
    second = winding(first)
    assert same_endpoint(first, second)
    assert quadratic(first, 4) == Fraction(153, 20)
    assert quadratic(second, 4) == Fraction(73, 20)
    assert max(map(abs, first)) == Fraction(4, 5)
    small = (Fraction(2, 5),) * 3
    assert same_endpoint(small, winding(small))
    assert quadratic(small, 4) == Fraction(156, 25)
    assert quadratic(winding(small), 4) == Fraction(136, 25)
    assert max(map(abs, small)) < Fraction(1, 2)

    family_cases = 0
    for dimension in range(2, 9):
        coefficients = [Fraction(-1, dimension) + Fraction(1, 100 * dimension),
                        Fraction(-1, 2 * dimension), Fraction(-1, 100 * dimension),
                        Fraction(1, 100), Fraction(1, 2), Fraction(1),
                        Fraction(4), Fraction(100)]
        for coefficient in coefficients:
            epsilon = abs(coefficient) / (4 * (1 + coefficient))
            sign = 1 if coefficient > 0 else -1
            angles = (1 - epsilon, Fraction(sign, 2)) + (Fraction(0),) * (dimension - 2)
            shifted = winding(angles)
            scale_squared = 1 / min(Fraction(1), 1 + dimension * coefficient)
            assert coefficient > Fraction(-1, dimension)
            assert 0 < epsilon < Fraction(1, 4)
            assert max(map(abs, angles)) < 1
            assert same_endpoint(angles, shifted)
            assert quadratic(shifted, coefficient) - quadratic(angles, coefficient) == -abs(coefficient)
            assert scale_squared > 0
            assert scale_squared * quadratic(shifted, coefficient) < scale_squared * quadratic(angles, coefficient)
            family_cases += 1

    gap_cases = 0
    for first_angle, second_angle, coefficient in product(
            [Fraction(-3, 4), Fraction(0), Fraction(2, 5), Fraction(4, 5)],
            [Fraction(-1, 2), Fraction(0), Fraction(1, 2)],
            [Fraction(-1, 4), Fraction(0), Fraction(1), Fraction(4)]):
        angles = (first_angle, second_angle)
        expected = 4 * ((1 - first_angle) + coefficient * (1 - sum(angles)))
        assert quadratic(winding(angles), coefficient) - quadratic(angles, coefficient) == expected
        gap_cases += 1

    frobenius_cases = 0
    for angles in product([Fraction(-1), Fraction(-1, 2), Fraction(0),
                           Fraction(1, 2), Fraction(1)], repeat=2):
        for shifts in product(range(-3, 4), repeat=2):
            shifted = tuple(angle + 2 * shift for angle, shift in zip(angles, shifts, strict=True))
            assert quadratic(angles, 0) <= quadratic(shifted, 0)
            frobenius_cases += 1

    dimension_cases = 0
    for dimension in range(3, 65):
        angles = (Fraction(2, dimension),) * dimension
        assert same_endpoint(angles, winding(angles))
        difference = quadratic(winding(angles), 4) - quadratic(angles, 4)
        assert difference == -4 * (3 + Fraction(2, dimension)) < 0
        dimension_cases += 1

    scalar_cases = 0
    fixed_dimension_cases = 0
    for dimension in range(2, 33):
        for coefficient in [Fraction(1, 10), Fraction(1), Fraction(4), Fraction(100)]:
            threshold = (1 + coefficient) / (1 + dimension * coefficient)
            for angle, sign in [(threshold / 2, 1), (threshold, 0), ((1 + threshold) / 2, -1)]:
                angles = (angle,) * dimension
                shifted = winding(angles)
                gap = quadratic(shifted, coefficient) - quadratic(angles, coefficient)
                assert gap == 4 * ((1 + coefficient) - angle * (1 + dimension * coefficient))
                assert same_endpoint(angles, shifted)
                assert (gap > 0) - (gap < 0) == sign
                scalar_cases += 1
        for margin in [Fraction(1, 100), Fraction(1, 10), Fraction(1, 2), Fraction(2)]:
            radius = Fraction(1, dimension) + margin
            angle = (Fraction(1, dimension) + min(radius, Fraction(1))) / 2
            coefficient_bound = (1 - angle) / (dimension * angle - 1)
            coefficient = coefficient_bound + 1
            angles = (angle,) * dimension
            assert Fraction(1, dimension) < angle < min(radius, Fraction(1))
            assert quadratic(winding(angles), coefficient) < quadratic(angles, coefficient)
            assert same_endpoint(angles, winding(angles))
            fixed_dimension_cases += 1

    circle_cases = 0
    for angle in [Fraction(index, 8) for index in range(-8, 9)]:
        for shift in range(-8, 9):
            assert abs(angle) <= abs(angle + 2 * shift)
            circle_cases += 1

    return {
        'status': 'PASS',
        'arithmetic': 'Exact fractions; angles in units of pi and squared norms in units of pi^2; no rounding.',
        'two_dimensional': {'angles': ['4/5', '1/2'], 'shifted_angles': ['-6/5', '1/2'],
                            'coefficient': 4, 'principal_squared': '153/20', 'competitor_squared': '73/20'},
        'three_dimensional': {'angles': ['2/5', '2/5', '2/5'], 'shifted_angles': ['-8/5', '2/5', '2/5'],
                              'coefficient': 4, 'principal_squared': '156/25', 'competitor_squared': '136/25'},
        'family': {'dimensions': [2, 8], 'cases': family_cases, 'coefficients_per_dimension': 8,
                   'scope': 'Three negative and five positive rational coefficients in each dimension.'},
        'winding_identity': {'cases': gap_cases, 'scope': 'Specified rational two-angle grid.'},
        'frobenius': {'cases': frobenius_cases, 'scope': 'Five angles per coordinate in [-1,1], and winding integers -3 through 3, dimension two.'},
        'dimension_family': {'dimensions': [3, 64], 'cases': dimension_cases, 'coefficient': 4,
                             'scope': 'Equal angles 2/n and one winding shift.'},
        'scalar_threshold': {'dimensions': [2, 32], 'cases': scalar_cases,
                             'scope': 'Four positive coefficients; below, at, and above the scalar one-shift threshold.'},
        'fixed_dimension_obstruction': {'dimensions': [2, 32], 'cases': fixed_dimension_cases,
                                       'scope': 'Four radius margins per dimension, with the displayed constructive coefficient bound.'},
        'circle': {'cases': circle_cases, 'angle_grid': 'Integers -8 through 8 divided by 8',
                   'winding_range': [-8, 8], 'scope': 'Absolute-angle comparisons on the circle.'},
        'coverage': 'Finite coefficient, periodicity and winding comparisons. General norm admissibility and curve-length identities have written proofs in note.tex.'
    }


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2, sort_keys=True))
