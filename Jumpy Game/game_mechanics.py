# Key game mechanics in Jumpy Game:

# 1. Auto-jumping mechanic
def auto_jump_example():
    """
    The bee automatically jumps when landing on a platform:
    - Sets vel_y to jump velocity
    - Plays jump sound
    - Sets in_air to True
    - Disables auto_jump until landing again
    """
    # From the Player.move() method:
    if not self.in_air and self.can_auto_jump:
        self.vel_y = self.current_jump_vel
        jump_fx.play()
        self.in_air = True
        self.can_auto_jump = False


# 2. Double jump mechanic
def double_jump_example():
    """
    Player can perform a second jump while in the air:
    - Activated by pressing SPACE
    - Only works if has_double_jump is True
    - has_double_jump is reset when landing on a platform
    """
    # From the Player.move() method:
    if key[pygame.K_SPACE] and self.in_air and self.has_double_jump:
        self.vel_y = self.current_jump_vel
        jump_fx.play()
        self.has_double_jump = False


# 3. Vertical scrolling with score
def scrolling_example():
    """
    The world scrolls down when player reaches upper threshold:
    - Scroll amount is tied to player's upward movement
    - Score increases based on scroll amount
    - Creates infinite vertical gameplay
    """
    # From the Player.move() method:
    if self.rect.top <= SCROLL_THRESH:
        if self.vel_y < 0:
            scroll = -dy

    # In main game loop:
    if scroll > 0:
        score += scroll


# 4. Platform generation
def platform_generation():
    """
    Platforms are generated above the screen:
    - Random width between 40-60 pixels
    - Random horizontal position
    - Random vertical gap between 80-120 pixels
    - Platforms can be static or moving (after score > 1000)
    """
    # From main game loop:
    if len(platform_group) < MAX_PLATFORMS:
        p_w = random.randint(40, 60)
        p_x = random.randint(0, SCREEN_WIDTH - p_w)
        p_y = platform.rect.y - random.randint(80, 120)
        p_type = random.randint(1, 2)
        if p_type == 1 and score > 1000:
            p_moving = True
        else:
            p_moving = False
        platform = Platform(p_x, p_y, p_w, p_moving)
        platform_group.add(platform)


# 5. Power-up system
def power_up_system():
    """
    Two types of power-ups:
    - Boosters: Increase jump height (15% chance per platform)
    - Extra Lives: Add one life (5% chance per platform, max 1 on screen)
    """
    # From main game loop:
    # Generate boosters (15% chance)
    if random.random() < 0.15:
        booster = Booster(p_x + p_w // 2, p_y - 30)
        booster_group.add(booster)

    # Generate extra lives (5% chance)
    if random.random() < 0.05 and len(extra_life_group) < 1:
        extra_life = ExtraLife(p_x + p_w // 2, p_y - 60)
        extra_life_group.add(extra_life)


# 6. Lives system
def lives_system():
    """
    Player has multiple lives:
    - Start with 3 lives, maximum of 5
    - Lose a life when falling off screen or hitting an enemy
    - Game over when lives reach 0
    - Extra lives can be collected
    """
    # Life loss logic from main game loop
    if jumpy.rect.top > SCREEN_HEIGHT:
        LIVES -= 1
        if LIVES <= 0:
            game_over = True
        else:
            # Reset player position
            jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            # Reset jump mechanics
            jumpy.vel_y = 0
            jumpy.in_air = False
            jumpy.can_auto_jump = True
            jumpy.has_double_jump = True


print("Game mechanics analysis complete")
