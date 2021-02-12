import random
''''

step 1, the math

there will be two ways of parsing through the date

the first one is a deterministic aproach, using actual number to get a single example

the second one will atempt analize the probability to kill from a single unit to a particular target.

the deterministic process for assessing damage is as follows, with each step building on the last


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
        numb of models slain this turn - highest Ld of models left = new Ld
    b) roll to see if the models suffer morale penalties
        if roll=< new Ld then remove one model
            if failed check if the unit has any invulnerabilities to morale then
            check if number of models < "starting number of models"/2 if so add +1 to the target of the next roll
            roll 2+ for each remaining unit

attacker: the dictionary containing all information invoved in the current damage dealing it is a bunch of lists inside dictionary inside a dictionary inside a dictionary

the organization of this object is as follows from highest level to lowest

Name of Unit: str - this identifies a unit among hundred to note what kinds of models it contains

    Name of Model: str - this identifies the specific model that we are working with among all the posible models in the unit

        M: int - the ammount of movement in inches of the model
        WS: int - the Weapon Skill or minimum roll needed to hit a target in melee
        BS: int - the Ballistic Skill or minimum roll needed to hit a target in range
        S: int - the Strength of the model in melee
        T: int - the Toughness of the model, how strong a hit it can take and shrug off
        W: int - the number of Wounds the model can take before its taken out of action
        A: int - the number of Attacks the model can dish out in close combat
        Ld: int - the Leadership of the model, how many of its breatheren it can watch die before thinking of running away
        Ar: int - the Armor of the model, the amount of armor penetration the weapons will need to stand a chance
        Inv_M: int - the Invulnerable save in Melee for the model, like its armor save but it can't be diminished by regular attacks
        Inv_R: int - the Invulnerable save in Range for the model, like its armor save but it can't be diminished by regular attacks
        FnP: int - the Feel no Pain save of the model, what are the chances to ignore damage all together on a damage by damage basis
        FnP_Mw: int- the Feel no Pain for Mortal Wounds of the model, what are the chances of ignoring mortal wounds all together
        Cost: int - the point cost of the model in order to add it to the army.
        Weapon1: str list - the names of the weaopn equipped in this particular slot

            R: int - the range of the weapon, the distance at which it can be used
            Type: str - the details on how the weapon works and when can it be shot
            A: str - the number of attacks that the weapon has, melee weapons add this number to the Attack characteristic of the model, variable Attack weapons are marked with a "d" before the number like "d6" for a random value between 1 and 6
            S: str - the Stregth of the weapon, melee weapons add this number to the Stregth characteristic of the model, variable Stregth weapons are marked with a "d" before the number like "d6"
            AP: int - the Armor Penetration value of the weapon, how much of the armor on their target do they get through
            D: str - the Damage of the weapon, variable Damage weapons are marked with a "d" before the number like "d6"
            Abilities: str - a list of the special rules that apply to this weapon, they can be things like re-roll all failed to hit rolls, or always wound on a particular number
 
        Weapon2: str list - the names of the weaopn equipped in this particular slot
            +
        Weapon3: str list - the names of the weaopn equipped in this particular slot
            +
        Weapon4: str list - the names of the weaopn equipped in this particular slot
            +
        Min: int - the Minimum ammount of models of this type that can be in this unit
        Max: int - the Maximum ammount of models of this type that can be in this unit
        Req: str - the requirements that must be met for this model to be part of the unit, E means every x models ex: "E5" means every 5 models, A means after x models ex: "A10" means after 10 models
        Abilities: str list - a list of all the abilities the unit has, it can include things like advance and charge, objective secure, or fly
        Key-Words: str list - a list of all the Key-Words that are aprticular to that unit and what kinds of things it will be affected by.

"Kabalite Warriors":
    {"Kabalite Warrior":
        {"M":7,
        "WS":3,
        "BS":3,
        "S":3,
        "T":3,
        "W":1,
        "A":1,
        "Ld":7,
        "Ar":5,
        "InvM":7,
        "InvR":7,
        "FnP":6,
        "FnPM":6,
        "Cost":8,
        "Weapon1":
            {"weapon_name":"splinter rifle",
            "R":24,
            "Type": "Rapid Fire",
            "A":1,
            "S":0,
            "AP":0,
            "D":1,
            "Abilities":("poison")},
        "Weapon2":none,
        "Weapon3":none,
        "Min":3, 
        "Max":19,
        "Requirements":none,
        "Min squad":5,
        "Max_squad":20,
        "Ability":("power from pain","vanguard of the dark city"),
        "Key-word":("Ealdari", "Drukhari", "Infantry", "Kabalite Warriors", "Troops", "Kabal")}
    }
}

because the weapons are shared across units, there are two separate dictionaries, the first on of each unit with each model in the game, the second dictionary contains the specifics of each weapon.
the first and second dictionaries come together to populate the template of the attacker, there should be a third list called sub-factions which can modify the atributes of a given unit.

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

would love the final result to be a detail exploration of what each unit does against particular matchups, with a zoom into their offensive and defensive power, as well as a more well rounded star chart expression of how do their other areas work

'''

