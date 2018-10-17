def kick(self, text_input):
    success_verb = f"kicked"
    fail_verb = f"kicked at"
    outcome = f", stunning it for a round"
    dam_mod = (operator.truediv, 1.75)
    if self.cooldowns["physical"] == 0:
        self.cooldowns["physical"] = 6 - self.haste_amount()
        attack = self.attack_target_mob(
            text_input,
            success_verb=success_verb,
            fail_verb=fail_verb,
            outcome=outcome,
            dam_mod=dam_mod
        )
        if attack.success:
            stun_dur = 2 + self.equipped_weapon.main_hand.stun
            attack.target.stun_monster(stun_dur)
            self.advance_turn()
        else:
            if attack.target:
                if attack.target.current_hp >= 1:
                    self.advance_turn(attack.target)
                else:
                    self.advance_turn()
            else:
                self.advance_turn()
    else:
        combat_report = (
            f"You are still tired from your last kick.\n"
            f"Please wait to try again."
        )
        self.add_messages(combat_report)
