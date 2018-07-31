from random import randint

class Fighter:
    def __init__(self, name, level, max_health, max_energy, attacks):
        self.name = name
        self.level = level
        self.max_health = max_health
        self.health = max_health
        self.max_energy = max_energy
        self.energy = max_energy
        self.attacks = attacks
        self.is_computer = False

    """ checks whether fighter has enough energy for the attack """
    def check_energy(self, attack):
        return attack.energy_cost >= self.energy

    """ performs attack """
    def perform_attack(self, enemy, attack):
        if not attack.will_hit():
            print(self.name + " missed the attack!")
            self.energy -= attack.energy_cost
            return
        if attack.will_hit_critically():
            print("Critical hit!")
            attack_power = attack.average_power * 1.5
        else:
            attack_power = attack.compute_power()
        enemy.take_damage(attack_power)
        
        self.energy -= attack.energy_cost

    """ checks whether player is defeated """
    def is_defeated(self):
        return self.health <= 0

    """ substracts fighter's lives according to the damage """
    def take_damage(self, damage):
        if damage == 0:
            print("What a shame! The attack had no effect on " + self.name + "!")
            return
        print(self.name + " was hit and lost " + str(damage) + " health!")
        self.health -= damage

    """ randomly chooses attack if fighter is computer """
    def choose_computer_attack(self):
        return randint(0, len(self.attacks) - 1)

    """ chooses homan's attack """
    def choose_attack(self):
        index = self.retype_input()
        while not self.check_attack_index(index):
            index = self.retype_input()

        return index-1

    """ retypes human's input """
    def retype_input(self):
        print("Choose the attack: ", sep="", end=" ")               
        while True:
            try:
                attack_index = int(input())
            except ValueError:
                print("Choose the attack: ", sep="", end=" ")
                continue
            else:
                break

        return attack_index

    """ checks index of attack of human's input """
    def check_attack_index(self, attack_index):
        return attack_index >= 1 and attack_index <= len(self.attacks)

    """ checks whether fighter has enough energy to perform the attack """
    def has_energy_for_attack(self, attack):
        if self.energy < attack.energy_cost:
            if not self.is_computer:
                print(self.name + " does not have enough energy for the attack!")
            return False
        return True

    """ checks whether fighter can perform one more attack - min energy """
    def has_min_energy(self):
        return self.attacks[0].energy_cost <= self.energy

    """ sets attribute is_computer """   
    def set_is_computer(self, value):
        self.is_computer = value

    """ adds 10 % of max energy to fighter's energy """
    def regenerate(self):
        self.energy = int(1.1 * self.energy)
        if self.energy > self.max_energy:
            self.energy = self.max_energy
    
    def __str__(self):
        return "Name: " + self.name + ", health: " + str(self.health) + "/" \
               + str(self.max_health) + ", energy: " + str(self.energy) + "/" \
               + str(self.max_energy) + ", level: " + str(self.level)

    def print_fighter(self):
        print("{:-^70}".format(" " + self.name.upper() + " "))
        print()
        self.print_attacks()
        print()
        print("{:-^70}".format("-"))
        
    def print_attacks(self):
        print("{:<5}".format(" "), end="")
        print("{:<25} {:<15} {:<10} {:<15}".format \
              ("Attack", "Average Power", "Accuracy", "Energy Cost"))

        i = 1         
        for attack in self.attacks:
            print(str(i) + " -- ", end="")
            print("{:<23} {:>15} {:>10} {:>13}".format \
                  (attack.name, attack.average_power, attack.accuracy, attack.energy_cost))
            i += 1


class Attack:
    def __init__(self, name, accuracy, energy_cost, average_power):
        self.name = name
        self.accuracy = accuracy
        self.energy_cost = energy_cost
        self.average_power = average_power

    """ computer power: +- 30 % of average power """
    def compute_power(self):
        power = int(self.average_power + self.average_power * randint(-3, 3) * 0.1)
        if power < 0:
            return 0
        return power

    """ 3% chance for a critihal hit """
    def will_hit_critically(self):
        return randint(0, 100) > 97

    """ checks whether attack is accurate enough to hit """
    def will_hit(self):
        return randint(0, 100) <= self.accuracy * 100       

    def __str__(self):
        return "Attack: " + self.name + ", accuracy: " + str(self.accuracy) \
                + ", energy_cost: " + str(self.energy_cost) +  ", average power: " \
                + str(self.average_power)


class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    """ player with lower level starts the game """
    def choose_players_start(self):
        if self.player1.level >= self.player2.level:
            return self.player2, self.player1
        return self.player1, self.player2

    def print_match(self):
        print("{:<25}".format(" "), end="")
        print("{:<14} {:>5}".format \
              ("Health", "Energy"))

        print("{:<20} {:>10} {:>10}".format \
        (self.player1.name, str(self.player1.health) + "/" + str(self.player1.max_health), \
        str(self.player1.energy)) + "/" + str(self.player1.max_energy))
        print("{:<20} {:>10} {:>10}".format \
        (self.player2.name, str(self.player2.health) + "/" + str(self.player2.max_health), \
        str(self.player2.energy)) + "/" + str(self.player2.max_energy))
        print()
         
        

