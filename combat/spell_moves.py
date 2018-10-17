def cast_fireblast(self, text_input):
    verb = f"threw a blast of fire at"
    # TODO: introduce DoT
    outcome = f" lighting it on fire."
    # TODO: Figure out what the real damage of spells should be. Ideally, make lots of unique spells
    damage_modifier = (operator.mul, 1.75)
    if self.cooldowns["spell"] == 0:
        self.cooldowns["spell"] = 6 - self.haste_amount()
        attack = self.attack_target_mob(
            text_input,
            dam_mod=damage_modifier,
            success_verb=verb,
            fail_verb=verb
        )
        if attack.target:
            if attack.target.current_hp >= 1:
                self.advance_turn(attack.target)
            else:
                self.advance_turn()
        else:
            self.advance_turn()
    else:
        combat_report = (
            f"You are still weary from casting your last fireball.\n"
            f"Please wait to try again."
        )
        self.add_messages(combat_report)