def user_input():
    NumberOfGreenNodes = input("Enter the size of the Green Team: ")
    ProbabilityOfConnection = input(
        "Enter the probability of a connection between any given green player: "
    )
    NumberOfGreyAgents = input("Enter Number of agents in the Grey Team: ")
    RedSpyProportion = input("Enter the proportion of Red Spies within the Grey Team: ")
    Uncertainty = input(
        "Enter the Uncertainty interval of the Green Team. (e.g. [-0.1,0.1] or [-0.5,0.7]): "
    )
    print(
        NumberOfGreenNodes,
        ProbabilityOfConnection,
        NumberOfGreyAgents,
        RedSpyProportion,
        Uncertainty,
    )


user_input()
