''''

step 1, the math

analize the probability to wound from a single unit to a particular target.

the process for assessing damage is as follows, with each step building on the last


1) NUMBER OF ATTACKS
    a)determine the number of shots by looking at the weapon type, range, and distance from the target and following this logic
        if range>distance
        if Weapon Type rapid fire and range/2>distance then the ammount of attacks is doubled
        if Weapon Type is blast and target has >5 models min 3 attacks
        if Weapon Type is blast and target has >10 models min 6 attacks

2) TO HIT 
    a) determine the base target by this logic
        if weapon type == Melee* then WS
        else BS
    b) apply modifiers to the target
    c) apply re-rolls to the dice that fail to hit
    d) add any mortal wounds to the wounds being generated
    e) apply extra hits for the dice that would fall under that category
     1) repeat step a, b, c, and d for the newly generated rolls if aplicable

3) TO WOUND
    a) compare Stregth of the weapon against Toughtness of the target, except on poison weapons
    b) determine the base target by this logic, 
        S == T then 4+
        S>T and S<2T then 3+
        S>=2T then 2+
        S<T and 2S>T then 5+
        2S>=T then 6+
    c) apply modifiers to the target
    d) add any mortal wounds to the wounds being generated
    e) apply re-rolls to the dice that fail to wound
    f) apply extra hits for the dice that would fall under that category
     1) repeat step a, b, c, and d for the newly generated rolls if aplicable

4) SAVE
    a) determine base target by this logic
        apply AP to Ar = new Ar
        if new Ar < Inv then new Ar
        if new Ar > Inv then Inv
    d) apply modifiers to the target
    e) add any mortal wounds to the wounds being generated
    f) apply re-rolls to the dice that fail to wound

5) FEEL NO PAIN
    a) determine the total damage thought the damage variable for the weapon
    b) apply modifiers to the damage
    c) determine the base target by looking at the FnP value on the model
    d) Dmg > W then dead
    e) check if there are any mortal wounds left to be allocated on the target apply the next available Mw to the target
    f) determine the base target by looking at the FnP Mw value on the model
    g) repeat steps d, e, and f until the is dead or there are no more Mw to be allocated

6) MORALE
    a) determine the base target through this logic
        numb of models slain this turn - highest Ld of units left = new Ld
    b) roll to see if the models suffer morale penalties
        if roll=< new Ld then remove one model
            if failed check if the unit has any invulnerabilities to morale then
            check if number of models < "starting number of models"/2 if so add +1 to the target of the next roll
            roll 2+ for each remaining unit

attacker: the dictionary containing all information invoved in the current damage dealing it is a bunch of lists inside dictionary inside a dictionary inside a dictionary

the organization of this object is as follows from highest level to lowest

Name of Unit:




step 2, implement dice rolling for the system.



posible unit composition
unit type min ammount to maximum ammount
so for example

kabalite Warriors have a min of 5 units composed of either 1 syrabite and 4 kabalite warriors, or 1 syrabite, 3 kabalite warriors and 1 kabalite warrior with special weapon.

to identify this we need a running to total number of units with a split in values and profiles for each composition

that would look something like this

kabalite warrior: x4
32
syrabite: x1
    blast pistol
    agonizer
    18
total points 50
average damage against  
                        infantry T1 Ar7 Inv7 FnP7:
                        infantry T2 Ar7 Inv7 FnP7:
                        infantry T3 Ar7 Inv7 FnP7:
                        infantry T5 Ar7 Inv7 FnP7:
                        infantry T6 Ar7 Inv7 FnP7:
                        infantry T7 Ar7 Inv7 FnP7:
                        infantry T8 Ar7 Inv7 FnP7:
                        monster/bike T1 Ar7 Inv7 FnP7:
                        monster/bike T2 Ar7 Inv7 FnP7:
                        monster/bike T3 Ar7 Inv7 FnP7:
                        monster/bike T4 Ar7 Inv7 FnP7:
                        monster/bike T5 Ar7 Inv7 FnP7:
                        monster/bike T6 Ar7 Inv7 FnP7:
                        monster/bike T7 Ar7 Inv7 FnP7:

'''


