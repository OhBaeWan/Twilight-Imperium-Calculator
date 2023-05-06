# Part of ImGui Bundle - MIT License - Copyright (c) 2022-2023 Pascal Thomet - https://github.com/pthom/imgui_bundle
import math
import numpy as np
from imgui_bundle import imgui, implot, imgui_md, immapp, ImVec2, ImVec4
from imgui_bundle.demos_python import demo_utils # this will set the assets folder
from dataclasses import dataclass

@dataclass
class ShipDefault:
    rolls: int
    attack: int
    health: int

@dataclass
class ShipType:
    default: ShipDefault
    title: str
    shortTitle: str
    count: int
    max: int
    rolls: int
    attack: int
    health: int

class ShipsState:
    capitalShip: ShipType
    warSun: ShipType
    dreadnaught: ShipType
    cruiser: ShipType
    destroyer: ShipType
    fighter: ShipType
    spaceCannon: ShipType
    bombardmant: ShipType
    groundForces: ShipType
    
    
    
    def __init__(self):
        self.ShipTypes = []
        self.warSun = ShipType(ShipDefault(3,3,2),"War Sun","WS",0 , 2, 3, 3,2)
        self.capitalShip = ShipType(ShipDefault(2,6,2),"Capital Ship", "CS", 0, 1, 2, 6,2)
        self.dreadnaught = ShipType(ShipDefault(1,5,1),"Dreadnaught", "DR" , 0,5, 1, 5,1) 
        self.cruiser = ShipType(ShipDefault(1,7,1),"Cruiser", "CR", 0, 8,1,7,1)
        self.destroyer = ShipType(ShipDefault(1,6,1),"Destroyer", "DS", 0, 8,1,6,1)
        self.fighter = ShipType(ShipDefault(1,9,1),"Fighter", "FI" , 0,20,1,9,1)
        self.spaceCannon = ShipType(ShipDefault(1,6,1),"Space Cannon", "SC" ,0,20,1,6,1)
        self.bombardmant = ShipType(ShipDefault(1,5,1),"Bombardmant", "BB" , 0,20,1,5,1)
        self.groundForces = ShipType(ShipDefault(1,7,1),"Ground Forces", "GF", 0,20,1,7,1)
        
        
        self.ShipTypes.append(self.warSun);
        self.ShipTypes.append(self.capitalShip);
        self.ShipTypes.append(self.dreadnaught);
        self.ShipTypes.append(self.cruiser);
        self.ShipTypes.append(self.destroyer);
        self.ShipTypes.append(self.fighter);
        self.ShipTypes.append(self.spaceCannon);
        self.ShipTypes.append(self.bombardmant);
        self.ShipTypes.append(self.groundForces);
        



