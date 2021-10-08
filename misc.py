import random

pastas = [
    'if I may offer input, ezili seems restrained rather than an actual bottom, if you get her to open up then'
    'she willabsolutely destroy you\ngwen strikes me as the type to act tough on the field but enjoy cuddles'
    'and rainbows and stuff',
    'si puedo aportar, ezili parece retraida mas que un fondo, si logras que se abra, ella te destruira\n'
    'gwen me parece que es el tipo que intenta actuar duro pero en el fondo adora los cariños y arcoiris y esas cosas',
    'imagine how easy it would be to btfo everyone calling you out with a video showing that you beat people legit, '
    'such an easy way to be like "hey, you sniped me, even when I just had a superior legit strat?, damn bro...", and '
    'yet somehow absolutely no one fucking does this\n\npsa tip for anyone in the community who is a top 50 grinder '
    'and got or almost got top 3, just record your shit, it\'s that easy. instant community respect and transparency, '
    'at 0 expense of your own',
    '- Mid path Dartling A-\n - Gorgon Storm is such a cool MK man. Like it stuns so much and it has so much range and '
    'its uptime is actually pretty high. Like 30% or something like that. It can also stun DDTs so that means that '
    'stuff like Sabotage Supply Lines actually is kinda outclassed by Rocket Storm ability. Every single Odyssey these '
    'days (which I play on Hard mode now, I previously couldn\'t beat Hard mode without using all my Monkey Money on '
    'powers and instas) I just build my early game defense, which is always my favorite 4-2-0 Sniper since it pops '
    'leads and camo bloons (which means I\'m set against the super difficult round 59 where some of the bloons are '
    'both camos and leads), and then start building tons of 2-4-0 Dartling Gunners. Honestly I\'m super happy that '
    'Ninja Kiwi added this Monkey Knowledge, even though I had to buy a couple packs of Monkey Knowledge and Monkey '
    'Money to reach Gorgon Storm. I hope they add something even cooler like COBRA from my second favorite game Bloons '
    'Tower Defense Battles, or even like C4 Charlie from my third favorite game Bloons Adventure Time Tower Defense. '
    'Anyways this is exephur2000 a.k.a. Colton T. a.k.a. greengoblin55 signing out, see you guys in my next post.',
    '13. wall of fire change: holy shit. the epitome of ninja kiwi foolishness. this HUGE FUCKING NERF FROM NOWHERE '
    'SERIOUSLY WHAT THE HELL. this makes me mad because in 24.2 i couldnt get all the wlp combos for 2tc cuz rng was '
    'borked (still is) AND NOW RNG DOESNT EVEN EXIST IN REAL GAMES? SERIOUSLY THIS CHANGE IS SO FUCKING STUPID. now '
    'wof doesnt work on ANY multipath map such as muddy geared infernal or what have you seriously who the fuck asked '
    'for this nonsense the ONLY place where this change is SLIGHTLY good is on geared... or you could just place wof '
    'well. NO ONE ASKED FOR THIS NONSENSE',
    'You are the type of player that spends 26 hours a day playing a dumb video game. Go touch grass. Seriously stop '
    'bragging about this dumb video game. I have looked at your profile and you always brag about having 1000000000 '
    'hours. Shut up let people enjoy the game and have fun. I don\'t wann hear your dumb tips on how to play the game '
    'I wanna use my own startegies. You can\'t control me. You can\'t force me to use your bs. And now you are just '
    'being an elitist again. 5 seconds ago u said \"Oh guys I have 1000000000000 hours and all BBs xd you guys are '
    'noobs\" that\'s toxic elitism. You are basically saying that those who don\'t have all BBs are trash at the game '
    'and that\'s not pog. And now u said \"the sad part is that none of what I said even denotes that much skill\" '
    'that is just on a whole different level. It is sad that people like you still exist in the video gaming '
    'community. If everyone stopped bragging about how good they are the world would be a much better place.',
    'dude stop being a fucking idiot, ik ur pride be being hurt rn bc u use macros and u dont want to be known as a '
    'cheater but 1st idc 2nd u not gunna be called a cheater so actually pls stop insulting to insult and yeah',
    'i just need to fucking say it. If i put over 1000 hours into something and then replicate every almost every '
    'hard thing ever done with it and then go on to do shit thats much much harder it is not egotistical to view '
    'myself as the best at it. nor is it egotistical for me to say that there is a chance that something that took me '
    '15 hours using something that i have over 1000 hours of practice in may be the hardest thing ever done in the '
    'game. note i have almost never called plorder the hardest thing in the game i usually say “arguably” or '
    '\"probably\" and whenever i have been in an actual civil discussion most of the time people agree that plorder is '
    'in fact probably the hardest thing ever done in the game. not to mention that there is no reason for you to '
    'argue when i call something harder than something else when the person that did that something else agrees with '
    'me. ',
    '**Regarding the slowdown drama:**\n\nIf you don’t know what happened, on race 146 (Bloons to the corn) I had '
    'uploaded a race guide to my YouTube channel , after other peoples suspects and me admitting, I had used slowdown '
    'to get a decent time at that point (1:10.41) so I could upload a video to the race. with all honesty, I have no '
    'idea why I did it, could be because I needed it to compete with other racers, since at this point many already '
    'use slowdown to get a top 3 score, on the other hand, I didn\'t even need it, 2 hours later I streamed in this '
    'server and got a 1:10.01 while people were watching, which showed I did not need it, 1 day later, I got a '
    '1:09.26 without slowdown. After all it was a very dumb decision to use slowdown and break everyone\'s trust in a '
    'server moderator just  to get a video out, it will (definitely) never happen again, and I am very sorry for what '
    'I did, I don’t expect you to forgive me, but I just want you to know that I am aware of what I did, and that it '
    'was wrong, Colt. ',
    'MUDDY PUDDLES CHIMPS WITH PERMACHANGE AND CHINOOK PERMACHGIANGE AND CHINFOSPK PRJABMNAGHE AND CHOISNOLFOK',
    '**Chocbox**\n\nChocbox is a patented plastic box for safely enclosing electrical connections made with screw '
    'connector strips. It was invented by entrepreneur Peter Moule, who appeared on the BBC television programme '
    '*Dragons\' Den* in 2007. He secured a deal with two \"dragons\", Duncan Bannatyne and James Caan, for £150,000 '
    'funding and soon made a deal for sales worth £25 million. Bannatyne describes Chocbox as one of his best '
    'investments from the show.',
    'Hello, as you may be aware, someone was discussion roomed for completing all the expert maps Black Border. By '
    'itself, we are perfectly fine with people showing their achievements, however on closer inspection it was '
    'revealed in another server that the person who posted this openly talked about using alt BTD6 accounts with '
    'infinite MM hacks to practice races as well as talked about unflagging accounts after using mods. As such, I have '
    'solely decided to ban this person who is causing a commotion in this server. It is simply hypocritical from some '
    'of the community to allow people to use hacked accounts to gain advantage in competitive areas just to flaunt '
    'while completely trying to destroy people who are using for example, pirated versions that are basically '
    'identical copies of the legitimate version for simply being in a a situation where they cannot financially pay '
    'for BTD6. Fyi, Raven was debating whether to let the person go until staff were available since they were being '
    'relatively co-operative, it is me who insisted on him staying in the room and me who is banning the person. '
    'Another part of the reason why I am banning is that the person is acting as if they are completely innocent '
    'while deliberately trying to demonise the moderators in this server for doing the unacceptable things I mentioned '
    'above. That is all. Anyone who talks about how anyone involved in moderation is being unfair about this in chat I '
    'will personally ban for one week for trying to cause a ruckus in the server.',
    'The monkey bank in general sucks as if you want to go for a passive style it is simply more effective to rush '
    'straight for a bia. As while it is mathematically better to get a bank with 1 plantation on the side and then get '
    'a r17 bia without banking out it directly gives the advantage to the enemy for multiple reasons. First You will '
    'have only a small amount of budget to afford defense and still be able to pull it off and at the same time you '
    'absolutely cannot rush the enemy allowing them to even sell defenses and get better farms then you while still '
    'being able to rush. Exemples would be equalizing with a r16 bia while forcing defense r16 which is an important '
    'round for ai layering. Or selling defense to get a r15 bia and overshadow your r14 bank.\n\nOutside of this '
    'specific scenario which has a use in 1 single scenario (DFA vs NFE) bank sucks, getting a bank without the gimmik '
    'of upgrading to a bia without banking out is straight up just losing 1k$ even if you gain 30 eco it\'s not worth '
    'as getting a bia would give 80 eco in 1 round and once again overshadow your effort. You can argue that bank is '
    'useful in moab drain games where both players are stuck with low eco and low farms r20+ but those situations '
    'don\'t happen in competitive anymore.',
    'I suppose I will have to tell to the server owners about your absurd behavior and abuse of your powers and '
    'abilities, furthermore, I don\'t think you are a good mod if you treat people of the server harshly and taking '
    'roles of players of the server, I don\'t think you deserve to be a moderator after this action, this wasn\'t '
    'intended to be a good deed and I don\'t understand why you would do that.',
    'you can send rounds faster with 1 more alc selling\nalso 1st and 2nd place use the same strat... they work '
    'together\nand both of them use cheatengine\nthat is a 3rd party application that can slow your game 5 times more '
    'then you see in this video...\n\nthey can not beat me so they coop and cheat hahaha.. noobs gonna noob\ni feel '
    'honored they go true such trouble just to beat me'
]
random.shuffle(pastas)
pasta_index = 0


def random_pasta():
    global pasta_index
    if pasta_index >= len(pastas):
        random.shuffle(pastas)
        pasta_index = 0
    pasta = pastas[pasta_index]
    pasta_index += 1
    return pasta