def play():
    fighters = FighterCollection()
    mode = select_mode()
    print()
    fighter1, fighter2 = fighters.select_fighters(mode)

    match = Match(fighter1, fighter2)
    current_player, second_player = match.choose_players_start()
        
    while(True):
        second_player.regenerate()
        match.print_match()
        current_player.print_fighter()
        if not current_player.is_computer:
            attack_index = current_player.choose_attack()
        else:
            attack_index = current_player.choose_computer_attack()
        attack = current_player.attacks[attack_index]
            
        while not current_player.has_energy_for_attack(attack):
            if not current_player.has_min_energy():
                print (current_player.name + " has no energy left! " \
                       + second_player.name + " wins!")
                return
            if not current_player.is_computer:
                attack_index = current_player.choose_attack()
            else:
                attack_index = current_player.choose_computer_attack()
            attack = current_player.attacks[attack_index] 
        
        print(current_player.name + " used " + attack.name + ".")
        current_player.perform_attack(second_player, attack)
        print("\n")
        if second_player.is_defeated():
            print(current_player.name + " wins!")
            return
        
        current_player, second_player = second_player, current_player

""" selects game mode """
def select_mode():
    print("{:-^70}".format(" GAME MODE "))
    print("[1]", end="")
    print("{:>15}".format("singleplayer"))
    print("[2]", end="")
    print("{:>14}".format("multiplayer"))
    print("{:-^70}".format("-"))
            
    print("Select game mode: ", sep="", end=" ")               
    while True:
        try:
            mode = int(input())
        except ValueError:
            return select_mode()
        if mode < 1 or mode > 2:
            return select_mode()
        else:
            return mode   
      

class FighterCollection:
    def __init__(self):
        """ Doge """
        such_attack = Attack("Such attack!", 0.9, 10, 15)
        very_pain = Attack("Very pain!", 0.7, 40, 45)
        wow = Attack("Wow!", 0.25, 100, 100)
        doge_attacks = [such_attack, very_pain, wow]

        doge = Fighter("Doge", 2, 150, 300, doge_attacks)

        """ Ivan the Slav """
        squat = Attack("Squat", 1, 10, 10)
        adidas_kick = Attack("Adidas kick", 0.6, 50, 65)
        spy_stab = Attack("Western spy stabbing", 0.35, 80, 85)
        slav_attacks = [squat, adidas_kick, spy_stab]

        slav = Fighter("Ivan the Slav", 4, 220, 230, slav_attacks)

        """ Johnny [The Room] """
        hit_her = Attack("I did not hit her!", 0.85, 10, 20)
        did_not = Attack("I did not!", 0.7, 40, 55)
        hi_mark = Attack("Oh, hi Mark.", 0.3, 70, 70)
        johnny_attacks = [hit_her, did_not, hi_mark]

        johnny = Fighter("Johnny [The Room]", 1, 200, 250, johnny_attacks)

        """ Rainbow Dash """
        flash = Attack("Fantastic Filly Flash", 1, 10, 10)
        dry = Attack("Rainblow Dry", 0.65, 45, 50)
        rainboom = Attack("Sonic Rainboom", 0.25, 90, 130)
        dash_attacks = [flash, dry, rainboom]

        dash = Fighter("Rainbow Dash", 3, 210, 240, dash_attacks)

        """ The Swan princess """
        transform = Attack("Swan transformation", 1, 15, 20)
        song = Attack("Catchy song", 0.75, 70, 80)
        evil = Attack("Evil Odette", 0.4, 160, 170)
        swan_attacks = [transform, song, evil]

        swan = Fighter("The Swan princess", 8, 100, 350, swan_attacks)

        self.fighters = [doge, slav, johnny, dash, swan]

    """ selects fighters in to act in the game """
    def select_fighters(self, mode):
        print("Player1")
        print("{:-^70}".format("-"))
        self.print_fighters()
        print("{:-^70}".format("-"))
        fighter1, fighter1_index = self.select_human_fighter(-1)
        print("Player1 has chosen " + fighter1.name + ".")
        if mode == 2:
            fighter2, fighter2_index = self.select_human_fighter(fighter1_index)
            print("Player2 has chosen " + fighter2.name + ".")
        else:
            fighter2 = self.select_computer_fighter(fighter1_index)
            fighter2.set_is_computer(True)
            print("Computer has chosen " + fighter2.name + ".")
        print()
        print("Let the game begin!")
        
        return fighter1, fighter2   

    """ human chooses fighter """
    def select_human_fighter(self, taken_index):
        print("Select Fighter: ", sep="", end=" ")               
        while True:
            try:
                index = int(input())
            except ValueError:
                print("Select Fighter: ", sep="", end=" ")
                continue
            if index < 1 or index > len(self.fighters):
                print("Select Fighter: ", sep="", end=" ")
                continue
            if taken_index == index-1:
                print("This fighter is already taken. " \
                      + "Select another fighter: ", sep="", end=" ")
                continue
            else:
                break

        return self.fighters[index-1], index-1

    """ computer randomly chooses fighter """
    def select_computer_fighter(self, taken_index):
        index = randint(0, len(self.fighters)-1)
        while index == taken_index:
            index = randint(0, len(self.fighters)-1)
        
        return self.fighters[index]
    
    def print_fighters(self):
        print("{:<5}".format(" "), end="")
        print("{:<25} {:<10} {:<10} {:<10}".format \
              ("Name", "Health", "Energy", "Level"))

        i = 1        
        for fighter in self.fighters:
            print(str(i) + " -- ", end="")
            print("{:<21} {:>10} {:>10} {:>9}".format \
                  (fighter.name, fighter.health, fighter.energy, fighter.level))
            i += 1
