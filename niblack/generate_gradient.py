def generate_gradient_pgm(filename="gradient.pgm"):
    width, height = 89, 89
    maxv = 255

    with open(filename, "w") as f:
        f.write("P2\n")
        f.write("# gradiente horizontal 89x89\n")
        f.write(f"{width} {height}\n")
        f.write(f"{maxv}\n")

        for y in range(height):
            row = []
            for x in range(width):
                v = int(x * (maxv / (width - 1)))
                row.append(str(v))
            f.write(" ".join(row) + "\n")

if __name__ == "__main__":
    generate_gradient_pgm()
    print("Gerado gradient.pgm com 89×89 pixels.")
