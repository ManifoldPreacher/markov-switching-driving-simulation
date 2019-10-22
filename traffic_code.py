import math, random, networkx, collections, sys, time
import numpy as np
from progress.spinner import Spinner

G = networkx.read_graphml("/home/manifoldpreacher/pCloudDrive/Schoolwork/SPECTO1/markov_switching_traffic_code/mm_road_graph.graphml")

intersections = list(G.nodes())

# In[ ]:


states = ["prospect", "rational"]

transitionNames = [["pp", "pr",], ["rp", "rr"]]

transitionProbabilities = [[0.5, 0.5], [0.5, 0.5]]

if sum(transitionProbabilities[0])+sum(transitionProbabilities[1]) != 2:
	print("Something went wrong, Master! Transition matrix, perhaps?")
	sys.exit()
else: print("Transition matrices are alright, Master!")


# In[ ]:


class markov:
	def __init__(self, *args):
		self.info_state = random.choice(["prospect", "rational"])
		self.periods = 0
		self.info_state_list = []
	def activity_forecast(self):
		prob = 1
		if self.info_state == "prospect":
			change = np.random.choice(transitionNames[0],replace=True,p=transitionProbabilities[0])
			if change == "pp":
				prob = prob * 0.5
				self.info_state = "prospect"
				self.info_state_list.append(self.info_state)
			elif change == "pr":
				prob = prob * 0.5
				self.info_state = "rational"
				self.info_state_list.append(self.info_state)
		elif self.info_state == "rational":
			change = np.random.choice(transitionNames[1],replace=True,p=transitionProbabilities[1])
			if change == "rr":
				prob = prob * 0.5
				self.info_state = "rational"
				self.info_state_list.append(self.info_state)
			elif change == "rp":
				prob = prob * 0.5
				self.info_state = "prospect"
				self.info_state_list.append(self.info_state)
		self.periods += 1
#    def end_result(self):
#        print("Possible states: " + str(info_state_list)
#        print("End state after "+ str(nodes) + " nodes: " + "info_state")
#        print("Probability of the possible sequence of states: " + str(prob))


# In[49]:


class choice:
    def __init__(self):
        self.references = [0]
        #self.current, self.destination = random.sample(intersections, 2)
        self.current = build_up.source
        self.choice_set = []
        self.options = []
        self.gains = []
        self.probs = []
        self.option_gains = []
        self.lottery = []
        self.choice_list = []
    def calc_gains(self):
        self.choice_set = list(networkx.neighbors(G, self.current))
        self.options = []
        self.gains = []
        self.option_gains = []
        for i in self.choice_set:
            self.options.append(float(G.get_edge_data(self.current, i)[0].get("length")))
        for i in self.options:
            self.gains.append(self.references[-1] - i)
            self.option_gains = list(zip(self.options, self.gains))
    def probabilities(self):
        self.probs = []
        self.lottery = []
        for i in self.gains:
            self.probs.append(random.uniform(0, 1))
            self.lottery = list(zip(self.gains, self.probs))
    def gain_value_func(self, y, p):
        return math.exp(-1.05*(-math.log(p))**0.5)*y**0.88
    def loss_value_func(self, y, p):
        return math.exp(-0.9*(-math.log(p))**0.61)*(-2.25*(-y)**0.61)
    def prospect_choice(self):
        x = []
        y = []
        for i in self.lottery:
            if i[0] >= 0:
                x.append(self.gain_value_func(*i))
            elif i[0] < 0:
                y.append(self.loss_value_func(*i))
        cumulative = sum(x) + sum(y)
        decision = min(self.gains, key=lambda x:abs(x-cumulative))
        self.references.append(decision)
        new_node = str(self.references[-1] - decision)
        for i in self.choice_set:
            if new_node in G.get_edge_data(self.current, i)[0].values():
                self.current = i
                self.choice_list.append(i)
                print(i)
    def time_minimize(self):
        optimal = str(self.references[-1] - max(self.gains))
        for i in self.choice_set:
            if optimal in G.get_edge_data(self.current, i)[0].items():
                self.current = i
                self.choice_list.append(i)
                self.references.append(max(self.gains))
                print(i)
# In[ ]:

class build_up:
    def __init__(self):
        self.source, self.destination = random.sample(intersections, 2)
    def set_points(self):
        self.source, self.destination = random.sample(intersections, 2)

build_up = build_up()
markov = markov()
choice = choice()

def switching():
    choice.calc_gains()
    choice.probabilities()
    if markov.info_state == "prospect":
        choice.prospect_choice()
    else:
        choice.time_minimize()
    print(markov.info_state)
    markov.activity_forecast()
#    markov.end_result()

class operate:
    def __init__(self):
        self.maximum = None
    def greeting(self):
        time.sleep(3)
        print("Hello, Master! How many drivers would you like to simulate?")
        try:
            i = abs(int(input()))
            print("Yay! Thank you, Master! I'll drop by your room again before you sleep <3")
        except ValueError:
            print("Aww, Master! Please be serious...")
            sys.exit()
        self.maximum = i
    def program(self):
        if markov.info_state == "rational":
            conversation = " He must be really well-informed :-o"
        else:
            conversation = " I hope he makes a good decision..."
        for i in range(0, self.maximum):
            time.sleep(3)
            print("The starting state is %s, Master! %s" % (markov.info_state, conversation))
            print("Going from %s to %s!" % (build_up.source, build_up.destination))
            #print("Going from %s to %s!" % (choice.current, choice.destination))	
            time.sleep(3)
            program_spinner = Spinner("Simulating, Master!")
            while True:
                switching()
                print("Running!")
                program_spinner.next()
                print(choice.current)
                if choice.current == build_up.destination:
                    break
            program_spinner.finish()
            build_up.set_points()
    def graph_color(self):
        import matplotlib.pyplot as plt
        appearance = list(collections.Counter(choice.choice_list).items())
        chosen = []
        times_chosen = []
        pos_attrs = {}
        for i in appearance:
            chosen.append(i[0])
            times_chosen.append(i[1])
        plt.figure()
        pos = networkx.spring_layout(G)
        networkx.draw(G, pos_nodes, with_labels=True)
        for node, coords in pos_nodes.items():
            pos_attrs[node] = (coords[0], coords[1] + 0.08)
        node_attrs = networkx.get_node_attributes(G, 'type')
        custom_node_attrs = {}
        for node, attr in node_attrs.items():
            custom_node_attrs[node] = "{'type': '" + attr + "'}"
        networkx.draw_networkx_labels(G, pos_attrs, labels=custom_node_attrs)
        plt.show()

operate = operate()

operate.greeting()

operate.program()

draw_spinner = Spinner("Drawing the driver/s' route, Master!")
operate.graph_color()
draw_spinner.next()
draw_spinner.finish()
print("All done, Master! I'm sorry 선배님 turned you down by the way...")
#markov.end_result()
