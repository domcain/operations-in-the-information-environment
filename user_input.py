NumberOfGreenNodes = None
ProbabilityOfConnection = None
NumberOfGreyAgents = None
RedSpyProportion = None
Certainty = None

def user_input():
    NumberOfGreenNodes = input("Enter the size of the Green Team: ")
    ProbabilityOfConnection = input(
        "Enter the probability of a connection between any given green player: "
    )
    NumberOfGreyAgents = input("Enter Number of agents in the Grey Team: ")
    RedSpyProportion = input("Enter the proportion of Red Spies within the Grey Team: ")
    Certainty = input(
        "Enter the Certainty interval of the Green Team. (e.g. [-0.1,0.1] or [-0.5,0.7]): "
    )
    print(
        "Size of the Green Team:" + NumberOfGreenNodes + "\n",
        "Probability of a connection between any given green player: " + ProbabilityOfConnection + "\n",
        "Number of agents in the Grey Team: " + NumberOfGreyAgents + "\n",
        "Proportion of Red Spies within the Grey Team: " + RedSpyProportion + "\n",
        "Certainty interval of the Green Team: " + Certainty + "\n"
    )


user_input()