# Dummy Data!
attacker = {
    "WS":3,
    "BS":3,
    "S":3,
    "A":1,
    "Cost":8,
    "Weapon_Type": "Rapid_Fire",
    "Weapon_Attacks":1,
    "Weapon_Abilities": ["Poison"],
    "Weapon_S":3,
    "R" : 24,
    "N" :5,
    "AP":0,
    "D":2
}

defender= {
"T":3,
"Ar":5,
"Inv_R":7,
"Inv_M":7,
"W":3,
"FnP":6,
"FnP_Mw":7,
"Ld":6,
"N":10
}

distance = 11
dead = 0

def ROLL(dice):
    """ a simple dice roll

    Args: 
        dice: how many sides are on the dice

    Returns: the roll of the dice
    """
    result= random.randint(1,dice)
    print("rolled: " + str(result))
    return result


def CHANCE(target):
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
    chance = (7-target)/6
    return chance

def NUMBER_OF_ATTACKS(attacker, distance, defender, process):
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
    if attacker.get("R")>distance:
        num_attacks = attacker.get("Weapon_Attacks")
        if attacker.get("R")/2>distance and attacker.get("Weapon_Type")=="Rapid_Fire":
            num_attacks = num_attacks*2
        num_attacks = num_attacks * attacker.get("N")
    else:
        num_attacks = 0
    return num_attacks

def TO_HIT(attacker,num_attacks, defender,process):
    """ 
    a) determine the base target by this logic
        if weapon type == Melee* then WS
        else BS
    b) apply modifiers to the target
    c) apply re-rolls to the dice that fail to hit
    d) add any mortal wounds to the wounds being generated
    e) apply extra hits for the dice that would fall under that category
        1) repeat step a, b, c, and d for the newly generated rolls if aplicable

    Args:   attacker; the atributes of the attacker indicating what is its WS and BS, as well as any modifiers or re-rolls it might have
            num_attacks; the number of attacks that were produced by the NUMBER_OF_ATTACKS variable
            defender; the atributes of the defender indicating if it has any modifiers to get hit

    Return: the number of hits on the target 
    """
    total_hits = 0
    if attacker.get("Weapon_Type") == "melee":
        target = attacker.get("WS")
    else:
        target = attacker.get("BS")
    if process == "deterministic":
        for n in range(num_attacks):
            if ROLL(6) >= target:
                total_hits = total_hits+1
    else:
        total_hits = CHANCE(target)
    print("target to hit: " + str(target))
    return total_hits