#attacker = {"Kabalite Warrior":{"M":7,"WS":3,"BS":3,"S":3,"T":3,"W":1,"A":1,"Ld":7,"Ar":5,"InvM":7,"InvR":7,"FnP":6,"FnPM":6,"Cost":8,"Unit":"kabalite Warriors","Weapon1":"splinter rifle","Weapon2":none,"Weapon3":none,"Min":3, "Max":19,"Requirements":none,"Min squad":5,"Max_squad":20,"Ability":("power from pain","vanguard of the dark city"),"Key-word":("Ealdari", "Drukhari", "Infantry", "Kabalite Warriors", "Troops", "Kabal")}}
#defender = {"Guardsmen":0}

attacker = {
"WS":3,
"BS":3,
"S":3,
"A":1,
"Cost":8,
"Weapon Type": ["Rapid Fire", 1],
"Weapon Abilities": ["Poison"],
"R" : 24,
"N" :5,
}

defender= {
"T":3,
"Ar":5,
"Inv_R":7,
"Inv_M":7,
"W":1,
"FnP":7,
"FnP_Mw":7,
"Ld":6,
"N":10
}

distance = 11

def NUMBER_OF_ATTACKS(attacker, distance, defender):
    """
    determine the number of shots by looking at the weapon type, range, and distance from the target and following this logic
    if range>distance
    if Weapon Type rapid fire and range/2>distance then the ammount of attacks is doubled
    if Weapon Type is blast and target has >5 models min 3 attacks
    if Weapon Type is blast and target has >10 models min 6 attacks
    multply that number by the ammount of weapons of that type in the group
    
    Args:   attacker; the atributes of the attacker, indicating what kind of weapon its using and how many of them, weapon Type and number of shots need to be unpacked from this list inside a dictionary
            distance; the distance that between the attacker and the defender
            defender; the attributes of the defender, indicating what kind of abilties if any does it have that would affect this
    
    Return: returns the number of attacks being produced
    """
    weapon_type = attacker.get("Weapon Type")
    if attacker.get("R")>distance:
        output = weapon_type[1]
        if attacker.get("R")/2>distance and weapon_type[0]=="Rapid Fire":
            output = weapon_type[1]*2
        output= output*attacker.get("N")
    else:
        output = 0
    print(output)
    return output

def TO_HIT(attacker, defender):
    """ 
    a) determine the base target by this logic
        if weapon type == Melee* then WS
        else BS
    b) apply modifiers to the target
    c) apply re-rolls to the dice that fail to hit
    d) add any mortal wounds to the wounds being generated
    e) apply extra hits for the dice that would fall under that category
     1) repeat step a, b, c, and d for the newly generated rolls if aplicable
    """
    weapon_type = attacker.get("Weapon Type")
    if weapon_type[0]=="melee":
        num_hits = attacker.get("WS")



def CHANCE(target)
    """
    determine the probability for a particular result to come true
    in warhammer the results are marked as 2 or higher, 3 or higher, etc
    indicating that all numbers higher than the marked number including it would mark a success
    the formula for chance to roll those results is: 
    all results lower than a 2+ are considered a 2+
    2+ has a 5/6 chance to succed
    3+ has a 4/6 chance to succeed
    4+ has a 3/6 chance to succeed
    5+ has a 2/6 chacne to succeed
    6+ has a 1/6 cahcne to succeed
    7+ has no chance to succeed
    or (7-target)/6

    Args: the target indicates what value on a 6 sided dice is considered a success

    Returns: the chance of success for that value
    """
    if target<2:
        target=2
    if target>7:
        target=7
    output = (7-target)/6
    return output

def modifiers():
    """establishig the modifiers that will be affecting the unit"""


def solve():
    num_attacks = NUMBER_OF_ATTACKS(attacker, distance, defender)
    num_hits = TO_HIT(attacker, defender)



def main():
    solve()


if __name__ == "__main__":
    main()

