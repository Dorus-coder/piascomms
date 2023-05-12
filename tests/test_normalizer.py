def inverse_rescale_actions(y, low, high):
    range = high - low
    return (2 / range) * (y - (low + (0.5 * range)))


def rescale_actions(tanh_output, low, high):
    range = high - low
    return tanh_output * range / 2 + (low + (0.5 * range))


if __name__ == "__main__":
    normalised_val = [-1, -0.5, 0, 0.5, 1]
    _range = 50, 100
    calc_v =[]
    for v in normalised_val:
        a = rescale_actions(v, *_range)
      
        b = inverse_rescale_actions(a, *_range)
        calc_v.append(b)
#         print(f"{a = }, {b = }")

# print(inverse_rescale_actions(-3.972, 0, 11.5))

