import random


# Dummy Data!
attacker = {
    "WS":3,
    "BS":3,
    "S":3,
    "A":4,
    "Cost":20,
    "Weapon_Type": "heavy",
    "Weapon_Attacks":3,
    "v_Weapon_Attacks":True,
    "Weapon_Abilities": ["poison"],
    "Weapon_S":0,
    "R" : 0,
    "N" :4,
    "AP":-1,
    "D":2,
    "to_hit":{
        "re-roll1": False,
        "re-roll_all":False,
        "modifier": -1,
        "extra_form":"add",
        "extra_target":0,
        "extra_ammount":0,
        "extra_target_hard": False,
        "target":0,
        "target_hard":False
    },
    "to_wound":{
        "re-roll1":False,
        "re-roll_all":False,
        "modifier":0,
        "extra_form":"add",
        "extra_target":0,
        "extra_ammount":0,
        "extra_target_hard": False,
        "target":0,
        "target_hard":False
    },
    "to_save":{
        "no_invul":False,
        "no_re-rolls":False
    },
    "to_FnP":{
        "no_invul":False,
        "no_re-rolls":False
    }
}

defender= {
"T":4,
"Ar":3,
"Inv_R":7,
"Inv_M":7,
"W":2,
"FnP":7,
"FnP_Mw":7,
"Ld":8,
"N":10
}

distance = 0

def ROLL(dice):
    """ a simple dice roll

    Args: 
        dice: how many sides are on the dice

    Returns: the roll of the dice
    """
    result= random.randint(1,dice)
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

    
def HIT_TARGET(roll, modifier, target, extra_target, extra_form, extra_ammount):
    """
    the process of rolling a dice and deciding weather or not its a success and if it receives extra effects

    Args:
        roll; the value of the roll
        modifier; the number that the roll is modified by
        target; the target the roll needs to hit or exceed
        extra_target; the target for which the roll gets extra bonuses
        extra_form; the type of extra bonuses
        extra_ammount; the ammount of extra bonuses

    Returns: a list of values, the first one being the number of regular successes the second one the number of extra successes, this variable is reserved for mortal wounds or other values that would skip the next step in the process
    """
    total_hits = [0,0]
    if roll+modifier >= target:             
        total_hits[0] = total_hits[0]+1
        if roll+modifier >= extra_target:
            if extra_form == "add":         
                total_hits[0] = total_hits[0] + extra_ammount
            if extra_form == "roll":
                roll = ROLL(6)
                print ("extra roll: " + str(roll))
                if roll+modifier >= target:
                    total_hits[0] = total_hits[0]+ extra_ammount
            if extra_form == "Mw":
                total_hits[1] = total_hits[1] +extra_ammount

    return total_hits

def NUMBER_OF_ATTACKS(attacker, distance, defender, process):
    """
    determine the number of shots by looking at the weapon type, range, and distance from the target and following this logic 
        if range>distance √
        if Weapon Type rapid fire and range/2>distance then the ammount of attacks is doubled √
        if Weapon Type is blast and target has >5 models min 3 attacks
        if Weapon Type is blast and target has >10 models min 6 attacks
    multply that number by the ammount of weapons of that type in the group √
    
    Args:   attacker; the atributes of the attacker, indicating what kind of weapon its using and how many of them, weapon Type and number of shots need to be unpacked from this list inside a dictionary
            distance; the distance that between the attacker and the defender
            defender; the attributes of the defender, indicating what kind of abilties if any does it have that would affect this
    
    Return: returns the number of attacks being produced
    """
    N = attacker.get("N")
    num_attacks = attacker.get("Weapon_Attacks")
    weapon_type = attacker.get("Weapon_Type")
    R = attacker.get("R")

    if R>distance:
        if R/2>distance and weapon_type=="rapid_fire":
            num_attacks = num_attacks*2
        num_attacks = num_attacks * N
    else:
        num_attacks = 0
    print("number of attacks: " + str(num_attacks))
    return num_attacks

def TO_HIT(attacker,num_attacks, defender,process):
    """ 
    a) determine the base target by this logic √
        if weapon type == Melee* then WS √
        else BS √
    b) apply modifiers to the rolls
    c) apply re-rolls to the dice that fail to hit
    d) add any mortal wounds to the wounds being generated
    e) apply extra hits for the dice that would fall under that category
        1) repeat step a, b, c, and d for the newly generated rolls if aplicable

    Args:   attacker; the atributes of the attacker indicating what is its WS and BS, as well as any modifiers or re-rolls it might have
            num_attacks; the number of attacks that were produced by the NUMBER_OF_ATTACKS variable
            defender; the atributes of the defender indicating if it has any modifiers to get hit

    Return: the number of hits on the target 
    """
    weapon_type = attacker.get("Weapon_Type")
    WS = attacker.get("WS")
    BS = attacker.get("BS")
    A = attacker.get("A")
    N = attacker.get("N")
    weapon_attacks = attacker.get("Weapon_Attacks")
    to_hit = attacker.get("to_hit")
    re_roll1 = to_hit.get("re-roll1")
    re_roll_all = to_hit.get("re-roll_all")
    modifier = to_hit.get("modifier")
    extra_form = to_hit.get("extra_form")
    extra_target= to_hit.get("extra_target")
    extra_ammount= to_hit.get("extra_ammount")
    extra_target_hard= to_hit.get("extra_target_hard")
    target = to_hit.get("target")
    target_hard= to_hit.get("target_hard")
    total_hits = 0

    if target == 0:
        if weapon_type == "melee":
            target = WS
            num_attacks = (A + weapon_attacks) * N
            print("number of melee attacks: " + str(num_attacks))
        else:
            target = BS
            num_attacks = weapon_attacks * N
            print("number of ranged attacks: " + str(num_attacks))

   
    if process == "deterministic":
        
        for n in range(num_attacks):
            roll=ROLL(6)
            print("rolled: " + str(roll))
            total_hits = total_hits + HIT_TARGET(roll,modifier, target, extra_target, extra_form, extra_ammount)[0]
    
            if re_roll1== True and roll ==1:
                roll=ROLL(6)
                if roll != 1:
                    print("re-rolled into: " + str(roll))
                    total_hits = total_hits + HIT_TARGET(roll,modifier, target, extra_target, extra_form, extra_ammount)[0]
            
            elif re_roll_all == True and roll < target:
                roll=ROLL(6)
                if roll != 1:
                    print("re-rolled into: " + str(roll))
                    total_hits = total_hits + HIT_TARGET(roll,modifier, target, extra_target, extra_form, extra_ammount)[0]

    else:
        total_hits = CHANCE(target)
    print("target to hit: " + str(target) + " with a " + "+" + str(modifier) + " modifier" if modifier >-1 else "target to hit: " + str(target) + " with a " + str(modifier) + " modifier" )
    return total_hits