def TO_WOUND(attacker, total_hits, defender, process):
    """
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

    Args:   attacker; the atributes of the attacker, indicating what is the stregth of the weapon it is using, and any special abilities or modifiers that might affect this roll
            num_hits; the number of hits on the target
            defender; the atributes of the defender, indicating the toughness of the target and any modifiers that might change the result
    
    Return: the number of wounds on the target
    """
    total_wounds = 0
    S = attacker.get("Weapon_S")
    T = defender.get("T")
    if S == T:
        target=4
    elif 2*T<S>T:
        target=3
    elif 2*T<=S:
        target=2
    elif 2*S<T>S:
        target=5
    elif 2*S<=T:
        target=6
    if process == "deterministic":
        for n in range(total_hits):
            if ROLL(6) >= target:
                total_wounds = total_wounds+1
    if process == "probabilistic": 
        total_wounds=total_hits*CHANCE(target)
    print("target to wound: " + str(target))
    return total_wounds

def TO_SAVE(attacker, total_wounds, defender,process):
    """4) SAVE
    a) determine base target by this logic
        apply AP to Ar = new Ar
        if new Ar < Inv then new Ar
        if new Ar > Inv then Inv
    d) apply modifiers to the target
    e) add any mortal wounds to the wounds being generated
    f) apply re-rolls to the dice that fail to wound
    
    Args:   attacker; the atributes of the attacker including the Armor Penetration of its weapons and any modifiers that might affect the result
            total_wounds; the number of wounds on the target
            defender; the atributes of the defender including any Armor and Invulnerable saves and any modifiers taht might affect the results
    
    Return: the total number of unsaved wounds
    """
    total_f_saves = 0
    target = defender.get("Ar") + attacker.get("AP")
    if target>defender.get("Inv_R"):
        target=defender.get("Inv_R")
    if process == "deterministic":
        for n in range(total_wounds):
            if not ROLL(6) >= target:
                total_f_saves = total_f_saves+1
    if process == "probabilistic": 
        if(target>6):
            total_f_saves = total_wounds
        else:
            total_f_saves = total_wounds*CHANCE(7-target)
    print("target to save: " + str(target))
    return total_f_saves    
    
def TO_FNP(attacker, total_f_saves, defender, process):
    """
    a) determine the total damage thought the damage variable for the weapon
    b) apply modifiers to the damage
    c) determine the base target by looking at the FnP value on the model
    d) Dmg > W then dead
    e) check if there are any mortal wounds left to be allocated on the target apply the next available Mw to the target
    f) determine the base target by looking at the FnP Mw value on the model
    g) repeat steps d, e, and f until the is dead or there are no more Mw to be allocated

    Args:   attacker;the atributes of the attacker including the damage of their weapons and any modifiers that might apply
            total_f_saves; the number of saves that were failed, the number of deaths may not excede the number of failed saves unless there were mortal wounds involved
            defender; the atributes of the defender including their wounds, Feel no Pain and any other atributes that might apply

    Return: remaining wounds on the current model
    """
    r_wounds = defender.get("W")
    dead = 0
    damage = attacker.get("D")
    target = defender.get("FnP")
    if process == "deterministic":
        for n in range(total_f_saves):
            for n in range(damage):
                if not ROLL(6) >= target:
                    r_wounds=r_wounds-1
                    print("remainig wounds: " + str(r_wounds))
                    if r_wounds==0:
                        dead = dead+1
                        r_wounds = defender.get("W")
    if process == "probabilistic": 
        if target>6:
            fail_FnP = damage 
        else:
            fail_FnP = CHANCE(7-target*damage)
        r_wounds = r_wounds-fail_FnP
    print("target to FnP: " + str(target))
    return dead


def solve(process):
    if process == "deterministic":
        num_attacks = NUMBER_OF_ATTACKS(attacker, distance, defender, process)
        total_hits = TO_HIT(attacker, num_attacks, defender, process)
        print("total hits: " + str(total_hits))
        total_wounds = TO_WOUND(attacker, total_hits, defender, process)
        print("total wounds: " + str(total_wounds))
        total_f_saves = TO_SAVE(attacker, total_wounds, defender, process)
        print("total failed saves: " + str(total_f_saves))
        dead = TO_FNP(attacker, total_f_saves, defender, process)
        print("total dead: " + str(dead))



def main():
    solve("deterministic")


if __name__ == "__main__":
    main()

