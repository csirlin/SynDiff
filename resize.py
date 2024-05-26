import numpy as np

# resize an n1 x m1 image to an n2 x m2 image
# resize from source each time if possible
def resize(data, n1, m1, n2, m2):
    new_data = np.zeros((n2, m2))

    for y in range(n1):
        for x in range(m1):
            if 0 <= y + (n2 - n1) // 2 < n2 and 0 <= x + (m2 - m1) // 2 < m2:
                new_data[y + (n2 - n1) // 2][x + (m2 - m1) // 2] = data[y][x]

    return new_data




# testing with small examples
mat5x5 = np.arange(5 * 5).reshape(5, 5)
print("Original 5x5 matrix:")
print(mat5x5)
print("Resized to 7x7:")
print(resize(mat5x5, 5, 5, 7, 7))
print("Resized to 3x3:")
print(resize(mat5x5, 5, 5, 3, 3))
print("Resized to 8x8:")
print(resize(mat5x5, 5, 5, 8, 8))
print("Resized to 6x6:")
print(resize(mat5x5, 5, 5, 6, 6))
print("Resized to 4x4:")
print(resize(mat5x5, 5, 5, 4, 4))
print("Resized to 2x2:")
print(resize(mat5x5, 5, 5, 2, 2))

mat6x6 = np.arange(6 * 6).reshape(6, 6)
print("Original 6x6 matrix:")
print(mat6x6)
print("Resized to 8x8:")
print(resize(mat6x6, 6, 6, 8, 8))
print("Resized to 4x4:")
print(resize(mat6x6, 6, 6, 4, 4))
print("Resized to 9x9:")
print(resize(mat6x6, 6, 6, 9, 9))
print("Resized to 7x7:")
print(resize(mat6x6, 6, 6, 7, 7))
print("Resized to 5x5:")
print(resize(mat6x6, 6, 6, 5, 5))
print("Resized to 3x3:")
print(resize(mat6x6, 6, 6, 3, 3))
