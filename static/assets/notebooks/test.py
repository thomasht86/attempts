# /// script
# dependencies = [
# black==23.12.1,
# click==8.1.7,
# contourpy==1.2.0,
# cycler==0.12.1,
# fonttools==4.47.0,
# jedi==0.19.1,
# kiwisolver==1.4.5,
# marimo==0.1.66,
# Markdown==3.5.1,
# matplotlib==3.8.2,
# mypy-extensions==1.0.0,
# numpy==1.26.2,
# packaging==23.2,
# parso==0.8.3,
# pathspec==0.12.1,
# Pillow==10.1.0,
# platformdirs==4.1.0,
# Pygments==2.17.2,
# pymdown-extensions==10.5,
# pyparsing==3.1.1,
# python-dateutil==2.8.2,
# PyYAML==6.0.1,
# six==1.16.0,
# tomli==2.0.1,
# tomlkit==0.12.3,
# tornado==6.4,
# typing_extensions==4.9.0,
# ]
# ///

import marimo

__generated_with = "0.1.65"
app = marimo.App()


@app.cell
def _(mo):
    mo.md("# Merry Christmas! 🎄").left()
    return


@app.cell
def __(mo):
    mo.md(
        """
        This marimo notebook is [adapted from](https://isquared.digital/visualizations/2020-06-15-koch-curve/) Vladimir Ilievski's Jupyter notebook
        for drawing snowflakes using the Koch snowflake algortithm, and was generated using [https://marimo.io/convert]().
        """
    )
    return


@app.cell
def __(mo):
    degree = mo.ui.slider(1, 5, label="Snowflake degree")
    degree
    return (degree,)


@app.cell
def _(degree, draw_snowflake):
    draw_snowflake(degree.value)
    return


@app.cell
def __(koch_snowflake, plt):
    def draw_snowflake(d):
        _, ax = plt.subplots(subplot_kw={"aspect": "equal"})
        lines = koch_snowflake(degree=d)

        # extract the line coordinates
        x, y = [], []
        for l in lines:
            x.extend([l["a"][0], l["b"][0], l["c"][0], l["d"][0], l["e"][0]])
            y.extend([l["a"][1], l["b"][1], l["c"][1], l["d"][1], l["e"][1]])

        # remove all ticks and axes
        ax.set_xticks([], [])
        ax.set_yticks([], [])
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

        # fill the polygons
        ax.fill(x, y, color="white", edgecolor="black", lw=1)
        return ax

    return (draw_snowflake,)


@app.cell
def _(np):
    def koch_line(start, end, factor):
        """
        Segments a line to Koch line, creating fractals.


        :param tuple start:  (x, y) coordinates of the starting point
        :param tuple end: (x, y) coordinates of the end point
        :param float factor: the multiple of sixty degrees to rotate
        :returns tuple: tuple of all points of segmentation
        """

        # coordinates of the start
        x1, y1 = start[0], start[1]

        # coordinates of the end
        x2, y2 = end[0], end[1]

        # the length of the line
        l = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # first point: same as the start
        a = (x1, y1)

        # second point: one third in each direction from the first point
        b = (x1 + (x2 - x1) / 3.0, y1 + (y2 - y1) / 3.0)

        # third point: rotation for multiple of 60 degrees
        c = (
            b[0] + l / 3.0 * np.cos(factor * np.pi / 3.0),
            b[1] + l / 3.0 * np.sin(factor * np.pi / 3.0),
        )

        # fourth point: two thirds in each direction from the first point
        d = (x1 + 2.0 * (x2 - x1) / 3.0, y1 + 2.0 * (y2 - y1) / 3.0)

        # the last point
        e = end

        return {"a": a, "b": b, "c": c, "d": d, "e": e, "factor": factor}

    return (koch_line,)


@app.cell
def _(functools, koch_line, np):
    @functools.cache
    def koch_snowflake(degree, s=5.0):
        """Generates all lines for a Koch Snowflake with a given degree.

        :param int degree: how deep to go in the branching process
        :param float s: the length of the initial equilateral triangle
        :returns list: list of all lines that form the snowflake
        """
        # all lines of the snowflake
        lines = []

        # we rotate in multiples of 60 degrees
        sixty_degrees = np.pi / 3.0

        # vertices of the initial equilateral triangle
        A = (0.0, 0.0)
        B = (s, 0.0)
        C = (s * np.cos(sixty_degrees), s * np.sin(sixty_degrees))

        # set the initial lines
        if degree == 0:
            lines.append(koch_line(A, B, 0))
            lines.append(koch_line(B, C, 2))
            lines.append(koch_line(C, A, 4))
        else:
            lines.append(koch_line(A, B, 5))
            lines.append(koch_line(B, C, 1))
            lines.append(koch_line(C, A, 3))

        for i in range(1, degree):
            # every lines produce 4 more lines
            for _ in range(3 * 4 ** (i - 1)):
                line = lines.pop(0)
                factor = line["factor"]

                lines.append(koch_line(line["a"], line["b"], factor % 6))  # a to b
                lines.append(
                    koch_line(line["b"], line["c"], (factor - 1) % 6)
                )  # b to c
                lines.append(
                    koch_line(line["c"], line["d"], (factor + 1) % 6)
                )  # d to c
                lines.append(koch_line(line["d"], line["e"], factor % 6))  # d to e

        return lines

    return (koch_snowflake,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import functools
    import numpy as np
    import matplotlib.pyplot as plt

    return functools, np, plt


if __name__ == "__main__":
    app.run()
