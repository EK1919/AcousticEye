import os

import csv


sample_rate = 32000
PATH_TO_ROOT = os.path.join(
    r"C:\Users\Public\Documents\Classification\PANN_files")


with open(os.path.join(PATH_TO_ROOT, "class_labels_indices.csv"), 'r') as f:
    reader = csv.reader(f, delimiter=',')
    lines = list(reader)

labels = []
ids = []    # Each label has a unique id such as "/m/068hy"
for i1 in range(1, len(lines)):
    id = lines[i1][1]
    label = lines[i1][2]
    ids.append(id)
    labels.append(label)
classes_num = len(labels)


daniel_motors_sounds = {
    'Vehicle', 'Boat, Water vehicle', 'Sailboat, sailing ship', 'Rowboat, canoe, kayak',
    'Motorboat, speedboat', 'Ship', 'Motor vehicle (road)', 'Car', 'Car passing by',
    'Race car, auto racing', 'Truck', 'Bus', 'Emergency vehicle', 'Motorcycle',
    'Train', 'Train whistle', 'Aircraft', 'Aircraft engine', 'Jet engine', 'Propeller, airscrew',
    'Helicopter', 'Fixed-wing aircraft, airplane', 'Engine', 'Light engine (high frequency)',
    "Dental drill, dentist's drill", 'Lawn mower', 'Chainsaw', 'Medium engine (mid frequency)',
    'Heavy engine (low frequency)', 'Engine knocking', 'Engine starting', 'Idling',
    'Accelerating, revving, vroom', 'Microwave oven', 'Blender', 'Hair dryer',
    'Electric toothbrush', 'Vacuum cleaner', 'Electric shaver, electric razor', 'Jackhammer',
    'Power tool', 'Drill',
}

ours_motors_sounds = {'Hum', 'Throbbing', 'Buzz', "Mains hum", "Chainsaw", "Steam whistle", "Train horn", "Hiss", "Foghorn", "Mechanical fan", "Air conditioning", "Humming"}

motors_sounds = daniel_motors_sounds.union(ours_motors_sounds)

ignore_sounds = {'Insect', 'Music', 'Outside, urban or manmade', 'Outside, rural or natural', 'Steam', 'Idling',  'Animal', 'Guitar', 'Clickety-clack', 'Wind noise (microphone)', 'Wind', 'Inside, small room', 'Civil defense siren', 'White noise', 'Siren', 'Musical instrument',  'Railroad car, train wagon', 'Rail transport', 'Speech', 'Drum', 'Drum kit', 'Bass drum', 'Percussion', 'Snare drum', 'Cymbal', 'Drum machine', 'Rimshot', 'Drum roll', 'Scary music', 'Thunderstorm', 'Thunder', 'Water', 'Rain', 'Raindrop', 'Rain on surface', 'Stream', 'Waterfall', 'Ocean', 'Waves, surf', 'Fire', 'Water tap, faucet', 'Whistle', 'Splash, splatter'}

ignore_warfare = {'Explosion', 'Gunshot, gunfire', 'Machine gun', 'Fusillade', 'Artillery fire', 'Cap gun', 'Fireworks', 'Firecracker', 'Boom'}

ignore_human = {'Male speech, man speaking', 'Female speech, woman speaking', 'Child speech, kid speaking', 'Conversation', 'Narration, monologue', 'Speech synthesizer', 'Shout', 'Yell', 'Children shouting', 'Screaming'}

ignore_animals = {'Owl', 'Bird', 'Sonar', 'Domestic animals, pets', 'Whale vocalization', 'Fowl', 'Wild animals', 'Bird vocalization, bird call, bird song', 'Hoot', 'Goose', 'Cat', 'Wail, moan', 'Dog', 'Bark', 'Howl', 'Meow', 'Livestock, farm animals, working animals', 'Clip-clop', 'Horse', 'Neigh, whinny', 'Moo', 'Pig', 'Oink', 'Goat', 'Bleat', 'Sheep', 'Fowl', 'Chicken, rooster', 'Crowing, cock-a-doodle-doo', 'Turkey', 'Gobble', 'Duck', 'Quack', 'Honk', 'Roaring cats (lions, tigers)', 'Roar', 'Chirp, tweet', 'Squawk', 'Pigeon, dove', 'Coo', 'Crow', 'Caw', 'Owl', 'Bird flight, flapping wings', 'Canidae, dogs, wolves','Rodents, rats, mice', 'Mouse',  'Mosquito', 'Fly, housefly', 'Bee, wasp, etc.', 'Frog', 'Croak', 'Snake', 'Rattle'}

ignore_traffic = {'Air brake', 'Air horn, truck horn', 'Reversing beeps', 'Police car (siren)', 'Ambulance (siren)', 'Fire engine, fire truck (siren)', 'Traffic noise, roadway noise', 'Vehicle horn, car horn, honking'}

ignore_not_sure = {'Bellow', 'Whispering', 'Laughter', 'Baby laughter', 'Giggle', 'Belly laugh', 'Chuckle, chortle', 'Crying, sobbing', 'Baby cry, infant cry', 'Sigh', 'Singing', 'Groan', 'Grunt', 'Breathing', 'Wheeze', 'Snoring', 'Walk, footsteps', 'Hubbub, speech noise, speech babble', 'Children playing', 'Growling', 'Purr', 'Hiss', 'Cowbell', 'Bell', 'Church bell'}

ignore_all = ignore_sounds | ignore_warfare | ignore_human | ignore_animals | ignore_traffic | ignore_not_sure

other_sounds = [label for label in labels if label not in motors_sounds]
other_sounds = [label for label in other_sounds if label not in ignore_all]

