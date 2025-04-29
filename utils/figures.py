import matplotlib.pyplot as plt


def display_shape_file(file, label):
    fig, ax = plt.subplots(figsize=(8, 6))
    file.plot(ax=ax, color="lightblue", edgecolor="white")

    label_clean = label.lower()

    if "river line" in label_clean:
        ax.set_title("Nepal's River Line", color="white")
    elif "river polygon" in label_clean or "river poly" in label_clean:
        ax.set_title("Nepal's Water Bodies", color="white")
    else:
        paren_index = label.find("(")
        if paren_index != -1:
            label = label[:paren_index].strip()

        label = label.replace("Boundary", "").strip()
        ax.set_title(f"Nepal's {label} Boundary", color="white")

    ax.set_axis_off()
    fig.patch.set_facecolor("none")

    return fig
