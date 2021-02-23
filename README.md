# Warhammer
engine to math out warhammer


comparing the different units and their costs to their best and worst matchups

''''

## Step 1, the math

there will be two ways of parsing through the date

the first one is a deterministic aproach, using actual number to get a single example

the second one will atempt analize the probability to kill from a single unit to a particular target.

the deterministic process for assessing damage is as follows, with each step building on the last


### NUMBER OF ATTACKS
1. determine the number of attacks by looking at the weapon type, range, and distance from the target and following this logic.

            if range>distance
            if Weapon Type rapid fire and range/2>distance then the ammount of attacks is doubled
            if Weapon Type is blast and target has >5 models min 3 attacks
            if Weapon Type is blast and target has >10 models min 6 attacks

### TO HIT 
1. determine the base target by this logic:
        
        if weapon type == Melee* then WS
        else BS
1. apply modifiers to the target
1. apply re-rolls to the dice that fail to hit
1. add any mortal wounds to the wounds being generated
1. apply extra hits for the dice that would fall under that category
    1. repeat step 1,2,3 and 4 for the newly generated rolls if aplicable

### TO WOUND
1. compare Stregth of the weapon against Toughtness of the target, except on poison weapons
1. determine the base target by this logic:

        S == T then 4+
        S>T and S<2T then 3+
        S>=2T then 2+
        S<T and 2S>T then 5+
        2S>=T then 6+

1. apply modifiers to the target
1. add any mortal wounds to the wounds being generated
1. apply re-rolls to the dice that fail to wound
1. apply extra hits for the dice that would fall under that category
    1. repeat step 1,2,3 and 4 for the newly generated rolls if aplicable


### SAVE
1. determine base target by this logic:

        apply AP to Ar = new Ar
        if new Ar < Inv then new Ar
        if new Ar > Inv then Inv

1. apply modifiers to the target
1. add any mortal wounds to the wounds being generated
1. apply re-rolls to the dice that fail to wound

### FEEL NO PAIN
1. determine the total damage thought the damage variable for the weapon
1. apply modifiers to the damage
1. determine the base target by looking at the FnP value on the model
1. Dmg > W then dead
1. check if there are any mortal wounds left to be allocated on the target apply the next available Mw to the target
1. determine the base target by looking at the FnP Mw value on the model
1. repeat steps d, e, and f until the is dead or there are no more Mw to be allocated

### MORALE
1. determine the base target through this logic:

        numb of models slain this turn - highest Ld of models left = new Ld

1. roll to see if the models suffer morale penalties

        if roll=< new Ld then remove one model
            if failed check if the unit has any invulnerabilities to morale then
            check if number of models < "starting number of models"/2 if so add +1 to the target of the next roll
            roll 2+ for each remaining unit

## Step 2, variable descrption and source      


**attacker**: the dictionary containing all information invoved in the attacker side of the analysis, it is a combination of all the choices for Unit, models, and bonuses that would be producing the attack

**defender** the dictionary containing all information involved in teh  defender side of the analysis, it is a combination of all the choices dor unit, model,and bonuses that would be receiving the attack

the organization of this objects is as follows from highest level to lowest

**Name of Unit**: str - this identifies a unit among hundred to note what kinds of models it contains

**Name of Model**: str - this identifies the specific model that we are working with among all the posible models in the unit

**M**: int - the ammount of movement in inches of the model

**WS**: int - the Weapon Skill or minimum roll needed to hit a target in melee

**BS**: int - the Ballistic Skill or minimum roll needed to hit a target in range

**S**: int - the Strength of the model in melee

**T**: int - the Toughness of the model, how strong a hit it can take and shrug off

**W**: int - the number of Wounds the model can take before its removed from the game

**A**: int - the number of Attacks the model can dish out in close combat

**Ld**: int - the Leadership of the model, how many of its breatheren it can watch die before thinking of running away

**Ar**: int - the Armor of the model, the amount of armor penetration the weapons will need to stand a chance

**Inv_M**: int - the Invulnerable save in Melee for the model, like its armor save but it can't be diminished by regular attacks

**Inv_R**: int - the Invulnerable save in Range for the model, like its armor save but it can't be diminished by regular attacks

**FnP**: int - the Feel no Pain save of the model, what are the chances to ignore damage all together on a damage by damage basis

**FnP_Mw**: int- the Feel no Pain for Mortal Wounds of the model, what are the chances of ignoring mortal wounds all together

**Cost**: int - the point cost of the model in order to add it to the army.

**Weapon1**: str DICT - the names of the weapons equipped in this particular slot, and the cost for each one

**R**: int - the range of the weapon, the distance at which it can be used

**Type**: str - the details on how the weapon works and when can it be shot

**A**: str - the number of attacks that the weapon has, melee weapons add this number to the Attack characteristic of the model, variable Attack weapons are marked with a "d" before the number like "d6" for a random value between 1 and 6

**S**: str - the Stregth of the weapon, melee weapons add this number to the Stregth characteristic of the model, variable Stregth weapons are 
marked with a "d" before the number like "d6"

**AP**: str - the Armor Penetration value of the weapon, how much of the armor on their target do they get through

**D**: str - the Damage of the weapon, variable Damage weapons are marked with a "d" before the number like "d6"

**Abilities**: str DICT - a list of the special rules that apply to this weapon, they can be things like re-roll all failed to hit rolls, or always wound on a particular number

**slots**: int - the number of slots that that weapon uses. a two handed weapon uses two slots. a one handed weapon uses one

**to_hit**: str DICT - a dictionary containing all the variables that would apply for this case

**re-roll1**: boolean - does this unit re-rolls 1s to hit with this weapon

**re-roll_all**:boolean - does this unit re-rolls all failed to hit with this weapon

**modifier**: int - what modifier is applied to the rolls on this weapon

**extra_form**:"re-roll" or "add" - does a an extra add a roll or a success

**extra_target**:int - the target for the extra

**extra_ammount**:int - the ammount of rolls or successes added on an extra

**extra_target_hard**: boolean - can the extra target be modified

**target**:int - does this particular weapon have a targeted number to hit

**target_hard**:boolean - can the target be modified

**to_wound**:{

**re-roll1**: boolean - does this unit re-rolls 1s to hit with this weapon

**re-roll_all**:boolean - does this unit re-rolls all failed to hit with this weapon

**modifier**: int - what modifier is applied to the rolls on this weapon

**extra_form**:"re-roll" or "add" - does a an extra add a roll or a success

**extra_target**:int - the target for the extra

**extra_ammount**:int - the ammount of rolls or successes added on an extra

**extra_target_hard**: boolean - can the extra target be modified

**target**:int - does this particular weapon have a targeted number to hit

**target_hard**:boolean - can the target be modified

},

**to_save**:{

**no_invul**:False,

**no_re-rolls**:False

},

**to_FnP**:{

**no_invul**:False,

**no_re-rolls**:False

}

**Weapon2**: str list - the names of the weaopn equipped in this particular slot

+ same as **Weapon1**

**Weapon3**: str list - the names of the weaopn equipped in this particular slot

+ same as **Weapon1**

**Weapon4**: str list - the names of the weaopn equipped in this particular slot

+ same as **Weapon1**

**Min**: int - the Minimum ammount of models of this type that can be in this unit

**Max**: int - the Maximum ammount of models of this type that can be in this unit

**Req**: str - the requirements that must be met for this model to be part of the unit, E means every x models ex: "E5" means every 5 models, A means after x models ex: "A10" means after 10 models

**Abilities**: str list - a list of all the abilities the unit has, it can include things like advance and charge, objective secure, or fly
Key-Words: str list - a list of all the Key-Words that are aprticular to that unit and what kinds of things it will be affected by.

## Example of what this architecture would look like:


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

the object attacker is a simplified version of the full list including only the information that would be relevant to the attacker

## Step 3, implement dice rolling for the system.

apply the random library and simplify the variable to ROLL():


## step 4, implement probabilistical analysis to the system

this would mean creating an average result for the entire steps, a max result and a min result.

and then mapping the probability for those results to happen.

creating results along a curve for each of the matchups

meaning that each step need to produce at least 3 values, a minimum, an average, and a maximum, as well as quartiles (this needs to be revised)

## step 5, posible unit composition

unit type min ammount to maximum ammount
so for example

kabalite Warriors have a min of 5 units composed of either 1 syrabite and 4 kabalite warriors, or 1 syrabite, 3 kabalite warriors and 1 kabalite warrior with special weapon.

to identify this we need a running to total number of units with a split in values and profiles for each composition

that would look something like this

    kabalite warrior: x4
    syrabite: x1
        blast pistol
        agonizer
        18
    total points 50

would love the final result to be a detail exploration of what each unit does against particular matchups, with a zoom into their offensive and defensive power, as well as a more well rounded star chart expression of how do their other areas work

KNOWN BUGS

natural 1s should always be counted as a fail

