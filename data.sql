DROP TABLE IF EXISTS `reviews`;

CREATE TABLE `reviews` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `movie_id` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  `rating` TINYINT NOT NULL,
  `comment` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_reviews_movie_id` (`movie_id`),
  KEY `idx_reviews_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `reviews` (`id`, `movie_id`, `user_id`, `rating`, `comment`, `created_at`, `updated_at`) VALUES
-- movie_id 1: Tötet nicht mehr
(1, 1, 1, 5, 'I was not prepared for how hard "Tötet nicht mehr" would hit me; watching the father break after his son is killed during a peaceful reading made the anti death penalty message feel painfully real.', '2025-10-01 20:00:00', '2025-10-01 20:00:00'),
(2, 1, 2, 3, '"Tötet nicht mehr" is clearly important and the images are powerful, but the slow expressionist pacing and heavy melodrama kept me at a distance even while I admired what it was saying.', '2025-10-01 22:00:00', '2025-10-01 22:00:00'),

-- movie_id 2: The Tango of the Widower and Its Distorting Mirror
(3, 2, 3, 4, 'I loved how "The Tango of the Widower and Its Distorting Mirror" turns grief into a ghost story, and the way the film rewinds made me feel like I was trapped inside the widower and his looping memories.', '2025-10-02 20:00:00', '2025-10-02 20:00:00'),
(4, 2, 4, 3, 'The backwards structure in "The Tango of the Widower and Its Distorting Mirror" is clever and unsettling, but I often felt more impressed by the experiment than emotionally moved by the husband and his dead wife.', '2025-10-02 22:00:00', '2025-10-02 22:00:00'),

-- movie_id 3: The Other Side of the Wind
(5, 3, 4, 5, 'As a film nerd I was hypnotised by "The Other Side of the Wind"; the chaotic cutting, shifting film stocks and that endless birthday party made me feel like I was wandering through the fractured mind of a dying director.', '2025-10-03 20:00:00', '2025-10-03 20:00:00'),
(6, 3, 1, 2, 'I respect what Orson Welles was doing with "The Other Side of the Wind", but the constant noise, overlapping dialogue and jagged editing exhausted me instead of pulling me into the story of Jake Hannaford.', '2025-10-03 22:00:00', '2025-10-03 22:00:00'),

-- movie_id 4: Socialist Realism
(7, 4, 2, 4, 'Watching "Socialist Realism" felt like being dropped into the last days of Popular Unity in Chile; the bitter jokes and shabby apartments made the political disillusionment hurt more than any straight history lesson.', '2025-10-04 20:00:00', '2025-10-04 20:00:00'),
(8, 4, 3, 3, '"Socialist Realism" is sharp and mean in the best way, but the fragmented structure and constant tonal shifts sometimes left me feeling like an outsider peeking at a political moment I barely understand.', '2025-10-04 22:00:00', '2025-10-04 22:00:00'),

-- movie_id 5: Histórias de Combóios em Portugal
(9, 5, 1, 4, 'I found "Histórias de Combóios em Portugal" strangely soothing; the lingering shots of old stations, railway workers and quiet passengers turned the train network into a moving portrait of the memory of the country.', '2025-10-05 20:00:00', '2025-10-05 20:00:00'),
(10, 5, 4, 3, 'The documentary "Histórias de Combóios em Portugal" is beautiful to look at, but its gentle pace and minimal narration sometimes made me feel like I was watching another persons nostalgia rather than forming my own.', '2025-10-05 22:00:00', '2025-10-05 22:00:00'),

-- movie_id 6: Grizzly II: Revenge
(11, 6, 2, 2, 'I watched "Grizzly II: Revenge" mostly out of curiosity about the young Clooney and Dern, and while the idea of a giant bear stalking a rock concert is amazing on paper, the clumsy editing and stiff attack scenes killed the suspense for me.', '2025-10-06 20:00:00', '2025-10-06 20:00:00'),
(12, 6, 3, 3, '"Grizzly II: Revenge" is a mess, but I had fun with the ridiculous bear shots and the whole outdoor concert setup; it felt like the kind of so bad it is good horror movie you put on with friends and laugh through.', '2025-10-06 22:00:00', '2025-10-06 22:00:00'),

