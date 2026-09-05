// ============================================================
//  LESSON 4 — The Kinetic Engine: Movement & Player State
//  ✏️  Write your code in each function below.
//  Do NOT modify engine.js or App.jsx
//
//  Your code here will be carried forward into Lesson 5 & 6.
// ============================================================

import { TILE_S, WORLD_W, WORLD_H, isWalkable, speedMult, T } from './engine.js'

// ── TASK 1 ───────────────────────────────────────────────────
// createPlayer(startX, startY)
// Build and return the player object.
// startX, startY are pixel coordinates.
//
// Required fields:
//   x, y               — use startX, startY
//   hp, maxHp          — 120
//   stamina, maxStamina — 100
//   xp, level          — 0, 1
//   gold               — 0
//   potions            — 3
//   kills              — 0
//   state              — 'idle'
//   dir                — 'down'
//   facingDir          — 'right'
//   comboCount         — 0
//   invincible         — 0
//   attackCd           — 0
//   dodgeCd            — 0
//   score              — 0

export function createPlayer(startX, startY) {
  // ✏️ YOUR CODE HERE

}

// ── TASK 2 ───────────────────────────────────────────────────
// movePlayer(player, direction, tiles)
// Move the player one tile in the given direction.
// direction: 'up' | 'down' | 'left' | 'right'
//
// Steps:
//   1. Calculate new x/y by ±TILE_S
//   2. Tile coords: tx = Math.floor(newX / TILE_S)
//   3. Block if out of bounds (tx < 0 || tx >= WORLD_W etc.)
//   4. Block if !isWalkable(tiles[ty][tx])
//   5. Update dir, facingDir ('left' if moving left, else 'right')
//   6. Set state = 'walking'
//   7. Return { ...player, x, y, dir, facingDir, state }

export function movePlayer(player, direction, tiles) {
  // ✏️ YOUR CODE HERE

}

// ── TASK 3 ───────────────────────────────────────────────────
// getSpeedMultiplier(player, tiles)
// Return the terrain speed multiplier for the player's tile.
// Use speedMult(tileType) from engine.js.
//
// Steps:
//   1. tx = Math.floor(player.x / TILE_S), ty = Math.floor(player.y / TILE_S)
//   2. Return 1.0 if out of bounds
//   3. Return speedMult(tiles[ty][tx])
//
// Reference: PATH=1.18, GRASS=1.0, TALL_GRASS=0.85,
//            FOREST=0.72, SNOW=0.78, SHALLOW=0.5

export function getSpeedMultiplier(player, tiles) {
  // ✏️ YOUR CODE HERE

}

// ── TASK 4 ───────────────────────────────────────────────────
// collectItem(player, item)
// Apply item effect and return a message.
//
//   'coin'   → player.gold += 10  → message: '💰 +10 gold'
//   'potion' → player.potions += 1 → message: '🧪 +1 potion'
//
// Returns: { player, message }

export function collectItem(player, item) {
  // ✏️ YOUR CODE HERE

}

// ── TASK 5 ───────────────────────────────────────────────────
// checkLevelUp(player)
// Level up if player.xp >= player.level * 150
//
// On level up:
//   level += 1
//   xp -= threshold
//   maxHp += 12,  hp = maxHp
//   maxStamina += 5, stamina = maxStamina
//
// Returns: { player, leveledUp }

export function checkLevelUp(player) {
  // ✏️ YOUR CODE HERE

}
