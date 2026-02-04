import matplotlib.pyplot as plt

def plot_actual_vs_predicted(dates, actual, predicted):
    plt.figure(figsize=(12, 5))
    plt.plot(dates, actual, label="Actual Sales")
    plt.plot(dates, predicted, label="Predicted Sales")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.title("Actual vs Predicted Daily Sales")
    plt.legend()
    plt.tight_layout()
    plt.show()
