import random
import math
from Board import Board
from Settings import VAMPIRES, WAREWOLVES

class TestBoard(Board):

	def __init__(self, rows, columns):
		super().__init__(rows, columns)

	def play_with_battle(self, action, player_type):
		for single_action in action:
			players, enemies = self.battle(single_action, player_type)
			if player_type == VAMPIRES:
				self.vampires = players
				self.warewolves = enemies
			else:
				self.vampires = enemies
				self.warewolves = players

	def battle(self, move, player_type):
		# if overlap, do battle return move
		# else directly return move
		(start_x, start_y), (end_x, end_y), player_num = move
		enemies = self.warewolves if (player_type == VAMPIRES) else self.vampires
		players = self.warewolves if (player_type != VAMPIRES) else self.vampires

		# For now, since they all move in group
		del players[(start_x, start_y)]

		if (not (end_x, end_y) in enemies) and (not (end_x, end_y) in self.humans):
			players[(end_x, end_y)] = player_num
			return players, enemies

		# Enemy battle
		if (end_x, end_y) in enemies:
			enemies_num = enemies[(end_x, end_y)]
			if enemies_num > 1.5 * player_num:
				enemies[(end_x, end_y)] += player_num
				return players, enemies
			if player_num > 1.5 * enemies_num:
				del enemies[(end_x, end_y)]
				players[(end_x, end_y)] = player_num + enemies_num
				return players, enemies
			p = 0.5
			if player_num > enemies_num:
				p = player_num / enemies_num - 0.5
			if enemies_num > player_num:
				p = 0.5 * player_num / enemies_num
			rand = random.random()
			if rand < p:
				# Player wins
				del enemies[(end_x, end_y)]
				players[(end_x, end_y)] = math.floor(p * player_num)
			else:
				enemies[(end_x, end_y)] = math.floor((1-p) * enemies_num)
			return players, enemies

		# Human battle
		if (end_x, end_y) in self.humans:
			humans_num = self.humans[(end_x, end_y)]
			if humans_num > player_num:
				return players, enemies
			if player_num > humans_num:
				del self.humans[(end_x, end_y)]
				players[(end_x, end_y)] = player_num + humans_num
				return players, enemies
			p = 0.5
			if player_num > humans_num:
				p = player_num / humans_num - 0.5
			if humans_num > player_num:
				p = 0.5 * player_num / humans_num
			rand = random.random()
			if rand < p:
				# Player wins
				del self.humans[(end_x, end_y)]
				players[(end_x, end_y)] = math.floor(p * player_num) + math.floor(p * humans_num)
			return players, enemies

