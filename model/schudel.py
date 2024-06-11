
class ScudelDataModel:
    
   def ScudelDataModelExplor(targets, times):
    """
    Create a data model that associates targets with their corresponding times.

    Parameters:
    targets (list): A list of targets.
    times (list): A list of lists, where each sublist contains times corresponding to each target.

    Returns:
    dict: A dictionary with targets as keys and lists of times as values.
    """
    if len(targets) != len(times):
        raise ValueError("Targets and times must have the same length")

    model = {target: time_list for target, time_list in zip(targets, times)}
    return model