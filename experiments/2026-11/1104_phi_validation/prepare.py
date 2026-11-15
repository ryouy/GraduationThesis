"""Create the frozen, model-unseen validation set; never executed by inference."""
import csv
from pathlib import Path
DATA={
'banana':[
'A shopper opens a curved yellow fruit by pulling its thick skin downward in three long strips.',
'Several elongated fruits share a single stalk. Their smooth yellow coverings protect soft cream-colored flesh.',
'At breakfast, she slices a peeled, curved tropical fruit into round pieces for her cereal.',
'The lunchbox contains a long yellow fruit with a short dark tip and an easily removable skin.',
'On the counter lies a crescent-shaped fruit whose yellow jacket has a few brown freckles.',
'He pulls apart a cluster of long curved fruits, then peels one before taking a bite.',
'This fruit is harvested green in large hanging bunches and becomes yellow and soft as it ripens.',
'A monkey holds an elongated yellow fruit, folds back the peel, and eats the pale interior.',
'The smoothie recipe calls for a curved yellow fruit that can be peeled by hand and mashed with a fork.',
'Unlike a round fruit with a core, this familiar yellow fruit has a long curved body beneath a thick peel.'
],
'apple':[
'She bites into a round red fruit and hears a crisp crunch; a small core with dark seeds remains.',
'A green round fruit has firm white flesh, a thin edible skin, and seeds clustered around its central core.',
'At the orchard, a child picks a shiny red fruit from a tree and polishes its thin skin before eating it.',
'The pie filling uses slices of a crisp round fruit with a central seed core and red or green skin.',
'A small stem rises from the top of this round red fruit; cutting it reveals white flesh around a seed core.',
'This crunchy fruit can be red, green, or yellow and is commonly pressed to make cider.',
'He removes the core from a round green fruit, then cuts the firm white flesh into wedges.',
'A lunch snack consists of crisp wedges of a red-skinned fruit, each trimmed away from a central core.',
'In a classroom experiment, a round red fruit is cut across its middle to expose a star-shaped seed pattern.',
'The fruit in her hand has thin green skin, crunchy pale flesh, and a small seed-filled core she discards.'
],
'elephant':[
'A huge gray land mammal draws water into its long trunk and sprays it over its back.',
'The keeper watches an enormous animal pick up a branch with a flexible nose that reaches the ground.',
'A massive herbivore with tusks and a trunk walks slowly on four thick, pillar-like legs.',
'A calf follows a gigantic gray mother whose long flexible trunk curls around a bundle of grass.',
'This very large land animal flaps broad ears while lifting food to its mouth with an elongated nose.',
'At a watering hole, a tusked gray mammal uses its trunk as a hose to drink.',
'The animal has an immense body, thick wrinkled gray skin, and a long trunk capable of grasping objects.',
'A huge African herbivore shades its body with broad ears and reaches for leaves using its trunk.',
'Four heavy feet support a giant mammal with ivory tusks and a muscular trunk in place of a short nose.',
'A visitor sees an enormous gray animal curl its trunk upward and fan its wide ears.'
],
'giraffe':[
'A tall spotted mammal stretches its extraordinarily long neck to browse the top of an acacia tree.',
'The safari animal has very long legs, a long neck, and a tan coat patterned with dark patches.',
'A small head with two short horn-like knobs sits above the remarkably long neck of this spotted herbivore.',
'This African mammal towers above nearby animals and uses its long tongue to pull leaves from high branches.',
'A spotted calf stands beside a towering mother with an exceptionally long neck and slender legs.',
'The tallest living land animal bends its long neck down to drink while spreading its front legs.',
'A tan animal covered in irregular brown patches reaches high foliage with a very long neck.',
'From the safari vehicle, she sees a spotted, long-necked herbivore whose head rises above the trees.',
'Long slender legs and an extremely elongated neck allow this patch-coated mammal to feed high in trees.',
'The animal at the zoo has two small knobs on its head, brown body patches, and a towering neck.'
],
'piano':[
'A musician sits at a large instrument and presses black and white keys that make hammers strike strings inside.',
'The concert instrument has eighty-eight keys, foot pedals, and strings stretched beneath a raised lid.',
'At an upright wooden instrument, she plays a melody on black and white keys while operating a sustain pedal.',
'This acoustic keyboard instrument creates sound when felt-covered hammers hit internal strings.',
'The recital performer sits on a bench before a grand instrument with a long curved body and a keyboard.',
'Pressing a key on this large acoustic instrument sends a hammer toward a string; foot pedals alter the sound.',
'A child practices scales on an upright instrument with eighty-eight black and white keys.',
'The tuner adjusts strings inside a grand keyboard instrument whose sound is produced by small hammers.',
'With both hands on the keyboard and one foot on a pedal, the soloist plays a large string-and-hammer instrument.',
'A raised triangular lid reveals strings inside the acoustic instrument played from a row of black and white keys.'
],
'violin':[
'A player tucks a small four-stringed wooden instrument beneath the chin and draws a bow across its strings.',
'The orchestra musician holds a small bowed instrument against the shoulder rather than between the knees.',
'This high-pitched string instrument has four strings, a wooden body with f-shaped holes, and is played under the chin.',
'A beginner rests a small wooden instrument beneath her jaw and moves a horsehair bow over four strings.',
'The concertmaster raises a small four-stringed instrument to the shoulder and begins a bowed solo.',
'The folk player draws a bow across four strings on a small wooden instrument held between the chin and shoulder.',
'A small orchestral instrument tuned G, D, A, and E is played with a bow while supported beneath the chin.',
'The musician rubs rosin on a bow before playing a small wooden four-stringed instrument under his chin.',
'An orchestral soloist fingers four strings with the left hand while bowing a small instrument held at the shoulder.',
'This small bowed member of the string family usually plays higher than the viola and rests beneath the player\'s chin.'
],
'none':[
'The librarian renews a membership card and prints a receipt.',
'A delivery driver checks the address written on a cardboard parcel.',
'The engineer draws a diagram of a bridge on a sheet of paper.',
'A student calculates the average of five numbers in a spreadsheet.',
'The janitor replaces a broken light bulb in the hallway.',
'An assistant schedules a meeting for Thursday afternoon.',
'A cyclist checks the tire pressure before leaving the garage.',
'The receptionist hands a visitor a numbered ticket.',
'A shopkeeper folds a paper bag and places it behind the counter.',
'The bus reaches the last stop and the passengers step onto the pavement.',
'A painter rinses a brush and closes a tin of paint.',
'The technician connects a printer to the office network.'
]}
def main():
 rows=[]
 for target,texts in DATA.items():
  for i,text in enumerate(texts):
   category={'banana':'fruit','apple':'fruit','elephant':'animal','giraffe':'animal','piano':'musical instrument','violin':'musical instrument'}.get(target,['fruit','animal','musical instrument'][i//4])
   prompt=f'Context:\n{text}\n\nName the specific {category} described in the context. If no specific {category} can be identified, answer none. Answer with one name only.'
   rows.append(dict(item_id=f'{target}_{i:02d}',target=target,text=text,prompt=prompt))
 with (Path(__file__).parent/'questions.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
if __name__=='__main__':main()
