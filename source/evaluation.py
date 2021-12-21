from matplotlib import pyplot as plt


def plot_fit_curves(fit_history, train_metric='loss', val_metric='val_loss', remove_first=True):
    """
    Plots the history of training a model into a line graph
    :param fit_history: history object from model.fit()
    :param train_metric: what to use for the training metrics (only use if you have custom metrics)
    :param val_metric: what to use for the validation metrics (only use if you have custom metrics)
    :param remove_first: whether to remove the first epoch from the history. This can be useful if your first epoch
    has a extremely high score, which messes with the visuals of the plot
    """
    if remove_first:
        train_hist = fit_history.history[train_metric][1:]
        val_hist = fit_history.history[val_metric][1:]
    else:
        train_hist = fit_history.history[train_metric]
        val_hist = fit_history.history[val_metric]
    plt.plot(train_hist)
    plt.plot(val_hist)
    plt.title('Training curve')
    plt.ylabel(train_metric)
    plt.xlabel('epochs')
    plt.legend(['train', 'val'], loc='upper left')
    plt.yscale('log')
    plt.show()