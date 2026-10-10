import numpy as np

def grad(u):
    x, y = u
    return np.array([4 * x**3, 4 * y**3])


def hessian(u):
    x, y = u
    return np.array([[12 * x**2, 0.0], [0.0, 12 * y**2]])


def newton_optimization(f, u0, epsition=1e-6, max_iter=100):
    u = np.array(u0)
    for i in range(max_iter):
        g = grad(u)
        H = hessian(u)

        if np.linalg.norm(g) < epsition:
            print(f"Thuật toán hội tụ sau {i} bước lặp.")
            return u

        delta_u = np.linalg.solve(H, -g)
        u += delta_u

        if np.linalg.norm(delta_u) < epsition:
            print(f"Thuật toán hội tụ sau {i + 1} bước lặp.")
            return u
    return u


if __name__ == "__main__":
    def f(u):
        x, y = u
        return x**4 + y**4

    u0 = np.array([10.0, 10.0])
    optimal_u = newton_optimization(f, u0)
    print("Điểm cực tiểu là:", optimal_u)
    print("Giá trị nhỏ nhất f(u) là:", f(optimal_u))