@immapp.static(state=ShipsState())
def demo_gui():
    state = demo_gui.state

    imgui_md.render_unindented(
        """
        # Twilight Imperium Battle Simulator
        Enter the number of ships for each side to simulate a single engagement.
        """
    )

    imgui.text("Side 1")

    for ship in state.ShipTypes:
        imgui.text(f"{ship.title}:")
        if imgui.begin_popup_context_item(f"{ship.shortTitle}"):
            imgui.text(f"Attack:")
            imgui.same_line()
            imgui.text(f"{ship.attack} ")
            imgui.same_line()
            #button to increase the attack value
            if imgui.button(f"+##A{ship.shortTitle}"):
                if ship.attack < 10:
                    ship.attack += 1
            imgui.same_line()
            #button to decrease the attack value
            if imgui.button(f"-##A{ship.shortTitle}"):
                if ship.attack > 1:
                    ship.attack -= 1
            imgui.same_line()
            #button to reset the attack value
            if imgui.button(f"Reset##A{ship.shortTitle}"):
                ship.attack = ship.default.attack

            imgui.text(f"Rolls:")
            imgui.same_line()
            imgui.text(f"{ship.rolls} ")
            imgui.same_line()
            #button to increase the number of rolls
            if imgui.button(f"+##R{ship.shortTitle}"):
                if ship.rolls < 10:
                    ship.rolls += 1
            imgui.same_line()
            #button to decrease the number of rolls
            if imgui.button(f"-##R{ship.shortTitle}"):
                if ship.rolls > 1:
                    ship.rolls -= 1
            imgui.same_line()
            #button to reset the number of rolls
            if imgui.button(f"Reset##R{ship.shortTitle}"):
                ship.rolls = ship.default.rolls

            imgui.text(f"Health:")
            imgui.same_line()
            imgui.text(f"{ship.health} ")
            imgui.same_line()

            ## button to increase the health value
            if imgui.button(f"+##H{ship.shortTitle}"):
                if ship.health < 2:
                     ship.health += 1
            imgui.same_line()
            ## button to decrease the health value
            if imgui.button(f"-##H{ship.shortTitle}"):
                if ship.health > 1:
                    ship.health -= 1
            imgui.same_line()
            ## button to reset the health value
            if imgui.button(f"Reset##H{ship.shortTitle}"):
                ship.health = ship.default.health
            
            imgui.end_popup()
        imgui.same_line()
    imgui.text(" ")
    for ship in state.ShipTypes:
        imgui.text(f"       {ship.count}          ")
        imgui.same_line()
    imgui.text(" ")
    for ship in state.ShipTypes:
        if imgui.button(f"     +{ship.shortTitle}     "):
            if ship.count < ship.max:
                ship.count += 1
        imgui.same_line()
    imgui.text(" ")
    for ship in state.ShipTypes:
        if imgui.button(f"     -{ship.shortTitle}      "):
            if ship.count > 0:
                ship.count -= 1
        imgui.same_line()
    imgui.text(" ")

    ## create a popup menue for each of the ship names
    for ship in state.ShipTypes:
        if imgui.begin_popup_context_item(f"popup_{ship.shortTitle}"):
            if imgui.menu_item("Reset"):
                ship.count = 0
            imgui.end_popup()
        imgui.same_line()


    num_ships = 0
    num_types = 0
    health = 0
    for ship in state.ShipTypes:
        num_ships += ship.count*ship.rolls
        num_types += 1 if ship.count > 0 else 0
        health += ship.count*ship.health
    
    probabilities = [] 

    for ship in state.ShipTypes:
        if ship.count > 0:
            probability = (10-(ship.attack-1))/10
            trials = ship.count * ship.rolls
            binom_dist = [0 for _ in range(trials+1)]
            for j in range(trials+1):
                prob = math.comb(trials,j) * (probability**j) * ((1-probability)**(trials-j))
                binom_dist[j] = prob
            probabilities.append(binom_dist)

    total_prob = [0 for _ in range((num_ships+num_ships))] 

    ## find the longest binomial distribution
    max_length = 0
    for i in range(len(probabilities)):
        if len(probabilities[i]) > max_length:
            max_length = len(probabilities[i])
    ## normalize the length of each binomial distribution to be the same length as the longest one by adding zeros to the end
    for i in range(len(probabilities)):
        while len(probabilities[i]) < max_length:
            probabilities[i].append(0)


    ## convolve each binomial distribution with the next one and the result with the next one and so on
    for i in range(len(probabilities)):
        if i == 0:
            total_prob = probabilities[i]
        else:
            total_prob = np.convolve(total_prob, probabilities[i])

    imgui.text("")

    plot_height = immapp.em_size() * 20
    if implot.begin_plot("Hits", ImVec2(-1, plot_height)):
        implot.setup_axes("Hits", "Probability")
        implot.setup_axes_limits(-0.5, 10, 0, 1)
        implot.plot_bars("Hits", np.array(total_prob), .9)
        #adjust the x axis to be the length of the total probability array
        #def set_next_axes_limits(
        # x_min: float, x_max: float, y_min: float, y_max: float, cond: Cond = Cond_Once
        #) -> None:
        
        #plot a vertical line at the value of health
        #(function) def plot_line(
        # label_id: str,
        # xs: ndarray,
        # ys: ndarray,
        # flags: LineFlags = 0,
        # offset: int = 0,
        # stride: int = -1
        #) -> None
        implot.plot_line("Health", np.array([health, health]), np.array([0, 1]), 1)
        
        #Display the height of the bar on top of the bar
        for i in range(len(total_prob)):
            implot.plot_text(f"{100*total_prob[i]:.4}", i, total_prob[i] + 0.02)
        implot.end_plot()
        implot.set_next_axes_to_fit()
    else:
        imgui.text("Plot Error")


    
def main():
    immapp.run(demo_gui, with_implot=True, with_markdown=True, window_size=(1000, 800))




if __name__ == "__main__":
    main()
