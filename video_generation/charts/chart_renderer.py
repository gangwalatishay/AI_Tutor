import matplotlib.pyplot as plt
import os


def render_chart(scene, output_path):
    chart_type = scene["chart_type"]
    data = scene["chart_data"]

    labels = data["labels"]
    values = data["values"]

    plt.figure(figsize=(8, 5))

    if chart_type == "bar":
        plt.bar(labels, values, color="#4F46E5")

    elif chart_type == "pie":
        plt.pie(values, labels=labels, autopct="%1.1f%%")

    elif chart_type == "line":
        plt.plot(labels, values, marker="o")

    plt.title(scene.get("chart_title", ""))
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    return output_path