-- movie_id 7: Loading Ludwig
(13, 7, 4, 4, 'I really vibed with "Loading Ludwig"; watching Mimi obey that cold computer voice and tumble through her own memories felt like seeing performance art mashed up with a glitchy science fiction nightmare.', '2025-10-07 20:00:00', '2025-10-07 20:00:00'),
(14, 7, 1, 2, '"Loading Ludwig" is visually wild, but all the symbolic chases through time and the constant references to Ludwig left me more confused than moved; it felt more like an art installation than a story I could follow.', '2025-10-07 22:00:00', '2025-10-07 22:00:00'),

-- movie_id 8: The Wandering Soap Opera
(15, 8, 1, 5, 'I loved how "The Wandering Soap Opera" keeps flipping between absurd telenovela scenes and political jabs at Chilean reality; every vignette made me feel like the country itself was channel surfing through its own history.', '2025-10-08 20:00:00', '2025-10-08 20:00:00'),
(16, 8, 2, 3, '"The Wandering Soap Opera" is clever and surreal, but the constant switches between mini soap operas wore me down, and I sometimes felt like the political satire was flying over my head.', '2025-10-08 22:00:00', '2025-10-08 22:00:00'),

-- movie_id 9: A Thin Life
(17, 9, 3, 4, 'What hit me in "A Thin Life" was how small everything feels; watching this lonely man drift through dim apartments and almost empty streets, I felt the weight of a life reduced to routines and regrets.', '2025-10-09 20:00:00', '2025-10-09 20:00:00'),
(18, 9, 4, 2, '"A Thin Life" is intentionally minimal and introspective, but for me the long quiet scenes of the main character just sitting and remembering became monotonous instead of profound.', '2025-10-09 22:00:00', '2025-10-09 22:00:00'),

-- movie_id 10: Vazir
(19, 10, 1, 4, '"Vazir" pulled me right into the chaos of state politics; watching the ambitious personal assistant slowly realise how dirty the world of the chief minister really is made every smoky backroom meeting feel tense.', '2025-10-10 20:00:00', '2025-10-10 20:00:00'),
(20, 10, 2, 3, 'I enjoyed the power games in "Vazir", but sometimes the speeches and plotting felt more like a political stage play than real life; I liked it, I just never fully believed in this world of endless schemes.', '2025-10-10 22:00:00', '2025-10-10 22:00:00'),

-- movie_id 11: Bigfoot
(21, 11, 3, 3, 'As a creature feature fan, I had a decent time with "Bigfoot"; the low budget shows, but the night time forest stalking and the glimpses of something huge in the trees gave me a few genuine chills.', '2025-10-11 20:00:00', '2025-10-11 20:00:00'),
(22, 11, 4, 2, '"Bigfoot" leans hard on shaky cameras and screaming instead of building real suspense, and by the third attack scene I felt like I was just waiting for the credits rather than fearing the monster.', '2025-10-11 22:00:00', '2025-10-11 22:00:00'),

-- movie_id 12: Mariette in Ecstasy
(23, 12, 4, 5, '"Mariette in Ecstasy" wrecked me; the mix of sensual close ups, convent routine and the mysterious wounds on Mariette made me feel constantly torn between believing in a miracle and fearing for her mental health.', '2025-10-12 20:00:00', '2025-10-12 20:00:00'),
(24, 12, 1, 3, 'I appreciated the atmosphere in "Mariette in Ecstasy", but the slow pacing and ambiguous visions kept me at arm length emotionally even while I admired how carefully the film captured the cloistered world.', '2025-10-12 22:00:00', '2025-10-12 22:00:00'),

-- movie_id 13: The Surgeon of the Rusty Knife
(25, 13, 2, 4, '"The Surgeon of the Rusty Knife" really got under my skin; watching a simple man channel the spirit of Dr Fritz and perform rough spiritual surgeries made me question what was faith and what was dangerous desperation.', '2025-10-13 20:00:00', '2025-10-13 20:00:00'),
(26, 13, 3, 3, 'I found the story in "The Surgeon of the Rusty Knife" fascinating, but some of the dramatised healing scenes felt a bit too glossy for such a morally grey true story about pain, hope and exploitation.', '2025-10-13 22:00:00', '2025-10-13 22:00:00'),