def TO_WOUND(attacker, total_hits, defender, process):
    """
    a) compare Stregth of the weapon against Toughtness of the target √
    b) determine the base target by this logic, √
        S == T then 4+ √
        S>T and S<2T then 3+ √
        S>=2T then 2+ √
        S<T and 2S>T then 5+ √
        2S>=T then 6+ √
    c) apply modifiers to the target √
    d) add any mortal wounds to the wounds being generated
    e) apply re-rolls to the dice that fail to wound √
    f) apply extra hits for the dice that would fall under that category √
        1) repeat step a, b, c, and d for the newly generated rolls if aplicable √

    Args:   attacker; the atributes of the attacker, indicating what is the stregth of the weapon it is using, and any special abilities or modifiers that might affect this roll
            num_hits; the number of hits on the target
            defender; the atributes of the defender, indicating the toughness of the target and any modifiers that might change the result
    
    Return: the number of wounds on the target.
    """

    weapon_type = attacker.get("Weapon_Type")
    S = attacker.get("S")
    weapon_S = attacker.get("Weapon_S")
    T = defender.get("T")
    to_wound = attacker.get("to_wound")
    re_roll1 = to_wound.get("re-roll1")
    re_roll_all = to_wound.get("re-roll_all")
    modifier = to_wound.get("modifier")
    extra_form = to_wound.get("extra_form")
    extra_target= to_wound.get("extra_target")
    extra_ammount= to_wound.get("extra_ammount")
    extra_target_hard= to_wound.get("extra_target_hard")
    target = to_wound.get("target")
    target_hard= to_wound.get("target_hard")
    weapon_special = attacker.get("Weapon_Abilities")

    
    total_wounds = 0

    if weapon_type == "melee":
        S = S + weapon_S
    
    

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
            roll = ROLL(6)
            print("rolled: " + str(roll))
            total_wounds = total_wounds + HIT_TARGET(roll,modifier, target, extra_target, extra_form, extra_ammount)[0]

            if re_roll1== True and roll ==1:
                roll=ROLL(6)
                if roll != 1:
                    print("re-rolled 1s into: " + str(roll))
                    total_wounds = total_wounds + HIT_TARGET(roll,modifier, target, extra_target, extra_form, extra_ammount)[0]
            
            elif re_roll_all == True and roll < target:
                roll=ROLL(6)
                if roll != 1:
                    print("re-rolled all fail into: " + str(roll))
                    total_wounds = total_wounds + HIT_TARGET(roll,modifier, target, extra_target, extra_form, extra_ammount)[0]

    if process == "probabilistic": 
        total_wounds=total_hits*CHANCE(target)
    print("target to wound: " + str(target) + " with a " + "+" + str(modifier) + " modifier" if modifier >-1 else "target to wound: " + str(target) + " with a " + str(modifier) + " modifier" )
    return total_wounds

def TO_SAVE(attacker, total_wounds, defender,process):
    """
    a) determine base target by this logic √
        apply AP to Ar = new Ar √
        if new Ar < Inv then new Ar √
        if new Ar > Inv then Inv √
    d) apply modifiers to the target
    e) add any mortal wounds to the wounds being generated
    f) apply re-rolls to the dice that fail to wound
    
    Args:   attacker; the atributes of the attacker including the Armor Penetration of its weapons and any modifiers that might affect the result
            total_wounds; the number of wounds on the target
            defender; the atributes of the defender including any Armor and Invulnerable saves and any modifiers taht might affect the results
    
    Return: the total number of unsaved wounds
    """
    inv_R = defender.get("Inv_R")
    inv_M = defender.get("Inv_M")
    Ar = defender.get("Ar")
    AP = attacker.get("AP")


    total_f_saves = 0
    target = Ar - AP
    if target>inv_R:
        target=inv_R
    if process == "deterministic":
        for n in range(total_wounds):
            roll = ROLL(6)
            if not roll >= target:
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
    a) determine the total damage thought the damage variable for the weapon √
    b) apply modifiers to the damage
    c) determine the base target by looking at the FnP value on the model √
    d) Dmg > W then dead √
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
            if r_wounds<=0:
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
    ''' Analyze the data through deterministic or probabilistic expressions

    Args:   
        process: analysis can be either deterministic, meaning using actual number from a random number generator, or probabilistic, giving a percentage chance of achieving the desired result

    '''
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