-- movie_id 14: Joe Finds Grace
(27, 14, 1, 4, '"Joe Finds Grace" felt like a live action cartoon about loneliness; following Joseph, with his gentle voice and awkward body language, through that blend of real streets and comic book panels really touched me.', '2025-10-14 20:00:00', '2025-10-14 20:00:00'),
(28, 14, 4, 3, 'I liked the idea of "Joe Finds Grace", but the exaggerated performances and sudden shifts into fantasy sometimes pushed the emotion too far for me, even though the final revelation about his sister still hit hard.', '2025-10-14 22:00:00', '2025-10-14 22:00:00'),

-- movie_id 15: Housesitter: The Night They Saved Siegfried's Brain
(29, 15, 2, 4, '"Housesitter: The Night They Saved Siegfried''s Brain" is exactly my kind of cult oddity; the goofy brain transfer experiments, neon lab fluid and slasher style house party made it feel like a lost 80s VHS I stumbled onto at midnight.', '2025-10-15 20:00:00', '2025-10-15 20:00:00'),
(30, 15, 3, 2, 'I wanted to love "Housesitter: The Night They Saved Siegfried''s Brain", but the mix of mad scientist homage and awkward gore never quite clicked for me, and many of the jokes landed more as cringe than camp.', '2025-10-15 22:00:00', '2025-10-15 22:00:00'),

-- movie_id 16: Shyamchi Aai
(31, 16, 3, 5, 'Watching "Shyamchi Aai", I kept thinking about my own mother; the simple rural scenes, the lessons about honesty and sacrifice and the way Shyam looks at his mother with awe made me cry more than once.', '2025-10-16 20:00:00', '2025-10-16 20:00:00'),
(32, 16, 4, 4, '"Shyamchi Aai" is slightly preachy in places, but the warmth between Shyam and his mother and the quiet village details made the film feel like listening to a beloved elder telling childhood stories by lamplight.', '2025-10-16 22:00:00', '2025-10-16 22:00:00'),

-- movie_id 17: Nine Ball
(33, 17, 1, 4, '"Nine Ball" drew me in with how honestly it shows addiction; every time Nicky reaches for another drink and slips back into that one tragic night with Doug, I felt the same mix of guilt and helplessness he does.', '2025-10-17 20:00:00', '2025-10-17 20:00:00'),
(34, 17, 2, 3, 'I appreciate the emotional ambition of "Nine Ball", but the constant flashbacks and stylised bar scenes sometimes felt repetitive, as if the film was stuck in the same loop as the conscience of Nicky.', '2025-10-17 22:00:00', '2025-10-17 22:00:00'),

-- movie_id 18: Sul 45° parallelo
(35, 18, 4, 4, '"Sul 45° parallelo" fascinated me; jumping between quiet stretches of the Po Valley and the long trip toward Mongolia made the 45th parallel feel like an invisible line that stitches together very different lives.', '2025-10-18 20:00:00', '2025-10-18 20:00:00'),
(36, 18, 1, 3, 'The idea behind "Sul 45° parallelo" is strong, but the documentary style is so relaxed and meandering that I occasionally found my attention drifting even while I enjoyed the music and landscapes.', '2025-10-18 22:00:00', '2025-10-18 22:00:00'),

-- movie_id 19: Blood Type
(37, 19, 2, 4, '"Blood Type" surprised me with how heartfelt it was; once all those wildly different characters crash into the same emergency room, their bickering and confessions turn the chaos of the car chase into something oddly hopeful.', '2025-10-19 20:00:00', '2025-10-19 20:00:00'),
(38, 19, 3, 3, 'I liked the ensemble energy in "Blood Type", but the way each character represents a social type made some of the dialogue feel a bit on the nose, even though the final twist about the motive of the thief worked for me.', '2025-10-19 22:00:00', '2025-10-19 22:00:00'),

-- movie_id 20: Heartland of Darkness
(39, 20, 1, 4, '"Heartland of Darkness" scratched my itch for grainy satanic panic horror; the small town church front, the creepy preacher and the sudden bursts of 16mm style gore made me feel like I had dug up a cursed VHS from the 90s.', '2025-10-20 20:00:00', '2025-10-20 20:00:00'),
(40, 20, 4, 3, 'I enjoyed the atmosphere in "Heartland of Darkness", but the acting and pacing are uneven, and I sometimes felt that the film cared more about showing off occult imagery than digging into the fear of the father and daughter.', '2025-10-20 22:00:00', '2025-10-20 22:00:00');